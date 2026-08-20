from __future__ import annotations

import json
from enum import StrEnum
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from mcpsec import __version__
from mcpsec.baseline import create_baseline, load_baseline, write_baseline
from mcpsec.compare import compare_baseline
from mcpsec.constants import APP_NAME
from mcpsec.detectors import BUILTIN_DETECTORS
from mcpsec.exceptions import McpsecError
from mcpsec.fingerprint import fingerprint_tool
from mcpsec.loader import load_tools
from mcpsec.models import SEVERITY_RANK, ScanReport, Severity, ToolDefinition, ToolScanResult
from mcpsec.normalizer import normalize_tools
from mcpsec.reporter import render_terminal, serialize
from mcpsec.risk import calculate_risk
from mcpsec.rules import RULE_EXPLANATIONS, CustomRuleDetector, load_rules

console = Console()
app = typer.Typer(name="mcpsec", help="Defensive static analysis for MCP tool definitions.", no_args_is_help=True)
rules_app = typer.Typer(help="List, validate, and explain rules.", no_args_is_help=True)
app.add_typer(rules_app, name="rules")


class ReportFormat(StrEnum):
    table = "table"
    json = "json"
    csv = "csv"
    sarif = "sarif"


class FailSeverity(StrEnum):
    medium = "medium"
    high = "high"
    critical = "critical"


def _version(value: bool) -> None:
    if value:
        typer.echo(f"mcpsec {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool | None,
        typer.Option("--version", callback=_version, is_eager=True, help="Show version and exit."),
    ] = None,
) -> None:
    """Inspect MCP tool metadata without invoking tools."""


def _tools(path: Path) -> list[ToolDefinition]:
    return normalize_tools(load_tools(path), str(path))


def analyze(path: Path, rules_path: Path | None = None, redact: bool = False) -> ScanReport:
    tools = _tools(path)
    detectors = list(BUILTIN_DETECTORS)
    if rules_path:
        detectors.append(CustomRuleDetector(load_rules(rules_path)))
    results: list[ToolScanResult] = []
    for tool in tools:
        findings = [item for detector in detectors for item in detector.detect(tool, redact)]
        score, severity = calculate_risk(findings)
        results.append(ToolScanResult(tool=tool, findings=findings, risk_score=score, severity=severity))
    return ScanReport(application=APP_NAME, version=__version__, source=str(path), tools=results)


def _handle_error(exc: Exception) -> None:
    if isinstance(exc, McpsecError):
        console.print(f"[red]Input error:[/red] {exc}", markup=True)
        raise typer.Exit(2) from exc
    console.print("[red]Internal application failure.[/red]")
    raise typer.Exit(3) from exc


@app.command()
def scan(
    file: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
    format: Annotated[ReportFormat, typer.Option("--format")] = ReportFormat.table,
    rules: Annotated[Path | None, typer.Option("--rules", exists=True, dir_okay=False)] = None,
    redact: Annotated[bool, typer.Option("--redact", help="Redact evidence excerpts.")] = False,
    fail_on: Annotated[FailSeverity | None, typer.Option("--fail-on")] = None,
    output: Annotated[Path | None, typer.Option("--output", help="Write a structured report.")] = None,
) -> None:
    """Scan static JSON; no tool is invoked and no metadata URL is fetched."""
    try:
        report = analyze(file, rules, redact)
        if format == ReportFormat.table:
            render_terminal(report, console)
        else:
            content = serialize(report, format.value)
            if output:
                output.write_text(content + ("" if content.endswith("\n") else "\n"), encoding="utf-8")
                console.print(f"Wrote {format.value} report to {output}")
            else:
                typer.echo(content)
        if fail_on:
            threshold = Severity[fail_on.value.upper()]
            if any(
                SEVERITY_RANK[finding.severity] >= SEVERITY_RANK[threshold]
                for result in report.tools
                for finding in result.findings
            ):
                raise typer.Exit(1)
    except typer.Exit:
        raise
    except Exception as exc:
        _handle_error(exc)


@app.command()
def baseline(
    file: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
    output: Annotated[Path, typer.Option("--output", help="Baseline JSON destination.")],
) -> None:
    """Create a privacy-conscious SHA-256 baseline."""
    try:
        value = create_baseline(_tools(file), str(file))
        write_baseline(value, output)
        console.print(f"Baseline created: {output} ({len(value.tools)} tools)")
    except Exception as exc:
        _handle_error(exc)


@app.command()
def compare(
    file: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
    baseline: Annotated[Path, typer.Option("--baseline", exists=True, dir_okay=False)],
    verbose: Annotated[bool, typer.Option("--verbose")] = False,
) -> None:
    """Compare current tool metadata with an approved baseline."""
    try:
        drifts = compare_baseline(_tools(file), load_baseline(baseline), verbose)
        if not drifts:
            console.print("No tool-definition drift detected.")
            return
        table = Table("Kind", "Tool", "Previous", "Fields", "Differences", show_lines=True)
        for item in drifts:
            table.add_row(
                item.kind,
                item.tool_name,
                item.previous_name or "—",
                ", ".join(item.fields) or "—",
                json.dumps(item.differences, ensure_ascii=True) if item.differences else "—",
            )
        console.print(table)
    except Exception as exc:
        _handle_error(exc)


@app.command()
def fingerprint(
    file: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
) -> None:
    """Print SHA-256 fingerprints for every tool and component."""
    try:
        payload = {tool.name: fingerprint_tool(tool).model_dump(mode="json") for tool in _tools(file)}
        typer.echo(json.dumps(payload, indent=2))
    except Exception as exc:
        _handle_error(exc)


@rules_app.command("list")
def list_rules() -> None:
    """List built-in rules."""
    table = Table("Rule ID", "Name")
    for rule_id, details in RULE_EXPLANATIONS.items():
        table.add_row(rule_id, details[0])
    console.print(table)


@rules_app.command("validate")
def validate_rules(
    file: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
) -> None:
    """Strictly validate a data-only YAML rule file."""
    try:
        validated = load_rules(file)
        console.print(f"Valid: {len(validated)} rules")
    except Exception as exc:
        _handle_error(exc)


@app.command()
def explain(rule_id: Annotated[str, typer.Argument()]) -> None:
    """Explain rationale, benign uses, and analyst guidance for a built-in rule."""
    details = RULE_EXPLANATIONS.get(rule_id.upper())
    if not details:
        console.print(f"Unknown rule ID: {rule_id}")
        raise typer.Exit(2)
    name, why, benign, guidance = details
    console.print(
        f"[bold]Rule:[/bold] {rule_id.upper()} — {name}\n\n[bold]Why it triggers:[/bold] {why}\n\n"
        f"[bold]Possible benign usage:[/bold] {benign}\n\n[bold]Analyst recommendation:[/bold] {guidance}"
    )


@app.command()
def demo() -> None:
    """Scan the bundled mixed demonstration catalog."""
    demo_path = Path(__file__).parents[2] / "examples" / "mixed_tools.json"
    scan(demo_path)
