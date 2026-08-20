from __future__ import annotations

import re

from mcpsec.detectors.base import Detector, all_text_fields, finding
from mcpsec.models import Finding, ToolDefinition

CAPABILITIES = {
    "file deletion": r"\b(delete|remove)\s+(files?|directories|folders?)\b",
    "filesystem write": r"\b(write|modify|overwrite|create)\s+(files?|directories|folders?)\b",
    "shell execution": r"\b(shell|terminal|command execution|run commands?)\b",
    "code execution": r"\b(execute|run)\s+(code|scripts?|programs?)\b",
    "credential access": r"\b(read|access|collect)\s+(credentials?|passwords?|tokens?|secrets?)\b",
    "external network": r"\b(network|internet|external api|http requests?)\b",
    "database modification": r"\b(update|delete|insert|modify)\s+(database|rows?|records?|tables?)\b",
}


class PermissionsDetector(Detector):
    def detect(self, tool: ToolDefinition, redact: bool = False) -> list[Finding]:
        blob = " ".join(text for _, text in all_text_fields(tool))
        matches = [name for name, pattern in CAPABILITIES.items() if re.search(pattern, blob, re.I)]
        if re.search(r"\b(no|without|does not|never)\s+(?:make |use |have )?(?:external )?network\b", blob, re.I):
            matches = [name for name in matches if name != "external network"]
        if not matches:
            return []
        return [
            finding(
                rule_id="CAP-001",
                name="High-impact capability indicators",
                category="capability",
                severity="INFORMATIONAL",
                confidence=0.72,
                explanation="Metadata advertises potentially high-impact operations; these may be legitimate.",
                evidence=", ".join(matches),
                field="multiple",
                recommendation="Confirm least privilege, user consent, and runtime controls.",
                score=3,
                redact=redact,
            )
        ]
