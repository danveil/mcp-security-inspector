from __future__ import annotations

import json
from enum import StrEnum
from importlib.resources import as_file, files
from io import StringIO
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from mcpsec import __version__
from mcpsec.baseline import create_baseline, load_baseline, write_baseline
from mcpsec.compare import compare_baseline
from mcpsec.constants import BUILTIN_RULE_PACK_NAME, BUILTIN_RULE_PACK_VERSION
from mcpsec.evaluation.comparison import compare_experiment_files, comparison_json
from mcpsec.evaluation.evaluator import evaluate_corpus
from mcpsec.evaluation.integrity import compare_corpus_splits, sha256_file
from mcpsec.evaluation.models import AblationPreset, ExperimentCompatibility, TimingMode
from mcpsec.evaluation.reporter import (
    integrity_report_json,
    render_comparison_terminal,
    render_integrity_terminal,
)
from mcpsec.evaluation.reporter import render_terminal as render_evaluation_terminal
from mcpsec.evaluation.reporter import serialize as serialize_evaluation
from mcpsec.exceptions import McpsecError
from mcpsec.fingerprint import fingerprint_tool
from mcpsec.loader import load_tools
from mcpsec.models import SEVERITY_RANK, ScanReport, Severity, ToolDefinition
from mcpsec.normalizer import normalize_tools
from mcpsec.reporter import render_terminal, serialize, terminal_safe
from mcpsec.resource_policy import MAX_RULE_FILE_BYTES, MAX_SUPPRESSION_FILE_BYTES
from mcpsec.retrieval import DEFAULT_MAX_TOOLS, DEFAULT_TIMEOUT_SECONDS, fetch_local_catalog
from mcpsec.rules import RULE_EXPLANATIONS, load_rule_pack, load_rules
from mcpsec.scanner import analyze_file
from mcpsec.suppressions import load_suppressions

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


class EvaluationFormat(StrEnum):
    terminal = "terminal"
    json = "json"
    csv = "csv"


class IntegrityFormat(StrEnum):
    terminal = "terminal"
    json = "json"


class ComparisonFormat(StrEnum):
    terminal = "terminal"
    json = "json"


class EvaluationThreshold(StrEnum):
    informational = "informational"
    low = "low"
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


def analyze(
    path: Path,
    rules_path: Path | None = None,
    redact: bool = False,
    suppressions_path: Path | None = None,
) -> ScanReport:
    custom_rules = load_rules(rules_path) if rules_path else []
    known_rule_ids = set(RULE_EXPLANATIONS) | {rule.id for rule in custom_rules}
    suppressions = load_suppressions(suppressions_path, known_rule_ids) if suppressions_path else []
    return analyze_file(path, rules=custom_rules, suppressions=suppressions, redact=redact)


def _handle_error(exc: Exception) -> None:
    if isinstance(exc, McpsecError):
        console.print("[red]Input error:[/red]", terminal_safe(exc))
        raise typer.Exit(2) from exc
    console.print("[red]Internal application failure.[/red]")
    raise typer.Exit(3) from exc


@app.command()
def scan(
    file: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
    format: Annotated[ReportFormat, typer.Option("--format")] = ReportFormat.table,
    rules: Annotated[Path | None, typer.Option("--rules", exists=True, dir_okay=False)] = None,
    suppressions: Annotated[
        Path | None,
        typer.Option("--suppressions", exists=True, dir_okay=False, help="Apply justified data-only suppressions."),
    ] = None,
    redact: Annotated[bool, typer.Option("--redact", help="Redact evidence excerpts.")] = False,
    fail_on: Annotated[FailSeverity | None, typer.Option("--fail-on")] = None,
    output: Annotated[Path | None, typer.Option("--output", help="Write a structured report.")] = None,
) -> None:
    """Scan static JSON; no tool is invoked and no metadata URL is fetched."""
    try:
        report = analyze(file, rules, redact, suppressions)
        if format == ReportFormat.table:
            if output:
                buffer = StringIO()
                render_terminal(report, Console(file=buffer, color_system=None, width=120))
                output.write_text(buffer.getvalue(), encoding="utf-8")
                console.print(f"Wrote table report to {terminal_safe(output)}")
            else:
                render_terminal(report, console)
        else:
            content = serialize(report, format.value)
            if output:
                output.write_text(content + ("" if content.endswith("\n") else "\n"), encoding="utf-8")
                console.print(f"Wrote {format.value} report to {terminal_safe(output)}")
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
        console.print(f"Baseline created: {terminal_safe(output)} ({len(value.tools)} tools)")
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
                terminal_safe(item.kind),
                terminal_safe(item.tool_name),
                terminal_safe(item.previous_name or "—"),
                terminal_safe(", ".join(item.fields) or "—"),
                terminal_safe(json.dumps(item.differences, ensure_ascii=True) if item.differences else "—"),
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
        validated = load_rule_pack(file)
        console.print(
            f"Valid: {len(validated.rules)} rules "
            f"({terminal_safe(validated.rule_pack.name)} {terminal_safe(validated.rule_pack.version)})"
        )
    except Exception as exc:
        _handle_error(exc)


@app.command()
def explain(rule_id: Annotated[str, typer.Argument()]) -> None:
    """Explain rationale, benign uses, and analyst guidance for a built-in rule."""
    details = RULE_EXPLANATIONS.get(rule_id.upper())
    if not details:
        console.print(f"Unknown rule ID: {terminal_safe(rule_id)}")
        raise typer.Exit(2)
    name, why, benign, guidance = details
    console.print(
        f"[bold]Rule:[/bold] {rule_id.upper()} — {name}\n\n[bold]Why it triggers:[/bold] {why}\n\n"
        f"[bold]Possible benign usage:[/bold] {benign}\n\n[bold]Analyst recommendation:[/bold] {guidance}"
    )


@app.command()
def demo() -> None:
    """Scan the bundled mixed demonstration catalog."""
    resource = files("mcpsec").joinpath("resources", "mixed_tools.json")
    with as_file(resource) as demo_path:
        scan(demo_path)


@app.command()
def fetch(
    url: Annotated[str, typer.Argument(help="Explicit localhost MCP Streamable HTTP endpoint.")],
    output: Annotated[Path, typer.Option("--output", help="Static JSON catalog destination.")],
    timeout: Annotated[float, typer.Option("--timeout", help="Overall tools/list timeout in seconds.")] = (
        DEFAULT_TIMEOUT_SECONDS
    ),
    max_tools: Annotated[int, typer.Option("--max-tools", help="Maximum accepted catalog size.")] = DEFAULT_MAX_TOOLS,
) -> None:
    """Opt in to a bounded localhost tools/list request; discovered tools are never invoked."""
    try:
        tools = fetch_local_catalog(url, timeout_seconds=timeout, max_tools=max_tools)
        output.write_text(json.dumps({"tools": tools}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        console.print(f"Wrote {len(tools)} tools to {terminal_safe(output)}; no tools were invoked.")
    except Exception as exc:
        _handle_error(exc)


@app.command("evaluate")
def evaluate_command(
    manifest: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
    format: Annotated[EvaluationFormat, typer.Option("--format")] = EvaluationFormat.terminal,
    output: Annotated[Path | None, typer.Option("--output", help="Write the evaluation report.")] = None,
    rules: Annotated[Path | None, typer.Option("--rules", exists=True, dir_okay=False)] = None,
    suppressions: Annotated[
        Path | None,
        typer.Option(
            "--suppressions",
            exists=True,
            dir_okay=False,
            help="Explicitly apply suppressions; disabled by default for research evaluation.",
        ),
    ] = None,
    threshold: Annotated[EvaluationThreshold, typer.Option("--threshold")] = EvaluationThreshold.medium,
    timing_mode: Annotated[TimingMode, typer.Option("--timing-mode")] = TimingMode.analysis_core,
    timing_warmups: Annotated[
        int, typer.Option("--timing-warmups", min=0, max=100, help="Unmeasured warm-ups per sample.")
    ] = 0,
    timing_repetitions: Annotated[
        int, typer.Option("--timing-repetitions", min=1, max=1_000, help="Measured repetitions per sample.")
    ] = 1,
    ablation: Annotated[AblationPreset, typer.Option("--ablation")] = AblationPreset.full,
    disable_rule: Annotated[
        list[str] | None, typer.Option("--disable-rule", help="Disable a stable built-in rule ID; repeatable.")
    ] = None,
    disable_family: Annotated[
        list[str] | None, typer.Option("--disable-family", help="Disable a detector family; repeatable.")
    ] = None,
    runs_dir: Annotated[
        Path | None,
        typer.Option("--runs-dir", help="Also preserve authoritative JSON as <experiment-id>.json in this directory."),
    ] = None,
) -> None:
    """Evaluate detectors against a versioned, labeled static corpus."""
    try:
        custom_rules = []
        pack_name = BUILTIN_RULE_PACK_NAME
        pack_version = BUILTIN_RULE_PACK_VERSION
        custom_pack_name = None
        custom_pack_version = None
        custom_rule_file_sha256 = None
        if rules:
            pack = load_rule_pack(rules)
            custom_rules = pack.rules
            custom_pack_name = pack.rule_pack.name
            custom_pack_version = pack.rule_pack.version
            pack_name = f"{BUILTIN_RULE_PACK_NAME}+{pack.rule_pack.name}"
            pack_version = f"{BUILTIN_RULE_PACK_VERSION}+{pack.rule_pack.version}"
            custom_rule_file_sha256 = sha256_file(rules, max_bytes=MAX_RULE_FILE_BYTES, label="Custom rule file")
        known_rule_ids = set(RULE_EXPLANATIONS) | {rule.id for rule in custom_rules}
        active_suppressions = load_suppressions(suppressions, known_rule_ids) if suppressions else []
        suppression_file_sha256 = (
            sha256_file(suppressions, max_bytes=MAX_SUPPRESSION_FILE_BYTES, label="Suppression file")
            if suppressions
            else None
        )
        invocation = [
            "mcpsec",
            "evaluate",
            manifest.name,
            "--format",
            format.value,
            "--threshold",
            threshold.value,
            "--timing-mode",
            timing_mode.value,
            "--timing-warmups",
            str(timing_warmups),
            "--timing-repetitions",
            str(timing_repetitions),
            "--ablation",
            ablation.value,
        ]
        if output:
            invocation.extend(["--output", output.name])
        if rules:
            invocation.extend(["--rules", rules.name])
        if suppressions:
            invocation.extend(["--suppressions", suppressions.name])
        for rule_id in disable_rule or []:
            invocation.extend(["--disable-rule", rule_id.upper()])
        for family_id in disable_family or []:
            invocation.extend(["--disable-family", family_id.casefold()])
        if runs_dir:
            invocation.extend(["--runs-dir", runs_dir.name])
        report = evaluate_corpus(
            manifest,
            rules=custom_rules,
            rule_pack_name=pack_name,
            rule_pack_version=pack_version,
            custom_rule_pack_name=custom_pack_name,
            custom_rule_pack_version=custom_pack_version,
            custom_rule_file_sha256=custom_rule_file_sha256,
            suppressions=active_suppressions,
            suppression_file_sha256=suppression_file_sha256,
            threshold=Severity[threshold.value.upper()],
            ablation_preset=ablation,
            disabled_builtin_rule_ids=disable_rule,
            disabled_builtin_family_ids=disable_family,
            timing_mode=timing_mode,
            timing_warmups=timing_warmups,
            timing_repetitions=timing_repetitions,
            invocation=invocation,
            repository_path=Path.cwd(),
        )
        if format == EvaluationFormat.terminal:
            if output:
                buffer = StringIO()
                render_evaluation_terminal(report, Console(file=buffer, color_system=None, width=120))
                output.write_text(buffer.getvalue(), encoding="utf-8")
                console.print(f"Wrote terminal evaluation report to {terminal_safe(output)}")
            else:
                render_evaluation_terminal(report, console)
        else:
            content = serialize_evaluation(report, format.value)
            if output:
                output.write_text(content + ("" if content.endswith("\n") else "\n"), encoding="utf-8")
                console.print(f"Wrote {format.value} evaluation report to {terminal_safe(output)}")
            else:
                typer.echo(content)
        if runs_dir:
            runs_dir.mkdir(parents=True, exist_ok=True)
            artifact = runs_dir / f"{report.metadata.experiment_id}.json"
            artifact.write_text(serialize_evaluation(report, "json") + "\n", encoding="utf-8")
            Console(stderr=True).print(f"Preserved authoritative JSON artifact at {terminal_safe(artifact)}")
    except Exception as exc:
        _handle_error(exc)


@app.command("corpus-check")
def corpus_check_command(
    development: Annotated[
        Path, typer.Argument(exists=True, dir_okay=False, readable=True, help="Development corpus manifest.")
    ],
    holdout: Annotated[
        Path, typer.Argument(exists=True, dir_okay=False, readable=True, help="Holdout corpus manifest.")
    ],
    format: Annotated[IntegrityFormat, typer.Option("--format")] = IntegrityFormat.terminal,
    output: Annotated[Path | None, typer.Option("--output", help="Write the integrity report.")] = None,
) -> None:
    """Reject duplicate IDs and exact normalized content across corpus splits."""
    try:
        report = compare_corpus_splits(development, holdout)
        if format == IntegrityFormat.terminal:
            if output:
                buffer = StringIO()
                render_integrity_terminal(report, Console(file=buffer, color_system=None, width=120))
                output.write_text(buffer.getvalue(), encoding="utf-8")
                console.print(f"Wrote terminal corpus integrity report to {terminal_safe(output)}")
            else:
                render_integrity_terminal(report, console)
        else:
            content = integrity_report_json(report)
            if output:
                output.write_text(content + "\n", encoding="utf-8")
                console.print(f"Wrote JSON corpus integrity report to {terminal_safe(output)}")
            else:
                typer.echo(content)
        if not report.passed:
            raise typer.Exit(1)
    except typer.Exit:
        raise
    except Exception as exc:
        _handle_error(exc)


@app.command("compare-experiments")
def compare_experiments_command(
    experiment_a: Annotated[
        Path, typer.Argument(exists=True, dir_okay=False, readable=True, help="Authoritative JSON artifact A.")
    ],
    experiment_b: Annotated[
        Path, typer.Argument(exists=True, dir_okay=False, readable=True, help="Authoritative JSON artifact B.")
    ],
    format: Annotated[ComparisonFormat, typer.Option("--format")] = ComparisonFormat.terminal,
    output: Annotated[Path | None, typer.Option("--output", help="Write the comparison report.")] = None,
) -> None:
    """Compare compatible authoritative experiment artifacts without rescanning."""
    try:
        report = compare_experiment_files(experiment_a, experiment_b)
        if format == ComparisonFormat.terminal:
            if output:
                buffer = StringIO()
                render_comparison_terminal(report, Console(file=buffer, color_system=None, width=140))
                output.write_text(buffer.getvalue(), encoding="utf-8")
                console.print(f"Wrote terminal experiment comparison to {terminal_safe(output)}")
            else:
                render_comparison_terminal(report, console)
        else:
            content = comparison_json(report)
            if output:
                output.write_text(content + "\n", encoding="utf-8")
                console.print(f"Wrote JSON experiment comparison to {terminal_safe(output)}")
            else:
                typer.echo(content)
        if report.compatibility == ExperimentCompatibility.incompatible:
            raise typer.Exit(1)
    except typer.Exit:
        raise
    except Exception as exc:
        _handle_error(exc)
