# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-18
# Date updated:      2026-10-02
# Version:           2.0.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Proves every always-on rule file is reachable from CLAUDE.md in the real config.

Per ``authoring_rules.md``'s "Wire up every documented child" gate, a rule file that
exists but is never ``@import``ed silently never loads. Each always-on tier gets its own
test so a failure names the tier, and the per-parent ``_lazy_load/`` exemption is checked
against its contract: every exempt child must be named by a "Read on demand" pointer.
``test_rule_reachability.py`` proves the detector itself on fake rule trees.
"""
from __future__ import annotations

import re
from functools import cache

from _rule_reachability import find_reachability_issues
from _shared_paths import ALIASES_FILE, CLAUDE_DIR, CLAUDE_MD, RULES_DIR

ALWAYS_ON_TIERS = ("01_essentials", "02_claude_standards", "03_authoring_guidelines", "04_claude_reference")
ENTRY_FILES = [CLAUDE_MD, ALIASES_FILE]


@cache
def scan() -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Run the reachability scan over the real config once.

    :return: Broken import targets and orphaned rule files.
    :rtype: tuple[tuple[str, ...], tuple[str, ...]]
    """
    broken, orphaned = find_reachability_issues(RULES_DIR, ENTRY_FILES)
    return tuple(broken), tuple(orphaned)


def orphans_in(tier: str) -> list[str]:
    """List the orphaned files in one tier.

    :param tier: Tier folder name, e.g. ``01_essentials``.
    :type tier: str
    :return: Orphaned paths under ``_rules/<tier>/``.
    :rtype: list[str]
    """
    return [o for o in scan()[1] if o.startswith(f"_rules/{tier}/")]


def test_entry_files_exist():
    """CLAUDE.md and aliases.md, where the import walk starts, both exist."""
    missing = [str(p) for p in ENTRY_FILES if not p.is_file()]
    assert not missing, f"import walk entry files are missing: {missing}"


def test_every_tier_has_rule_files():
    """Each always-on tier holds rule files, so the orphan checks can't pass on an empty folder."""
    empty = [t for t in ALWAYS_ON_TIERS if not any((RULES_DIR / t).rglob("*.md"))]
    assert not empty, f"always-on tiers with no rule files: {empty} — check RULES_DIR"


def test_no_orphans_in_essentials():
    """Every file in 01_essentials/ is imported."""
    orphans = orphans_in("01_essentials")
    assert not orphans, f"01_essentials/ files that are never @imported: {orphans}"


def test_no_orphans_in_claude_standards():
    """Every file in 02_claude_standards/ is imported."""
    orphans = orphans_in("02_claude_standards")
    assert not orphans, f"02_claude_standards/ files that are never @imported: {orphans}"


def test_no_orphans_in_authoring_guidelines():
    """Every file in 03_authoring_guidelines/ is imported or an exempt on-demand child."""
    orphans = orphans_in("03_authoring_guidelines")
    assert not orphans, f"03_authoring_guidelines/ files that are never @imported: {orphans}"


def test_no_orphans_in_claude_reference():
    """Every file in 04_claude_reference/ is imported."""
    orphans = orphans_in("04_claude_reference")
    assert not orphans, f"04_claude_reference/ files that are never @imported: {orphans}"


def test_no_broken_imports():
    """Every @import line in the always-on tree resolves to a real file."""
    broken = scan()[0]
    assert not broken, f"broken @import targets: {list(broken)}"


def test_lazy_load_tier_is_never_reported():
    """05_lazy_load/ is read on demand, so the scan never reports it as orphaned."""
    hits = [o for o in scan()[1] if "/05_lazy_load/" in o]
    assert not hits, f"05_lazy_load/ files leaked into the orphan report: {hits}"


def test_claude_md_imports_every_tier():
    """CLAUDE.md imports at least one file from each always-on tier."""
    text = CLAUDE_MD.read_text()
    missing = [t for t in ALWAYS_ON_TIERS if f"/_rules/{t}/" not in text]
    assert not missing, f"CLAUDE.md imports nothing from {missing}"


def test_lazy_load_children_are_pointed_to():
    """Every exempt per-parent _lazy_load/ child is named by a 'Read on demand' pointer."""
    rule_files = [p for t in ALWAYS_ON_TIERS for p in (RULES_DIR / t).rglob("*.md")]
    children = [p for p in rule_files if "_lazy_load" in p.relative_to(RULES_DIR).parts]
    assert children, "expected per-parent _lazy_load/ children in the always-on tiers"
    pointers = "\n".join(
        line for p in rule_files for line in p.read_text().splitlines() if "**Read on demand:**" in line
    )
    unnamed = sorted(str(c.relative_to(CLAUDE_DIR)) for c in children if str(c.relative_to(CLAUDE_DIR)) not in pointers)
    assert not unnamed, f"_lazy_load/ children no 'Read on demand' pointer names, so nothing loads them: {unnamed}"
    missing = sorted(set(re.findall(r"`~/[^/]+/(_rules/[^`]*/_lazy_load/[^`]+\.md)`", pointers)) - {
        str(c.relative_to(CLAUDE_DIR)) for c in children
    })
    assert not missing, f"'Read on demand' pointers to _lazy_load/ files that don't exist: {missing}"


def import_lines() -> list[str]:
    """List every @import target in the always-on tiers and CLAUDE.md.

    :return: Import paths with the ``@~/<config-dir>/`` prefix removed.
    :rtype: list[str]
    """
    files = [CLAUDE_MD] + [p for t in ALWAYS_ON_TIERS for p in (RULES_DIR / t).rglob("*.md")]
    return [m for f in files for m in re.findall(r"^@~/[^/\s]+/(\S+)$", f.read_text(), re.M)]


def test_claude_md_imports_aliases():
    """CLAUDE.md really imports aliases.md, which the scan otherwise treats as a starting point."""
    assert re.search(r"^@~/[^/\s]+/aliases\.md$", CLAUDE_MD.read_text(), re.M), "CLAUDE.md must @import aliases.md"


def test_nothing_imports_lazy_load_tier():
    """No always-on file imports from 05_lazy_load/, which loads only on demand."""
    bad = [i for i in import_lines() if i.startswith("_rules/05_lazy_load/")]
    assert not bad, f"always-on files import lazy-load rules: {bad}"


def test_nothing_imports_lazy_load_children():
    """No always-on file imports a per-parent _lazy_load/ child, which is read on demand."""
    bad = [i for i in import_lines() if "/_lazy_load/" in i]
    assert not bad, f"always-on files import _lazy_load/ children: {bad}"
