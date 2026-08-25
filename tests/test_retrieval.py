import asyncio
from typing import Any

import pytest

from mcpsec.exceptions import RetrievalError
from mcpsec.retrieval import fetch_local_catalog, validate_local_url


async def valid_retriever(url: str, timeout: float, max_tools: int, max_bytes: int) -> list[dict[str, Any]]:
    return [{"name": "calculator", "description": "Add numbers.", "inputSchema": {"type": "object"}}]


def test_valid_tools_list() -> None:
    tools = fetch_local_catalog("http://127.0.0.1:8765/mcp", retriever=valid_retriever)
    assert tools[0]["name"] == "calculator"


@pytest.mark.parametrize(
    "url",
    ["https://example.com/mcp", "file:///tmp/server", "http://user:pass@localhost/mcp", "http://localhost/mcp#x"],
)
def test_non_local_or_unsafe_url_rejected(url: str) -> None:
    with pytest.raises(RetrievalError):
        validate_local_url(url)


def test_ipv6_loopback_allowed() -> None:
    validate_local_url("http://[::1]:8765/mcp")


def test_no_tools() -> None:
    async def empty(url: str, timeout: float, max_tools: int, max_bytes: int) -> list[dict[str, Any]]:
        return []

    with pytest.raises(RetrievalError, match="no tools"):
        fetch_local_catalog("http://localhost/mcp", retriever=empty)


def test_excessive_tool_count() -> None:
    async def many(url: str, timeout: float, max_tools: int, max_bytes: int) -> list[dict[str, Any]]:
        return [{"name": f"tool_{index}"} for index in range(3)]

    with pytest.raises(RetrievalError, match="tool limit"):
        fetch_local_catalog("http://localhost/mcp", max_tools=2, retriever=many)


def test_excessive_response_size() -> None:
    async def large(url: str, timeout: float, max_tools: int, max_bytes: int) -> list[dict[str, Any]]:
        return [{"name": "large", "description": "x" * 100}]

    with pytest.raises(RetrievalError, match="byte metadata limit"):
        fetch_local_catalog("http://localhost/mcp", max_bytes=20, retriever=large)


def test_malformed_response() -> None:
    async def malformed(url: str, timeout: float, max_tools: int, max_bytes: int) -> list[dict[str, Any]]:
        return [{"description": "missing name"}]

    with pytest.raises(RetrievalError, match="invalid tool metadata"):
        fetch_local_catalog("http://localhost/mcp", retriever=malformed)


@pytest.mark.parametrize("failure", [ConnectionError("offline"), RuntimeError("server error")])
def test_connection_and_server_failure(failure: Exception) -> None:
    async def broken(url: str, timeout: float, max_tools: int, max_bytes: int) -> list[dict[str, Any]]:
        raise failure

    with pytest.raises(RetrievalError, match="tools/list failed"):
        fetch_local_catalog("http://localhost/mcp", retriever=broken)


def test_timeout() -> None:
    async def slow(url: str, timeout: float, max_tools: int, max_bytes: int) -> list[dict[str, Any]]:
        await asyncio.sleep(1)
        return []

    with pytest.raises(RetrievalError, match="timed out"):
        fetch_local_catalog("http://localhost/mcp", timeout_seconds=0.1, retriever=slow)
