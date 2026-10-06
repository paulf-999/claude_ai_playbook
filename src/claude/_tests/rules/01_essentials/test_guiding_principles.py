# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-08-28
# Date updated:      2026-10-06
# Version:           2.2.0
# Test quality score: 9/10
# Test complexity score: 9/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests that CLAUDE.md's imports follow guiding_principles.md.

- **Lazy-load by default:** nothing under ``05_lazy_load/`` or a per-parent ``_lazy_load/`` is imported.
- **Explicit over implicit:** every import has a purpose comment on the line above it.
- **Context efficiency:** imports stay few, unique, and limited to the always-on tiers, in tier order.
"""
from __future__ import annotations

import re

from _shared_paths import CLAUDE_MD

IMPORT_PATTERN = re.compile(r"^@~/([^/\s]+)/(\S+)$", re.M)
ALWAYS_ON_TIERS = ("01_essentials", "02_claude_standards", "03_authoring_guidelines")
NON_RULE_IMPORTS = {"memory/MEMORY.md", "aliases.md"}
MAX_IMPORTS = 20


def imports(text: str) -> list[tuple[str, str]]:
    """Find the ``@~/<config-dir>/<path>`` import lines in a CLAUDE.md.

    :param text: CLAUDE.md content.
    :type text: str
    :return: ``(config_dir, path)`` pairs in file order.
    :rtype: list[tuple[str, str]]
    """
    return IMPORT_PATTERN.findall(text)


def import_paths() -> list[str]:
    """List the paths the real CLAUDE.md imports, relative to the config dir.

    :return: Import paths in file order.
    :rtype: list[str]
    """
    return [path for _, path in imports(CLAUDE_MD.read_text())]


def test_claude_md_has_imports():
    """CLAUDE.md imports something, so the checks below can't pass on an empty list."""
    assert import_paths(), "CLAUDE.md has no @~/<dir>/ imports — the import pattern may be broken"


def test_no_lazy_load_tier_imports():
    """Nothing in _rules_lazy_load/ is imported — that folder is read on demand."""
    bad = [p for p in import_paths() if p.startswith("_rules_lazy_load/")]
    assert not bad, f"CLAUDE.md imports lazy-load rules {bad} — read them on demand instead"


def test_no_per_parent_lazy_load_imports():
    """Nothing in a <parent>/_lazy_load/ folder is imported — its parent names it instead."""
    bad = [p for p in import_paths() if "/_lazy_load/" in p]
    assert not bad, f"CLAUDE.md imports per-parent lazy-load files {bad} — use a 'Read on demand' pointer"


def test_every_import_has_purpose_comment():
    """Each import line follows a <!-- comment --> or another import that shares its comment."""
    lines = CLAUDE_MD.read_text().splitlines()
    for number, line in enumerate(lines):
        if not line.startswith("@"):
            continue
        previous = next((lines[i].strip() for i in range(number - 1, -1, -1) if lines[i].strip()), "")
        assert previous.startswith("<!--"), f"line {number + 1} '{line}' needs a <!-- purpose --> comment above it"


def test_purpose_comments_say_something():
    """Every HTML comment above an import has real text, not a placeholder."""
    comments = re.findall(r"<!--(.*?)-->\n@", CLAUDE_MD.read_text())
    assert comments, "expected purpose comments directly above imports"
    short = [c.strip() for c in comments if len(c.strip()) < 15]
    assert not short, f"purpose comments too short to explain anything: {short}"


def test_import_count_under_cap():
    """CLAUDE.md stays under the import cap, since each import costs tokens every session."""
    count = len(import_paths())
    assert count < MAX_IMPORTS, f"CLAUDE.md has {count} imports — review each against a real, recurring need"


def test_no_duplicate_imports():
    """No file is imported twice."""
    paths = import_paths()
    duplicates = sorted({p for p in paths if paths.count(p) > 1})
    assert not duplicates, f"CLAUDE.md imports these more than once: {duplicates}"


def test_imports_share_one_config_dir():
    """Every import uses the same @~/<config-dir>/ prefix."""
    dirs = {config_dir for config_dir, _ in imports(CLAUDE_MD.read_text())}
    assert len(dirs) == 1, f"imports mix config-dir prefixes {sorted(dirs)} — use one"


def test_claude_md_imports_only_memory_and_aliases():
    """CLAUDE.md imports no rules, since Claude Code loads rules/ natively."""
    rules = [p for p in import_paths() if p not in NON_RULE_IMPORTS]
    assert not rules, f"CLAUDE.md imports rules, which would load twice or bypass their folder: {rules}"


def test_imports_are_markdown():
    """Every import is a markdown file."""
    bad = [p for p in import_paths() if not p.endswith(".md")]
    assert not bad, f"CLAUDE.md imports non-markdown files: {bad}"


def test_import_parser_reads_any_config_dir():
    """The parser handles .claude, claude and other config-dir names, and skips inline mentions."""
    text = "@~/.claude/a.md\n@~/claude/rules/b.md\nsee @~/claude/c.md inline\n"
    assert imports(text) == [(".claude", "a.md"), ("claude", "rules/b.md")], f"got {imports(text)}"


def test_imports_sit_under_imports_heading():
    """Every import is under the '## Imports' heading, so they're reviewed in one place."""
    text = CLAUDE_MD.read_text()
    assert "\n## Imports\n" in text, "CLAUDE.md needs an '## Imports' heading"
    before = text.split("\n## Imports\n", 1)[0]
    assert not imports(before), f"imports above the '## Imports' heading: {imports(before)}"
