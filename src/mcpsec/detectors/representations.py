from __future__ import annotations

import base64
import binascii
import re
import unicodedata
from dataclasses import dataclass

MAX_CANDIDATE_INPUT = 512
MIN_DECODED_TEXT = 8
MAX_DECODED_OUTPUT = 512
MAX_CANDIDATES_PER_FIELD = 4
MAX_CANDIDATES_PER_TOOL = 32
MAX_RETAINED_DECODED_TEXT = 4096
MIN_PRINTABLE_RATIO = 0.9

HTML_NUMERIC = re.compile(r"(?:(?:&#(?:[0-9]{1,7}|[xX][0-9A-Fa-f]{1,6});)[ \t]*){8,}")
PREFIXED_HEX = re.compile(r"(?:(?:(?:0[xX]|\\x)[0-9A-Fa-f]{2})[ \t,:-]*){8,}")
SEPARATED_HEX = re.compile(r"(?<![#0-9A-Fa-f])(?:[0-9A-Fa-f]{2}[ \t,:-]+){7,}[0-9A-Fa-f]{2}(?![0-9A-Fa-f])")
DECIMAL_CODES = re.compile(r"(?<!\d)(?:\d{2,3}[ \t,;:]+){7,}\d{2,3}(?!\d)")
BASE64_TEXT = re.compile(r"(?<![A-Za-z0-9+/])[A-Za-z0-9+/]{16,}={0,2}(?![A-Za-z0-9+/=])")
HTML_TOKEN = re.compile(r"&#(?:(?P<hex>[xX][0-9A-Fa-f]+)|(?P<decimal>[0-9]+));")


@dataclass(frozen=True)
class EncodedCandidate:
    field: str
    encoding: str
    original: str
    start: int
    end: int


@dataclass(frozen=True)
class DecodedCandidate:
    field: str
    encoding: str
    original: str
    decoded: str
    start: int
    end: int


@dataclass(frozen=True)
class DecodeIssue:
    field: str
    encoding: str
    reason: str
    observed: int


@dataclass(frozen=True)
class DecodedBatch:
    candidates: tuple[DecodedCandidate, ...]
    issues: tuple[DecodeIssue, ...]


PATTERNS = (
    ("html_numeric", HTML_NUMERIC),
    ("hex_prefixed", PREFIXED_HEX),
    ("hex_separated", SEPARATED_HEX),
    ("decimal_codes", DECIMAL_CODES),
    ("base64", BASE64_TEXT),
)


def _recognized_candidates(field: str, text: str) -> list[EncodedCandidate]:
    found = [
        EncodedCandidate(field, encoding, match.group(0), match.start(), match.end())
        for encoding, pattern in PATTERNS
        for match in pattern.finditer(text)
    ]
    found.sort(key=lambda item: (item.start, item.end, item.encoding))
    selected: list[EncodedCandidate] = []
    for candidate in found:
        if any(candidate.start < existing.end and existing.start < candidate.end for existing in selected):
            continue
        selected.append(candidate)
    return selected


def _decode(candidate: EncodedCandidate) -> str | None:
    try:
        if candidate.encoding == "html_numeric":
            codepoints = []
            for match in HTML_TOKEN.finditer(candidate.original):
                value = match.group("hex")
                codepoints.append(int(value[1:], 16) if value else int(match.group("decimal")))
            return "".join(chr(value) for value in codepoints)
        if candidate.encoding.startswith("hex_"):
            byte_values = re.findall(r"(?:0[xX]|\\x)?([0-9A-Fa-f]{2})", candidate.original)
            return bytes(int(value, 16) for value in byte_values).decode("utf-8", errors="strict")
        if candidate.encoding == "decimal_codes":
            values = [int(value) for value in re.findall(r"\d{2,3}", candidate.original)]
            if any(value not in {9, 10, 13} and not 32 <= value <= 126 for value in values):
                return None
            return "".join(chr(value) for value in values)
        if len(candidate.original) % 4:
            return None
        decoded = base64.b64decode(candidate.original, validate=True)
        return decoded.decode("utf-8", errors="strict")
    except (ValueError, OverflowError, UnicodeDecodeError, binascii.Error):
        return None


def acceptable_decoded_text(decoded: str) -> bool:
    if not MIN_DECODED_TEXT <= len(decoded) <= MAX_DECODED_OUTPUT or "\x00" in decoded:
        return False
    permitted = sum(
        1
        for character in decoded
        if character in "\t\r\n" or (character.isprintable() and unicodedata.category(character) not in {"Cc", "Cf"})
    )
    return permitted / len(decoded) >= MIN_PRINTABLE_RATIO


def decode_representations(fields: list[tuple[str, str]]) -> DecodedBatch:
    """Decode only the explicit P0 representations, once, within fixed budgets."""
    decoded_items: list[DecodedCandidate] = []
    issues: list[DecodeIssue] = []
    retained = 0
    attempted = 0
    for field, text in sorted(fields, key=lambda item: (item[0], item[1])):
        recognized = _recognized_candidates(field, text)
        if len(recognized) > MAX_CANDIDATES_PER_FIELD:
            issues.append(DecodeIssue(field, "multiple", "per_field_candidate_limit", len(recognized)))
        for candidate in recognized[:MAX_CANDIDATES_PER_FIELD]:
            if attempted >= MAX_CANDIDATES_PER_TOOL:
                issues.append(DecodeIssue(field, candidate.encoding, "per_tool_candidate_limit", attempted + 1))
                return DecodedBatch(tuple(decoded_items), tuple(issues))
            attempted += 1
            if len(candidate.original) > MAX_CANDIDATE_INPUT:
                issues.append(DecodeIssue(field, candidate.encoding, "candidate_input_limit", len(candidate.original)))
                continue
            decoded = _decode(candidate)
            if decoded is None or not acceptable_decoded_text(decoded):
                continue
            if retained + len(decoded) > MAX_RETAINED_DECODED_TEXT:
                issues.append(DecodeIssue(field, candidate.encoding, "retained_text_limit", retained + len(decoded)))
                continue
            retained += len(decoded)
            decoded_items.append(
                DecodedCandidate(
                    field=field,
                    encoding=candidate.encoding,
                    original=candidate.original,
                    decoded=decoded,
                    start=candidate.start,
                    end=candidate.end,
                )
            )
    return DecodedBatch(tuple(decoded_items), tuple(issues))
