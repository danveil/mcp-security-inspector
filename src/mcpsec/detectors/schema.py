from __future__ import annotations

import re

from jsonschema import exceptions as js_exceptions
from jsonschema.validators import validator_for

from mcpsec.detectors.base import Detector, finding, strings
from mcpsec.models import Finding, ToolDefinition

PRIVILEGED = re.compile(
    r"\b(shell[ _-]?command|command|executable|working[ _-]?directory|environment|env|"
    r"private[ _-]?key|token|password|authorization|system[ _-]?prompt)\b",
    re.I,
)


def schema_error(schema: object) -> str | None:
    if not isinstance(schema, dict):
        return "schema is not an object"
    try:
        validator_for(schema).check_schema(schema)
    except (js_exceptions.SchemaError, ValueError, TypeError) as exc:
        return str(exc).splitlines()[0]
    return None


class SchemaDetector(Detector):
    def detect(self, tool: ToolDefinition, redact: bool = False) -> list[Finding]:
        findings: list[Finding] = []
        for field, schema in (
            ("input_schema", tool.input_schema),
            ("output_schema", tool.output_schema),
        ):
            if schema is None:
                continue
            error = schema_error(schema)
            if error:
                findings.append(
                    finding(
                        rule_id="SCH-001",
                        name="Malformed JSON Schema",
                        category="schema",
                        severity="MEDIUM",
                        confidence=0.98,
                        explanation="The declared schema is not valid for its selected JSON Schema dialect.",
                        evidence=error,
                        field=field,
                        recommendation="Correct the schema before exposing the tool.",
                        score=14,
                        redact=redact,
                    )
                )
        matches: list[tuple[str, str]] = []
        for path, text in strings(tool.input_schema):
            match = PRIVILEGED.search(text)
            if match:
                matches.append((path, match.group(0)))
        if matches:
            evidence = ", ".join(sorted({match for _, match in matches})[:6])
            severity = "HIGH" if len({m.lower() for _, m in matches}) >= 3 else "MEDIUM"
            findings.append(
                finding(
                    rule_id="SCH-002",
                    name="Privileged input parameters",
                    category="schema",
                    severity=severity,
                    confidence=0.82,
                    explanation="Input fields suggest privileged functionality and warrant capability review.",
                    evidence=evidence,
                    field=f"input_schema.{matches[0][0]}",
                    recommendation="Confirm every privileged parameter is required by the declared purpose.",
                    score=20 if severity == "HIGH" else 13,
                    redact=redact,
                )
            )
        return findings
