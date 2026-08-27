from __future__ import annotations

import json
import math
import unicodedata
from typing import Any

from mcpsec.exceptions import InputError
from mcpsec.models import ToolDefinition


def canonical_value(value: Any) -> Any:
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, dict):
        return {str(key): canonical_value(value[key]) for key in sorted(value, key=str)}
    if isinstance(value, list):
        return [canonical_value(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        raise InputError("NaN and Infinity are not valid canonical JSON numbers")
    if value is None or isinstance(value, (bool, int, float)):
        return value
    raise InputError(f"Unsupported canonical value: {type(value).__name__}")


def canonical_json(value: Any) -> str:
    return json.dumps(
        canonical_value(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def canonical_tool(tool: ToolDefinition) -> str:
    payload = tool.model_dump(exclude={"provenance"}, mode="json")
    if tool.source is None:
        payload.pop("source", None)
    return canonical_json(payload)
