from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from mcpsec.resource_policy import MAX_RULE_FIELDS, MAX_RULE_PATTERNS

JsonObject = dict[str, Any]


class Severity(StrEnum):
    INFORMATIONAL = "INFORMATIONAL"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


SEVERITY_RANK = {
    Severity.INFORMATIONAL: 0,
    Severity.LOW: 1,
    Severity.MEDIUM: 2,
    Severity.HIGH: 3,
    Severity.CRITICAL: 4,
}


class ToolDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    title: str | None = None
    description: str = ""
    input_schema: JsonObject = Field(default_factory=dict)
    output_schema: JsonObject | None = None
    annotations: JsonObject = Field(default_factory=dict)
    execution: JsonObject = Field(default_factory=dict)
    icons: list[JsonObject] = Field(default_factory=list)
    metadata: JsonObject = Field(default_factory=dict)
    unknown_fields: JsonObject = Field(default_factory=dict)
    source: Any = None
    provenance: str = "unknown"


class Finding(BaseModel):
    rule_id: str
    rule_name: str
    category: str
    severity: Severity
    confidence: float = Field(ge=0, le=1)
    explanation: str
    evidence: str
    field: str
    recommendation: str
    score_contribution: float = Field(ge=0)


class ToolScanResult(BaseModel):
    tool: ToolDefinition
    findings: list[Finding]
    risk_score: int = Field(ge=0, le=100)
    severity: Severity
    findings_detected: int | None = Field(default=None, ge=0)
    findings_truncated: bool = False

    @model_validator(mode="after")
    def validate_finding_counts(self) -> ToolScanResult:
        if self.findings_detected is None:
            self.findings_detected = len(self.findings)
        if self.findings_detected < len(self.findings):
            raise ValueError("findings_detected cannot be smaller than retained findings")
        if self.findings_truncated != (self.findings_detected > len(self.findings)):
            raise ValueError("findings_truncated does not match detected and retained finding counts")
        return self


class FindingBudgetStatus(BaseModel):
    per_tool_limit: int = Field(ge=1)
    report_limit: int = Field(ge=1)
    evidence_char_limit_per_tool: int = Field(ge=1)
    findings_detected: int = Field(ge=0)
    findings_retained: int = Field(ge=0)
    truncated: bool


class ScanReport(BaseModel):
    application: str
    version: str
    source: str
    tools: list[ToolScanResult]
    finding_budget: FindingBudgetStatus | None = None


class Fingerprints(BaseModel):
    full_sha256: str
    description_sha256: str
    input_schema_sha256: str
    output_schema_sha256: str | None = None
    annotations_sha256: str
    execution_sha256: str
    metadata_sha256: str


class BaselineTool(BaseModel):
    name: str
    fingerprints: Fingerprints
    summary: JsonObject


class BaselineFile(BaseModel):
    format_version: str = "1.0"
    application_version: str
    created_at: str
    source: str
    tools: list[BaselineTool]

    @model_validator(mode="after")
    def validate_unique_tool_names(self) -> BaselineFile:
        names = [tool.name for tool in self.tools]
        if len(set(names)) != len(names):
            raise ValueError("Baseline tool names must be unique")
        return self


class Drift(BaseModel):
    kind: str
    tool_name: str
    previous_name: str | None = None
    fields: list[str] = Field(default_factory=list)
    differences: JsonObject = Field(default_factory=dict)


class RuleDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(pattern=r"^[A-Z][A-Z0-9_-]{2,31}$")
    name: str = Field(min_length=1, max_length=256)
    category: str = Field(min_length=1, max_length=64)
    fields: list[str] = Field(min_length=1, max_length=MAX_RULE_FIELDS)
    patterns: list[str] = Field(min_length=1, max_length=MAX_RULE_PATTERNS)
    severity: Severity
    confidence: float = Field(ge=0, le=1)
    score: float = Field(ge=0, le=40)
    recommendation: str = Field(min_length=1, max_length=2_000)
    enabled: bool = True
    rationale: str = Field(default="", max_length=2_000)
    benign_usage: str = Field(default="", max_length=2_000)


class RulePackMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(min_length=1, max_length=64, pattern=r"^[a-zA-Z0-9][a-zA-Z0-9_.-]*$")
    version: str = Field(pattern=r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


class RulePack(BaseModel):
    model_config = ConfigDict(extra="forbid")
    rule_pack: RulePackMetadata
    rules: list[RuleDefinition]


class SuppressionDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")
    rule_id: str = Field(pattern=r"^[A-Z][A-Z0-9_-]{2,31}$")
    tool: str | None = Field(default=None, min_length=1, max_length=256)
    justification: str = Field(min_length=10, max_length=1_000)
