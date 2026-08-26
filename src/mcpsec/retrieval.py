from __future__ import annotations

import asyncio
import ipaddress
import json
import socket
from collections.abc import AsyncIterator, Awaitable, Callable
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlsplit

import httpx2

from mcpsec.exceptions import RetrievalError
from mcpsec.normalizer import normalize_tools
from mcpsec.resource_policy import MAX_INPUT_BYTES, MAX_RETRIEVAL_PAGES, MAX_STATIC_TOOLS, validate_structure

DEFAULT_MAX_TOOLS = 500
MAX_ALLOWED_TOOLS = MAX_STATIC_TOOLS
DEFAULT_TIMEOUT_SECONDS = 10.0

Retriever = Callable[[str, float, int, int], Awaitable[list[dict[str, Any]]]]


def _validated_loopback_destination(url: str) -> tuple[str, str | None]:
    try:
        parsed = urlsplit(url)
        port = parsed.port
    except ValueError as exc:
        raise RetrievalError(f"Malformed MCP endpoint URL: {exc}") from exc
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise RetrievalError("MCP endpoint must be an explicit HTTP(S) URL")
    if parsed.username or parsed.password:
        raise RetrievalError("Credentials are not accepted in the MCP endpoint URL")
    if parsed.fragment:
        raise RetrievalError("MCP endpoint URL must not contain a fragment")
    if port == 0:
        raise RetrievalError("MCP endpoint port must be between 1 and 65535")
    hostname = parsed.hostname.casefold()
    if hostname == "localhost":
        try:
            addresses = {
                str(item[4][0])
                for item in socket.getaddrinfo(
                    hostname,
                    port or (443 if parsed.scheme == "https" else 80),
                    type=socket.SOCK_STREAM,
                )
            }
        except OSError as exc:
            raise RetrievalError(f"Cannot resolve localhost safely: {exc}") from exc
        if not addresses or any(not ipaddress.ip_address(address).is_loopback for address in addresses):
            raise RetrievalError("The localhost hostname resolved to a non-loopback address")
        # Prefer IPv4 for compatibility with localhost servers that bind only
        # 127.0.0.1. The selected literal is pinned into each transport request,
        # so the network layer cannot resolve localhost a second time.
        address = min(addresses, key=lambda item: (ipaddress.ip_address(item).version != 4, item))
        return hostname, address
    try:
        if ipaddress.ip_address(hostname).is_loopback:
            return hostname, None
    except ValueError:
        pass
    raise RetrievalError("v0.2 retrieval permits only localhost or loopback IP endpoints")


def validate_local_url(url: str) -> None:
    _validated_loopback_destination(url)


def _pin_localhost_request(request: httpx2.Request) -> httpx2.Request:
    hostname, address = _validated_loopback_destination(str(request.url))
    if address is None:
        return request
    extensions = dict(request.extensions)
    if request.url.scheme == "https":
        extensions["sni_hostname"] = hostname
    return httpx2.Request(
        request.method,
        request.url.copy_with(host=address),
        headers=request.headers,
        stream=request.stream,
        extensions=extensions,
    )


@dataclass
class _ResponseBudget:
    limit: int
    consumed: int = 0

    def add(self, size: int) -> None:
        self.consumed += size
        if self.consumed > self.limit:
            raise RetrievalError(f"MCP transport exceeded the {self.limit}-byte response limit")


class _BudgetedStream(httpx2.AsyncByteStream):
    def __init__(self, stream: httpx2.AsyncByteStream, budget: _ResponseBudget) -> None:
        self._stream = stream
        self._budget = budget

    async def __aiter__(self) -> AsyncIterator[bytes]:
        async for chunk in self._stream:
            self._budget.add(len(chunk))
            yield chunk

    async def aclose(self) -> None:
        await self._stream.aclose()


class _LoopbackTransport(httpx2.AsyncBaseTransport):
    def __init__(self, max_bytes: int, transport: httpx2.AsyncBaseTransport | None = None) -> None:
        self._transport = transport or httpx2.AsyncHTTPTransport(trust_env=False)
        self._budget = _ResponseBudget(max_bytes)

    async def __aenter__(self) -> _LoopbackTransport:
        await self._transport.__aenter__()
        return self

    async def handle_async_request(self, request: httpx2.Request) -> httpx2.Response:
        pinned_request = _pin_localhost_request(request)
        response = await self._transport.handle_async_request(pinned_request)
        if 300 <= response.status_code < 400:
            await response.aclose()
            raise RetrievalError("MCP endpoint redirects are not permitted")
        if content_length := response.headers.get("content-length"):
            try:
                declared_size = int(content_length)
            except ValueError:
                await response.aclose()
                raise RetrievalError("MCP endpoint returned an invalid Content-Length header") from None
            if declared_size < 0 or self._budget.consumed + declared_size > self._budget.limit:
                await response.aclose()
                raise RetrievalError(f"MCP transport exceeded the {self._budget.limit}-byte response limit")
        if not isinstance(response.stream, httpx2.AsyncByteStream):  # pragma: no cover - async transport contract
            await response.aclose()
            raise RetrievalError("MCP endpoint returned an invalid asynchronous response stream")
        return httpx2.Response(
            response.status_code,
            headers=response.headers,
            stream=_BudgetedStream(response.stream, self._budget),
            extensions=response.extensions,
        )

    async def aclose(self) -> None:
        await self._transport.aclose()


def create_loopback_http_client(*, max_bytes: int, timeout: float) -> httpx2.AsyncClient:
    """Create the only HTTP client used for opt-in retrieval."""
    return httpx2.AsyncClient(
        follow_redirects=False,
        trust_env=False,
        timeout=httpx2.Timeout(timeout),
        transport=_LoopbackTransport(max_bytes),
    )


def _encoded_size(tools: list[dict[str, Any]]) -> int:
    try:
        return len(json.dumps({"tools": tools}, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
    except (TypeError, ValueError) as exc:
        raise RetrievalError(f"MCP tools/list returned non-JSON metadata: {exc}") from exc


def validate_retrieved_tools(
    tools: list[dict[str, Any]],
    *,
    max_tools: int = DEFAULT_MAX_TOOLS,
    max_bytes: int = MAX_INPUT_BYTES,
) -> list[dict[str, Any]]:
    if not tools:
        raise RetrievalError("MCP tools/list returned no tools")
    if len(tools) > max_tools:
        raise RetrievalError(f"MCP tools/list exceeded the {max_tools}-tool limit")
    if _encoded_size(tools) > max_bytes:
        raise RetrievalError(f"MCP tools/list exceeded the {max_bytes}-byte metadata limit")
    try:
        validate_structure({"tools": tools}, label="MCP response")
        normalize_tools(tools, "local-mcp-tools-list")
    except Exception as exc:
        raise RetrievalError(f"MCP tools/list returned invalid tool metadata: {exc}") from exc
    return tools


async def _retrieve_sdk(url: str, timeout: float, max_tools: int, max_bytes: int) -> list[dict[str, Any]]:
    # Imported only for this opt-in path. Static scanning does not initialize
    # network transports or the SDK client.
    from mcp.client import Client
    from mcp.client.streamable_http import streamable_http_client

    tools: list[dict[str, Any]] = []
    cursor: str | None = None
    seen_cursors: set[str] = set()
    page_count = 0
    async with create_loopback_http_client(max_bytes=max_bytes, timeout=timeout) as http_client:
        transport = streamable_http_client(url, http_client=http_client)
        async with Client(transport, read_timeout_seconds=timeout, cache=None) as client:
            while True:
                page_count += 1
                if page_count > MAX_RETRIEVAL_PAGES:
                    raise RetrievalError(f"MCP tools/list exceeded the {MAX_RETRIEVAL_PAGES}-page limit")
                result = await client.list_tools(cursor=cursor, cache_mode="refresh")
                page = [item.model_dump(mode="json", by_alias=True, exclude_none=True) for item in result.tools]
                tools.extend(page)
                if len(tools) > max_tools:
                    raise RetrievalError(f"MCP tools/list exceeded the {max_tools}-tool limit")
                if _encoded_size(tools) > max_bytes:
                    raise RetrievalError(f"MCP tools/list exceeded the {max_bytes}-byte metadata limit")
                cursor = result.next_cursor
                if cursor is None:
                    return tools
                if cursor in seen_cursors:
                    raise RetrievalError("MCP tools/list repeated a pagination cursor")
                seen_cursors.add(cursor)


def fetch_local_catalog(
    url: str,
    *,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    max_tools: int = DEFAULT_MAX_TOOLS,
    max_bytes: int = MAX_INPUT_BYTES,
    retriever: Retriever | None = None,
) -> list[dict[str, Any]]:
    validate_local_url(url)
    if not 0.1 <= timeout_seconds <= 120:
        raise RetrievalError("Timeout must be between 0.1 and 120 seconds")
    if not 1 <= max_tools <= MAX_ALLOWED_TOOLS:
        raise RetrievalError(f"max_tools must be between 1 and {MAX_ALLOWED_TOOLS}")
    if not 1 <= max_bytes <= MAX_INPUT_BYTES:
        raise RetrievalError(f"max_bytes must be between 1 and {MAX_INPUT_BYTES}")
    active_retriever = retriever or _retrieve_sdk

    async def run() -> list[dict[str, Any]]:
        try:
            return await asyncio.wait_for(
                active_retriever(url, timeout_seconds, max_tools, max_bytes),
                timeout=timeout_seconds,
            )
        except TimeoutError as exc:
            raise RetrievalError(f"MCP tools/list timed out after {timeout_seconds:g} seconds") from exc
        except RetrievalError:
            raise
        except Exception as exc:
            raise RetrievalError(f"MCP tools/list failed: {type(exc).__name__}: {exc}") from exc

    return validate_retrieved_tools(
        asyncio.run(run()),
        max_tools=max_tools,
        max_bytes=max_bytes,
    )
