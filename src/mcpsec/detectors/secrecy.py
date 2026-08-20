from __future__ import annotations

import re

from mcpsec.detectors.base import Detector, finding
from mcpsec.models import Finding, ToolDefinition

PATTERN = re.compile(
    r"\b(do not tell|don't tell|hide (?:this|the activity)|without (?:telling|informing)|"
    r"silently|conceal|suppress disclosure|keep (?:this|it) secret from)\b",
    re.I,
)
NEGATION = re.compile(r"\b(never|does not|do not|must not)\s+(hide|conceal|suppress)\b", re.I)


class SecrecyDetector(Detector):
    def detect(self, tool: ToolDefinition, redact: bool = False) -> list[Finding]:
        if NEGATION.search(tool.description):
            return []
        match = PATTERN.search(tool.description)
        if not match:
            return []
        return [
            finding(
                rule_id="HID-001",
                name="Concealment wording",
                category="concealment",
                severity="HIGH",
                confidence=0.88,
                explanation="The description contains wording that may discourage user disclosure.",
                evidence=match.group(0),
                field="description",
                recommendation="Require explicit user-visible disclosure for tool activity.",
                score=22,
                redact=redact,
            )
        ]
