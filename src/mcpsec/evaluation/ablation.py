from __future__ import annotations

from dataclasses import dataclass

from mcpsec.detectors.base import Detector
from mcpsec.detectors.injection import InjectionDetector
from mcpsec.detectors.mismatch import MismatchDetector
from mcpsec.detectors.obfuscation import ObfuscationDetector
from mcpsec.detectors.permissions import PermissionsDetector
from mcpsec.detectors.schema import SchemaDetector
from mcpsec.detectors.secrecy import SecrecyDetector
from mcpsec.detectors.sensitive_data import SensitiveDataDetector
from mcpsec.evaluation.models import AblationPreset
from mcpsec.exceptions import InputError
from mcpsec.models import Finding, ToolDefinition


@dataclass(frozen=True)
class DetectorFamily:
    family_id: str
    detector: Detector
    rule_ids: tuple[str, ...]

    @property
    def detector_id(self) -> str:
        return f"{self.detector.__class__.__module__}.{self.detector.__class__.__qualname__}"


DETECTOR_FAMILIES = (
    DetectorFamily("injection", InjectionDetector(), ("PI-001",)),
    DetectorFamily("concealment", SecrecyDetector(), ("HID-001",)),
    DetectorFamily("sensitive-data", SensitiveDataDetector(), ("SEC-001",)),
    DetectorFamily("schema", SchemaDetector(), ("SCH-001", "SCH-002")),
    DetectorFamily("mismatch", MismatchDetector(), ("MIS-001",)),
    DetectorFamily("obfuscation", ObfuscationDetector(), ("OBF-001", "OBF-002", "OBF-003", "OBF-004")),
    DetectorFamily("capability", PermissionsDetector(), ("CAP-001",)),
)

PRESET_DISABLED_FAMILIES: dict[AblationPreset, frozenset[str]] = {
    AblationPreset.full: frozenset(),
    AblationPreset.without_injection: frozenset({"injection"}),
    AblationPreset.without_concealment: frozenset({"concealment"}),
    AblationPreset.without_sensitive_data: frozenset({"sensitive-data"}),
    AblationPreset.without_schema: frozenset({"schema"}),
    AblationPreset.without_mismatch: frozenset({"mismatch"}),
    AblationPreset.without_obfuscation: frozenset({"obfuscation"}),
    AblationPreset.without_capability: frozenset({"capability"}),
}


class RuleFilteredDetector(Detector):
    def __init__(self, detector: Detector, enabled_rule_ids: frozenset[str]) -> None:
        self.detector = detector
        self.enabled_rule_ids = enabled_rule_ids

    def detect(self, tool: ToolDefinition, redact: bool = False) -> list[Finding]:
        return [finding for finding in self.detector.detect(tool, redact) if finding.rule_id in self.enabled_rule_ids]


@dataclass(frozen=True)
class ResolvedAblation:
    preset: AblationPreset
    detectors: tuple[Detector, ...]
    enabled_detector_ids: tuple[str, ...]
    disabled_detector_ids: tuple[str, ...]
    enabled_family_ids: tuple[str, ...]
    disabled_family_ids: tuple[str, ...]
    enabled_rule_ids: tuple[str, ...]
    disabled_rule_ids: tuple[str, ...]


def resolve_ablation(
    *,
    preset: AblationPreset = AblationPreset.full,
    disabled_rule_ids: list[str] | tuple[str, ...] | None = None,
    disabled_family_ids: list[str] | tuple[str, ...] | None = None,
) -> ResolvedAblation:
    known_rules = {rule_id for family in DETECTOR_FAMILIES for rule_id in family.rule_ids}
    known_families = {family.family_id for family in DETECTOR_FAMILIES}
    requested_rules = {rule_id.upper() for rule_id in disabled_rule_ids or ()}
    requested_families = {family_id.casefold() for family_id in disabled_family_ids or ()}
    unknown_rules = sorted(requested_rules - known_rules)
    if unknown_rules:
        raise InputError(f"Unknown built-in ablation rule ID(s): {', '.join(unknown_rules)}")
    unknown_families = sorted(requested_families - known_families)
    if unknown_families:
        raise InputError(f"Unknown detector family ID(s): {', '.join(unknown_families)}")

    disabled_families = set(PRESET_DISABLED_FAMILIES[preset]) | requested_families
    disabled_rules = set(requested_rules)
    for family in DETECTOR_FAMILIES:
        if family.family_id in disabled_families:
            disabled_rules.update(family.rule_ids)

    detectors: list[Detector] = []
    enabled_detector_ids: list[str] = []
    disabled_detector_ids: list[str] = []
    enabled_families: list[str] = []
    effective_disabled_families: list[str] = []
    for family in DETECTOR_FAMILIES:
        enabled_for_family = frozenset(set(family.rule_ids) - disabled_rules)
        if not enabled_for_family:
            disabled_detector_ids.append(family.detector_id)
            effective_disabled_families.append(family.family_id)
            continue
        detector = (
            family.detector
            if len(enabled_for_family) == len(family.rule_ids)
            else RuleFilteredDetector(family.detector, enabled_for_family)
        )
        detectors.append(detector)
        enabled_detector_ids.append(family.detector_id)
        enabled_families.append(family.family_id)

    return ResolvedAblation(
        preset=preset,
        detectors=tuple(detectors),
        enabled_detector_ids=tuple(enabled_detector_ids),
        disabled_detector_ids=tuple(disabled_detector_ids),
        enabled_family_ids=tuple(enabled_families),
        disabled_family_ids=tuple(effective_disabled_families),
        enabled_rule_ids=tuple(sorted(known_rules - disabled_rules)),
        disabled_rule_ids=tuple(sorted(disabled_rules)),
    )
