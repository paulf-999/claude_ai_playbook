# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 9/10
# Test complexity score: 3/10
# Python style compliant: Yes
# Date created:      2026-09-18
# Version:           1.0.0
# Date updated:      [placeholder]
# ─────────────────────────────────────────────────────────

"""Tests for always-on-tier reachability — every file imported, nothing orphaned.

Per `authoring_rules.md`'s "Wire up every documented child" gate: a rule file
that describes child files but never `@import`s them is a real, recurring bug
class (found and fixed in `naming_standards.md`, 2026-09-17). This suite
verifies the current tree is clean, and proves the detection logic itself
works via synthetic fixtures — not just that it happens to pass today.
"""
from pathlib import Path

import pytest

from _shared_paths import ALIASES_FILE, CLAUDE_DIR, CLAUDE_MD

ALWAYS_ON_TIERS = [
    "01_essentials",
    "02_claude_standards",
    "03_authoring_guidelines",
    "04_claude_reference",
]
ENTRY_FILES = [CLAUDE_MD, ALIASES_FILE]


def find_reachability_issues(rules_root: Path, entry_files: list[Path]) -> tuple[list[str], list[str]]:
    """Walk `@import` chains from the given entry files and report gaps.

    :param rules_root: The root directory whose .md tree is being audited.
    :type rules_root: Path
    :param entry_files: Files to start the import walk from (e.g. CLAUDE.md).
    :type entry_files: list[Path]
    :return: A tuple of (broken import targets, orphaned files never reached).
    :rtype: tuple[list[str], list[str]]
    """
    all_md = {
        p.resolve() for p in rules_root.rglob("*.md")
        if p.name != "README.md"
        and "template" not in str(p).lower()
        and "05_lazy_load" not in p.parts
    }
    visited: set[Path] = set()
    broken: list[str] = []
    queue = list(entry_files)

    while queue:
        current = queue.pop()
        if not current.exists():
            broken.append(str(current))
            continue
        resolved = current.resolve()
        if resolved in visited:
            continue
        visited.add(resolved)
        for line in current.read_text(errors="ignore").splitlines():
            stripped = line.strip()
            if not stripped.startswith("@~/") or "/" not in stripped[len("@~/"):]:
                continue
            # "@~/<config-dir-name>/rest" — the config-dir-name varies (.claude,
            # claude, a repo checkout); strip both segments, resolve against
            # rules_root.parent. Never assume which convention is in play.
            rest = stripped[len("@~/"):].split("/", 1)[1]
            target = rules_root.parent / rest
            if target.exists():
                queue.append(target)
            else:
                broken.append(f"{current} -> {target}")

    orphaned = sorted(str(p.relative_to(rules_root.parent)) for p in all_md if p not in visited)
    return broken, orphaned


@pytest.mark.parametrize("tier", ALWAYS_ON_TIERS)
def test_no_orphaned_files_in_tier(tier):
    """Every .md file under each always-on tier must be reachable from CLAUDE.md."""
    _, orphaned = find_reachability_issues(CLAUDE_DIR / "_rules", ENTRY_FILES)
    tier_orphans = [o for o in orphaned if f"_rules/{tier}/" in o or f"_rules\\{tier}\\" in o]
    assert not tier_orphans, (
        f"{tier}/ has files that exist but are never @imported: {tier_orphans}"
    )


def test_no_broken_imports_in_always_on_tree():
    """Every @import line in the always-on tree must resolve to a real file."""
    broken, _ = find_reachability_issues(CLAUDE_DIR / "_rules", ENTRY_FILES)
    assert not broken, f"Broken @import targets found: {broken}"


def test_05_lazy_load_is_never_scanned():
    """05_lazy_load/ is intentionally unreachable from CLAUDE.md — must not be flagged."""
    _, orphaned = find_reachability_issues(CLAUDE_DIR / "_rules", ENTRY_FILES)
    lazy_load_hits = [o for o in orphaned if "05_lazy_load" in o]
    assert not lazy_load_hits, (
        "05_lazy_load/ files appeared in the orphan report — the scan should "
        f"never even reach that tier's contents: {lazy_load_hits}"
    )


def test_detector_catches_the_naming_standards_bug_pattern(tmp_path):
    """Regression: a parent listing a child in prose without @import must be flagged."""
    rules = tmp_path / "_rules" / "01_essentials"
    rules.mkdir(parents=True)
    (tmp_path / "CLAUDE.md").write_text("@~/.claude/_rules/01_essentials/parent.md\n")
    (rules / "parent.md").write_text("See `_child.md` for detail.\n")
    (rules / "_child.md").write_text("# Child content, never imported\n")

    broken, orphaned = find_reachability_issues(rules.parent, [tmp_path / "CLAUDE.md"])

    assert not broken, "This fixture has no broken imports — only an orphan"
    assert any("_child.md" in o for o in orphaned), (
        "Detector failed to catch a child mentioned in prose but never @imported"
    )


def test_detector_passes_when_child_is_properly_imported(tmp_path):
    """Same fixture, but wired correctly — must not be flagged as orphaned."""
    rules = tmp_path / "_rules" / "01_essentials"
    rules.mkdir(parents=True)
    (tmp_path / "CLAUDE.md").write_text("@~/.claude/_rules/01_essentials/parent.md\n")
    (rules / "parent.md").write_text("@~/.claude/_rules/01_essentials/_child.md\n")
    (rules / "_child.md").write_text("# Child content, properly imported\n")

    broken, orphaned = find_reachability_issues(rules.parent, [tmp_path / "CLAUDE.md"])

    assert not broken
    assert not orphaned, f"Properly-imported child was incorrectly flagged: {orphaned}"


def test_detector_resolves_multi_level_nesting(tmp_path):
    """A grandchild reachable only through a child's own @import must resolve."""
    rules = tmp_path / "_rules" / "01_essentials"
    rules.mkdir(parents=True)
    (tmp_path / "CLAUDE.md").write_text("@~/.claude/_rules/01_essentials/parent.md\n")
    (rules / "parent.md").write_text("@~/.claude/_rules/01_essentials/child.md\n")
    (rules / "child.md").write_text("@~/.claude/_rules/01_essentials/_grandchild.md\n")
    (rules / "_grandchild.md").write_text("# Grandchild content\n")

    broken, orphaned = find_reachability_issues(rules.parent, [tmp_path / "CLAUDE.md"])

    assert not broken
    assert not orphaned, f"Grandchild reachable via a two-hop import was flagged: {orphaned}"


def test_detector_flags_broken_import_separately_from_orphan(tmp_path):
    """A dangling @import to a nonexistent file is a broken import, not an orphan."""
    rules = tmp_path / "_rules" / "01_essentials"
    rules.mkdir(parents=True)
    (tmp_path / "CLAUDE.md").write_text("@~/.claude/_rules/01_essentials/parent.md\n")
    (rules / "parent.md").write_text("@~/.claude/_rules/01_essentials/_missing.md\n")

    broken, orphaned = find_reachability_issues(rules.parent, [tmp_path / "CLAUDE.md"])

    assert any("_missing.md" in b for b in broken), "Dangling import should be reported as broken"
    assert not orphaned, "A file that was never created can't also be an orphan"


def test_readme_files_excluded_from_scan(tmp_path):
    """README.md is documentation, not a rule file — must never be flagged as orphaned."""
    rules = tmp_path / "_rules" / "01_essentials"
    rules.mkdir(parents=True)
    (tmp_path / "CLAUDE.md").write_text("@~/.claude/_rules/01_essentials/parent.md\n")
    (rules / "parent.md").write_text("# Parent, self-contained\n")
    (rules / "README.md").write_text("# Directory index, not a rule\n")

    _, orphaned = find_reachability_issues(rules.parent, [tmp_path / "CLAUDE.md"])

    assert not any("README.md" in o for o in orphaned), (
        "README.md must be excluded from the orphan scan"
    )


def test_orphan_report_names_the_specific_file(tmp_path):
    """The orphan report must identify which file is unreachable, not just that one exists."""
    rules = tmp_path / "_rules" / "01_essentials"
    rules.mkdir(parents=True)
    (tmp_path / "CLAUDE.md").write_text("@~/.claude/_rules/01_essentials/parent.md\n")
    (rules / "parent.md").write_text("# Parent, self-contained\n")
    (rules / "_forgotten.md").write_text("# Never referenced anywhere\n")

    _, orphaned = find_reachability_issues(rules.parent, [tmp_path / "CLAUDE.md"])

    assert len(orphaned) == 1
    assert "_forgotten.md" in orphaned[0]


@pytest.mark.parametrize("config_dir_name", [".claude", "claude"])
def test_detector_works_with_either_config_dir_convention(tmp_path, config_dir_name):
    """The import parser must not assume a specific config-dir name (~/.claude vs ~/claude)."""
    rules = tmp_path / "_rules" / "01_essentials"
    rules.mkdir(parents=True)
    (tmp_path / "CLAUDE.md").write_text(f"@~/{config_dir_name}/_rules/01_essentials/parent.md\n")
    (rules / "parent.md").write_text("# Parent, self-contained\n")

    broken, orphaned = find_reachability_issues(rules.parent, [tmp_path / "CLAUDE.md"])

    assert not broken, f"Import using '~/{config_dir_name}/' convention wasn't resolved: {broken}"
    assert not orphaned


def test_entry_file_itself_never_counts_as_orphaned(tmp_path):
    """CLAUDE.md is the walk's starting point — it must never appear in its own orphan report."""
    rules = tmp_path / "_rules" / "01_essentials"
    rules.mkdir(parents=True)
    claude_md = tmp_path / "CLAUDE.md"
    claude_md.write_text("@~/.claude/_rules/01_essentials/parent.md\n")
    (rules / "parent.md").write_text("# Parent, self-contained\n")

    _, orphaned = find_reachability_issues(rules.parent, [claude_md])

    assert not orphaned
