"""Reads a parent rule together with every child it imports or points to on demand.

A parent+child rule (per ``multifile_document_organisation.md``) keeps its content
across several files. ``resolved_content`` inlines each ``@~/<config-dir>/...`` import
and each ``**Read on demand:**`` pointer, so content checks see the whole rule and a
future re-split doesn't silently break them.
"""
from __future__ import annotations

import re
from pathlib import Path

from _shared_paths import CLAUDE_DIR

POINTER = re.compile(r"\*\*Read on demand:\*\* `~/[^/]+/([^`]+)`")


def child_paths(rule_file: Path) -> list[Path]:
    """List the files a rule imports or points to on demand.

    :param rule_file: The parent rule.
    :type rule_file: Path
    :return: Target paths in file order, whether or not they exist.
    :rtype: list[Path]
    """
    paths = []
    for line in rule_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("@~/") and "/" in stripped[len("@~/"):]:
            paths.append(CLAUDE_DIR / stripped[len("@~/"):].split("/", 1)[1])
        elif pointer := POINTER.search(stripped):
            paths.append(CLAUDE_DIR / pointer.group(1))
    return paths


def resolved_content(rule_file: Path) -> str:
    """Return a rule's text with every import and on-demand child inlined.

    :param rule_file: The parent rule.
    :type rule_file: Path
    :return: The parent's lines, with each import or pointer line replaced by its target's text.
    :rtype: str
    """
    parts = []
    for line in rule_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        target = None
        if stripped.startswith("@~/") and "/" in stripped[len("@~/"):]:
            target = CLAUDE_DIR / stripped[len("@~/"):].split("/", 1)[1]
        elif pointer := POINTER.search(stripped):
            target = CLAUDE_DIR / pointer.group(1)
        parts.append(target.read_text(encoding="utf-8") if target and target.exists() else line)
    return "\n".join(parts)
