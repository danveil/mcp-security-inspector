from __future__ import annotations

import re

from mcpsec.detectors.base import (
    Detector,
    TextSignal,
    bounded_context,
    finding,
    has_local_pattern,
    is_educational_reference,
    poisoning_text_fields,
)
from mcpsec.models import Finding, ToolDefinition

PATTERN = re.compile(
    r"\b(do not tell|don't tell|hide (?:this|the activity)|without (?:telling|informing)|"
    r"silently|conceal|suppress disclosure|keep (?:this|it) secret from)\b",
    re.I,
)
NEGATION = re.compile(r"\b(never|does not|do not|must not)\s+(hide|conceal|suppress)\b", re.I)
OMISSION = re.compile(r"\b(omit|withhold|exclude|leave out|keep\b.{0,32}\bout|suppress)\b", re.I)
MATERIAL = re.compile(
    r"\b(activity|operation|side effects?|existence|actions?|access|transfer|behavio[u]?r|instructions?)\b",
    re.I,
)
OBSERVER = re.compile(
    r"\b(user-facing|user-visible|operator-visible|audit(?: log| trail)?|notice|mention|report|"
    r"explanation|view|disclosure|summary)\b",
    re.I,
)
OMISSION_NEGATION = re.compile(
    r"\b(?:never|does not|do not|must not|should not|cannot|won't|will not)\s+"
    r"(?:omit|withhold|exclude|leave out|suppress|hide)\b",
    re.I,
)


def concealment_signal(text: str) -> TextSignal | None:
    for action in OMISSION.finditer(text):
        context, offset = bounded_context(text, action.start(), action.end())
        material = MATERIAL.search(context)
        observer = OBSERVER.search(context)
        if not material or not observer or OMISSION_NEGATION.search(context):
            continue
        start = min(action.start(), offset + material.start(), offset + observer.start())
        end = max(action.end(), offset + material.end(), offset + observer.end())
        return TextSignal(start=start, end=end, evidence=text[start:end], kind="concealment")
    return None


class SecrecyDetector(Detector):
    def detect(self, tool: ToolDefinition, redact: bool = False) -> list[Finding]:
        findings: list[Finding] = []
        for field, text in poisoning_text_fields(tool):
            match = PATTERN.search(text)
            if (
                match
                and not has_local_pattern(NEGATION, text, match.start(), match.end())
                and not is_educational_reference(text, match.end())
            ):
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
            concealment = concealment_signal(text)
            if concealment and not is_educational_reference(text, concealment.end):
                findings.append(
                    finding(
                        rule_id="HID-002",
                        name="Withheld material activity",
                        category="concealment",
                        severity="HIGH",
                        confidence=0.85,
                        explanation=(
                            "Material tool activity is intentionally excluded from user or operator visibility."
                        ),
                        evidence=concealment.evidence,
                        field=field,
                        recommendation=(
                            "Disclose material operations and side effects in user-visible output and audit records."
                        ),
                        score=22,
                        redact=redact,
                    )
                )
        return findings
