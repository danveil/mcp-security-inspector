from __future__ import annotations

import base64
import re
import unicodedata

from mcpsec.detectors.base import Detector, all_text_fields, finding, is_educational_reference, safe_transformed_text
from mcpsec.detectors.injection import PATTERNS as INJECTION_PATTERNS
from mcpsec.detectors.injection import instruction_priority_signal
from mcpsec.detectors.permissions import capability_signals_for_text
from mcpsec.detectors.representations import decode_representations
from mcpsec.detectors.secrecy import PATTERN as SECRECY_PATTERN
from mcpsec.detectors.secrecy import concealment_signal
from mcpsec.detectors.sensitive_data import sensitive_action_signal
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
        decoded_batch = decode_representations(all_text_fields(tool))
        if decoded_batch.issues:
            issue = decoded_batch.issues[0]
            results.append(
                finding(
                    rule_id="OBF-005",
                    name="Bounded encoded-content review",
                    category="obfuscation",
                    severity="INFORMATIONAL",
                    confidence=1.0,
                    explanation=(
                        "A recognized encoded candidate was not decoded because a fixed safety budget was reached."
                    ),
                    evidence=(f"encoding={issue.encoding}; reason={issue.reason}; observed={issue.observed}"),
                    field=issue.field,
                    recommendation="Reduce the candidate size or count and review it in an isolated, bounded workflow.",
                    score=1,
                    redact=redact,
                )
            )
        fields = dict(all_text_fields(tool))
        for candidate in decoded_batch.candidates:
            signals: list[str] = []
            if any(pattern.search(candidate.decoded) for pattern in INJECTION_PATTERNS) or instruction_priority_signal(
                candidate.decoded
            ):
                signals.append("instruction_priority")
            if SECRECY_PATTERN.search(candidate.decoded) or concealment_signal(candidate.decoded):
                signals.append("concealment")
            if sensitive_action_signal(candidate.decoded):
                signals.append("sensitive_value_action")
            if capability_signals_for_text(candidate.decoded, candidate.field):
                signals.append("high_impact_capability")
            original_field = fields.get(candidate.field, "")
            if not signals or is_educational_reference(original_field, candidate.start, candidate.end):
                continue
            results.append(
                finding(
                    rule_id="OBF-005",
                    name="Decoded high-risk metadata",
                    category="obfuscation",
                    severity="MEDIUM",
                    confidence=0.88,
                    explanation="A bounded depth-one decode exposed a high-risk static metadata construct.",
                    evidence=(
                        f"encoding={candidate.encoding}; "
                        f"original={safe_transformed_text(candidate.original, limit=64)}; "
                        f"decoded={safe_transformed_text(candidate.decoded, limit=96)}; signal={','.join(signals)}"
                    ),
                    field=candidate.field,
                    recommendation="Replace encoded directives with transparent metadata and review the decoded text.",
                    score=14,
                    redact=redact,
                )
            )
        return results
