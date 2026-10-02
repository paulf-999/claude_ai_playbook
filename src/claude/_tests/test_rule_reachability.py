# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-18
# Date updated:      2026-10-02
# Version:           2.0.1
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Proves the rule-reachability detector on small fake rule trees.

``_rule_reachability.py`` reports rule files CLAUDE.md never imports — a real,
recurring bug (found and fixed in ``naming_standards.md``, 2026-09-17). These tests
build fake trees in a temp directory so each case, including the exemptions, is
proven to work rather than just passing on today's config.
``rules/02_claude_standards/test_always_on_reachability.py`` runs it on the real config.
"""
import pytest

from _rule_reachability import find_reachability_issues


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


def test_detector_ignores_template_in_path_above_rules_root(tmp_path):
    """Regression: a checkout folder named with 'template' must not hide orphans."""
    root = tmp_path / "repo_skill_template"
    rules = root / "_rules" / "01_essentials"
    rules.mkdir(parents=True)
    (root / "CLAUDE.md").write_text("@~/.claude/_rules/01_essentials/parent.md\n")
    (rules / "parent.md").write_text("See `_child.md` for detail.\n")
    (rules / "_child.md").write_text("# Child content, never imported\n")

    _, orphaned = find_reachability_issues(rules.parent, [root / "CLAUDE.md"])

    assert any("_child.md" in o for o in orphaned), (
        "A 'template' folder above _rules/ hid the orphaned child — the scan checked nothing"
    )


def test_template_files_below_rules_root_still_excluded(tmp_path):
    """Template files inside _rules/ are still skipped, so they never count as orphans."""
    rules = tmp_path / "_rules" / "01_essentials"
    rules.mkdir(parents=True)
    (tmp_path / "CLAUDE.md").write_text("@~/.claude/_rules/01_essentials/parent.md\n")
    (rules / "parent.md").write_text("# Parent, self-contained\n")
    (rules / "rule_template.md").write_text("# Template, never imported by design\n")

    _, orphaned = find_reachability_issues(rules.parent, [tmp_path / "CLAUDE.md"])

    assert not orphaned, f"A template file inside _rules/ was reported as orphaned: {orphaned}"


def test_lazy_load_folder_beside_parent_is_exempt(tmp_path):
    """A child in a parent's `_lazy_load/` folder is read on demand — never an orphan."""
    rules = tmp_path / "_rules" / "03_authoring_guidelines"
    lazy = rules / "parent" / "_lazy_load"
    lazy.mkdir(parents=True)
    (tmp_path / "CLAUDE.md").write_text("@~/.claude/_rules/03_authoring_guidelines/parent.md\n")
    (rules / "parent.md").write_text("**Read on demand:** `parent/_lazy_load/_child.md`\n")
    (lazy / "_child.md").write_text("# Child content, read on demand\n")
    (rules / "parent" / "_sibling.md").write_text("# Sibling outside _lazy_load, never imported\n")

    broken, orphaned = find_reachability_issues(rules.parent, [tmp_path / "CLAUDE.md"])

    assert not broken
    assert not any("_lazy_load" in o for o in orphaned), (
        f"A `_lazy_load/` child was flagged as orphaned: {orphaned}"
    )
    assert any("_sibling.md" in o for o in orphaned), (
        "The exemption leaked: an un-imported file outside `_lazy_load/` was not flagged"
    )


def test_lazy_load_exemption_matches_whole_segment_only(tmp_path):
    """Only a folder named exactly `_lazy_load` is exempt — a name merely containing it is not."""
    rules = tmp_path / "_rules" / "01_essentials"
    lookalike = rules / "parent" / "_lazy_loader"
    lookalike.mkdir(parents=True)
    (tmp_path / "CLAUDE.md").write_text("@~/.claude/_rules/01_essentials/parent.md\n")
    (rules / "parent.md").write_text("# Parent, self-contained\n")
    (lookalike / "_child.md").write_text("# Never imported\n")

    _, orphaned = find_reachability_issues(rules.parent, [tmp_path / "CLAUDE.md"])

    assert any("_lazy_loader" in o for o in orphaned), (
        "A folder merely containing '_lazy_load' in its name was wrongly exempted"
    )
