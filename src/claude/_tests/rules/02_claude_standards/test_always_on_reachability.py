# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-18
# Date updated:      2026-10-06
# Version:           3.1.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Proves the real config's rules load the way their folders say, with no @import chain.

Claude Code loads every ``.md`` under ``rules/`` on its own: tiers 01–03 in every session,
and any file with ``paths:`` frontmatter only when a matching file is open. Read-on-demand
rules live in ``_rules_lazy_load/``, outside ``rules/``. Each check below names the folder
it guards, so a failure says which tier broke. ``test_rule_reachability.py`` proves the
detector itself on fake rule trees.
"""
from __future__ import annotations

import re
from functools import cache

from _rule_reachability import find_native_load_issues, has_paths_frontmatter
from _shared_paths import CLAUDE_DIR, CLAUDE_MD, LAZY_RULES_DIR, RULES_DIR

ALWAYS_ON_TIERS = ("01_essentials", "02_claude_standards", "03_authoring_guidelines")


@cache
def issues() -> dict[str, list[str]]:
    """Run the native-load scan over the real rules/ folder once."""
    return find_native_load_issues(RULES_DIR)


def test_every_tier_has_rule_files():
    """Each always-on tier holds rule files, so the checks can't pass on an empty folder."""
    empty = [t for t in ALWAYS_ON_TIERS if not any((RULES_DIR / t).rglob("*.md"))]
    assert not empty, f"always-on tiers with no rule files: {empty} — check RULES_DIR"


def test_no_readme_under_rules():
    """A README.md under rules/ would load every session — tier READMEs live in _rules_lazy_load/_tier_readmes/."""
    assert not issues()["readme"], f"move these to _rules_lazy_load/_tier_readmes/: {issues()['readme']}"


def test_no_lazy_load_folder_under_rules():
    """On-demand children belong in _rules_lazy_load/, since anything under rules/ auto-loads."""
    assert not issues()["lazy_folder"], f"_lazy_load/ folders under rules/: {issues()['lazy_folder']}"


def test_no_imports_under_rules():
    """Children load natively, so no rule file still @imports another."""
    assert not issues()["import"], f"rule files with leftover @import lines: {issues()['import']}"


def test_path_scoped_folder_holds_only_scoped_files():
    """Every file in rules/04_path_scoped/ has paths:, or it would load every session."""
    assert not issues()["unscoped"], f"add paths: frontmatter or move to _rules_lazy_load/: {issues()['unscoped']}"


def test_read_on_demand_pointers_resolve():
    """Every Read-on-demand pointer under rules/ names a file that exists."""
    assert not issues()["pointer"], f"pointers to missing files: {issues()['pointer']}"


def test_claude_md_imports_no_rules():
    """CLAUDE.md imports no rule, so nothing loads twice or out of its folder's mode."""
    bad = re.findall(r"^@~/[^/\s]+/(_?rules\S*)$", CLAUDE_MD.read_text(), re.M)
    assert not bad, f"CLAUDE.md still imports rules: {bad}"


def test_claude_md_imports_aliases():
    """CLAUDE.md still imports aliases.md, which isn't a rule and doesn't load on its own."""
    assert re.search(r"^@~/[^/\s]+/aliases\.md$", CLAUDE_MD.read_text(), re.M), "CLAUDE.md must @import aliases.md"


def test_lazy_rules_live_outside_rules():
    """The read-on-demand folder exists beside rules/ and holds rule files."""
    assert any(LAZY_RULES_DIR.rglob("*.md")), f"no rule files under {LAZY_RULES_DIR}"


# ── startup budget ───────────────────────────────────────────────────────────

# Config files loaded at every session start: CLAUDE.md, its imports, and every rules/ file
# without paths:. Lower it when a rule is demoted; raising it needs the evidence
# guiding_principles.md asks for.
MAX_STARTUP_FILES = 39
STARTUP_IMPORT = re.compile(r"^@~/[^/\s]+/(\S+\.md)\s*$", re.M)


def startup_files() -> list[str]:
    """List every file loaded at session start, relative to the config directory, CLAUDE.md first."""
    seen, pending = [], ["CLAUDE.md"]
    while pending:
        rel = pending.pop(0)
        path = CLAUDE_DIR / rel
        if rel in seen or not path.is_file():
            continue
        seen.append(rel)
        pending += STARTUP_IMPORT.findall(path.read_text())
    native = sorted(
        p.relative_to(CLAUDE_DIR).as_posix()
        for p in RULES_DIR.rglob("*.md") if not has_paths_frontmatter(p.read_text())
    )
    return seen + [n for n in native if n not in seen]


def test_startup_file_count_stays_within_budget():
    """Startup loads no more config files than the budget, so new always-on rules need a decision."""
    files = startup_files()
    assert files[0] == "CLAUDE.md", "the startup scan must begin at CLAUDE.md"
    assert len(files) <= MAX_STARTUP_FILES, (
        f"{len(files)} files load at startup, over the budget of {MAX_STARTUP_FILES} — "
        "make the new rule lazy, or justify raising MAX_STARTUP_FILES"
    )


def test_demoted_rules_stay_out_of_startup():
    """Rules moved to path-scoping on 2026-10-01 must not creep back into the startup set."""
    files = startup_files()
    assert not [f for f in files if f.endswith("/authoring_agents.md")], "authoring_agents.md is back at startup"
    assert not [f for f in files if "claude_directory_structure" in f], "directory-structure rule is back at startup"
    assert not [f for f in files if "04_path_scoped/" in f or "_rules_lazy_load/" in f], "a lazy rule is at startup"


DIRECTORY_RULES = [
    "claude_directory_structure.md",
    "claude_directory_structure/_claude_directory_organisation.md",
    "claude_directory_structure/_claude_directory_naming.md",
    "claude_directory_structure/_file_structure_validation.md",
]


def test_directory_structure_loads_with_config_files():
    """The directory-structure rule and its 3 children load through paths: whenever a config file is read."""
    for target in DIRECTORY_RULES:
        path = RULES_DIR / "04_path_scoped" / target
        assert path.read_text().startswith('---\npaths:\n  - "**/.claude/**"\n'), f"{target} lost its paths: trigger"


def test_directory_structure_keeps_a_pointer_and_a_backstop():
    """New config files rely on an always-on pointer, with the naming hook catching what slips through."""
    usage = (RULES_DIR / "01_essentials" / "claude_usage_standards.md").read_text()
    assert "04_path_scoped/claude_directory_structure.md" in usage, "claude_usage_standards.md lost its pointer"
    assert (CLAUDE_DIR / "hooks" / "hook_enforcement_naming_convention.sh").is_file(), (
        "the naming-convention hook is the backstop that makes this rule safe to lazy-load — keep it"
    )
