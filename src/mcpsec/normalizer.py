from __future__ import annotations

import unicodedata
from typing import Any

from mcpsec.constants import KNOWN_FIELDS, MAX_TEXT_LENGTH
from mcpsec.exceptions import InputError
from mcpsec.models import ToolDefinition


def _normalize(value: Any) -> Any:
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value[:MAX_TEXT_LENGTH])
    if isinstance(value, dict):
        return {str(key): _normalize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalize(item) for item in value]
    return value


def _object(value: Any, field: str, optional: bool = False) -> dict[str, Any] | None:
    if value is None and optional:
        return None
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise InputError(f"{field} must be a JSON object")
    normalized = _normalize(value)
    if not isinstance(normalized, dict):  # defensive type narrowing
        raise InputError(f"{field} must be a JSON object")
    return normalized


def normalize_tool(raw: dict[str, Any], source: str = "unknown") -> ToolDefinition:
    name = raw.get("name")
    if not isinstance(name, str) or not name.strip():
        raise InputError("Every tool requires a non-empty string name")
    description = raw.get("description", "")
    title = raw.get("title")
    if not isinstance(description, str) or (title is not None and not isinstance(title, str)):
        raise InputError("title and description must be strings")
    icons = raw.get("icons", [])
    if not isinstance(icons, list) or not all(isinstance(icon, dict) for icon in icons):
        raise InputError("icons must be an array of objects")
    meta = raw.get("_meta", raw.get("metadata", {}))
    return ToolDefinition(
        name=_normalize(name),
        title=_normalize(title),
        description=_normalize(description),
        input_schema=_object(raw.get("inputSchema", raw.get("input_schema", {})), "inputSchema") or {},
        output_schema=_object(raw.get("outputSchema", raw.get("output_schema")), "outputSchema", True),
        annotations=_object(raw.get("annotations"), "annotations") or {},
        execution=_object(raw.get("execution"), "execution") or {},
        icons=_normalize(icons),
        metadata=_object(meta, "_meta") or {},
        unknown_fields=_normalize({key: value for key, value in raw.items() if key not in KNOWN_FIELDS}),
        source=source,
    )


def normalize_tools(raw_tools: list[dict[str, Any]], source: str = "unknown") -> list[ToolDefinition]:
    tools = [normalize_tool(raw, source) for raw in raw_tools]
    names = [tool.name for tool in tools]
    if len(names) != len(set(names)):
        raise InputError("Duplicate tool names are not supported in one catalog")
    return tools
