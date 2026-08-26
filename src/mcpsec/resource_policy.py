from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from yaml.nodes import MappingNode, Node, ScalarNode, SequenceNode
from yaml.tokens import AliasToken, ScalarToken

MAX_INPUT_BYTES = 10 * 1024 * 1024
MAX_BASELINE_BYTES = MAX_INPUT_BYTES
MAX_RULE_FILE_BYTES = 1024 * 1024
MAX_SUPPRESSION_FILE_BYTES = 1024 * 1024
MAX_TEXT_LENGTH = 100_000
MAX_NESTING_DEPTH = 64
MAX_STRUCTURE_NODES = 100_000
MAX_STATIC_TOOLS = 1_000
MAX_RETRIEVAL_PAGES = 100
MAX_RULES = 200
MAX_SUPPRESSIONS = 500
MAX_RULE_PATTERNS = 32
MAX_RULE_FIELDS = 9
MAX_PATTERN_LENGTH = 256
MAX_YAML_ALIASES = 50
MAX_YAML_NODES = 10_000
MAX_YAML_DEPTH = 64
MAX_YAML_SCALAR_LENGTH = MAX_TEXT_LENGTH


class ResourcePolicyError(ValueError):
    """An input exceeded a deterministic resource boundary."""


def read_bounded_text(path: Path, *, max_bytes: int, label: str, encoding: str = "utf-8") -> str:
    size = path.stat().st_size
    if size > max_bytes:
        raise ResourcePolicyError(f"{label} exceeds the {max_bytes}-byte limit")
    with path.open("rb") as handle:
        content = handle.read(max_bytes + 1)
    if len(content) > max_bytes:
        raise ResourcePolicyError(f"{label} exceeds the {max_bytes}-byte limit")
    return content.decode(encoding)


def validate_structure(value: Any, *, label: str) -> None:
    nodes = 0

    def visit(item: Any, depth: int) -> None:
        nonlocal nodes
        if depth > MAX_NESTING_DEPTH:
            raise ResourcePolicyError(f"{label} nesting exceeds {MAX_NESTING_DEPTH} levels")
        nodes += 1
        if nodes > MAX_STRUCTURE_NODES:
            raise ResourcePolicyError(f"{label} exceeds the {MAX_STRUCTURE_NODES}-node limit")
        if isinstance(item, str):
            if len(item) > MAX_TEXT_LENGTH:
                raise ResourcePolicyError(f"{label} contains a string exceeding {MAX_TEXT_LENGTH} characters")
        elif isinstance(item, dict):
            for key, child in item.items():
                if len(str(key)) > MAX_TEXT_LENGTH:
                    raise ResourcePolicyError(f"{label} contains a key exceeding {MAX_TEXT_LENGTH} characters")
                visit(child, depth + 1)
        elif isinstance(item, list):
            for child in item:
                visit(child, depth + 1)

    visit(value, 0)


def load_bounded_yaml(path: Path, *, max_bytes: int, label: str) -> Any:
    text = read_bounded_text(path, max_bytes=max_bytes, label=label)
    aliases = 0
    for token in yaml.scan(text, Loader=yaml.SafeLoader):
        if isinstance(token, AliasToken):
            aliases += 1
            if aliases > MAX_YAML_ALIASES:
                raise ResourcePolicyError(f"{label} exceeds the {MAX_YAML_ALIASES}-alias limit")
        if isinstance(token, ScalarToken) and len(token.value) > MAX_YAML_SCALAR_LENGTH:
            raise ResourcePolicyError(f"{label} contains a scalar exceeding {MAX_YAML_SCALAR_LENGTH} characters")

    root = yaml.compose(text, Loader=yaml.SafeLoader)
    nodes = 0

    def visit(node: Node | None, depth: int, ancestors: frozenset[int]) -> None:
        nonlocal nodes
        if node is None:
            return
        if depth > MAX_YAML_DEPTH:
            raise ResourcePolicyError(f"{label} nesting exceeds {MAX_YAML_DEPTH} levels")
        identifier = id(node)
        if identifier in ancestors:
            raise ResourcePolicyError(f"{label} contains a recursive YAML alias")
        nodes += 1
        if nodes > MAX_YAML_NODES:
            raise ResourcePolicyError(f"{label} exceeds the {MAX_YAML_NODES}-node expansion limit")
        active = ancestors | {identifier}
        if isinstance(node, MappingNode):
            for key, value in node.value:
                visit(key, depth + 1, active)
                visit(value, depth + 1, active)
        elif isinstance(node, SequenceNode):
            for value in node.value:
                visit(value, depth + 1, active)
        elif not isinstance(node, ScalarNode):  # pragma: no cover - PyYAML currently exposes these three node types
            raise ResourcePolicyError(f"{label} contains an unsupported YAML node")

    visit(root, 0, frozenset())
    return yaml.load(text, Loader=yaml.SafeLoader)
