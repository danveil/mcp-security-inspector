from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from mcpsec import __version__
from mcpsec.exceptions import InputError
from mcpsec.fingerprint import fingerprint_tool
from mcpsec.models import BaselineFile, BaselineTool, ToolDefinition


def _summary(tool: ToolDefinition) -> dict[str, object]:
    # Keep structural review data, not descriptions, defaults, or example values.
    properties = tool.input_schema.get("properties", {})
    output_properties = (tool.output_schema or {}).get("properties", {})
    return {
        "title": tool.title,
        "input_properties": sorted(properties) if isinstance(properties, dict) else [],
        "output_properties": sorted(output_properties) if isinstance(output_properties, dict) else [],
        "annotation_keys": sorted(tool.annotations),
        "execution_keys": sorted(tool.execution),
        "metadata_keys": sorted(tool.metadata),
        "unknown_keys": sorted(tool.unknown_fields),
    }


def create_baseline(tools: list[ToolDefinition], source: str, created_at: str | None = None) -> BaselineFile:
    timestamp = created_at or datetime.now(UTC).isoformat()
    entries = [
        BaselineTool(name=tool.name, fingerprints=fingerprint_tool(tool), summary=_summary(tool)) for tool in tools
    ]
    return BaselineFile(application_version=__version__, created_at=timestamp, source=source, tools=entries)


def write_baseline(baseline: BaselineFile, path: Path) -> None:
    path.write_text(
        json.dumps(baseline.model_dump(mode="json"), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def load_baseline(path: Path) -> BaselineFile:
    try:
        return BaselineFile.model_validate_json(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise InputError(f"Invalid baseline: {exc}") from exc
