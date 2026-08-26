from __future__ import annotations

import asyncio
import socket
import sys
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from types import ModuleType
from typing import Any

import pytest

import mcpsec.retrieval as retrieval
from mcpsec.exceptions import RetrievalError
from mcpsec.retrieval import _LoopbackTransport, create_loopback_http_client


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        if self.path == "/redirect-public":
            self.send_response(302)
            self.send_header("Location", "https://example.com/mcp")
            self.end_headers()
            return
        if self.path == "/redirect-private":
            self.send_response(307)
            self.send_header("Location", "http://192.168.1.10/mcp")
            self.end_headers()
            return
        body = b"x" * 128 if self.path in {"/large", "/chunked-large"} else b"loopback-ok"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        if self.path != "/chunked-large":
            self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: Any) -> None:
        return


class _IPv6Server(ThreadingHTTPServer):
    address_family = socket.AF_INET6


@contextmanager
def _server(host: str = "127.0.0.1", *, ipv6: bool = False) -> Iterator[ThreadingHTTPServer]:
    server_type = _IPv6Server if ipv6 else ThreadingHTTPServer
    server = server_type((host, 0), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def _get(url: str, *, max_bytes: int = 1_024) -> tuple[int, str]:
    async def run() -> tuple[int, str]:
        async with create_loopback_http_client(max_bytes=max_bytes, timeout=2) as client:
            response = await client.get(url)
            return response.status_code, response.text

    return asyncio.run(run())


@pytest.mark.parametrize("hostname", ["localhost", "127.0.0.1"])
def test_loopback_transport_accepts_localhost_and_ipv4(hostname: str) -> None:
    with _server() as server:
        status, text = _get(f"http://{hostname}:{server.server_port}/ok")
    assert status == 200
    assert text == "loopback-ok"


def test_loopback_transport_accepts_ipv6_when_supported() -> None:
    try:
        with _server("::1", ipv6=True) as server:
            status, text = _get(f"http://[::1]:{server.server_port}/ok")
    except OSError as exc:
        pytest.skip(f"IPv6 loopback is unavailable: {exc}")
    assert status == 200
    assert text == "loopback-ok"


@pytest.mark.parametrize("path", ["redirect-public", "redirect-private"])
def test_loopback_redirects_are_rejected(path: str) -> None:
    with _server() as server, pytest.raises(RetrievalError, match="redirects are not permitted"):
        _get(f"http://127.0.0.1:{server.server_port}/{path}")


def test_proxy_environment_is_ignored(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HTTP_PROXY", "http://127.0.0.1:1")
    monkeypatch.setenv("HTTPS_PROXY", "http://127.0.0.1:1")
    monkeypatch.setenv("ALL_PROXY", "http://127.0.0.1:1")
    monkeypatch.setenv("NO_PROXY", "")
    with _server() as server:
        assert _get(f"http://127.0.0.1:{server.server_port}/ok") == (200, "loopback-ok")


def test_transport_revalidates_every_request_destination() -> None:
    with pytest.raises(RetrievalError, match="only localhost"):
        _get("http://192.168.1.10/mcp")


@pytest.mark.parametrize("path", ["large", "chunked-large"])
def test_transport_enforces_wire_response_limit(path: str) -> None:
    with _server() as server, pytest.raises(RetrievalError, match="response limit"):
        _get(f"http://127.0.0.1:{server.server_port}/{path}", max_bytes=64)


def test_localhost_resolution_must_remain_loopback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(socket, "getaddrinfo", lambda *args, **kwargs: [(2, 1, 6, "", ("203.0.113.10", 80))])
    with pytest.raises(RetrievalError, match="resolved to a non-loopback"):
        retrieval.validate_local_url("http://localhost/mcp")


def test_localhost_connection_is_pinned_to_validated_address(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[retrieval.httpx2.Request] = []

    async def handler(request: retrieval.httpx2.Request) -> retrieval.httpx2.Response:
        seen.append(request)
        return retrieval.httpx2.Response(200, content=b"ok")

    monkeypatch.setattr(
        socket,
        "getaddrinfo",
        lambda *args, **kwargs: [
            (socket.AF_INET6, socket.SOCK_STREAM, 6, "", ("::1", 8765, 0, 0)),
            (socket.AF_INET, socket.SOCK_STREAM, 6, "", ("127.0.0.1", 8765)),
        ],
    )

    async def run() -> None:
        transport = _LoopbackTransport(1_024, retrieval.httpx2.MockTransport(handler))
        async with retrieval.httpx2.AsyncClient(transport=transport) as client:
            response = await client.get("https://localhost:8765/mcp")
            await response.aread()

    asyncio.run(run())

    assert seen[0].url.host == "127.0.0.1"
    assert seen[0].headers["host"] == "localhost:8765"
    assert seen[0].extensions["sni_hostname"] == "localhost"


def test_pagination_is_bounded(monkeypatch: pytest.MonkeyPatch) -> None:
    class Result:
        def __init__(self, cursor: str) -> None:
            self.tools: list[Any] = []
            self.next_cursor = cursor

    class FakeClient:
        calls = 0

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

        async def __aenter__(self) -> FakeClient:
            return self

        async def __aexit__(self, *args: Any) -> None:
            return None

        async def list_tools(self, **kwargs: Any) -> Result:
            self.calls += 1
            return Result(str(self.calls))

    fake_mcp = ModuleType("mcp")
    fake_client = ModuleType("mcp.client")
    fake_streamable = ModuleType("mcp.client.streamable_http")
    fake_client.Client = FakeClient  # type: ignore[attr-defined]
    fake_streamable.streamable_http_client = lambda url, http_client: object()  # type: ignore[attr-defined]
    fake_mcp.client = fake_client  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "mcp", fake_mcp)
    monkeypatch.setitem(sys.modules, "mcp.client", fake_client)
    monkeypatch.setitem(sys.modules, "mcp.client.streamable_http", fake_streamable)
    monkeypatch.setattr(retrieval, "MAX_RETRIEVAL_PAGES", 2)
    with pytest.raises(RetrievalError, match="2-page limit"):
        asyncio.run(retrieval._retrieve_sdk("http://127.0.0.1:8765/mcp", 1, 10, 1_024))
