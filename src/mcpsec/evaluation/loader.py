from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from pydantic import ValidationError

from mcpsec.evaluation.models import CorpusEntry, CorpusManifest
from mcpsec.exceptions import CorpusValidationError, McpsecError
from mcpsec.loader import load_tools
from mcpsec.models import ToolDefinition
from mcpsec.normalizer import normalize_tools

MAX_MANIFEST_BYTES = 2 * 1024 * 1024


@dataclass(frozen=True)
class LoadedSample:
    entry: CorpusEntry
    tool: ToolDefinition


def load_manifest(path: Path) -> CorpusManifest:
    try:
        if path.stat().st_size > MAX_MANIFEST_BYTES:
            raise CorpusValidationError(f"Manifest exceeds {MAX_MANIFEST_BYTES} bytes")
        raw = json.loads(path.read_text(encoding="utf-8"))
        return CorpusManifest.model_validate(raw)
    except CorpusValidationError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError, ValidationError) as exc:
        raise CorpusValidationError(f"Cannot load corpus manifest: {exc}") from exc


def _safe_sample_path(root: Path, relative: str) -> Path:
    candidate = (root / relative).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise CorpusValidationError(f"Sample path escapes corpus directory: {relative}")
    return candidate


def load_corpus(path: Path) -> tuple[CorpusManifest, list[LoadedSample]]:
    manifest = load_manifest(path)
    root = path.resolve().parent
    cache: dict[Path, list[ToolDefinition]] = {}
    loaded: list[LoadedSample] = []
    for entry in manifest.samples:
        sample_path = _safe_sample_path(root, entry.file)
        try:
            if sample_path not in cache:
                cache[sample_path] = normalize_tools(load_tools(sample_path), sample_path.name)
            tools = cache[sample_path]
        except McpsecError as exc:
            raise CorpusValidationError(f"Sample {entry.id}: {exc}") from exc
        if entry.tool_name:
            matches = [tool for tool in tools if tool.name == entry.tool_name]
            if len(matches) != 1:
                raise CorpusValidationError(
                    f"Sample {entry.id}: tool_name {entry.tool_name!r} did not select exactly one tool"
                )
            tool = matches[0]
        elif len(tools) == 1:
            tool = tools[0]
        else:
            raise CorpusValidationError(f"Sample {entry.id}: tool_name is required for a multi-tool catalog")
        loaded.append(LoadedSample(entry=entry, tool=tool))
    return manifest, loaded
