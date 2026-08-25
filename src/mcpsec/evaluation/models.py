from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator

from mcpsec.constants import KNOWN_CATEGORIES
from mcpsec.models import Finding


class CorpusLabel(StrEnum):
    benign = "benign"
    suspicious = "suspicious"


class SourceType(StrEnum):
    tool_definition = "tool_definition"
    tool_catalog = "tool_catalog"


class Difficulty(StrEnum):
    easy = "easy"
    borderline = "borderline"


class CorpusEntry(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(pattern=r"^[a-z0-9][a-z0-9_-]{2,63}$")
    file: str = Field(min_length=1, max_length=512)
    tool_name: str | None = Field(default=None, min_length=1, max_length=256)
    source_type: SourceType
    expected: CorpusLabel
    categories: list[str] = Field(default_factory=list)
    rationale: str = Field(min_length=10, max_length=1_000)
    difficulty: Difficulty = Difficulty.easy
    language: str = Field(default="en", min_length=2, max_length=16)
    expected_rule_ids: list[str] = Field(default_factory=list)
    notes: str = Field(default="", max_length=1_000)

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


class SampleEvaluation(BaseModel):
    sample_id: str
    expected: CorpusLabel
    predicted: CorpusLabel
    expected_categories: list[str]
    predicted_categories: list[str]
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
    application: str
    application_version: str
    rule_pack_name: str
    rule_pack_version: str
    corpus_name: str
    corpus_version: str
    python_version: str
    timestamp_utc: str
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
