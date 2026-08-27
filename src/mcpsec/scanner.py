from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from mcpsec import __version__
from mcpsec.constants import APP_NAME
from mcpsec.detectors import BUILTIN_DETECTORS
from mcpsec.detectors.base import Detector
from mcpsec.loader import load_tools
from mcpsec.models import (
    SEVERITY_RANK,
    Finding,
    FindingBudgetStatus,
    RuleDefinition,
    ScanReport,
    SuppressionDefinition,
    ToolDefinition,
    ToolScanResult,
)
from mcpsec.normalizer import normalize_tools
from mcpsec.resource_policy import (
    MAX_FINDINGS_PER_REPORT,
    MAX_FINDINGS_PER_TOOL,
    MAX_RETAINED_EVIDENCE_CHARS_PER_TOOL,
)
from mcpsec.risk import calculate_risk
from mcpsec.rules.loader import CustomRuleDetector, validate_custom_rule_ids


def is_suppressed(finding_rule_id: str, tool_name: str, suppressions: list[SuppressionDefinition]) -> bool:
    return any(
        item.rule_id == finding_rule_id and (item.tool is None or item.tool == tool_name) for item in suppressions
    )


def _finding_sort_key(item: Finding) -> tuple[int, str, str, str, str]:
    return (-SEVERITY_RANK[item.severity], item.rule_id, item.field, item.evidence, item.explanation)


def _retain_findings(findings: list[Finding], report_capacity: int) -> list[Finding]:
    retained: list[Finding] = []
    evidence_chars = 0
    limit = min(MAX_FINDINGS_PER_TOOL, max(0, report_capacity))
    for item in sorted(findings, key=_finding_sort_key):
        if len(retained) >= limit:
            break
        next_evidence_chars = evidence_chars + len(item.evidence)
        if next_evidence_chars > MAX_RETAINED_EVIDENCE_CHARS_PER_TOOL:
            break
        retained.append(item)
        evidence_chars = next_evidence_chars
    return retained


def analyze_tools(
    tools: list[ToolDefinition],
    *,
    source: str,
    rules: list[RuleDefinition] | None = None,
    suppressions: list[SuppressionDefinition] | None = None,
    redact: bool = False,
    builtin_detectors: Sequence[Detector] | None = None,
) -> ScanReport:
    validate_custom_rule_ids(rules or [])
    detectors = list(BUILTIN_DETECTORS if builtin_detectors is None else builtin_detectors)
    if rules:
        detectors.append(CustomRuleDetector(rules))
    active_suppressions = suppressions or []
    results: list[ToolScanResult] = []
    findings_detected = 0
    findings_retained = 0
    for tool in tools:
        findings = [item for detector in detectors for item in detector.detect(tool, redact)]
        findings = [item for item in findings if not is_suppressed(item.rule_id, tool.name, active_suppressions)]
        detected_for_tool = len(findings)
        retained = _retain_findings(findings, MAX_FINDINGS_PER_REPORT - findings_retained)
        findings_detected += detected_for_tool
        findings_retained += len(retained)
        score, severity = calculate_risk(retained)
        results.append(
            ToolScanResult(
                tool=tool,
                findings=retained,
                risk_score=score,
                severity=severity,
                findings_detected=detected_for_tool,
                findings_truncated=detected_for_tool > len(retained),
            )
        )
    return ScanReport(
        application=APP_NAME,
        version=__version__,
        source=source,
        tools=results,
        finding_budget=FindingBudgetStatus(
            per_tool_limit=MAX_FINDINGS_PER_TOOL,
            report_limit=MAX_FINDINGS_PER_REPORT,
            evidence_char_limit_per_tool=MAX_RETAINED_EVIDENCE_CHARS_PER_TOOL,
            findings_detected=findings_detected,
            findings_retained=findings_retained,
            truncated=findings_detected > findings_retained,
        ),
    )


def analyze_file(
    path: Path,
    *,
    rules: list[RuleDefinition] | None = None,
    suppressions: list[SuppressionDefinition] | None = None,
    redact: bool = False,
) -> ScanReport:
    tools = normalize_tools(load_tools(path), str(path))
    return analyze_tools(tools, source=str(path), rules=rules, suppressions=suppressions, redact=redact)
