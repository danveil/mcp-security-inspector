from __future__ import annotations

import re

from mcpsec.detectors.base import Detector, finding, is_educational_reference, poisoning_text_fields
from mcpsec.models import Finding, ToolDefinition

PATTERNS = [
    re.compile(
        r"\b(ignore|disregard|override)\s+(all\s+)?(previous|prior|system|user)\s+instructions?\b",
        re.I,
    ),
    re.compile(r"\b(follow|prioriti[sz]e|obey)\s+(this|tool)\s+instructions?\s+(above|over|instead)", re.I),
    re.compile(r"\b(system|assistant|model)\s*:\s*(must|always|never)\b", re.I),
]
NEGATION = re.compile(
    r"\b(does not|do not|never|cannot|must not|won't|will not)\s+(ignore|override|disregard)\b",
    re.I,
)


class InjectionDetector(Detector):
    def detect(self, tool: ToolDefinition, redact: bool = False) -> list[Finding]:
        findings: list[Finding] = []
        for field, text in poisoning_text_fields(tool):
            if NEGATION.search(text):
                continue
            match = next((candidate for pattern in PATTERNS if (candidate := pattern.search(text))), None)
            if not match or is_educational_reference(text, match.end()):
                continue
            findings.append(
                finding(
                    rule_id="PI-001",
                    name="Possible instruction override",
                    category="instruction_override",
                    severity="HIGH",
                    confidence=0.86,
                    explanation=(
                        "Language appears directed at changing model instruction priority; context requires review."
                    ),
                    evidence=match.group(0),
                    field=field,
                    recommendation=(
                        "Remove model-directed instruction-priority language or document why it is necessary."
                    ),
                    score=24,
                    redact=redact,
                )
            )
        return findings
