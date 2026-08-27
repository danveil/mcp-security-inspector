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
PRIORITY = re.compile(
    r"\b(governs?|controlling|binding|authoritative|takes? precedence|"
    r"ranks? (?:before|ahead of)|supersedes?|yields? to)\b",
    re.I,
)
INSTRUCTION_OBJECT = re.compile(
    r"\b(directives?|polic(?:y|ies)|guidance|instructions?|metadata|tool (?:entry|description)|"
    r"operating rules?)\b",
    re.I,
)
CONFLICT_TARGET = re.compile(
    r"\b(agent|assistant|model)(?:'s)?(?: guidance| requests?| instructions?)?\b|"
    r"\buser(?:'s)? (?:guidance|requests?|instructions?)\b|"
    r"\bconversation (?:guidance|requests?|instructions?)\b|\bregardless of\b|\beven if\b",
    re.I,
)
PRIORITY_NEGATION = re.compile(
    r"\b(?:does not|do not|never|cannot|must not|should not|won't|will not)\s+"
    r"(?:be treated as )?(?:govern|control|override|supersede|take precedence|rank ahead|authoritative)\b",
    re.I,
)


def instruction_priority_signal(text: str) -> TextSignal | None:
    for authority in PRIORITY.finditer(text):
        context, offset = bounded_context(text, authority.start(), authority.end())
        instruction = INSTRUCTION_OBJECT.search(context)
        target = CONFLICT_TARGET.search(context)
        if (
            not instruction
            or not target
            or has_local_pattern(PRIORITY_NEGATION, text, authority.start(), authority.end())
        ):
            continue
        start = min(authority.start(), offset + instruction.start(), offset + target.start())
        end = max(authority.end(), offset + instruction.end(), offset + target.end())
        return TextSignal(start=start, end=end, evidence=text[start:end], kind="instruction_priority")
    return None


class InjectionDetector(Detector):
    def detect(self, tool: ToolDefinition, redact: bool = False) -> list[Finding]:
        findings: list[Finding] = []
        for field, text in poisoning_text_fields(tool):
            match = next((candidate for pattern in PATTERNS if (candidate := pattern.search(text))), None)
            if (
                match
                and not has_local_pattern(NEGATION, text, match.start(), match.end())
                and not is_educational_reference(text, match.start(), match.end())
            ):
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
            priority = instruction_priority_signal(text)
            if priority and not is_educational_reference(text, priority.start, priority.end):
                findings.append(
                    finding(
                        rule_id="PI-002",
                        name="Instruction-priority claim",
                        category="instruction_override",
                        severity="HIGH",
                        confidence=0.84,
                        explanation="Metadata claims authority over conflicting agent or user guidance.",
                        evidence=priority.evidence,
                        field=field,
                        recommendation=(
                            "Remove metadata-level authority claims and preserve normal instruction priority."
                        ),
                        score=23,
                        redact=redact,
                    )
                )
        return findings
