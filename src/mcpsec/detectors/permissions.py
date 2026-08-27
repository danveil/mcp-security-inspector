from __future__ import annotations

import re
from dataclasses import dataclass

from mcpsec.detectors.base import Detector, all_text_fields, bounded_context, finding
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


@dataclass(frozen=True)
class CapabilitySignal:
    category: str
    field: str
    evidence: str
    context: str
    destructive: bool


STRUCTURED_CAPABILITIES = (
    (
        "filesystem_read",
        re.compile(
            r"\b(?:read|open|list|inspect)(?:s|ed|ing)?\b.{0,40}\b(?:files?|directories|folders?|paths?)\b", re.I
        ),
        False,
    ),
    (
        "filesystem_write",
        re.compile(
            r"\b(?:create|write|modify|overwrite)(?:s|d|ing)?\b.{0,40}\b(?:files?|directories|folders?|paths?)\b", re.I
        ),
        False,
    ),
    (
        "file_delete",
        re.compile(r"\b(?:delete|remove)(?:s|d|ing)?\b.{0,40}\b(?:files?|directories|folders?|paths?)\b", re.I),
        True,
    ),
    (
        "process_execution",
        re.compile(
            r"\b(?:start|launch|run|execute)(?:s|d|ing)?\b.{0,40}"
            r"\b(?:process(?:es)?|commands?|scripts?|executables?|programs?)\b|"
            r"\b(?:shell|terminal|command execution)\b",
            re.I,
        ),
        False,
    ),
    (
        "outbound_network",
        re.compile(
            r"\b(?:send|post|upload|request|connect)(?:s|ed|ing)?\b.{0,48}"
            r"\b(?:remote|network|internet|api|endpoints?|webhooks?|servers?)\b|"
            r"\b(?:outbound network|external api|http requests?)\b",
            re.I,
        ),
        False,
    ),
    (
        "database_read",
        re.compile(r"\b(?:query|read|select)(?:s|ed|ing)?\b.{0,40}\b(?:databases?|tables?|rows?|records?)\b", re.I),
        False,
    ),
    (
        "database_write",
        re.compile(
            r"\b(?:insert|update|delete|modify)(?:s|d|ing)?\b.{0,40}\b(?:databases?|tables?|rows?|records?)\b", re.I
        ),
        True,
    ),
    (
        "credential_access",
        re.compile(
            r"\b(?:read|access|collect|request|retrieve)(?:s|ed|ing)?\b.{0,40}"
            r"\b(?:credentials?|passwords?|tokens?|keys?|authentication stores?)\b",
            re.I,
        ),
        False,
    ),
    (
        "secret_output",
        re.compile(
            r"\b(?:return|echo|expose|transmit|send|output)(?:s|ed|ing)?\b.{0,40}\b(?:credentials?|passwords?|tokens?|keys?|secrets?)\b",
            re.I,
        ),
        False,
    ),
    (
        "destructive_operation",
        re.compile(
            r"\b(?:purge|wipe|destroy|factory[ _-]?reset)(?:s|d|ing)?\b.{0,40}"
            r"\b(?:data|storage|systems?|resources?|accounts?)\b",
            re.I,
        ),
        True,
    ),
)
NEGATED_CAPABILITY = re.compile(
    r"\b(?:does not|do not|never|cannot|must not|will not|without)\s+(?:\w+[ _-]+){0,3}"
    r"(?:read|open|list|inspect|create|write|modify|overwrite|delete|remove|start|launch|run|execute|"
    r"send|post|upload|request|connect|query|select|insert|update|access|collect|retrieve|return|echo|"
    r"expose|transmit|output|purge|wipe|destroy)\b",
    re.I,
)
NON_OPERATIVE_CONTEXT = re.compile(
    r"\b(simulation only|simulates?|dry[ -]?run|plan[ -]?only|documentation (?:for|of)|would (?:only )?)\b",
    re.I,
)


def capability_signals_for_text(text: str, field: str) -> tuple[CapabilitySignal, ...]:
    signals: list[CapabilitySignal] = []
    for category, pattern, destructive in STRUCTURED_CAPABILITIES:
        for match in pattern.finditer(text):
            context, _ = bounded_context(text, match.start(), match.end())
            if NEGATED_CAPABILITY.search(context) or NON_OPERATIVE_CONTEXT.search(context):
                continue
            signals.append(
                CapabilitySignal(
                    category=category,
                    field=field,
                    evidence=match.group(0),
                    context=context.strip(),
                    destructive=destructive,
                )
            )
    return tuple(sorted(signals, key=lambda item: (item.field, item.category, item.evidence.casefold())))


def capability_signals(tool: ToolDefinition) -> tuple[CapabilitySignal, ...]:
    signals = [
        signal
        for field, text in sorted(all_text_fields(tool), key=lambda item: (item[0], item[1]))
        for signal in capability_signals_for_text(text, field)
    ]
    return tuple(sorted(signals, key=lambda item: (item.field, item.category, item.evidence.casefold())))


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
