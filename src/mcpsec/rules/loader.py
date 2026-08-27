from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import TypeAdapter, ValidationError

from mcpsec.detectors.base import Detector, all_text_fields, finding
from mcpsec.exceptions import RuleValidationError
from mcpsec.models import Finding, RuleDefinition, RulePack, RulePackMetadata, ToolDefinition
from mcpsec.resource_policy import (
    MAX_PATTERN_LENGTH,
    MAX_RULE_FILE_BYTES,
    MAX_RULES,
    ResourcePolicyError,
    StrictJsonError,
    load_bounded_json,
    load_bounded_yaml,
)
from mcpsec.rules.builtin import RULE_EXPLANATIONS


def load_rule_pack(path: Path) -> RulePack:
    try:
        raw = (
            load_bounded_json(path, max_bytes=MAX_RULE_FILE_BYTES, label="Rules file")
            if path.suffix.casefold() == ".json"
            else load_bounded_yaml(path, max_bytes=MAX_RULE_FILE_BYTES, label="Rules file")
        )
    except (OSError, UnicodeError, yaml.YAMLError, StrictJsonError, ResourcePolicyError) as exc:
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
    validate_custom_rule_ids(rules)
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
        "icons",
        "metadata",
        "source",
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


def validate_custom_rule_ids(rules: list[RuleDefinition]) -> None:
    ids = [rule.id for rule in rules]
    if len(set(ids)) != len(ids):
        raise RuleValidationError("Custom rule IDs must be unique")
    collisions = sorted(set(ids) & set(RULE_EXPLANATIONS))
    if collisions:
        raise RuleValidationError(f"Custom rule ID(s) conflict with built-in rule IDs: {', '.join(collisions)}")


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
            root = path.split(".", 1)[0].split("[", 1)[0]
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
