# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-18
# Date updated:      2026-10-06
# Version:           3.1.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Proves the native-load detector on small fake rule trees.

Claude Code loads every ``.md`` under ``rules/`` on its own, so ``_rule_reachability.py``
reports files there that would load wrongly (READMEs, ``_lazy_load/`` folders, leftover
``@import`` lines, path-scoped files without ``paths:``) and on-demand pointers that lead
nowhere. These tests build fake trees in a temp directory so each case is proven to work
rather than just passing on today's config.
``rules/02_claude_standards/test_always_on_reachability.py`` runs it on the real config.
"""
import pytest

from _rule_reachability import find_native_load_issues, has_paths_frontmatter


def make_rules(tmp_path):
    """Create an empty ``rules/01_essentials/`` tree and return the ``rules/`` folder."""
    (tmp_path / "rules" / "01_essentials").mkdir(parents=True)
    return tmp_path / "rules"


def test_clean_tree_reports_nothing(tmp_path):
    """A plain rule, a scoped rule and a resolving pointer produce no issues."""
    rules = make_rules(tmp_path)
    (tmp_path / "_rules_lazy_load").mkdir()
    (tmp_path / "_rules_lazy_load" / "extra.md").write_text("# Extra\n")
    pointer = "- **Read on demand:** `~/.claude/_rules_lazy_load/extra.md` — detail.\n"
    (rules / "01_essentials" / "a.md").write_text(pointer)
    (rules / "04_path_scoped").mkdir()
    (rules / "04_path_scoped" / "sql.md").write_text('---\npaths:\n  - "**/*.sql"\n---\n# SQL\n')

    issues = find_native_load_issues(rules)

    assert not any(issues.values()), f"a clean tree must report nothing, got {issues}"


def test_readme_under_rules_is_flagged(tmp_path):
    """A README.md under rules/ would load every session, so it must be reported."""
    rules = make_rules(tmp_path)
    (rules / "01_essentials" / "README.md").write_text("# Tier index\n")

    assert find_native_load_issues(rules)["readme"] == ["rules/01_essentials/README.md"]


def test_lazy_load_folder_under_rules_is_flagged(tmp_path):
    """A _lazy_load/ folder under rules/ would auto-load its on-demand children."""
    rules = make_rules(tmp_path)
    (rules / "01_essentials" / "parent" / "_lazy_load").mkdir(parents=True)

    assert find_native_load_issues(rules)["lazy_folder"] == ["rules/01_essentials/parent/_lazy_load"]


def test_lazy_load_check_matches_whole_folder_name_only(tmp_path):
    """Only a folder named exactly `_lazy_load` is flagged — a name merely containing it is not."""
    rules = make_rules(tmp_path)
    (rules / "01_essentials" / "_lazy_load_notes").mkdir()

    assert not find_native_load_issues(rules)["lazy_folder"], "a folder merely containing '_lazy_load' was flagged"


@pytest.mark.parametrize("config_dir_name", [".claude", "claude"])
def test_leftover_import_is_flagged_for_either_config_dir(tmp_path, config_dir_name):
    """An @import line under rules/ is redundant now, whichever config-dir name it uses."""
    rules = make_rules(tmp_path)
    (rules / "01_essentials" / "parent.md").write_text(f"@~/{config_dir_name}/rules/01_essentials/_child.md\n")

    assert find_native_load_issues(rules)["import"] == ["rules/01_essentials/parent.md"]


def test_unscoped_file_in_path_scoped_folder_is_flagged(tmp_path):
    """A 04_path_scoped/ file without paths: would load every session despite its folder."""
    rules = make_rules(tmp_path)
    (rules / "04_path_scoped" / "style").mkdir(parents=True)
    (rules / "04_path_scoped" / "style" / "_child.md").write_text("# Child, no frontmatter\n")

    assert find_native_load_issues(rules)["unscoped"] == ["rules/04_path_scoped/style/_child.md"]


def test_scoped_file_in_tier_folder_is_allowed(tmp_path):
    """A tier folder may hold a path-scoped rule (e.g. authoring_agents.md), so it is not flagged."""
    rules = make_rules(tmp_path)
    (rules / "01_essentials" / "agents.md").write_text('---\npaths:\n  - "**/agents/**"\n---\n# Agents\n')

    assert not any(find_native_load_issues(rules).values()), "a path-scoped rule in a tier folder was flagged"


@pytest.mark.parametrize("pointer", [
    "- **Read on demand:** `~/.claude/_rules_lazy_load/gone.md` — detail.",
    "- **Read on demand:** [`~/claude/_rules_lazy_load/gone.md`](gone.md) — detail.",
])
def test_broken_pointer_is_flagged_in_both_forms(tmp_path, pointer):
    """A Read-on-demand pointer to a missing file is reported, plain or wrapped in a link."""
    rules = make_rules(tmp_path)
    (rules / "01_essentials" / "a.md").write_text(pointer + "\n")

    assert find_native_load_issues(rules)["pointer"] == ["rules/01_essentials/a.md -> _rules_lazy_load/gone.md"]


def test_template_files_are_ignored(tmp_path):
    """Non-markdown files such as templates or YAML never load, so they are never flagged."""
    rules = make_rules(tmp_path)
    (rules / "04_path_scoped").mkdir()
    (rules / "04_path_scoped" / "domains.yaml").write_text("x: 1\n")

    assert not any(find_native_load_issues(rules).values()), "a non-markdown file was flagged"


@pytest.mark.parametrize(("text", "expected"), [
    ('---\npaths:\n  - "**/*.py"\n---\n# X\n', True),
    ("---\ntitle: x\n---\npaths: not frontmatter\n", False),
    ("# No frontmatter\npaths: x\n", False),
])
def test_paths_frontmatter_is_read_only_from_the_opening_block(text, expected):
    """paths: counts only inside the frontmatter block that opens the file."""
    assert has_paths_frontmatter(text) is expected, f"wrong answer for {text!r}"
