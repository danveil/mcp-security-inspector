from __future__ import annotations

import json
from abc import ABC, abstractmethod
from collections.abc import Iterable
from typing import Any

from mcpsec.constants import EVIDENCE_LENGTH
from mcpsec.models import Finding, Severity, ToolDefinition


def excerpt(value: str, redact: bool = False) -> str:
    value = value.replace("\x1b", "\\x1b")
    if redact:
        return "[REDACTED: untrusted evidence]"
    return value[:EVIDENCE_LENGTH] + ("…" if len(value) > EVIDENCE_LENGTH else "")


def strings(value: Any, prefix: str = "") -> Iterable[tuple[str, str]]:
    if isinstance(value, str):
        yield prefix, value
    elif isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            yield path, str(key)
            yield from strings(item, path)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from strings(item, f"{prefix}[{index}]")


def all_text_fields(tool: ToolDefinition) -> list[tuple[str, str]]:
    values = [("name", tool.name), ("title", tool.title or ""), ("description", tool.description)]
    for field, value in (
        ("input_schema", tool.input_schema),
        ("output_schema", tool.output_schema),
        ("annotations", tool.annotations),
        ("execution", tool.execution),
        ("metadata", tool.metadata),
        ("unknown_fields", tool.unknown_fields),
    ):
        values.extend((f"{field}.{path}", text) for path, text in strings(value))
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
