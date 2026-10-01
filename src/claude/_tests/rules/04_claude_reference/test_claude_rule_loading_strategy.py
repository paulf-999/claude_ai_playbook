# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-30
# Date updated:      2026-10-01
# Version:           1.1.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Drift tests for _rules/04_claude_reference/claude_rule_loading_strategy.md.

The rule's five-tier table describes the real ``_rules/`` layout. These tests
fail when the table and the folders on disk stop matching, or when the table's
example files, loading claims or key guidance quietly go stale.
"""
import re

from _shared_paths import CLAUDE_MD
from _shared_paths import RULES_DIR

RULE = RULES_DIR / "04_claude_reference" / "claude_rule_loading_strategy.md"

# A table row: | `01_essentials/` | ... | `example.md` | ... | Loading |
ROW_PATTERN = re.compile(
    r"^\| `(\d{2}_[a-z_]+)/` \|[^|]+\| `([^`]+)` \|[^|]+\| ([^|]+) \|$",
    re.MULTILINE,
)
# Matches any config-dir name (~/.claude/, ~/claude/, ...) per portable_paths.md.
IMPORT_PATTERN = re.compile(r"^@~/[^/]+/_rules/(\d{2}_[a-z_]+)/", re.MULTILINE)
LAZY_TIER = "05_lazy_load"
HEADER_LINES = 3
LINE_LIMIT = 110


def _content():
    """Return the rule file's text.

    :return: the full content of ``claude_rule_loading_strategy.md``
    """
    return RULE.read_text()


def _rows():
    """Return the tier table as ``(tier, example, loading)`` tuples.

    :return: one tuple per table row, in table order
    """
    return [
        (tier, example, loading.strip())
        for tier, example, loading in ROW_PATTERN.findall(_content())
    ]


def _tiers_on_disk():
    """Return the numbered tier folders under ``_rules/``.

    :return: sorted folder names such as ``01_essentials``
    """
    return sorted(
        path.name for path in RULES_DIR.iterdir()
        if path.is_dir() and re.match(r"^\d{2}_", path.name)
    )


def test_rule_file_exists():
    """The rule file must be present at its tier 04 path."""
    assert RULE.is_file(), f"Rule missing: {RULE}"


def test_table_has_five_rows():
    """The heading promises five tiers, so the table must have five rows."""
    assert "## 📁 The five tiers" in _content(), "'The five tiers' heading removed"
    assert len(_rows()) == 5, (
        f"Expected 5 tier rows, parsed {len(_rows())} — check the table format"
    )


def test_every_table_tier_exists_on_disk():
    """Every tier named in the table must be a real ``_rules/`` folder."""
    on_disk = set(_tiers_on_disk())
    for tier, _example, _loading in _rows():
        assert tier in on_disk, f"Table names tier '{tier}/' but no such folder exists"


def test_every_disk_tier_is_in_table():
    """Every numbered ``_rules/`` folder must have a row in the table."""
    in_table = {tier for tier, _example, _loading in _rows()}
    missing = set(_tiers_on_disk()) - in_table
    assert not missing, f"Tier folders missing from the table: {sorted(missing)}"


def test_table_tiers_in_numeric_order():
    """Table rows must list tiers in the same order as the folders."""
    tiers = [tier for tier, _example, _loading in _rows()]
    assert tiers == sorted(tiers), f"Tier rows out of order: {tiers}"


def test_example_files_exist():
    """Each row's example rule must exist inside that tier."""
    for tier, example, _loading in _rows():
        target = RULES_DIR / tier / example
        assert target.is_file(), (
            f"Example '{example}' for tier '{tier}/' no longer exists — update the table"
        )


def test_loading_column_matches_tier():
    """Tiers 01–04 must say always-on, and the lazy tier must say never imported."""
    for tier, _example, loading in _rows():
        if tier == LAZY_TIER:
            assert "never imported" in loading, f"{tier} loading should say never imported"
        else:
            assert loading.startswith("Always-on"), f"{tier} loading should start Always-on"


def test_always_on_tiers_are_imported_by_claude_md():
    """Every always-on tier must have at least one ``@import`` in CLAUDE.md."""
    imported = set(IMPORT_PATTERN.findall(CLAUDE_MD.read_text()))
    for tier, _example, _loading in _rows():
        if tier != LAZY_TIER:
            assert tier in imported, f"Always-on tier '{tier}' has no import in CLAUDE.md"
    assert LAZY_TIER not in imported, f"CLAUDE.md imports from {LAZY_TIER}, which the table forbids"


def test_pointers_resolve():
    """The README and per-parent ``_lazy_load/`` examples must point at real paths."""
    content = _content()
    assert "`_rules/README.md`" in content, "Pointer to _rules/README.md removed"
    assert (RULES_DIR / "README.md").is_file(), "_rules/README.md missing"
    assert "authoring_skills/_lazy_load/" in content, "Per-parent _lazy_load/ example removed"
    lazy_dir = RULES_DIR / "03_authoring_guidelines" / "authoring_skills" / "_lazy_load"
    assert lazy_dir.is_dir(), f"Per-parent _lazy_load/ example missing: {lazy_dir}"


def test_key_guidance_survives():
    """The lazy-by-default principle and its fallback must keep their wording."""
    content = _content()
    assert "Lazy-load by default" in content, "'Lazy-load by default' principle lost"
    assert "If unsure, lazy-load it" in content, "'If unsure, lazy-load it' fallback lost"


def test_placement_uses_measured_numbers():
    """Placement rests on the audit's applied % and each rule's miss_cost, not a guessed threshold."""
    content = _content()
    assert "70%" not in content, "the unmeasurable 70% threshold is back — use the audit's applied % instead"
    assert "**Applied %:**" in content, "applied % is no longer one of the placement inputs"
    assert "**Miss cost:**" in content, "miss_cost is no longer one of the placement inputs"
    assert "audit_rule_usage.md" in content, "the pointer to the usage report was removed"


def test_audit_flags_are_documented():
    """Each flag the audit sets is explained, so a report reader knows what to do."""
    content = _content()
    for flag in ("**Promote:**", "**Demote:**", "**Stale:**", "**Not enough data:**"):
        assert flag in content, f"the {flag} flag is no longer explained"


def test_adding_a_rule_runs_the_audit():
    """The 'When adding a rule' steps include the headers and an audit run."""
    steps = _content().split("## ➕ When adding a rule", 1)[1]
    assert "make audit_rule_usage" in steps, "adding a rule no longer runs the audit"
    assert "`applies_to` and `miss_cost`" in steps, "adding a rule no longer sets the usage headers"


def test_pointers_are_not_triggers():
    """A high-cost lazy rule needs a mechanical trigger, which test_rule_headers.py enforces."""
    assert "Pointers aren't triggers" in _content(), "the rule that pointers don't count as triggers was removed"


def test_line_limit():
    """The rule must stay within 110 lines, excluding the metadata header."""
    body = _content().splitlines()[HEADER_LINES:]
    assert len(body) <= LINE_LIMIT, f"{RULE.name}: {len(body)} lines exceeds {LINE_LIMIT}"


def test_ends_with_single_newline():
    """The rule must end with exactly one newline."""
    raw = RULE.read_bytes()
    assert raw.endswith(b"\n"), f"{RULE.name} does not end with a newline"
    assert not raw.endswith(b"\n\n"), f"{RULE.name} ends with multiple newlines"
