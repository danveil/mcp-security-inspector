from __future__ import annotations

import re

from mcpsec.detectors.base import Detector, finding, strings
from mcpsec.models import Finding, ToolDefinition

CATEGORIES = {
    "weather": {"weather", "forecast", "temperature"},
    "calculator": {"calculator", "calculate", "arithmetic", "sum", "number"},
    "filesystem": {"file", "filesystem", "path", "directory", "folder"},
    "database": {"database", "sql", "table", "record"},
    "network": {"network", "http", "url", "request", "download"},
    "shell": {"shell", "command", "executable", "terminal"},
    "email": {"email", "mail", "message", "recipient"},
    "browser": {"browser", "page", "navigate", "click"},
    "credential": {"credential", "password", "token", "secret", "authorization"},
    "search": {"search", "find", "lookup", "query"},
    "code_execution": {"code", "execute", "script", "runtime"},
}


def categories(text: str) -> set[str]:
    words = set(re.findall(r"[a-z][a-z0-9_ -]*", text.lower()))
    flat = " ".join(words).replace("_", "-")
    return {
        category
        for category, terms in CATEGORIES.items()
        if any(re.search(rf"\b{re.escape(term)}\b", flat) for term in terms)
    }


class MismatchDetector(Detector):
    def detect(self, tool: ToolDefinition, redact: bool = False) -> list[Finding]:
        declared = categories(f"{tool.name} {tool.title or ''} {tool.description}")
        schema_text = " ".join(text for _, text in strings(tool.input_schema))
        actual = categories(schema_text)
        high_impact = actual & {
            "shell",
            "filesystem",
            "credential",
            "code_execution",
            "network",
            "database",
        }
        if not high_impact or high_impact & declared:
            return []
        evidence = f"declared={sorted(declared) or ['unclear']}; schema={sorted(high_impact)}"
        return [
            finding(
                rule_id="MIS-001",
                name="Name/description/schema mismatch",
                category="mismatch",
                severity="HIGH",
                confidence=0.8,
                explanation="Privileged schema capabilities are not reflected in the tool's stated purpose.",
                evidence=evidence,
                field="input_schema",
                recommendation=(
                    "Align the name and description with actual capabilities or remove unrelated parameters."
                ),
                score=23,
                redact=redact,
            )
        ]
