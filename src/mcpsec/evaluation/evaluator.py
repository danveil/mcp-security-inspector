from __future__ import annotations

import platform
import time
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

from mcpsec import __version__
from mcpsec.constants import APP_NAME, BUILTIN_RULE_PACK_NAME, BUILTIN_RULE_PACK_VERSION, KNOWN_CATEGORIES
from mcpsec.evaluation.loader import load_corpus
from mcpsec.evaluation.metrics import calculate_metrics, confusion, timing_statistics
from mcpsec.evaluation.models import (
    CategoryEvaluation,
    CorpusLabel,
    EvaluationMetadata,
    EvaluationReport,
    SampleEvaluation,
)
from mcpsec.models import SEVERITY_RANK, RuleDefinition, Severity, SuppressionDefinition
from mcpsec.scanner import analyze_tools


def evaluate_corpus(
    manifest_path: Path,
    *,
    rules: list[RuleDefinition] | None = None,
    rule_pack_name: str = BUILTIN_RULE_PACK_NAME,
    rule_pack_version: str = BUILTIN_RULE_PACK_VERSION,
    suppressions: list[SuppressionDefinition] | None = None,
    threshold: Severity = Severity.MEDIUM,
    clock: Callable[[], float] = time.perf_counter,
) -> EvaluationReport:
    manifest, loaded = load_corpus(manifest_path)
    outcomes: list[SampleEvaluation] = []
    for sample in loaded:
        started = clock()
        scan = analyze_tools(
            [sample.tool],
            source=sample.entry.id,
            rules=rules,
            suppressions=suppressions,
        )
        elapsed_ms = max(0.0, (clock() - started) * 1_000)
        result = scan.tools[0]
        suspicious = any(SEVERITY_RANK[item.severity] >= SEVERITY_RANK[threshold] for item in result.findings)
        predicted = CorpusLabel.suspicious if suspicious else CorpusLabel.benign
        outcomes.append(
            SampleEvaluation(
                sample_id=sample.entry.id,
                expected=sample.entry.expected,
                predicted=predicted,
                expected_categories=sorted(sample.entry.categories),
                predicted_categories=sorted({item.category for item in result.findings}),
                risk_score=result.risk_score,
                findings=result.findings,
                elapsed_ms=elapsed_ms,
            )
        )

    expected_binary = [item.expected == CorpusLabel.suspicious for item in outcomes]
    predicted_binary = [item.predicted == CorpusLabel.suspicious for item in outcomes]
    matrix = confusion(expected_binary, predicted_binary)
    observed_categories = {category for item in outcomes for category in item.predicted_categories}
    category_metrics = []
    for category in sorted(KNOWN_CATEGORIES | observed_categories):
        category_matrix = confusion(
            [category in item.expected_categories for item in outcomes],
            [category in item.predicted_categories for item in outcomes],
        )
        category_metrics.append(
            CategoryEvaluation(
                category=category,
                confusion_matrix=category_matrix,
                metrics=calculate_metrics(category_matrix),
            )
        )
    return EvaluationReport(
        metadata=EvaluationMetadata(
            application=APP_NAME,
            application_version=__version__,
            rule_pack_name=rule_pack_name,
            rule_pack_version=rule_pack_version,
            corpus_name=manifest.corpus_name,
            corpus_version=manifest.corpus_version,
            python_version=platform.python_version(),
            timestamp_utc=datetime.now(UTC).isoformat(),
            sample_count=len(outcomes),
            suppressions_applied=bool(suppressions),
            suspicious_threshold=threshold.value,
        ),
        confusion_matrix=matrix,
        metrics=calculate_metrics(matrix),
        category_metrics=category_metrics,
        false_positives=[
            item
            for item in outcomes
            if item.expected == CorpusLabel.benign and item.predicted == CorpusLabel.suspicious
        ],
        false_negatives=[
            item
            for item in outcomes
            if item.expected == CorpusLabel.suspicious and item.predicted == CorpusLabel.benign
        ],
        samples=outcomes,
        timing=timing_statistics([item.elapsed_ms for item in outcomes]),
    )
