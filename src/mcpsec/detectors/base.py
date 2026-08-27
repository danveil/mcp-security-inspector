from __future__ import annotations

import json
import re
import unicodedata
from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from mcpsec.constants import EVIDENCE_LENGTH
from mcpsec.models import Finding, Severity, ToolDefinition


def excerpt(value: str, redact: bool = False) -> str:
    value = value.replace("\x1b", "\\x1b")
    if redact:
        return "[REDACTED: untrusted evidence]"
    return value[:EVIDENCE_LENGTH] + ("…" if len(value) > EVIDENCE_LENGTH else "")


@dataclass(frozen=True)
class TextSignal:
    start: int
    end: int
    evidence: str
    kind: str


CONTEXT_BOUNDARY = re.compile(r"[.!?;\r\n]")
CONTRASTIVE_CONNECTOR = re.compile(r"\b(?:but|however|yet|instead)\b", re.I)
COORDINATING_CONNECTOR = re.compile(r"(?:,|\b(?:and|or|nor)\b)", re.I)


def bounded_context(text: str, start: int, end: int, *, radius: int = 160) -> tuple[str, int]:
    """Return a sentence-bounded local window and its offset in ``text``."""
    lower = max(0, start - radius)
    upper = min(len(text), end + radius)
    prefix = text[lower:start]
    suffix = text[end:upper]
    previous = list(CONTEXT_BOUNDARY.finditer(prefix))
    if previous:
        lower += previous[-1].end()
    following = CONTEXT_BOUNDARY.search(suffix)
    if following:
        upper = end + following.start()
    return text[lower:upper], lower


def has_local_pattern(
    pattern: re.Pattern[str],
    text: str,
    start: int,
    end: int,
    *,
    radius: int = 160,
    include_coordinated: bool = False,
) -> bool:
    context, offset = bounded_context(text, start, end, radius=radius)
    local_start = start - offset
    local_end = end - offset
    for match in pattern.finditer(context):
        if match.start() < local_end and match.end() > local_start:
            return True
        if include_coordinated and match.end() <= local_start:
            bridge = context[match.end() : local_start]
            if len(bridge) <= 80 and COORDINATING_CONNECTOR.search(bridge) and not CONTRASTIVE_CONNECTOR.search(bridge):
                return True
    return False


def safe_transformed_text(value: str, *, limit: int = 96) -> str:
    """Render transformed hostile text without terminal or invisible control effects."""
    rendered: list[str] = []
    for character in value:
        category = unicodedata.category(character)
        if character == "\x1b" or (category in {"Cc", "Cf"} and character not in "\t\r\n"):
            rendered.append(f"U+{ord(character):04X}")
        elif character == "\n":
            rendered.append("\\n")
        elif character == "\r":
            rendered.append("\\r")
        elif character == "\t":
            rendered.append("\\t")
        else:
            rendered.append(character)
        if sum(len(part) for part in rendered) >= limit:
            break
    result = "".join(rendered)
    return result[:limit] + ("…" if len(result) > limit or len(value) > len(rendered) else "")


def strings(value: Any, prefix: str = "") -> Iterable[tuple[str, str]]:
    if isinstance(value, str):
        yield prefix, value
    elif isinstance(value, dict):
        for key in sorted(value, key=str):
            item = value[key]
            path = f"{prefix}.{key}" if prefix else str(key)
            yield path, str(key)
            yield from strings(item, path)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from strings(item, f"{prefix}[{index}]")


def text_values(value: Any, prefix: str = "") -> Iterable[tuple[str, str]]:
    """Yield string values with stable paths, without treating mapping keys as content."""
    if isinstance(value, str):
        yield prefix, value
    elif isinstance(value, dict):
        for key in sorted(value, key=str):
            path = f"{prefix}.{key}" if prefix else str(key)
            yield from text_values(value[key], path)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from text_values(item, f"{prefix}[{index}]")


def poisoning_text_fields(tool: ToolDefinition) -> list[tuple[str, str]]:
    values = [("description", tool.description)]
    if tool.title:
        values.append(("title", tool.title))
    for field, value in (
        ("inputSchema", tool.input_schema),
        ("outputSchema", tool.output_schema),
        ("annotations", tool.annotations),
        ("execution", tool.execution),
        ("icons", tool.icons),
        ("metadata", tool.metadata),
        ("source", tool.source),
    ):
        values.extend(text_values(value, field))
    values.extend(text_values(tool.unknown_fields))
    return values


EDUCATIONAL_CONTEXT = re.compile(
    r"\b(documentation|educational|training example|security warning|prompt[ -]injection|"
    r"unsafe phrase|quoted? (?:phrase|example)|reviewers?|terminology)\b",
    re.I,
)
DIRECT_ACTION_AFTER_INDICATOR = re.compile(
    r"\b(?:and|then)\s+(?:proceed|send|use|run|call|reveal|collect|obey|follow|execute)\b",
    re.I,
)


def is_educational_reference(text: str, match_start: int, match_end: int) -> bool:
    """Suppress an educational quotation unless it continues with a direct action."""
    context, offset = bounded_context(text, match_start, match_end)
    local_end = match_end - offset
    return bool(EDUCATIONAL_CONTEXT.search(context)) and not DIRECT_ACTION_AFTER_INDICATOR.search(context[local_end:])


def all_text_fields(tool: ToolDefinition) -> list[tuple[str, str]]:
    values = [("name", tool.name), ("title", tool.title or ""), ("description", tool.description)]
    for field, value in (
        ("input_schema", tool.input_schema),
        ("output_schema", tool.output_schema),
        ("annotations", tool.annotations),
        ("execution", tool.execution),
        ("icons", tool.icons),
        ("metadata", tool.metadata),
        ("source", tool.source),
        ("unknown_fields", tool.unknown_fields),
    ):
        values.extend(
            (
                field if not path else f"{field}{path}" if path.startswith("[") else f"{field}.{path}",
                text,
            )
            for path, text in strings(value)
        )
    return values


class Detector(ABC):
    @abstractmethod
    def detect(self, tool: ToolDefinition, redact: bool = False) -> list[Finding]: ...


def finding(
    *,
    rule_id: str,
    name: str,
    category: str,
    severity: str | Severity,
    confidence: float,
    explanation: str,
    evidence: str,
    field: str,
    recommendation: str,
    score: float,
    redact: bool = False,
) -> Finding:
    return Finding(
        rule_id=rule_id,
        rule_name=name,
        category=category,
        severity=Severity(severity),
        confidence=confidence,
        explanation=explanation,
        evidence=excerpt(evidence, redact),
        field=field,
        recommendation=recommendation,
        score_contribution=score,
    )


def compact_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, separators=(",", ":"))
