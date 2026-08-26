from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from mcpsec.constants import KNOWN_CATEGORIES
from mcpsec.models import Finding, Severity

SHA256_PATTERN = r"^[0-9a-f]{64}$"
FIELD_LOCATION_PATTERN = r"^[A-Za-z_$][A-Za-z0-9_$-]*(?:\.[A-Za-z_$][A-Za-z0-9_$-]*|\[[0-9]+\])*$"


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
    tp: int = Field(ge=0)
    tn: int = Field(ge=0)
    fp: int = Field(ge=0)
    fn: int = Field(ge=0)


class ClassificationMetrics(BaseModel):
    accuracy: float = Field(ge=0, le=1)
    precision: float = Field(ge=0, le=1)
    recall: float = Field(ge=0, le=1)
    f1: float = Field(ge=0, le=1)
    false_positive_rate: float = Field(ge=0, le=1)
    false_negative_rate: float = Field(ge=0, le=1)
    specificity: float = Field(ge=0, le=1)


class CategoryEvaluation(BaseModel):
    category: str
    confusion_matrix: ConfusionMatrix
    metrics: ClassificationMetrics


class SuppressionIdentity(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    rule_id: str
    tool: str | None = None


class EvaluationConfiguration(BaseModel):
    model_config = ConfigDict(extra="forbid")
    suspicious_threshold: Severity
    corpus_split: CorpusSplit
    builtin_detector_ids: list[str]
    builtin_rule_ids: list[str]
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
        for name in ("builtin_detector_ids", "builtin_rule_ids", "custom_rule_ids"):
            values = getattr(self, name)
            if len(set(values)) != len(values):
                raise ValueError(f"{name} must be unique")
            setattr(self, name, sorted(values))
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
    elapsed_ms: float = Field(ge=0)


class TimingStatistics(BaseModel):
    total_ms: float = Field(ge=0)
    mean_ms: float = Field(ge=0)
    median_ms: float = Field(ge=0)
    minimum_ms: float = Field(ge=0)
    maximum_ms: float = Field(ge=0)
    p95_ms: float = Field(ge=0)


class EvaluationMetadata(BaseModel):
    output_schema_version: str = "2.0.0"
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
    suppressions_applied: bool
    suspicious_threshold: str


class EvaluationReport(BaseModel):
    metadata: EvaluationMetadata
    confusion_matrix: ConfusionMatrix
    metrics: ClassificationMetrics
    category_metrics: list[CategoryEvaluation]
    false_positives: list[SampleEvaluation]
    false_negatives: list[SampleEvaluation]
    samples: list[SampleEvaluation]
    timing: TimingStatistics


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
