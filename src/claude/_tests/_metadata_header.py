"""Shared validator for the three-line metadata header (_claude_config_metadata.md).

Used by the rules and skills metadata tests so the format is checked by one implementation.
"""
import re
from datetime import date

HEADER_PREFIXES = ("<!-- version:", "<!-- created:", "<!-- updated:")

FIELD_PATTERNS = {
    "version": re.compile(r"^<!-- version: (0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*) -->$"),
    "created": re.compile(r"^<!-- created: (\d{4}-\d{2}-\d{2}) -->$"),
    "updated": re.compile(r"^<!-- updated: (\d{4}-\d{2}-\d{2}) -->$"),
}


def metadata_header_errors(content: str) -> list[str]:
    """Return format errors for a file's metadata header; empty if valid or absent.

    :param content: File text, starting where the header should begin.
    :type content: str
    :return: Human-readable error messages, one per problem found.
    :rtype: list[str]
    """
    lines = content.splitlines()
    header_idx = []
    in_fence = False
    for line_idx, line in enumerate(lines):
        # Header-shaped lines inside fenced code blocks are documentation examples
        if line.startswith("```"):
            in_fence = not in_fence
        elif not in_fence and line.startswith(HEADER_PREFIXES):
            header_idx.append(line_idx)
    if not header_idx:
        return []
    if header_idx != [0, 1, 2]:
        return [f"header must be exactly lines 1–3, found header lines {[line_idx + 1 for line_idx in header_idx]}"]
    values = {}
    for line, (field, pattern) in zip(lines[:3], FIELD_PATTERNS.items()):
        match = pattern.match(line)
        if not match:
            return [f"{field} line does not match format: {line!r}"]
        values[field] = match.group(1)
    try:
        created = date.fromisoformat(values["created"])
        updated = date.fromisoformat(values["updated"])
    except ValueError as exc:
        return [f"invalid date: {exc}"]
    if updated < created:
        return [f"updated ({updated}) is earlier than created ({created})"]
    return []
