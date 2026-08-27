from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import TypeAdapter, ValidationError

from mcpsec.exceptions import RuleValidationError
from mcpsec.models import SuppressionDefinition
from mcpsec.resource_policy import (
    MAX_SUPPRESSION_FILE_BYTES,
    MAX_SUPPRESSIONS,
    ResourcePolicyError,
    StrictJsonError,
    load_bounded_json,
    load_bounded_yaml,
)


def load_suppressions(path: Path, known_rule_ids: set[str]) -> list[SuppressionDefinition]:
    try:
        raw = (
            load_bounded_json(path, max_bytes=MAX_SUPPRESSION_FILE_BYTES, label="Suppressions file")
            if path.suffix.casefold() == ".json"
            else load_bounded_yaml(path, max_bytes=MAX_SUPPRESSION_FILE_BYTES, label="Suppressions file")
        )
    except (OSError, UnicodeError, yaml.YAMLError, StrictJsonError, ResourcePolicyError) as exc:
        raise RuleValidationError(f"Cannot load suppressions: {exc}") from exc
    if not isinstance(raw, dict) or set(raw) != {"suppressions"} or not isinstance(raw["suppressions"], list):
        raise RuleValidationError("Suppressions file must contain only a top-level 'suppressions' list")
    if len(raw["suppressions"]) > MAX_SUPPRESSIONS:
        raise RuleValidationError(f"Suppressions file exceeds {MAX_SUPPRESSIONS} entries")
    try:
        suppressions = TypeAdapter(list[SuppressionDefinition]).validate_python(raw["suppressions"])
    except ValidationError as exc:
        raise RuleValidationError(str(exc)) from exc
    unknown = sorted({item.rule_id for item in suppressions} - known_rule_ids)
    if unknown:
        raise RuleValidationError(f"Unknown suppression rule ID(s): {', '.join(unknown)}")
    scopes = [(item.rule_id, item.tool) for item in suppressions]
    if len(set(scopes)) != len(scopes):
        raise RuleValidationError("Suppression rule/tool scopes must be unique")
    return suppressions
