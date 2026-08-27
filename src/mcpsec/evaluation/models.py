from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from mcpsec.constants import KNOWN_CATEGORIES
from mcpsec.models import Finding, Severity

SHA256_PATTERN = r"^[0-9a-f]{64}$"
FIELD_LOCATION_PATTERN = r"^[A-Za-z_$][A-Za-z0-9_$-]*(?:\.[A-Za-z_$][A-Za-z0-9_$-]*|\[[0-9]+\])*$"
OUTPUT_SCHEMA_VERSION = "3.1.0"
SUPPORTED_OUTPUT_SCHEMA_VERSIONS = frozenset({"3.0.0", OUTPUT_SCHEMA_VERSION})
MIN_STRATUM_SAMPLE_COUNT = 10


class CorpusLabel(StrEnum):
    benign = "benign"
    suspicious = "suspicious"


class CorpusSplit(StrEnum):
    development = "development"
    holdout = "holdout"


class SourceType(StrEnum):
    tool_definition = "tool_definition"
    tool_catalog = "tool_catalog"


class Difficulty(StrEnum):
    obvious = "obvious"
    moderate = "moderate"
    subtle = "subtle"


class ProvenanceOrigin(StrEnum):
    synthetic = "synthetic"
    derived = "derived"
    real_world = "real_world"


class LabelReviewStatus(StrEnum):
    unreviewed = "unreviewed"
    single_reviewer = "single_reviewer"
    independently_reviewed = "independently_reviewed"


class FailureType(StrEnum):
    false_positive = "false_positive"
    false_negative_no_finding = "false_negative_no_finding"
    false_negative_below_threshold = "false_negative_below_threshold"
    category_mismatch = "category_mismatch"


class IntegritySeverity(StrEnum):
    error = "ERROR"
    warning = "WARNING"


class IntegrityIssueKind(StrEnum):
    duplicate_sample_id = "duplicate_sample_id"
    exact_normalized_content = "exact_normalized_content"


class TimingMode(StrEnum):
    analysis_core = "analysis-core"
    static_end_to_end = "static-end-to-end"


class AblationPreset(StrEnum):
    full = "full"
    without_injection = "without-injection"
    without_concealment = "without-concealment"
    without_sensitive_data = "without-sensitive-data"
    without_schema = "without-schema"
    without_mismatch = "without-mismatch"
    without_obfuscation = "without-obfuscation"
    without_capability = "without-capability"


class StratificationDimension(StrEnum):
    expected_category = "expected_category"
    field_location = "field_location"
    difficulty = "difficulty"
    ground_truth = "ground_truth"


class ExperimentCompatibility(StrEnum):
    compatible_by_design = "compatible_by_design"
    comparable_with_warning = "comparable_with_warning"
    incompatible = "incompatible"


class SampleProvenance(BaseModel):
    model_config = ConfigDict(extra="forbid")
    origin_type: ProvenanceOrigin = ProvenanceOrigin.synthetic
    source_reference: str | None = Field(default=None, min_length=1, max_length=1_000)
    derivation_notes: str | None = Field(default=None, min_length=1, max_length=2_000)


class CorpusEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(pattern=r"^[a-z0-9][a-z0-9_-]{2,63}$")
    file: str = Field(min_length=1, max_length=512)
    tool_name: str | None = Field(default=None, min_length=1, max_length=256)
    source_type: SourceType
    expected: CorpusLabel
    categories: list[str] = Field(default_factory=list)
    rationale: str = Field(min_length=10, max_length=1_000)
    difficulty: Difficulty = Difficulty.obvious
    language: str = Field(default="en", min_length=2, max_length=16)
    expected_rule_ids: list[str] = Field(default_factory=list)
    field_locations: list[str] = Field(default_factory=list)
    provenance: SampleProvenance = Field(default_factory=SampleProvenance)
    notes: str = Field(default="", max_length=1_000)

    @field_validator("difficulty", mode="before")
    @classmethod
    def migrate_legacy_difficulty(cls, value: Any) -> Any:
        if value == "easy":
            return Difficulty.obvious
        if value == "borderline":
            return Difficulty.moderate
        return value

    @field_validator("field_locations")
    @classmethod
    def validate_field_locations(cls, values: list[str]) -> list[str]:
        import re

        if len(set(values)) != len(values):
            raise ValueError("field_locations must be unique")
        invalid = [value for value in values if len(value) > 512 or not re.fullmatch(FIELD_LOCATION_PATTERN, value)]
        if invalid:
            raise ValueError("field_locations must use bounded dotted paths with optional numeric indexes")
        return values

    @model_validator(mode="after")
    def validate_ground_truth(self) -> CorpusEntry:
        if len(set(self.categories)) != len(self.categories):
            raise ValueError("categories must be unique")
        unknown = set(self.categories) - KNOWN_CATEGORIES
        if unknown:
            raise ValueError(f"unknown categories: {', '.join(sorted(unknown))}")
        if self.expected == CorpusLabel.benign and self.categories:
            raise ValueError("benign samples cannot declare suspicious categories")
        if self.expected == CorpusLabel.suspicious and not self.categories:
            raise ValueError("suspicious samples require at least one category")
        if len(set(self.expected_rule_ids)) != len(self.expected_rule_ids):
            raise ValueError("expected_rule_ids must be unique")
        return self


class CorpusManifest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    corpus_name: str = Field(min_length=1, max_length=128)
    corpus_version: str = Field(pattern=r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
    split: CorpusSplit = CorpusSplit.development
    methodology_version: str = Field(default="1.0.0", pattern=r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")
    methodology_note: str = Field(default="Legacy manifest with no methodology note.", min_length=10, max_length=1_000)
    label_review_status: LabelReviewStatus = LabelReviewStatus.unreviewed
    source_license_policy: str | None = Field(default=None, min_length=10, max_length=1_000)
    description: str = Field(min_length=10, max_length=1_000)
    samples: list[CorpusEntry] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_ids(self) -> CorpusManifest:
        ids = [sample.id for sample in self.samples]
        if len(set(ids)) != len(ids):
            raise ValueError("sample IDs must be unique")
        return self


class ConfusionMatrix(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tp: int = Field(ge=0)
    tn: int = Field(ge=0)
    fp: int = Field(ge=0)
    fn: int = Field(ge=0)


class ClassificationMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid")
    accuracy: float = Field(ge=0, le=1)
    precision: float = Field(ge=0, le=1)
    recall: float = Field(ge=0, le=1)
    f1: float = Field(ge=0, le=1)
    false_positive_rate: float = Field(ge=0, le=1)
    false_negative_rate: float = Field(ge=0, le=1)
    specificity: float = Field(ge=0, le=1)


class CategoryEvaluation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    category: str
    confusion_matrix: ConfusionMatrix
    metrics: ClassificationMetrics


class SuppressionIdentity(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    rule_id: str
    tool: str | None = None


class TimingConfiguration(BaseModel):
    model_config = ConfigDict(extra="forbid")
    mode: TimingMode = TimingMode.analysis_core
    warmup_repetitions: int = Field(default=0, ge=0, le=100)
    measured_repetitions: int = Field(default=1, ge=1, le=1_000)
    definition: str
    includes_loading: bool
    includes_normalization: bool
    sample_ordering: str = "sample_id_ascending"

    @model_validator(mode="after")
    def validate_boundary_flags(self) -> TimingConfiguration:
        includes_static_input = self.mode == TimingMode.static_end_to_end
        if self.includes_loading != includes_static_input or self.includes_normalization != includes_static_input:
            raise ValueError("timing boundary flags do not match timing mode")
        return self


class EvaluationConfiguration(BaseModel):
    model_config = ConfigDict(extra="forbid")
    suspicious_threshold: Severity
    corpus_split: CorpusSplit
    enabled_builtin_detector_ids: list[str]
    disabled_builtin_detector_ids: list[str]
    enabled_builtin_family_ids: list[str]
    disabled_builtin_family_ids: list[str]
    enabled_builtin_rule_ids: list[str]
    disabled_builtin_rule_ids: list[str]
    ablation_preset: AblationPreset = AblationPreset.full
    timing: TimingConfiguration
    custom_rule_pack_name: str | None = None
    custom_rule_pack_version: str | None = None
    custom_rule_ids: list[str] = Field(default_factory=list)
    custom_rule_configuration_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    custom_rule_file_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    suppressions: list[SuppressionIdentity] = Field(default_factory=list)
    suppression_file_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    options: dict[str, bool | int | float | str] = Field(default_factory=dict)

    @model_validator(mode="after")
    def normalize_unordered_configuration(self) -> EvaluationConfiguration:
        for name in (
            "enabled_builtin_detector_ids",
            "disabled_builtin_detector_ids",
            "enabled_builtin_family_ids",
            "disabled_builtin_family_ids",
            "enabled_builtin_rule_ids",
            "disabled_builtin_rule_ids",
            "custom_rule_ids",
        ):
            values = getattr(self, name)
            if len(set(values)) != len(values):
                raise ValueError(f"{name} must be unique")
            setattr(self, name, sorted(values))
        if set(self.enabled_builtin_rule_ids) & set(self.disabled_builtin_rule_ids):
            raise ValueError("built-in rules cannot be both enabled and disabled")
        if set(self.enabled_builtin_family_ids) & set(self.disabled_builtin_family_ids):
            raise ValueError("built-in families cannot be both enabled and disabled")
        suppression_keys = [(item.rule_id, item.tool or "") for item in self.suppressions]
        if len(set(suppression_keys)) != len(suppression_keys):
            raise ValueError("suppression identities must be unique")
        self.suppressions = sorted(self.suppressions, key=lambda item: (item.rule_id, item.tool or ""))
        self.options = dict(sorted(self.options.items()))
        return self


class GitMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    commit: str | None = Field(default=None, pattern=r"^[0-9a-f]{40,64}$")
    dirty: bool | None = None


class RuntimeEnvironment(BaseModel):
    model_config = ConfigDict(extra="forbid")
    python_version: str
    platform_system: str
    platform_release: str
    machine: str
    processor: str | None = None
    dependency_versions: dict[str, str]


class SampleEvaluation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sample_id: str
    corpus_split: CorpusSplit
    expected: CorpusLabel
    predicted: CorpusLabel
    expected_categories: list[str]
    predicted_categories: list[str]
    rationale: str
    difficulty: Difficulty
    provenance: SampleProvenance
    expected_rule_ids: list[str]
    expected_field_locations: list[str]
    triggered_rule_ids: list[str]
    classification_threshold: Severity
    failure_type: FailureType | None = None
    researcher_notes: str = ""
    risk_score: int = Field(ge=0, le=100)
    findings: list[Finding]
    findings_detected: int | None = Field(default=None, ge=0)
    findings_truncated: bool = False
    elapsed_ms: float = Field(ge=0)
    timing_observations: int = Field(default=1, ge=1)

    @model_validator(mode="after")
    def validate_finding_counts(self) -> SampleEvaluation:
        if self.findings_detected is None:
            self.findings_detected = len(self.findings)
        if self.findings_detected < len(self.findings):
            raise ValueError("findings_detected cannot be smaller than retained findings")
        if self.findings_truncated != (self.findings_detected > len(self.findings)):
            raise ValueError("findings_truncated does not match detected and retained finding counts")
        return self


class TimingStatistics(BaseModel):
    model_config = ConfigDict(extra="forbid")
    observation_count: int = Field(ge=0)
    sample_count: int = Field(ge=0)
    measured_repetitions: int = Field(ge=1)
    total_ms: float = Field(ge=0)
    mean_ms: float = Field(ge=0)
    median_ms: float = Field(ge=0)
    minimum_ms: float = Field(ge=0)
    maximum_ms: float = Field(ge=0)
    p95_ms: float = Field(ge=0)
    standard_deviation_ms: float = Field(ge=0)
    mean_per_tool_ms: float = Field(ge=0)
    mean_corpus_pass_ms: float = Field(ge=0)


class ProportionInterval(BaseModel):
    model_config = ConfigDict(extra="forbid")
    method: str = "wilson_score_95"
    confidence_level: float = 0.95
    numerator: int = Field(ge=0)
    denominator: int = Field(ge=0)
    estimate: float | None = Field(default=None, ge=0, le=1)
    lower: float | None = Field(default=None, ge=0, le=1)
    upper: float | None = Field(default=None, ge=0, le=1)
    defined: bool


class UncertaintyReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    accuracy: ProportionInterval
    recall: ProportionInterval
    false_positive_rate: ProportionInterval


class StratifiedGroup(BaseModel):
    model_config = ConfigDict(extra="forbid")
    dimension: StratificationDimension
    value: str
    sample_count: int = Field(ge=1)
    confusion_matrix: ConfusionMatrix
    metrics: ClassificationMetrics
    uncertainty: UncertaintyReport
    low_evidence: bool
    warning: str | None = None
    undefined_metrics: list[str] = Field(default_factory=list)


class StratificationReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    dimension: StratificationDimension
    available_sample_count: int = Field(ge=0)
    missing_sample_count: int = Field(ge=0)
    groups: list[StratifiedGroup]


class EvaluationMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    output_schema_version: str = OUTPUT_SCHEMA_VERSION
    experiment_id: str = Field(pattern=r"^exp-[0-9]{8}T[0-9]{6}(?:[0-9]{6})?Z-[0-9a-f]{8}-[0-9a-f]{8}$")
    application: str
    application_version: str
    rule_pack_name: str
    rule_pack_version: str
    corpus_name: str
    corpus_version: str
    corpus_split: CorpusSplit
    corpus_methodology_version: str
    corpus_methodology_note: str
    label_review_status: LabelReviewStatus
    source_license_policy: str | None
    corpus_sha256: str = Field(pattern=SHA256_PATTERN)
    configuration: EvaluationConfiguration
    configuration_sha256: str = Field(pattern=SHA256_PATTERN)
    git: GitMetadata
    environment: RuntimeEnvironment
    python_version: str
    timestamp_utc: str
    invocation: list[str]
    timing_methodology: str
    sample_count: int = Field(ge=0)
    findings_detected: int | None = Field(default=None, ge=0)
    findings_retained: int | None = Field(default=None, ge=0)
    findings_truncated: bool = False
    finding_report_limit: int | None = Field(default=None, ge=1)
    suppressions_applied: bool
    suspicious_threshold: str


class EvaluationReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    metadata: EvaluationMetadata
    confusion_matrix: ConfusionMatrix
    metrics: ClassificationMetrics
    category_metrics: list[CategoryEvaluation]
    false_positives: list[SampleEvaluation]
    false_negatives: list[SampleEvaluation]
    samples: list[SampleEvaluation]
    timing: TimingStatistics
    uncertainty: UncertaintyReport
    stratified_metrics: list[StratificationReport]


class CorpusIdentity(BaseModel):
    model_config = ConfigDict(extra="forbid")
    corpus_name: str
    corpus_version: str
    split: CorpusSplit
    corpus_sha256: str = Field(pattern=SHA256_PATTERN)
    sample_count: int = Field(ge=0)


class IntegrityIssue(BaseModel):
    model_config = ConfigDict(extra="forbid")
    severity: IntegritySeverity
    kind: IntegrityIssueKind
    development_sample_ids: list[str]
    holdout_sample_ids: list[str]
    normalized_content_sha256: str | None = Field(default=None, pattern=SHA256_PATTERN)
    explanation: str


class CrossSplitIntegrityReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    development: CorpusIdentity
    holdout: CorpusIdentity
    errors: list[IntegrityIssue]
    warnings: list[IntegrityIssue]

    @property
    def passed(self) -> bool:
        return not self.errors


class ConfigurationDifference(BaseModel):
    model_config = ConfigDict(extra="forbid")
    field: str
    experiment_a: Any
    experiment_b: Any


class ConfusionMatrixDelta(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tp: int
    tn: int
    fp: int
    fn: int


class ClassificationMetricDelta(BaseModel):
    model_config = ConfigDict(extra="forbid")
    accuracy: float
    precision: float
    recall: float
    f1: float
    false_positive_rate: float
    false_negative_rate: float
    specificity: float


class TimingDelta(BaseModel):
    model_config = ConfigDict(extra="forbid")
    comparable: bool
    reason: str | None = None
    mean_ms: float | None = None
    p95_ms: float | None = None
    mean_corpus_pass_ms: float | None = None


class SamplePredictionChange(BaseModel):
    model_config = ConfigDict(extra="forbid")
    sample_id: str
    expected: CorpusLabel
    prediction_a: CorpusLabel
    prediction_b: CorpusLabel
    triggered_rule_ids_a: list[str]
    triggered_rule_ids_b: list[str]
    risk_score_a: int = Field(ge=0, le=100)
    risk_score_b: int = Field(ge=0, le=100)
    failure_type_a: FailureType | None = None
    failure_type_b: FailureType | None = None


class PairedExperimentDelta(BaseModel):
    model_config = ConfigDict(extra="forbid")
    confusion_matrix: ConfusionMatrixDelta
    metrics: ClassificationMetricDelta
    timing: TimingDelta
    prediction_changes: list[SamplePredictionChange]
    newly_introduced_false_positives: list[str]
    resolved_false_positives: list[str]
    newly_introduced_false_negatives: list[str]
    resolved_false_negatives: list[str]


class ExperimentComparisonReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    experiment_a: str
    experiment_b: str
    compatibility: ExperimentCompatibility
    compatibility_reasons: list[str]
    warnings: list[str]
    configuration_differences: list[ConfigurationDifference]
    enabled_rule_ids_added: list[str]
    enabled_rule_ids_removed: list[str]
    paired_delta: PairedExperimentDelta | None = None
