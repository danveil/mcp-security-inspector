from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from mcpsec import __version__
from mcpsec.constants import APP_NAME
from mcpsec.detectors import BUILTIN_DETECTORS
from mcpsec.detectors.base import Detector
from mcpsec.loader import load_tools
from mcpsec.models import (
    RuleDefinition,
    ScanReport,
    SuppressionDefinition,
    ToolDefinition,
    ToolScanResult,
)
from mcpsec.normalizer import normalize_tools
from mcpsec.risk import calculate_risk
from mcpsec.rules.loader import CustomRuleDetector


def is_suppressed(finding_rule_id: str, tool_name: str, suppressions: list[SuppressionDefinition]) -> bool:
    return any(
        item.rule_id == finding_rule_id and (item.tool is None or item.tool == tool_name) for item in suppressions
    )


def analyze_tools(
    tools: list[ToolDefinition],
    *,
    source: str,
    rules: list[RuleDefinition] | None = None,
    suppressions: list[SuppressionDefinition] | None = None,
    redact: bool = False,
    builtin_detectors: Sequence[Detector] | None = None,
) -> ScanReport:
    detectors = list(BUILTIN_DETECTORS if builtin_detectors is None else builtin_detectors)
    if rules:
        detectors.append(CustomRuleDetector(rules))
    active_suppressions = suppressions or []
    results: list[ToolScanResult] = []
    for tool in tools:
        findings = [item for detector in detectors for item in detector.detect(tool, redact)]
        findings = [item for item in findings if not is_suppressed(item.rule_id, tool.name, active_suppressions)]
        score, severity = calculate_risk(findings)
        results.append(ToolScanResult(tool=tool, findings=findings, risk_score=score, severity=severity))
    return ScanReport(application=APP_NAME, version=__version__, source=source, tools=results)


def analyze_file(
    path: Path,
    *,
    rules: list[RuleDefinition] | None = None,
    suppressions: list[SuppressionDefinition] | None = None,
    redact: bool = False,
) -> ScanReport:
    tools = normalize_tools(load_tools(path), str(path))
    return analyze_tools(tools, source=str(path), rules=rules, suppressions=suppressions, redact=redact)
