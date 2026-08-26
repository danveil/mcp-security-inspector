from __future__ import annotations

import re

from mcpsec.detectors.base import Detector, finding, is_educational_reference, poisoning_text_fields
from mcpsec.models import Finding, ToolDefinition

PATTERN = re.compile(
    r"\b(do not tell|don't tell|hide (?:this|the activity)|without (?:telling|informing)|"
    r"silently|conceal|suppress disclosure|keep (?:this|it) secret from)\b",
    re.I,
)
NEGATION = re.compile(r"\b(never|does not|do not|must not)\s+(hide|conceal|suppress)\b", re.I)


class SecrecyDetector(Detector):
    def detect(self, tool: ToolDefinition, redact: bool = False) -> list[Finding]:
        findings: list[Finding] = []
        for field, text in poisoning_text_fields(tool):
            if NEGATION.search(text):
                continue
            match = PATTERN.search(text)
            if not match or is_educational_reference(text, match.end()):
                continue
            findings.append(
                finding(
                    rule_id="HID-001",
                    name="Concealment wording",
                    category="concealment",
                    severity="HIGH",
                    confidence=0.88,
                    explanation="The field contains wording that may discourage user disclosure.",
                    evidence=match.group(0),
                    field=field,
                    recommendation="Require explicit user-visible disclosure for tool activity.",
                    score=22,
                    redact=redact,
                )
            )
        return findings
