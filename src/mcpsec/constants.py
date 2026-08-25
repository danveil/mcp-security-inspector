from pathlib import Path

APP_NAME = "MCP Tool Security Inspector"
MAX_INPUT_BYTES = 10 * 1024 * 1024
MAX_TEXT_LENGTH = 100_000
MAX_NESTING_DEPTH = 64
EVIDENCE_LENGTH = 240
DEFAULT_RULES_PATH = Path(__file__).parents[2] / "rules" / "default_rules.yml"
BUILTIN_RULE_PACK_NAME = "builtin"
BUILTIN_RULE_PACK_VERSION = "1.0.0"
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
