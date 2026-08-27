from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from pydantic import ValidationError

from mcpsec.constants import KNOWN_CATEGORIES
from mcpsec.evaluation.ablation import resolve_ablation
from mcpsec.evaluation.metrics import calculate_metrics, confusion
from mcpsec.evaluation.models import (
    OUTPUT_SCHEMA_VERSION,
    ClassificationMetricDelta,
    ConfigurationDifference,
    ConfusionMatrixDelta,
    EvaluationReport,
    ExperimentComparisonReport,
    ExperimentCompatibility,
    PairedExperimentDelta,
    SampleEvaluation,
    SamplePredictionChange,
    TimingDelta,
)
from mcpsec.evaluation.research import configuration_sha256, experiment_id
from mcpsec.evaluation.stratification import stratify_samples
from mcpsec.evaluation.uncertainty import uncertainty_for_matrix
from mcpsec.exceptions import ExperimentArtifactError
from mcpsec.models import SEVERITY_RANK, Severity
from mcpsec.resource_policy import ResourcePolicyError, read_bounded_text, validate_structure
from mcpsec.risk import calculate_risk

MAX_EXPERIMENT_ARTIFACT_BYTES = 20 * 1024 * 1024
ABLATION_AND_TIMING_FIELDS = {
    "ablation_preset",
    "disabled_builtin_detector_ids",
    "disabled_builtin_family_ids",
    "disabled_builtin_rule_ids",
    "enabled_builtin_detector_ids",
    "enabled_builtin_family_ids",
    "enabled_builtin_rule_ids",
    "timing",
}


def _expected_failure(sample: SampleEvaluation) -> str | None:
    if sample.expected.value == "benign" and sample.predicted.value == "suspicious":
        return "false_positive"
    if sample.expected.value == "suspicious" and sample.predicted.value == "benign":
        return "false_negative_no_finding" if not sample.findings else "false_negative_below_threshold"
    if set(sample.expected_categories) != set(sample.predicted_categories):
        return "category_mismatch"
    return None


def _validate_report_consistency(report: EvaluationReport) -> None:
    metadata = report.metadata
    configuration = metadata.configuration
    sample_ids = [sample.sample_id for sample in report.samples]
    if len(sample_ids) != len(set(sample_ids)):
        raise ExperimentArtifactError("Experiment artifact contains duplicate sample IDs")
    if metadata.sample_count != len(report.samples):
        raise ExperimentArtifactError("Experiment artifact sample count does not match its sample records")
    if metadata.corpus_split != configuration.corpus_split:
        raise ExperimentArtifactError("Experiment artifact corpus split is internally inconsistent")
    if metadata.suspicious_threshold != configuration.suspicious_threshold.value:
        raise ExperimentArtifactError("Experiment artifact threshold is internally inconsistent")
    if metadata.python_version != metadata.environment.python_version:
        raise ExperimentArtifactError("Experiment artifact Python version is internally inconsistent")
    if metadata.configuration_sha256 != configuration_sha256(configuration):
        raise ExperimentArtifactError("Experiment artifact configuration SHA-256 is invalid")
    try:
        timestamp = datetime.fromisoformat(metadata.timestamp_utc)
    except ValueError as exc:
        raise ExperimentArtifactError("Experiment artifact timestamp is invalid") from exc
    if timestamp.tzinfo is None:
        raise ExperimentArtifactError("Experiment artifact timestamp must include a timezone")
    if metadata.experiment_id != experiment_id(timestamp, metadata.corpus_sha256, metadata.configuration_sha256):
        raise ExperimentArtifactError("Experiment artifact experiment ID is inconsistent with its identities")

    resolved = resolve_ablation(
        preset=configuration.ablation_preset,
        disabled_rule_ids=configuration.disabled_builtin_rule_ids,
        disabled_family_ids=configuration.disabled_builtin_family_ids,
    )
    recorded_ablation = (
        tuple(configuration.enabled_builtin_detector_ids),
        tuple(configuration.disabled_builtin_detector_ids),
        tuple(configuration.enabled_builtin_family_ids),
        tuple(configuration.disabled_builtin_family_ids),
        tuple(configuration.enabled_builtin_rule_ids),
        tuple(configuration.disabled_builtin_rule_ids),
    )
    resolved_ablation = (
        tuple(sorted(resolved.enabled_detector_ids)),
        tuple(sorted(resolved.disabled_detector_ids)),
        tuple(sorted(resolved.enabled_family_ids)),
        tuple(sorted(resolved.disabled_family_ids)),
        tuple(sorted(resolved.enabled_rule_ids)),
        tuple(sorted(resolved.disabled_rule_ids)),
    )
    if recorded_ablation != resolved_ablation:
        raise ExperimentArtifactError("Experiment artifact ablation sets are internally inconsistent")

    threshold = Severity(metadata.suspicious_threshold)
    for sample in report.samples:
        if sample.corpus_split != metadata.corpus_split or sample.classification_threshold != threshold:
            raise ExperimentArtifactError(f"Experiment artifact sample {sample.sample_id} has inconsistent context")
        triggered_rule_ids = sorted({finding.rule_id for finding in sample.findings})
        predicted_categories = sorted({finding.category for finding in sample.findings})
        predicted_suspicious = any(
            SEVERITY_RANK[finding.severity] >= SEVERITY_RANK[threshold] for finding in sample.findings
        )
        predicted = "suspicious" if predicted_suspicious else "benign"
        risk_score, _ = calculate_risk(sample.findings)
        if (
            sample.triggered_rule_ids != triggered_rule_ids
            or sample.predicted_categories != predicted_categories
            or sample.predicted.value != predicted
            or sample.risk_score != risk_score
            or (sample.failure_type.value if sample.failure_type else None) != _expected_failure(sample)
        ):
            raise ExperimentArtifactError(f"Experiment artifact sample {sample.sample_id} is internally inconsistent")
        if sample.timing_observations != configuration.timing.measured_repetitions:
            raise ExperimentArtifactError(f"Experiment artifact sample {sample.sample_id} has inconsistent timing")

    expected_binary = [sample.expected.value == "suspicious" for sample in report.samples]
    predicted_binary = [sample.predicted.value == "suspicious" for sample in report.samples]
    matrix = confusion(expected_binary, predicted_binary)
    if report.confusion_matrix != matrix or report.metrics != calculate_metrics(matrix):
        raise ExperimentArtifactError("Experiment artifact aggregate metrics are internally inconsistent")
    if report.uncertainty != uncertainty_for_matrix(matrix):
        raise ExperimentArtifactError("Experiment artifact uncertainty is internally inconsistent")
    if report.stratified_metrics != stratify_samples(report.samples):
        raise ExperimentArtifactError("Experiment artifact stratified metrics are internally inconsistent")

    observed_categories = {category for sample in report.samples for category in sample.predicted_categories}
    category_metrics = []
    for category in sorted(KNOWN_CATEGORIES | observed_categories):
        category_matrix = confusion(
            [category in sample.expected_categories for sample in report.samples],
            [category in sample.predicted_categories for sample in report.samples],
        )
        category_metrics.append((category, category_matrix, calculate_metrics(category_matrix)))
    recorded_category_metrics = [
        (item.category, item.confusion_matrix, item.metrics) for item in report.category_metrics
    ]
    if recorded_category_metrics != category_metrics:
        raise ExperimentArtifactError("Experiment artifact category metrics are internally inconsistent")

    expected_false_positives = [
        sample
        for sample in report.samples
        if sample.expected.value == "benign" and sample.predicted.value == "suspicious"
    ]
    expected_false_negatives = [
        sample
        for sample in report.samples
        if sample.expected.value == "suspicious" and sample.predicted.value == "benign"
    ]
    if report.false_positives != expected_false_positives or report.false_negatives != expected_false_negatives:
        raise ExperimentArtifactError("Experiment artifact failure lists are internally inconsistent")
    timing = report.timing
    if (
        timing.sample_count != metadata.sample_count
        or timing.measured_repetitions != configuration.timing.measured_repetitions
        or timing.observation_count != metadata.sample_count * configuration.timing.measured_repetitions
    ):
        raise ExperimentArtifactError("Experiment artifact timing counts are internally inconsistent")


def load_evaluation_artifact(path: Path) -> EvaluationReport:
    try:
        raw = json.loads(read_bounded_text(path, max_bytes=MAX_EXPERIMENT_ARTIFACT_BYTES, label="Experiment artifact"))
        validate_structure(raw, label="Experiment artifact")
        if not isinstance(raw, dict) or not isinstance(raw.get("metadata"), dict):
            raise ExperimentArtifactError("Experiment artifact must contain a metadata object")
        schema_version = raw["metadata"].get("output_schema_version")
        if schema_version != OUTPUT_SCHEMA_VERSION:
            raise ExperimentArtifactError(
                f"Unsupported experiment output schema {schema_version!r}; expected {OUTPUT_SCHEMA_VERSION}"
            )
        report = EvaluationReport.model_validate(raw)
        _validate_report_consistency(report)
        return report
    except ExperimentArtifactError:
        raise
    except (OSError, UnicodeError, json.JSONDecodeError, ValidationError, ResourcePolicyError) as exc:
        raise ExperimentArtifactError(f"Cannot load experiment artifact: {exc}") from exc


def _configuration_differences(a: EvaluationReport, b: EvaluationReport) -> list[ConfigurationDifference]:
    config_a = a.metadata.configuration.model_dump(mode="json")
    config_b = b.metadata.configuration.model_dump(mode="json")
    return [
        ConfigurationDifference(field=field, experiment_a=config_a.get(field), experiment_b=config_b.get(field))
        for field in sorted(set(config_a) | set(config_b))
        if config_a.get(field) != config_b.get(field)
    ]


def _sample_map(report: EvaluationReport) -> dict[str, SampleEvaluation]:
    return {sample.sample_id: sample for sample in report.samples}


def _failure_ids(report: EvaluationReport, expected: str, predicted: str) -> set[str]:
    return {
        sample.sample_id
        for sample in report.samples
        if sample.expected.value == expected and sample.predicted.value == predicted
    }


def _timing_delta(a: EvaluationReport, b: EvaluationReport) -> TimingDelta:
    same_boundary = a.metadata.configuration.timing.mode == b.metadata.configuration.timing.mode
    same_environment = a.metadata.environment == b.metadata.environment
    if not same_boundary or not same_environment:
        reasons = []
        if not same_boundary:
            reasons.append("timing boundaries differ")
        if not same_environment:
            reasons.append("runtime environments differ")
        return TimingDelta(comparable=False, reason="; ".join(reasons))
    return TimingDelta(
        comparable=True,
        mean_ms=b.timing.mean_ms - a.timing.mean_ms,
        p95_ms=b.timing.p95_ms - a.timing.p95_ms,
        mean_corpus_pass_ms=b.timing.mean_corpus_pass_ms - a.timing.mean_corpus_pass_ms,
    )


def _paired_delta(a: EvaluationReport, b: EvaluationReport) -> PairedExperimentDelta:
    samples_a = _sample_map(a)
    samples_b = _sample_map(b)
    prediction_changes = []
    for sample_id in sorted(samples_a):
        sample_a = samples_a[sample_id]
        sample_b = samples_b[sample_id]
        if sample_a.predicted == sample_b.predicted:
            continue
        prediction_changes.append(
            SamplePredictionChange(
                sample_id=sample_id,
                expected=sample_a.expected,
                prediction_a=sample_a.predicted,
                prediction_b=sample_b.predicted,
                triggered_rule_ids_a=sample_a.triggered_rule_ids,
                triggered_rule_ids_b=sample_b.triggered_rule_ids,
                risk_score_a=sample_a.risk_score,
                risk_score_b=sample_b.risk_score,
                failure_type_a=sample_a.failure_type,
                failure_type_b=sample_b.failure_type,
            )
        )
    fp_a = _failure_ids(a, "benign", "suspicious")
    fp_b = _failure_ids(b, "benign", "suspicious")
    fn_a = _failure_ids(a, "suspicious", "benign")
    fn_b = _failure_ids(b, "suspicious", "benign")
    return PairedExperimentDelta(
        confusion_matrix=ConfusionMatrixDelta(
            tp=b.confusion_matrix.tp - a.confusion_matrix.tp,
            tn=b.confusion_matrix.tn - a.confusion_matrix.tn,
            fp=b.confusion_matrix.fp - a.confusion_matrix.fp,
            fn=b.confusion_matrix.fn - a.confusion_matrix.fn,
        ),
        metrics=ClassificationMetricDelta(
            accuracy=b.metrics.accuracy - a.metrics.accuracy,
            precision=b.metrics.precision - a.metrics.precision,
            recall=b.metrics.recall - a.metrics.recall,
            f1=b.metrics.f1 - a.metrics.f1,
            false_positive_rate=b.metrics.false_positive_rate - a.metrics.false_positive_rate,
            false_negative_rate=b.metrics.false_negative_rate - a.metrics.false_negative_rate,
            specificity=b.metrics.specificity - a.metrics.specificity,
        ),
        timing=_timing_delta(a, b),
        prediction_changes=prediction_changes,
        newly_introduced_false_positives=sorted(fp_b - fp_a),
        resolved_false_positives=sorted(fp_a - fp_b),
        newly_introduced_false_negatives=sorted(fn_b - fn_a),
        resolved_false_negatives=sorted(fn_a - fn_b),
    )


def _ground_truth_signature(report: EvaluationReport) -> dict[str, tuple[str, tuple[str, ...]]]:
    return {
        sample.sample_id: (sample.expected.value, tuple(sorted(sample.expected_categories)))
        for sample in report.samples
    }


def compare_experiments(a: EvaluationReport, b: EvaluationReport) -> ExperimentComparisonReport:
    _validate_report_consistency(a)
    _validate_report_consistency(b)
    incompatibilities: list[str] = []
    warnings: list[str] = []
    if a.metadata.corpus_sha256 != b.metadata.corpus_sha256:
        incompatibilities.append("Corpus SHA-256 identities differ.")
    if a.metadata.corpus_split != b.metadata.corpus_split:
        incompatibilities.append("Corpus splits differ.")
    ids_a = {sample.sample_id for sample in a.samples}
    ids_b = {sample.sample_id for sample in b.samples}
    if ids_a != ids_b:
        incompatibilities.append("Sample populations differ.")
    elif _ground_truth_signature(a) != _ground_truth_signature(b):
        incompatibilities.append("Paired sample ground truth differs.")
    if a.metadata.suspicious_threshold != b.metadata.suspicious_threshold:
        incompatibilities.append("Classification thresholds differ.")

    differences = _configuration_differences(a, b)
    non_ablation_differences = [item.field for item in differences if item.field not in ABLATION_AND_TIMING_FIELDS]
    if non_ablation_differences:
        warnings.append("Non-ablation evaluation configuration differs: " + ", ".join(non_ablation_differences) + ".")
    if a.metadata.application_version != b.metadata.application_version:
        warnings.append("Application versions differ.")
    if a.metadata.git.commit != b.metadata.git.commit:
        warnings.append("Git commits differ.")
    if a.metadata.git.dirty or b.metadata.git.dirty:
        warnings.append("At least one experiment was produced from a dirty Git working tree.")

    if incompatibilities:
        compatibility = ExperimentCompatibility.incompatible
        paired_delta = None
    elif warnings:
        compatibility = ExperimentCompatibility.comparable_with_warning
        paired_delta = _paired_delta(a, b)
    else:
        compatibility = ExperimentCompatibility.compatible_by_design
        paired_delta = _paired_delta(a, b)

    enabled_a = set(a.metadata.configuration.enabled_builtin_rule_ids)
    enabled_b = set(b.metadata.configuration.enabled_builtin_rule_ids)
    reasons = incompatibilities or [
        "Same corpus identity, split, sample population, ground truth, and classification threshold."
    ]
    return ExperimentComparisonReport(
        experiment_a=a.metadata.experiment_id,
        experiment_b=b.metadata.experiment_id,
        compatibility=compatibility,
        compatibility_reasons=reasons,
        warnings=warnings,
        configuration_differences=differences,
        enabled_rule_ids_added=sorted(enabled_b - enabled_a),
        enabled_rule_ids_removed=sorted(enabled_a - enabled_b),
        paired_delta=paired_delta,
    )


def compare_experiment_files(path_a: Path, path_b: Path) -> ExperimentComparisonReport:
    return compare_experiments(load_evaluation_artifact(path_a), load_evaluation_artifact(path_b))


def comparison_json(report: ExperimentComparisonReport) -> str:
    return json.dumps(report.model_dump(mode="json"), indent=2, ensure_ascii=False)
