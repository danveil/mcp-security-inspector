from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import TypeAdapter, ValidationError

from mcpsec.detectors.base import Detector, all_text_fields, finding
from mcpsec.exceptions import RuleValidationError
from mcpsec.models import Finding, RuleDefinition, RulePack, RulePackMetadata, ToolDefinition

MAX_RULES = 200
MAX_PATTERN_LENGTH = 256


def load_rule_pack(path: Path) -> RulePack:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise RuleValidationError(f"Cannot load rules: {exc}") from exc
    if not isinstance(raw, dict) or set(raw) not in ({"rules"}, {"rule_pack", "rules"}):
        raise RuleValidationError("Rules file must contain 'rules' and optional 'rule_pack' metadata")
    if not isinstance(raw["rules"], list):
        raise RuleValidationError("Rules file 'rules' value must be a list")
    if len(raw["rules"]) > MAX_RULES:
        raise RuleValidationError(f"Rules file exceeds {MAX_RULES} rules")
    try:
        rules = TypeAdapter(list[RuleDefinition]).validate_python(raw["rules"])
    except ValidationError as exc:
        raise RuleValidationError(str(exc)) from exc
    if len({rule.id for rule in rules}) != len(rules):
        raise RuleValidationError("Rule IDs must be unique")
    if any(not rule.patterns or any(not p or len(p) > MAX_PATTERN_LENGTH for p in rule.patterns) for rule in rules):
        raise RuleValidationError(f"Patterns must be 1-{MAX_PATTERN_LENGTH} characters")
    allowed = {
        "name",
        "title",
        "description",
        "input_schema",
        "output_schema",
        "annotations",
        "execution",
        "metadata",
        "unknown_fields",
    }
    if any(not set(rule.fields) <= allowed for rule in rules):
        raise RuleValidationError("Rule fields contain an unsupported field name")
    metadata = raw.get("rule_pack", {"name": "legacy-custom", "version": "0.0.0"})
    try:
        validated_metadata = RulePackMetadata.model_validate(metadata)
    except ValidationError as exc:
        raise RuleValidationError(str(exc)) from exc
    return RulePack(rule_pack=validated_metadata, rules=rules)


def load_rules(path: Path) -> list[RuleDefinition]:
    """Load custom rules while preserving the v0.1 list-returning API."""
    return load_rule_pack(path).rules


class CustomRuleDetector(Detector):
    def __init__(self, rules: list[RuleDefinition]) -> None:
        self.rules = rules

    def detect(self, tool: ToolDefinition, redact: bool = False) -> list[Finding]:
        available: dict[str, list[tuple[str, str]]] = {
            field: [] for field in {r for rule in self.rules for r in rule.fields}
        }
        for path, text in all_text_fields(tool):
            root = path.split(".", 1)[0]
            if root in available:
                available[root].append((path, text))
        results: list[Finding] = []
        for rule in self.rules:
            if not rule.enabled:
                continue
            for field in rule.fields:
                for path, text in available.get(field, []):
                    pattern = next((p for p in rule.patterns if p.casefold() in text.casefold()), None)
                    if pattern:
                        results.append(
                            finding(
                                rule_id=rule.id,
                                name=rule.name,
                                category=rule.category,
                                severity=rule.severity,
                                confidence=rule.confidence,
                                explanation=rule.rationale
                                or "Configured literal indicator detected; context requires review.",
                                evidence=pattern,
                                field=path,
                                recommendation=rule.recommendation,
                                score=rule.score,
                                redact=redact,
                            )
                        )
                        break
                else:
                    continue
                break
        return results
