from pathlib import Path

from mcpsec.resource_policy import MAX_INPUT_BYTES as MAX_INPUT_BYTES
from mcpsec.resource_policy import MAX_NESTING_DEPTH as MAX_NESTING_DEPTH
from mcpsec.resource_policy import MAX_TEXT_LENGTH as MAX_TEXT_LENGTH

APP_NAME = "MCP Tool Security Inspector"
EVIDENCE_LENGTH = 240
DEFAULT_RULES_PATH = Path(__file__).parents[2] / "rules" / "default_rules.yml"
BUILTIN_RULE_PACK_NAME = "builtin"
BUILTIN_RULE_PACK_VERSION = "2.0.0"
KNOWN_CATEGORIES = {
    "capability",
    "concealment",
    "instruction_override",
    "mismatch",
    "obfuscation",
    "schema",
    "sensitive_data",
}
KNOWN_FIELDS = {
    "name",
    "title",
    "description",
    "inputSchema",
    "input_schema",
    "outputSchema",
    "output_schema",
    "annotations",
    "execution",
    "icons",
    "_meta",
    "metadata",
    "source",
}
