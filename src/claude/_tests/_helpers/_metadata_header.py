"""Shared validator for the three-line metadata header (_claude_config_metadata.md).

Used by the rules, skills, agents and hooks metadata tests so the format is checked by one
implementation. Markdown files wrap each line in ``<!-- … -->``; shell hooks use ``# …``.
"""
import re
from datetime import date

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)

# Comment wrapper (opening, closing) per file type
COMMENT_STYLES = {"html": ("<!-- ", " -->"), "shell": ("# ", "")}

FIELD_VALUES = {
    "version": r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)",
    "created": r"(\d{4}-\d{2}-\d{2})",
    "updated": r"(\d{4}-\d{2}-\d{2})",
}


def field_patterns(style: str) -> dict[str, re.Pattern]:
    """Return the compiled line pattern for each header field in the given comment style.

    :param style: A key of ``COMMENT_STYLES`` (``html`` or ``shell``).
    :type style: str
    :return: Field name to compiled full-line pattern, in header order.
    :rtype: dict[str, re.Pattern]
    """
    opening, closing = (re.escape(part) for part in COMMENT_STYLES[style])
    return {field: re.compile(f"^{opening}{field}: {value}{closing}$") for field, value in FIELD_VALUES.items()}


FIELD_PATTERNS = field_patterns("html")


def metadata_header_errors(content: str, style: str = "html", line_offset: int = 0) -> list[str]:
    """Return format errors for a file's metadata header; empty if valid or absent.

    :param content: File text, starting where the header should begin.
    :type content: str
    :param style: Comment style of the header lines — ``html`` or ``shell``.
    :type style: str
    :param line_offset: Lines above ``content`` in the real file, so messages report true line numbers.
    :type line_offset: int
    :return: Human-readable error messages, one per problem found.
    :rtype: list[str]
    """
    patterns = field_patterns(style)
    prefixes = tuple(f"{COMMENT_STYLES[style][0]}{field}:" for field in FIELD_VALUES)
    lines = content.splitlines()
    header_idx = []
    in_fence = False
    for line_idx, line in enumerate(lines):
        # Header-shaped lines inside fenced code blocks are documentation examples
        if line.startswith("```"):
            in_fence = not in_fence
        elif not in_fence and line.startswith(prefixes):
            header_idx.append(line_idx)
    if not header_idx:
        return []
    if header_idx != [0, 1, 2]:
        found = [line_idx + 1 + line_offset for line_idx in header_idx]
        return [f"header must be exactly lines {1 + line_offset}–{3 + line_offset}, found header lines {found}"]
    values = {}
    for line, (field, pattern) in zip(lines[:3], patterns.items()):
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


def frontmatter_header_errors(content: str) -> list[str]:
    """Return errors for a frontmatter file (SKILL.md, AGENT.md) whose header follows the frontmatter.

    :param content: Full text of the file.
    :type content: str
    :return: Human-readable error messages, one per problem found.
    :rtype: list[str]
    """
    match = FRONTMATTER_RE.match(content)
    if not match:
        return ["file must open with YAML frontmatter"]
    if re.search(r"^version:", match.group(1), re.M):
        return ["version belongs in the metadata header, not the frontmatter"]
    after = content[match.end():]
    if not after.startswith("<!-- version:"):
        return ["metadata header must start on the line after the frontmatter"]
    return metadata_header_errors(after)


def header_version_after_frontmatter(content: str) -> str:
    """Return the version from the header that follows a file's frontmatter.

    :param content: Full text of a file with a valid frontmatter and header.
    :type content: str
    :return: The semver string from the header's version line.
    :rtype: str
    """
    first_line = content[FRONTMATTER_RE.match(content).end():].splitlines()[0]
    return ".".join(FIELD_PATTERNS["version"].match(first_line).groups())


def shell_header_errors(content: str) -> list[str]:
    """Return errors for a shell hook whose ``#`` header must sit on lines 2–4, after the shebang.

    :param content: Full text of the script.
    :type content: str
    :return: Human-readable error messages, one per problem found.
    :rtype: list[str]
    """
    first_line, _, rest = content.partition("\n")
    if not first_line.startswith("#!"):
        return ["script must start with a shebang line"]
    if not rest.startswith("# version:"):
        return ["metadata header must start on line 2, straight after the shebang"]
    return metadata_header_errors(rest, style="shell", line_offset=1)
