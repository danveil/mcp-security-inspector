from mcpsec.detectors.injection import InjectionDetector
from mcpsec.detectors.mismatch import MismatchDetector
from mcpsec.detectors.obfuscation import ObfuscationDetector
from mcpsec.detectors.permissions import PermissionsDetector
from mcpsec.detectors.schema import SchemaDetector
from mcpsec.detectors.secrecy import SecrecyDetector
from mcpsec.detectors.sensitive_data import SensitiveDataDetector

BUILTIN_DETECTORS = [
    InjectionDetector(),
    SecrecyDetector(),
    SensitiveDataDetector(),
    SchemaDetector(),
    MismatchDetector(),
    ObfuscationDetector(),
    PermissionsDetector(),
]

__all__ = ["BUILTIN_DETECTORS"]
