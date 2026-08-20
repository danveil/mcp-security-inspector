from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mcpsec.constants import MAX_INPUT_BYTES
from mcpsec.exceptions import InputError


def load_json(path: Path) -> Any:
    try:
        size = path.stat().st_size
    except OSError as exc:
        raise InputError(f"Cannot read input: {path}") from exc
    if size > MAX_INPUT_BYTES:
        raise InputError(f"Input exceeds {MAX_INPUT_BYTES} byte limit")
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
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
    return tools


def load_tools(path: Path) -> list[dict[str, Any]]:
    return extract_tools(load_json(path))
