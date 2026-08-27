from __future__ import annotations

from pathlib import Path
from typing import Any

from mcpsec.exceptions import InputError
from mcpsec.resource_policy import (
    MAX_INPUT_BYTES,
    MAX_STATIC_TOOLS,
    ResourcePolicyError,
    StrictJsonError,
    load_bounded_json,
    validate_structure,
)


def load_json(path: Path) -> Any:
    try:
        value = load_bounded_json(path, max_bytes=MAX_INPUT_BYTES, label="Input", encoding="utf-8-sig")
        validate_structure(value, label="Input")
        return value
    except OSError as exc:
        raise InputError(f"Cannot read input: {path}") from exc
    except (UnicodeError, StrictJsonError, ResourcePolicyError) as exc:
        raise InputError(f"Invalid JSON input: {exc}") from exc


def extract_tools(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        tools = payload
    elif isinstance(payload, dict) and "tools" in payload:
        tools = payload["tools"]
    elif isinstance(payload, dict) and isinstance(payload.get("result"), dict) and "tools" in payload["result"]:
        tools = payload["result"]["tools"]
    elif isinstance(payload, dict) and "name" in payload:
        tools = [payload]
    else:
        raise InputError("Expected one tool, a tool array, or a tools/list response")
    if not isinstance(tools, list) or not all(isinstance(item, dict) for item in tools):
        raise InputError("Tool collection must be an array of objects")
    if len(tools) > MAX_STATIC_TOOLS:
        raise InputError(f"Tool collection exceeds the {MAX_STATIC_TOOLS}-tool limit")
    return tools


def load_tools(path: Path) -> list[dict[str, Any]]:
    return extract_tools(load_json(path))
