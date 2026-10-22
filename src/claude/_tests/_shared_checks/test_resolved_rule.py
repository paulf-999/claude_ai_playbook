# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-22
# Date updated:      2026-10-22
# Version:           1.0.0
# Test quality score: 10/10
# Test complexity score: 9/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Proves ``_resolved_rule.py`` still follows ``@~/`` imports as well as on-demand pointers.

Rules no longer use ``@`` imports, since Claude Code loads ``rules/`` natively, so the
real config never exercises that branch. These tests write a small rule that imports a
real file, so the branch is shown to work if an import ever comes back.
"""
from pathlib import Path

from _resolved_rule import child_paths, resolved_content
from _shared_paths import CLAUDE_DIR

IMPORTED = "rules/01_essentials/guiding_principles.md"


def write_rule(tmp_path: Path) -> Path:
    """Write a rule with one import of a real file and one of a missing file."""
    rule = tmp_path / "parent.md"
    rule.write_text(f"# Parent\n@~/claude/{IMPORTED}\n@~/claude/rules/no_such_file.md\n")
    return rule


def test_imports_are_listed_as_children(tmp_path: Path):
    """Each @~/<config>/ line is listed as a child path under the config folder."""
    children = child_paths(write_rule(tmp_path))
    assert children == [CLAUDE_DIR / IMPORTED, CLAUDE_DIR / "rules/no_such_file.md"], children


def test_imports_are_inlined_and_missing_ones_kept(tmp_path: Path):
    """An import of a real file is replaced by its text, and an import of a missing file stays as written."""
    content = resolved_content(write_rule(tmp_path))
    assert (CLAUDE_DIR / IMPORTED).read_text(encoding="utf-8") in content, "the real import should be inlined"
    assert "@~/claude/rules/no_such_file.md" in content, "a missing import should be left as written"
