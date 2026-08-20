from pathlib import Path

APP_NAME = "MCP Tool Security Inspector"
MAX_INPUT_BYTES = 10 * 1024 * 1024
MAX_TEXT_LENGTH = 100_000
EVIDENCE_LENGTH = 240
DEFAULT_RULES_PATH = Path(__file__).parents[2] / "rules" / "default_rules.yml"
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
