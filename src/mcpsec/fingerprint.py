from __future__ import annotations

import hashlib
from typing import Any

from mcpsec.canonicalizer import canonical_json, canonical_tool
from mcpsec.models import Fingerprints, ToolDefinition


def sha256(value: Any) -> str:
    text = value if isinstance(value, str) else canonical_json(value)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def fingerprint_tool(tool: ToolDefinition) -> Fingerprints:
    metadata = {
        "icons": tool.icons,
        "metadata": tool.metadata,
        "unknown_fields": tool.unknown_fields,
    }
    return Fingerprints(
        full_sha256=sha256(canonical_tool(tool)),
        description_sha256=sha256(tool.description),
        input_schema_sha256=sha256(tool.input_schema),
        output_schema_sha256=sha256(tool.output_schema) if tool.output_schema is not None else None,
        annotations_sha256=sha256(tool.annotations),
        execution_sha256=sha256(tool.execution),
        metadata_sha256=sha256(metadata),
    )
