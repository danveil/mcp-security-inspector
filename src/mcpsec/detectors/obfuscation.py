from __future__ import annotations

import base64
import re
import unicodedata

from mcpsec.detectors.base import Detector, all_text_fields, finding
from mcpsec.models import Finding, ToolDefinition

ZERO_WIDTH = {"\u200b", "\u200c", "\u200d", "\u2060", "\ufeff"}
BIDI = {chr(code) for code in (*range(0x202A, 0x202F), *range(0x2066, 0x206A))}
ENCODED = re.compile(r"(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{80,}={0,2}(?![A-Za-z0-9+/])")


def escaped_invisible(text: str) -> str:
    return " ".join(
        f"U+{ord(char):04X} {unicodedata.name(char, 'UNKNOWN')}" for char in text if char in ZERO_WIDTH | BIDI
    )


class ObfuscationDetector(Detector):
    def detect(self, tool: ToolDefinition, redact: bool = False) -> list[Finding]:
        results: list[Finding] = []
        for field, text in all_text_fields(tool):
            invisible = escaped_invisible(text)
            if invisible:
                severity = "HIGH" if any(char in BIDI for char in text) else "MEDIUM"
                results.append(
                    finding(
                        rule_id="OBF-001",
                        name="Invisible Unicode formatting",
                        category="obfuscation",
                        severity=severity,
                        confidence=0.96,
                        explanation="Hidden Unicode controls may alter how metadata is perceived or displayed.",
                        evidence=invisible,
                        field=field,
                        recommendation="Remove invisible controls unless explicitly required and reviewed.",
                        score=18 if severity == "HIGH" else 12,
                        redact=redact,
                    )
                )
                break
        if len(tool.description) > 12_000:
            results.append(
                finding(
                    rule_id="OBF-002",
                    name="Unusually long description",
                    category="obfuscation",
                    severity="LOW",
                    confidence=0.75,
                    explanation="An unusually long description can hide instructions and strain review.",
                    evidence=f"{len(tool.description)} characters",
                    field="description",
                    recommendation="Shorten the description and move documentation elsewhere.",
                    score=7,
                    redact=redact,
                )
            )
        if re.search(r"(?:\s*\n){20,}| {100,}", tool.description):
            results.append(
                finding(
                    rule_id="OBF-003",
                    name="Extreme whitespace",
                    category="obfuscation",
                    severity="LOW",
                    confidence=0.82,
                    explanation="Extreme whitespace may conceal content from ordinary review.",
                    evidence="extreme whitespace sequence",
                    field="description",
                    recommendation="Normalize whitespace before approval.",
                    score=6,
                    redact=redact,
                )
            )
        encoded = ENCODED.search(tool.description)
        if encoded:
            try:
                base64.b64decode(encoded.group(0), validate=True)
                valid = True
            except ValueError:
                valid = False
            if valid:
                results.append(
                    finding(
                        rule_id="OBF-004",
                        name="Encoded-looking block",
                        category="obfuscation",
                        severity="MEDIUM",
                        confidence=0.78,
                        explanation="A long valid Base64 block is present; it was not executed or interpreted.",
                        evidence=encoded.group(0),
                        field="description",
                        recommendation="Decode only in an isolated review workflow and document its purpose.",
                        score=11,
                        redact=redact,
                    )
                )
        return results
