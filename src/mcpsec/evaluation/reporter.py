from __future__ import annotations

import csv
import io
import json

from rich.console import Console
from rich.table import Table

from mcpsec.evaluation.models import (
    CrossSplitIntegrityReport,
    EvaluationReport,
    ExperimentComparisonReport,
    SampleEvaluation,
)
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
    timing_config = metadata.configuration.timing
    console.print(
        f"Timing ({timing_config.mode}, warm-ups={timing_config.warmup_repetitions}, "
        f"measured repetitions={timing_config.measured_repetitions}, machine-dependent): "
        f"observations={timing.observation_count}, total={timing.total_ms:.3f} ms, mean={timing.mean_ms:.3f} ms, "
        f"median={timing.median_ms:.3f} ms, min={timing.minimum_ms:.3f} ms, "
        f"max={timing.maximum_ms:.3f} ms, p95={timing.p95_ms:.3f} ms, "
        f"population SD={timing.standard_deviation_ms:.3f} ms, "
        f"mean corpus pass={timing.mean_corpus_pass_ms:.3f} ms"
    )
    interval_table = Table("Proportion", "Count", "Estimate", "Wilson 95% interval")
    for name, interval in (
        ("Accuracy", report.uncertainty.accuracy),
        ("Recall", report.uncertainty.recall),
        ("False-positive rate", report.uncertainty.false_positive_rate),
    ):
        interval_table.add_row(
            name,
            f"{interval.numerator}/{interval.denominator}",
            _percent(interval.estimate) if interval.estimate is not None else "undefined",
            (
                f"{_percent(interval.lower)} to {_percent(interval.upper)}"
                if interval.lower is not None and interval.upper is not None
                else "undefined"
            ),
        )
    console.print(interval_table)
    for stratification in report.stratified_metrics:
        console.print(
            f"[bold]Stratification: {stratification.dimension}[/bold] "
            f"(available={stratification.available_sample_count}, missing={stratification.missing_sample_count})"
        )
        if not stratification.groups:
            console.print("No populated strata.")
            continue
        stratum_table = Table("Value", "N", "TP", "TN", "FP", "FN", "F1", "Evidence")
        for group in stratification.groups:
            matrix = group.confusion_matrix
            stratum_table.add_row(
                terminal_safe(group.value),
                str(group.sample_count),
                str(matrix.tp),
                str(matrix.tn),
                str(matrix.fp),
                str(matrix.fn),
                _percent(group.metrics.f1),
                "low" if group.low_evidence else "adequate",
            )
        console.print(stratum_table)
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


def render_comparison_terminal(report: ExperimentComparisonReport, console: Console | None = None) -> None:
    console = console or Console()
    console.print("[bold cyan]MCP Experiment Comparison[/bold cyan]")
    console.print(f"A: {terminal_safe(report.experiment_a)}")
    console.print(f"B: {terminal_safe(report.experiment_b)}")
    console.print(f"Compatibility: [bold]{report.compatibility}[/bold]")
    for reason in report.compatibility_reasons:
        console.print(f"- {terminal_safe(reason)}")
    for warning in report.warnings:
        console.print(f"[yellow]Warning:[/yellow] {terminal_safe(warning)}")
    console.print(
        "Enabled built-in rules added in B: "
        + (", ".join(terminal_safe(value) for value in report.enabled_rule_ids_added) or "none")
    )
    console.print(
        "Enabled built-in rules removed in B: "
        + (", ".join(terminal_safe(value) for value in report.enabled_rule_ids_removed) or "none")
    )
    if report.configuration_differences:
        configuration_table = Table("Configuration field", "Experiment A", "Experiment B", show_lines=True)
        for difference in report.configuration_differences:
            configuration_table.add_row(
                terminal_safe(difference.field),
                terminal_safe(json.dumps(difference.experiment_a, ensure_ascii=True, sort_keys=True)),
                terminal_safe(json.dumps(difference.experiment_b, ensure_ascii=True, sort_keys=True)),
            )
        console.print(configuration_table)
    if report.paired_delta is None:
        console.print("No paired deltas were calculated for incompatible artifacts.")
        return
    delta = report.paired_delta
    matrix = delta.confusion_matrix
    metrics = delta.metrics
    table = Table("TP", "TN", "FP", "FN", "Accuracy", "Precision", "Recall", "F1", "FPR")
    table.add_row(
        f"{matrix.tp:+d}",
        f"{matrix.tn:+d}",
        f"{matrix.fp:+d}",
        f"{matrix.fn:+d}",
        f"{metrics.accuracy:+.4f}",
        f"{metrics.precision:+.4f}",
        f"{metrics.recall:+.4f}",
        f"{metrics.f1:+.4f}",
        f"{metrics.false_positive_rate:+.4f}",
    )
    console.print(table)
    console.print(
        f"Prediction changes: {len(delta.prediction_changes)}; "
        f"new/resolved FP: {len(delta.newly_introduced_false_positives)}/"
        f"{len(delta.resolved_false_positives)}; new/resolved FN: "
        f"{len(delta.newly_introduced_false_negatives)}/{len(delta.resolved_false_negatives)}"
    )
    console.print(
        "New false positives in B: "
        + (", ".join(terminal_safe(value) for value in delta.newly_introduced_false_positives) or "none")
    )
    console.print(
        "Resolved false positives in B: "
        + (", ".join(terminal_safe(value) for value in delta.resolved_false_positives) or "none")
    )
    console.print(
        "New false negatives in B: "
        + (", ".join(terminal_safe(value) for value in delta.newly_introduced_false_negatives) or "none")
    )
    console.print(
        "Resolved false negatives in B: "
        + (", ".join(terminal_safe(value) for value in delta.resolved_false_negatives) or "none")
    )
    if delta.prediction_changes:
        prediction_table = Table(
            "Sample",
            "Truth",
            "A → B",
            "Rules A",
            "Rules B",
            "Risk A → B",
            "Failure A → B",
            show_lines=True,
        )
        for change in delta.prediction_changes:
            prediction_table.add_row(
                terminal_safe(change.sample_id),
                change.expected,
                f"{change.prediction_a} → {change.prediction_b}",
                ", ".join(terminal_safe(value) for value in change.triggered_rule_ids_a) or "—",
                ", ".join(terminal_safe(value) for value in change.triggered_rule_ids_b) or "—",
                f"{change.risk_score_a} → {change.risk_score_b}",
                f"{terminal_safe(change.failure_type_a or 'none')} → {terminal_safe(change.failure_type_b or 'none')}",
            )
        console.print(prediction_table)
    if delta.timing.comparable:
        console.print(
            f"Latency Δ (B-A): mean={delta.timing.mean_ms:+.3f} ms, "
            f"p95={delta.timing.p95_ms:+.3f} ms, corpus pass={delta.timing.mean_corpus_pass_ms:+.3f} ms"
        )
    else:
        console.print(f"Latency delta unavailable: {terminal_safe(delta.timing.reason or 'not comparable')}")
