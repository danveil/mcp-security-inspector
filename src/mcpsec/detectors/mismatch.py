from __future__ import annotations

import re

from mcpsec.detectors.base import Detector, all_text_fields, finding, safe_transformed_text, strings
from mcpsec.detectors.permissions import capability_signals
from mcpsec.detectors.secrecy import PATTERN as LEGACY_CONCEALMENT
from mcpsec.detectors.secrecy import concealment_signal
from mcpsec.models import Finding, ToolDefinition

CATEGORIES = {
    "weather": {"weather", "forecast", "temperature"},
    "calculator": {"calculator", "calculate", "arithmetic", "sum", "number"},
    "filesystem": {"file", "filesystem", "path", "directory", "folder"},
    "database": {"database", "sql", "table", "record"},
    "network": {"network", "http", "url", "request", "download"},
    "shell": {"shell", "command", "executable", "terminal"},
    "email": {"email", "mail", "message", "recipient"},
    "browser": {"browser", "page", "navigate", "click"},
    "credential": {"credential", "password", "token", "secret", "authorization"},
    "search": {"search", "find", "lookup", "query"},
    "code_execution": {"code", "execute", "script", "runtime"},
}
ALIGNED_PURPOSE = {
    "filesystem_read": re.compile(r"\b(file (?:browser|reader|manager)|filesystem (?:reader|administrator))\b", re.I),
    "filesystem_write": re.compile(r"\b(file (?:editor|manager|writer)|filesystem administrator)\b", re.I),
    "file_delete": re.compile(r"\b(file manager|cleanup utility|filesystem administrator)\b", re.I),
    "process_execution": re.compile(r"\b(terminal|shell|command runner|process manager|script runner)\b", re.I),
    "outbound_network": re.compile(r"\b(http client|network client|webhook sender|api client|request client)\b", re.I),
    "database_read": re.compile(r"\b(database (?:reader|administrator|query tool)|sql client)\b", re.I),
    "database_write": re.compile(r"\b(database administrator|database editor|sql client)\b", re.I),
    "credential_access": re.compile(
        r"\b(password manager|credential manager|authentication client|secret vault)\b", re.I
    ),
    "secret_output": re.compile(r"\b(credential exporter|secret vault|password manager)\b", re.I),
    "destructive_operation": re.compile(r"\b(system maintenance|resource cleanup|administration utility)\b", re.I),
}
NARROW_PURPOSE = re.compile(
    r"\b(formatter|display|preview|summary|calculator|legend|title|read[ -]?only lookup|offline renderer|"
    r"local[ -]?only|simulation|dry[ -]?run|plan[ -]?only)\b",
    re.I,
)
OFFLINE_PURPOSE = re.compile(r"\b(offline|local[ -]?only|no network|without network)\b", re.I)
NO_CONFIRMATION = re.compile(r"\b(without (?:user )?(?:confirmation|consent)|no confirmation)\b", re.I)


def categories(text: str) -> set[str]:
    words = set(re.findall(r"[a-z][a-z0-9_ -]*", text.lower()))
    flat = " ".join(words).replace("_", "-")
    return {
        category
        for category, terms in CATEGORIES.items()
        if any(re.search(rf"\b{re.escape(term)}\b", flat) for term in terms)
    }


class MismatchDetector(Detector):
    def detect(self, tool: ToolDefinition, redact: bool = False) -> list[Finding]:
        declared = categories(f"{tool.name} {tool.title or ''} {tool.description}")
        schema_text = " ".join(text for _, text in strings(tool.input_schema))
        actual = categories(schema_text)
        high_impact = actual & {
            "shell",
            "filesystem",
            "credential",
            "code_execution",
            "network",
            "database",
        }
        results: list[Finding] = []
        if high_impact and not high_impact & declared:
            evidence = f"declared={sorted(declared) or ['unclear']}; schema={sorted(high_impact)}"
            results.append(
                finding(
                    rule_id="MIS-001",
                    name="Name/description/schema mismatch",
                    category="mismatch",
                    severity="HIGH",
                    confidence=0.8,
                    explanation="Privileged schema capabilities are not reflected in the tool's stated purpose.",
                    evidence=evidence,
                    field="input_schema",
                    recommendation=(
                        "Align the name and description with actual capabilities or remove unrelated parameters."
                    ),
                    score=23,
                    redact=redact,
                )
            )
        structured = self._purpose_capability_mismatch(tool, redact)
        if structured:
            results.append(structured)
        return results

    @staticmethod
    def _purpose_capability_mismatch(tool: ToolDefinition, redact: bool) -> Finding | None:
        purpose = f"{tool.name} {tool.title or ''} {tool.description}"
        unauthorized = [
            signal for signal in capability_signals(tool) if not ALIGNED_PURPOSE[signal.category].search(purpose)
        ]
        if not unauthorized:
            return None
        narrow = bool(NARROW_PURPOSE.search(purpose))
        offline_network = bool(OFFLINE_PURPOSE.search(purpose)) and any(
            signal.category == "outbound_network" for signal in unauthorized
        )
        sensitive_under_narrow = narrow and any(
            signal.destructive or signal.category in {"credential_access", "secret_output"} for signal in unauthorized
        )
        unrelated_under_narrow = narrow and len({signal.category for signal in unauthorized}) >= 2
        concealed = any(
            concealment_signal(text) or LEGACY_CONCEALMENT.search(text) for _, text in all_text_fields(tool)
        )
        destructive_without_confirmation = any(
            signal.destructive and NO_CONFIRMATION.search(signal.context) for signal in unauthorized
        )
        corroborators = [
            name
            for name, present in (
                ("offline_network_contradiction", offline_network),
                ("narrow_sensitive_or_destructive_purpose", sensitive_under_narrow),
                ("multiple_unrelated_capabilities", unrelated_under_narrow),
                ("concealed_side_effect", concealed),
                ("destructive_without_confirmation", destructive_without_confirmation),
            )
            if present
        ]
        if not corroborators:
            return None
        signal = unauthorized[0]
        purpose_field = "description" if tool.description else "title" if tool.title else "name"
        destructive_concealment = concealed and any(item.destructive for item in unauthorized)
        evidence = (
            f"purpose[{purpose_field}]={safe_transformed_text(getattr(tool, purpose_field) or '')}; "
            f"capability[{signal.field}]={signal.category}:{safe_transformed_text(signal.evidence)}; "
            f"corroborator={','.join(corroborators)}"
        )
        return finding(
            rule_id="MIS-002",
            name="Corroborated purpose/capability contradiction",
            category="mismatch",
            severity="HIGH" if destructive_concealment else "MEDIUM",
            confidence=0.88 if destructive_concealment else 0.84,
            explanation=(
                "A concrete high-impact capability conflicts with the declared purpose and has "
                "independent corroboration."
            ),
            evidence=evidence,
            field=f"{purpose_field} <-> {signal.field}",
            recommendation=(
                "Align the declared purpose and safeguards with the capability or remove the unrelated operation."
            ),
            score=23 if destructive_concealment else 16,
            redact=redact,
        )
