from __future__ import annotations

import re

from mcpsec.detectors.base import Detector, TextSignal, all_text_fields, bounded_context, finding, has_local_pattern
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
VALUE_ACTION = re.compile(
    r"\b(accept|collect|read|retrieve|access|store|transmit|send|return|output|expose|echo)(?:s|ed|ing)?\b",
    re.I,
)
NEGATED_ACTION = re.compile(
    r"\b(?:does not|do not|never|cannot|must not|should not|won't|will not|without)\s+"
    r"(?:accept|collect|read|retrieve|access|store|transmit|send|return|output|expose|echo)(?:s|ed|ing)?\b",
    re.I,
)
BENIGN_CONTEXT = re.compile(
    r"\b(placeholder|example values?|field names?|name only|aliases?|documentation|reference|"
    r"terminology|redacted|rotation (?:calendar|schedule)|never accepts?|does not accept|does not collect|"
    r"without (?:values?|secrets?|credentials?))\b",
    re.I,
)
SAFE_ACTION_CONTEXT = re.compile(
    r"\b(placeholder|example values?|field names?|name only|redacted|without values?)\b",
    re.I,
)


def sensitive_action_signal(text: str) -> TextSignal | None:
    for sensitive in PATTERN.finditer(text):
        context, offset = bounded_context(text, sensitive.start(), sensitive.end(), radius=96)
        actions = [
            action
            for action in VALUE_ACTION.finditer(context)
            if offset + action.end() <= sensitive.start() or offset + action.start() >= sensitive.end()
            if not has_local_pattern(
                NEGATED_ACTION,
                text,
                offset + action.start(),
                offset + action.end(),
                radius=96,
            )
        ]
        if not actions or SAFE_ACTION_CONTEXT.search(context):
            continue
        action = actions[0]
        start = min(sensitive.start(), offset + action.start())
        end = max(sensitive.end(), offset + action.end())
        return TextSignal(start=start, end=end, evidence=text[start:end], kind="sensitive_value_action")
    return None


class SensitiveDataDetector(Detector):
    def detect(self, tool: ToolDefinition, redact: bool = False) -> list[Finding]:
        legitimate = bool(LEGITIMATE.search(f"{tool.name} {tool.description}"))
        lexical_matches: list[tuple[bool, str, str]] = []
        action_matches: list[tuple[str, TextSignal]] = []
        for field, text in sorted(all_text_fields(tool), key=lambda item: (item[0], item[1])):
            action = sensitive_action_signal(text)
            if action:
                action_matches.append((field, action))
            for match in PATTERN.finditer(text):
                context, _ = bounded_context(text, match.start(), match.end(), radius=96)
                lexical_matches.append((bool(BENIGN_CONTEXT.search(context)), field, match.group(0)))
        if not lexical_matches:
            return []

        unsafe = [item for item in lexical_matches if not item[0]]
        _, lexical_field, lexical_evidence = (unsafe or lexical_matches)[0]
        low_context = legitimate or not unsafe
        results = [
            finding(
                rule_id="SEC-001",
                name="Sensitive credential terminology",
                category="sensitive_data",
                severity="LOW" if low_context else "MEDIUM",
                confidence=0.62 if low_context else 0.78,
                explanation=(
                    "Credential-related terminology indicates potentially sensitive data handling; "
                    "legitimate security tools may trigger this rule."
                ),
                evidence=lexical_evidence,
                field=lexical_field,
                recommendation="Verify the value is necessary, minimized, and protected for the declared purpose.",
                score=6 if low_context else 13,
                redact=redact,
            )
        ]
        if action_matches:
            action_field, action = action_matches[0]
            results.append(
                finding(
                    rule_id="SEC-002",
                    name="Sensitive value handling action",
                    category="sensitive_data",
                    severity="MEDIUM",
                    confidence=0.84,
                    explanation="Metadata links an active data-handling operation to a credential or secret value.",
                    evidence=action.evidence,
                    field=action_field,
                    recommendation="Require necessity, consent, minimization, and secure handling for the value.",
                    score=15,
                    redact=redact,
                )
            )
        return results
