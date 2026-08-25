from __future__ import annotations

import asyncio
import ipaddress
import json
from collections.abc import Awaitable, Callable
from typing import Any
from urllib.parse import urlsplit

from mcpsec.constants import MAX_INPUT_BYTES
from mcpsec.exceptions import RetrievalError
from mcpsec.normalizer import normalize_tools

DEFAULT_MAX_TOOLS = 500
MAX_ALLOWED_TOOLS = 1_000
DEFAULT_TIMEOUT_SECONDS = 10.0

Retriever = Callable[[str, float, int, int], Awaitable[list[dict[str, Any]]]]


def validate_local_url(url: str) -> None:
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise RetrievalError("MCP endpoint must be an explicit HTTP(S) URL")
    if parsed.username or parsed.password:
        raise RetrievalError("Credentials are not accepted in the MCP endpoint URL")
    if parsed.fragment:
        raise RetrievalError("MCP endpoint URL must not contain a fragment")
    hostname = parsed.hostname.casefold()
    if hostname == "localhost":
        return
    try:
        if ipaddress.ip_address(hostname).is_loopback:
            return
    except ValueError:
        pass
    raise RetrievalError("v0.2 retrieval permits only localhost or loopback IP endpoints")


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
        normalize_tools(tools, "local-mcp-tools-list")
    except Exception as exc:
        raise RetrievalError(f"MCP tools/list returned invalid tool metadata: {exc}") from exc
    return tools


async def _retrieve_sdk(url: str, timeout: float, max_tools: int, max_bytes: int) -> list[dict[str, Any]]:
    # Imported only for this opt-in path. Static scanning does not initialize
    # network transports or the SDK client.
    from mcp.client import Client

    tools: list[dict[str, Any]] = []
    cursor: str | None = None
    seen_cursors: set[str] = set()
    async with Client(url, read_timeout_seconds=timeout, cache=None) as client:
        while True:
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
