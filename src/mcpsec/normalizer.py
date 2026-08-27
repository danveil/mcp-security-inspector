from __future__ import annotations

import unicodedata
from typing import Any

from mcpsec.constants import KNOWN_FIELDS, MAX_NESTING_DEPTH, MAX_TEXT_LENGTH
from mcpsec.exceptions import InputError
from mcpsec.models import ToolDefinition


def _normalize(value: Any, depth: int = 0) -> Any:
    if depth > MAX_NESTING_DEPTH:
        raise InputError(f"Metadata nesting exceeds {MAX_NESTING_DEPTH} levels")
    if isinstance(value, str):
        if len(value) > MAX_TEXT_LENGTH:
            raise InputError(f"Metadata string exceeds {MAX_TEXT_LENGTH} characters")
        return unicodedata.normalize("NFC", value)
    if isinstance(value, dict):
        normalized: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key)
            if len(key_text) > MAX_TEXT_LENGTH:
                raise InputError(f"Metadata key exceeds {MAX_TEXT_LENGTH} characters")
            normalized_key = unicodedata.normalize("NFC", key_text)
            if normalized_key in normalized:
                raise InputError("Metadata contains duplicate keys after normalization")
            normalized[normalized_key] = _normalize(item, depth + 1)
        return normalized
    if isinstance(value, list):
        return [_normalize(item, depth + 1) for item in value]
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


_MISSING = object()


def _aliased_object(raw: dict[str, Any], primary: str, alias: str, *, optional: bool = False) -> dict[str, Any] | None:
    primary_value = raw.get(primary, _MISSING)
    alias_value = raw.get(alias, _MISSING)
    if primary_value is not _MISSING and alias_value is not _MISSING:
        if (primary_value is None) != (alias_value is None):
            raise InputError(f"Conflicting aliases: {primary} and {alias}")
        normalized_primary = _object(primary_value, primary, optional)
        normalized_alias = _object(alias_value, alias, optional)
        if normalized_primary != normalized_alias:
            raise InputError(f"Conflicting aliases: {primary} and {alias}")
        return normalized_primary
    value = primary_value if primary_value is not _MISSING else alias_value
    if value is _MISSING:
        value = None if optional else {}
    return _object(value, primary, optional)


def _required_aliased_object(raw: dict[str, Any], primary: str, alias: str) -> dict[str, Any]:
    if primary not in raw and alias not in raw:
        raise InputError(f"{primary} is required and must be a JSON object")
    value = _aliased_object(raw, primary, alias)
    if value is None:  # defensive narrowing; non-optional aliases never return None
        raise InputError(f"{primary} is required and must be a JSON object")
    if raw.get(primary, raw.get(alias)) is None:
        raise InputError(f"{primary} is required and must be a JSON object")
    return value


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
    return ToolDefinition(
        name=_normalize(name),
        title=_normalize(title),
        description=_normalize(description),
        input_schema=_required_aliased_object(raw, "inputSchema", "input_schema"),
        output_schema=_aliased_object(raw, "outputSchema", "output_schema", optional=True),
        annotations=_object(raw.get("annotations"), "annotations") or {},
        execution=_object(raw.get("execution"), "execution") or {},
        icons=_normalize(icons),
        metadata=_aliased_object(raw, "_meta", "metadata") or {},
        unknown_fields=_normalize({key: value for key, value in raw.items() if key not in KNOWN_FIELDS}),
        source=_normalize(raw.get("source")),
        provenance=source,
    )


def normalize_tools(raw_tools: list[dict[str, Any]], source: str = "unknown") -> list[ToolDefinition]:
    tools = [normalize_tool(raw, source) for raw in raw_tools]
    names = [tool.name for tool in tools]
    if len(names) != len(set(names)):
        raise InputError("Duplicate tool names are not supported in one catalog")
    return tools
