from __future__ import annotations

from typing import Any


def make_tool(**overrides: Any) -> dict[str, Any]:
    tool: dict[str, Any] = {
        "name": "calculator",
        "description": "Add two numbers.",
        "inputSchema": {
            "type": "object",
            "properties": {"a": {"type": "number"}, "b": {"type": "number"}},
        },
    }
    tool.update(overrides)
    return tool
