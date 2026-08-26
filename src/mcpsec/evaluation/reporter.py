from __future__ import annotations

import csv
import io
import json

from rich.console import Console
from rich.table import Table

from mcpsec.evaluation.models import CrossSplitIntegrityReport, EvaluationReport, SampleEvaluation
from mcpsec.reporter import neutralize_csv, terminal_safe


def report_json(report: EvaluationReport) -> str:
    return json.dumps(report.model_dump(mode="json"), indent=2, ensure_ascii=False)


def report_csv(report: EvaluationReport) -> str:
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(
        [
            "sample_id",
            "expected",
            "predicted",
            "risk_score",
            "expected_categories",
            "predicted_categories",
            "rule_ids",
            "corpus_split",
            "difficulty",
            "failure_type",
            "expected_rule_ids",
            "expected_field_locations",
        ]
    )
    for sample in report.samples:
        writer.writerow(
            [
                neutralize_csv(sample.sample_id),
                sample.expected,
                sample.predicted,
                sample.risk_score,
                ";".join(sample.expected_categories),
                ";".join(sample.predicted_categories),
                ";".join(sample.triggered_rule_ids),
                sample.corpus_split,
                sample.difficulty,
                sample.failure_type or "",
                ";".join(sample.expected_rule_ids),
                ";".join(sample.expected_field_locations),
            ]
        )
    return output.getvalue()


def _percent(value: float) -> str:
    return f"{value * 100:.2f}%"


def _render_errors(title: str, samples: list[SampleEvaluation], console: Console) -> None:
    console.print(f"\n[bold]{title} ({len(samples)})[/bold]")
    if not samples:
        console.print("None")
        return
    table = Table("Sample", "Failure", "Expected", "Predicted", "Risk", "Rules", "Evidence", show_lines=True)
    for sample in samples:
        table.add_row(
            terminal_safe(sample.sample_id),
            terminal_safe(sample.failure_type or "unclassified"),
            sample.expected,
            sample.predicted,
            str(sample.risk_score),
            ", ".join(terminal_safe(item.rule_id) for item in sample.findings) or "—",
            "\n".join(terminal_safe(item.evidence) for item in sample.findings) or "No finding",
        )
    console.print(table)


def render_terminal(report: EvaluationReport, console: Console | None = None) -> None:
    console = console or Console()
    metadata = report.metadata
    matrix = report.confusion_matrix
    metrics = report.metrics
    console.print("[bold cyan]MCP Security Evaluation[/bold cyan]")
    console.print(
        f"Corpus: {terminal_safe(metadata.corpus_name)} {metadata.corpus_version}  "
        f"Split: {metadata.corpus_split}  "
        f"Rules: {terminal_safe(metadata.rule_pack_name)} {metadata.rule_pack_version}  "
        f"Samples: {metadata.sample_count}"
    )
    console.print(
        f"Experiment: {metadata.experiment_id}  Corpus SHA-256: {metadata.corpus_sha256[:12]}…  "
        f"Configuration SHA-256: {metadata.configuration_sha256[:12]}…"
    )
    confusion_table = Table("Actual \\ Predicted", "Benign", "Suspicious")
    confusion_table.add_row("Benign", str(matrix.tn), str(matrix.fp))
    confusion_table.add_row("Suspicious", str(matrix.fn), str(matrix.tp))
    console.print(confusion_table)
    metric_table = Table("Accuracy", "Precision", "Recall", "F1", "FPR", "FNR", "Specificity")
    metric_table.add_row(
        _percent(metrics.accuracy),
        _percent(metrics.precision),
        _percent(metrics.recall),
        _percent(metrics.f1),
        _percent(metrics.false_positive_rate),
        _percent(metrics.false_negative_rate),
        _percent(metrics.specificity),
    )
    console.print(metric_table)
    category_table = Table("Category", "Precision", "Recall", "F1", "TP", "FP", "FN")
    for item in report.category_metrics:
        category_table.add_row(
            terminal_safe(item.category),
            _percent(item.metrics.precision),
            _percent(item.metrics.recall),
            _percent(item.metrics.f1),
            str(item.confusion_matrix.tp),
            str(item.confusion_matrix.fp),
            str(item.confusion_matrix.fn),
        )
    console.print(category_table)
    timing = report.timing
    console.print(
        f"Timing (machine-dependent): total={timing.total_ms:.3f} ms, mean={timing.mean_ms:.3f} ms, "
        f"median={timing.median_ms:.3f} ms, min={timing.minimum_ms:.3f} ms, "
        f"max={timing.maximum_ms:.3f} ms, p95={timing.p95_ms:.3f} ms"
    )
    _render_errors("False Positives", report.false_positives, console)
    _render_errors("False Negatives", report.false_negatives, console)


def serialize(report: EvaluationReport, format_name: str) -> str:
    if format_name == "json":
        return report_json(report)
    if format_name == "csv":
        return report_csv(report)
    raise ValueError(f"Unsupported evaluation format: {format_name}")


def integrity_report_json(report: CrossSplitIntegrityReport) -> str:
    return json.dumps(report.model_dump(mode="json"), indent=2, ensure_ascii=False)


def render_integrity_terminal(report: CrossSplitIntegrityReport, console: Console | None = None) -> None:
    console = console or Console()
    console.print("[bold cyan]MCP Corpus Split Integrity[/bold cyan]")
    console.print(
        f"Development: {terminal_safe(report.development.corpus_name)} {report.development.corpus_version} "
        f"({report.development.sample_count} samples, {report.development.corpus_sha256[:12]}…)"
    )
    console.print(
        f"Holdout: {terminal_safe(report.holdout.corpus_name)} {report.holdout.corpus_version} "
        f"({report.holdout.sample_count} samples, {report.holdout.corpus_sha256[:12]}…)"
    )
    issues = [*report.errors, *report.warnings]
    if not issues:
        console.print("[green]PASS:[/green] no duplicate IDs or exact normalized tool content found across splits.")
        return
    table = Table("Severity", "Kind", "Development IDs", "Holdout IDs", "Content SHA-256", show_lines=True)
    for issue in issues:
        table.add_row(
            issue.severity,
            issue.kind,
            ", ".join(terminal_safe(value) for value in issue.development_sample_ids),
            ", ".join(terminal_safe(value) for value in issue.holdout_sample_ids),
            issue.normalized_content_sha256 or "—",
        )
    console.print(table)
