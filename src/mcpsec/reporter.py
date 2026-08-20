from __future__ import annotations

import csv
import io
import json
from collections import Counter
from typing import Any

from rich.console import Console
from rich.markup import escape
from rich.table import Table

from mcpsec.models import ScanReport


def report_json(report: ScanReport) -> str:
    return json.dumps(report.model_dump(mode="json"), indent=2, ensure_ascii=False)


def neutralize_csv(value: Any) -> str:
    text = str(value).replace("\x00", "")
    if text.startswith(("\t", "\r")) or text.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + text
    return text


def terminal_safe(value: Any) -> str:
    """Render hostile values literally on both legacy and Unicode terminals."""
    text = str(value).replace("\x1b", r"\x1b")
    text = "".join(char if char in "\n\t" or ord(char) >= 32 else f"\\x{ord(char):02x}" for char in text)
    return escape(text.encode("ascii", "backslashreplace").decode("ascii"))


def report_csv(report: ScanReport) -> str:
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(
        [
            "tool",
            "risk_score",
            "severity",
            "rule_id",
            "rule_severity",
            "field",
            "evidence",
            "recommendation",
        ]
    )
    for result in report.tools:
        if not result.findings:
            writer.writerow(
                [
                    neutralize_csv(result.tool.name),
                    result.risk_score,
                    result.severity,
                    "",
                    "",
                    "",
                    "",
                    "",
                ]
            )
        for finding in result.findings:
            writer.writerow(
                [
                    neutralize_csv(result.tool.name),
                    result.risk_score,
                    result.severity,
                    neutralize_csv(finding.rule_id),
                    finding.severity,
                    neutralize_csv(finding.field),
                    neutralize_csv(finding.evidence),
                    neutralize_csv(finding.recommendation),
                ]
            )
    return output.getvalue()


def report_sarif(report: ScanReport) -> str:
    rules: dict[str, dict[str, Any]] = {}
    results: list[dict[str, Any]] = []
    levels = {
        "INFORMATIONAL": "note",
        "LOW": "note",
        "MEDIUM": "warning",
        "HIGH": "error",
        "CRITICAL": "error",
    }
    for tool_result in report.tools:
        for item in tool_result.findings:
            rules[item.rule_id] = {
                "id": item.rule_id,
                "name": item.rule_name,
                "shortDescription": {"text": item.explanation},
                "help": {"text": item.recommendation},
            }
            results.append(
                {
                    "ruleId": item.rule_id,
                    "level": levels[item.severity],
                    "message": {"text": f"{tool_result.tool.name}: {item.explanation} Evidence: {item.evidence}"},
                    "locations": [
                        {
                            "physicalLocation": {
                                "artifactLocation": {"uri": report.source},
                                "region": {"startLine": 1},
                            }
                        }
                    ],
                }
            )
    sarif = {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "mcpsec",
                        "version": report.version,
                        "informationUri": "https://github.com/",
                        "rules": list(rules.values()),
                    }
                },
                "results": results,
            }
        ],
    }
    return json.dumps(sarif, indent=2, ensure_ascii=False)


def render_terminal(report: ScanReport, console: Console | None = None) -> None:
    console = console or Console()
    total = len(report.tools)
    affected = sum(bool(result.findings) for result in report.tools)
    severity = Counter(str(finding.severity) for result in report.tools for finding in result.findings)
    console.print("[bold cyan]MCP Tool Security Inspector[/bold cyan]")
    console.print(f"Tools: {total}  Clean: {total - affected}  With findings: {affected}")
    if severity:
        console.print("Findings: " + ", ".join(f"{key}={value}" for key, value in sorted(severity.items())))
    table = Table(show_lines=True)
    table.add_column("Tool")
    table.add_column("Risk", justify="right")
    table.add_column("Severity")
    table.add_column("Findings")
    for result in report.tools:
        findings = (
            "\n".join(
                f"{item.severity} {terminal_safe(item.rule_id)} - {terminal_safe(item.rule_name)}\n"
                f"{terminal_safe(item.field)}: {terminal_safe(item.evidence)}\n"
                f"Recommendation: {terminal_safe(item.recommendation)}"
                for item in result.findings
            )
            or "No indicators detected"
        )
        table.add_row(terminal_safe(result.tool.name), f"{result.risk_score}/100", str(result.severity), findings)
    console.print(table)


def serialize(report: ScanReport, format_name: str) -> str:
    if format_name == "json":
        return report_json(report)
    if format_name == "csv":
        return report_csv(report)
    if format_name == "sarif":
        return report_sarif(report)
    raise ValueError(f"Unsupported format: {format_name}")
