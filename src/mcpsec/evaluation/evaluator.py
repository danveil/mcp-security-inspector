from __future__ import annotations

import statistics
import time
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path

from mcpsec import __version__
from mcpsec.constants import APP_NAME, BUILTIN_RULE_PACK_NAME, BUILTIN_RULE_PACK_VERSION, KNOWN_CATEGORIES
from mcpsec.evaluation.ablation import ResolvedAblation, resolve_ablation
from mcpsec.evaluation.integrity import corpus_sha256
from mcpsec.evaluation.loader import LoadedSample, load_corpus, load_sample
from mcpsec.evaluation.metrics import calculate_metrics, confusion, timing_statistics
from mcpsec.evaluation.models import (
    AblationPreset,
    CategoryEvaluation,
    CorpusLabel,
    EvaluationMetadata,
    EvaluationReport,
    FailureType,
    GitMetadata,
    RuntimeEnvironment,
    SampleEvaluation,
    TimingConfiguration,
    TimingMode,
)
from mcpsec.evaluation.research import (
    build_evaluation_configuration,
    build_timing_configuration,
    collect_git_metadata,
    collect_runtime_environment,
    configuration_sha256,
    experiment_id,
    utc_now,
)
from mcpsec.evaluation.stratification import stratify_samples
from mcpsec.evaluation.uncertainty import uncertainty_for_matrix
from mcpsec.models import SEVERITY_RANK, Finding, RuleDefinition, Severity, SuppressionDefinition, ToolScanResult
from mcpsec.scanner import analyze_tools


def _failure_type(
    *,
    expected: CorpusLabel,
    predicted: CorpusLabel,
    expected_categories: list[str],
    predicted_categories: list[str],
    findings: list[Finding],
) -> FailureType | None:
    if expected == CorpusLabel.benign and predicted == CorpusLabel.suspicious:
        return FailureType.false_positive
    if expected == CorpusLabel.suspicious and predicted == CorpusLabel.benign:
        if not findings:
            return FailureType.false_negative_no_finding
        return FailureType.false_negative_below_threshold
    if set(expected_categories) != set(predicted_categories):
        return FailureType.category_mismatch
    return None


def _portable_invocation(arguments: list[str] | None, manifest_path: Path) -> list[str]:
    values = arguments or ["mcpsec", "evaluate", manifest_path.name]
    return [Path(value).name if Path(value).is_absolute() else value for value in values]


def _analyze_sample(
    sample: LoadedSample,
    *,
    tool_root: Path,
    timing: TimingConfiguration,
    ablation: ResolvedAblation,
    rules: list[RuleDefinition],
    suppressions: list[SuppressionDefinition],
    clock: Callable[[], float],
) -> tuple[ToolScanResult, list[float]]:
    def execute() -> ToolScanResult:
        tool = load_sample(tool_root, sample.entry).tool if timing.mode == TimingMode.static_end_to_end else sample.tool
        return analyze_tools(
            [tool],
            source=sample.entry.id,
            rules=rules,
            suppressions=suppressions,
            builtin_detectors=ablation.detectors,
        ).tools[0]

    for _ in range(timing.warmup_repetitions):
        execute()

    observations: list[float] = []
    reference: ToolScanResult | None = None
    for _ in range(timing.measured_repetitions):
        started = clock()
        result = execute()
        observations.append(max(0.0, (clock() - started) * 1_000))
        if reference is None:
            reference = result
        elif result != reference:
            raise RuntimeError(f"Repeated evaluation produced inconsistent results for sample {sample.entry.id}")
    if reference is None:  # pragma: no cover - TimingConfiguration requires at least one measured repetition
        raise RuntimeError("Evaluation produced no measured result")
    return reference, observations


def evaluate_corpus(
    manifest_path: Path,
    *,
    rules: list[RuleDefinition] | None = None,
    rule_pack_name: str = BUILTIN_RULE_PACK_NAME,
    rule_pack_version: str = BUILTIN_RULE_PACK_VERSION,
    custom_rule_pack_name: str | None = None,
    custom_rule_pack_version: str | None = None,
    custom_rule_file_sha256: str | None = None,
    suppressions: list[SuppressionDefinition] | None = None,
    suppression_file_sha256: str | None = None,
    threshold: Severity = Severity.MEDIUM,
    ablation_preset: AblationPreset = AblationPreset.full,
    disabled_builtin_rule_ids: list[str] | None = None,
    disabled_builtin_family_ids: list[str] | None = None,
    timing_mode: TimingMode = TimingMode.analysis_core,
    timing_warmups: int = 0,
    timing_repetitions: int = 1,
    invocation: list[str] | None = None,
    repository_path: Path | None = None,
    git_metadata: GitMetadata | None = None,
    runtime_environment: RuntimeEnvironment | None = None,
    timestamp_factory: Callable[[], datetime] = utc_now,
    clock: Callable[[], float] = time.perf_counter,
) -> EvaluationReport:
    manifest, loaded_unsorted = load_corpus(manifest_path)
    loaded = sorted(loaded_unsorted, key=lambda sample: sample.entry.id)
    active_rules = rules or []
    active_suppressions = suppressions or []
    ablation = resolve_ablation(
        preset=ablation_preset,
        disabled_rule_ids=disabled_builtin_rule_ids,
        disabled_family_ids=disabled_builtin_family_ids,
    )
    timing_configuration = build_timing_configuration(
        mode=timing_mode,
        warmup_repetitions=timing_warmups,
        measured_repetitions=timing_repetitions,
    )
    tool_root = manifest_path.resolve().parent
    all_observations: list[float] = []
    outcomes: list[SampleEvaluation] = []
    for sample in loaded:
        result, observations = _analyze_sample(
            sample,
            tool_root=tool_root,
            timing=timing_configuration,
            ablation=ablation,
            rules=active_rules,
            suppressions=active_suppressions,
            clock=clock,
        )
        all_observations.extend(observations)
        suspicious = any(SEVERITY_RANK[item.severity] >= SEVERITY_RANK[threshold] for item in result.findings)
        predicted = CorpusLabel.suspicious if suspicious else CorpusLabel.benign
        expected_categories = sorted(sample.entry.categories)
        predicted_categories = sorted({item.category for item in result.findings})
        outcomes.append(
            SampleEvaluation(
                sample_id=sample.entry.id,
                corpus_split=manifest.split,
                expected=sample.entry.expected,
                predicted=predicted,
                expected_categories=expected_categories,
                predicted_categories=predicted_categories,
                rationale=sample.entry.rationale,
                difficulty=sample.entry.difficulty,
                provenance=sample.entry.provenance,
                expected_rule_ids=sorted(sample.entry.expected_rule_ids),
                expected_field_locations=sorted(sample.entry.field_locations),
                triggered_rule_ids=sorted({item.rule_id for item in result.findings}),
                classification_threshold=threshold,
                failure_type=_failure_type(
                    expected=sample.entry.expected,
                    predicted=predicted,
                    expected_categories=expected_categories,
                    predicted_categories=predicted_categories,
                    findings=result.findings,
                ),
                researcher_notes=sample.entry.notes,
                risk_score=result.risk_score,
                findings=result.findings,
                elapsed_ms=statistics.fmean(observations),
                timing_observations=len(observations),
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

    corpus_digest = corpus_sha256(manifest_path, manifest)
    configuration = build_evaluation_configuration(
        threshold=threshold,
        corpus_split=manifest.split,
        ablation=ablation,
        timing=timing_configuration,
        rules=active_rules,
        suppressions=active_suppressions,
        custom_rule_pack_name=custom_rule_pack_name,
        custom_rule_pack_version=custom_rule_pack_version,
        custom_rule_file_sha256=custom_rule_file_sha256,
        suppression_file_sha256=suppression_file_sha256,
    )
    configuration_digest = configuration_sha256(configuration)
    timestamp = timestamp_factory()
    if timestamp.tzinfo is None:
        raise ValueError("Evaluation timestamp must be timezone-aware")
    timestamp = timestamp.astimezone(UTC)
    environment = runtime_environment or collect_runtime_environment()
    git = git_metadata or collect_git_metadata(repository_path)
    return EvaluationReport(
        metadata=EvaluationMetadata(
            experiment_id=experiment_id(timestamp, corpus_digest, configuration_digest),
            application=APP_NAME,
            application_version=__version__,
            rule_pack_name=rule_pack_name,
            rule_pack_version=rule_pack_version,
            corpus_name=manifest.corpus_name,
            corpus_version=manifest.corpus_version,
            corpus_split=manifest.split,
            corpus_methodology_version=manifest.methodology_version,
            corpus_methodology_note=manifest.methodology_note,
            label_review_status=manifest.label_review_status,
            source_license_policy=manifest.source_license_policy,
            corpus_sha256=corpus_digest,
            configuration=configuration,
            configuration_sha256=configuration_digest,
            git=git,
            environment=environment,
            python_version=environment.python_version,
            timestamp_utc=timestamp.isoformat(),
            invocation=_portable_invocation(invocation, manifest_path),
            timing_methodology=(
                f"{timing_configuration.mode.value}; warm-ups excluded; {timing_configuration.definition}"
            ),
            sample_count=len(outcomes),
            suppressions_applied=bool(active_suppressions),
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
        timing=timing_statistics(
            all_observations,
            sample_count=len(outcomes),
            measured_repetitions=timing_configuration.measured_repetitions,
        ),
        uncertainty=uncertainty_for_matrix(matrix),
        stratified_metrics=stratify_samples(outcomes),
    )
