from __future__ import annotations

import re

from mcpsec.detectors.base import Detector, all_text_fields, finding
from mcpsec.models import Finding, ToolDefinition

PATTERN = re.compile(
    r"\b(password|credentials?|api[ _-]?keys?|access[ _-]?tokens?|refresh[ _-]?tokens?|"
    r"private[ _-]?keys?|authorization(?: header)?|cookies?|environment[ _-]?variables?|secrets?)\b",
    re.I,
)
LEGITIMATE = re.compile(
    r"\b(password manager|credential manager|authentication|oauth|secret vault|key rotation)\b",
    re.I,
)


class SensitiveDataDetector(Detector):
    def detect(self, tool: ToolDefinition, redact: bool = False) -> list[Finding]:
        legitimate = bool(LEGITIMATE.search(f"{tool.name} {tool.description}"))
        for field, text in all_text_fields(tool):
            match = PATTERN.search(text)
            if match:
                return [
                    finding(
                        rule_id="SEC-001",
                        name="Sensitive credential terminology",
                        category="sensitive_data",
                        severity="LOW" if legitimate else "MEDIUM",
                        confidence=0.62 if legitimate else 0.78,
                        explanation=(
                            "Credential-related terminology indicates potentially sensitive data handling; "
                            "legitimate security tools may trigger this rule."
                        ),
                        evidence=match.group(0),
                        field=field,
                        recommendation=(
                            "Verify the value is necessary, minimized, and protected for the declared purpose."
                        ),
                        score=6 if legitimate else 13,
                        redact=redact,
                    )
                ]
        return []
