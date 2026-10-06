# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-30
# Date updated:      2026-10-06
# Version:           2.1.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Drift tests for rules/04_path_scoped/claude_rule_loading_strategy.md.

The rule's folder table describes the real ``rules/`` and ``_rules_lazy_load/`` layout. These tests
fail when the table and the folders on disk stop matching, or when the table's
example files, loading claims or key guidance quietly go stale.
"""
import re

from _shared_paths import CLAUDE_MD, LAZY_RULES_DIR, RULES_DIR

RULE = RULES_DIR / "04_path_scoped" / "claude_rule_loading_strategy.md"

# A table row: | `01_essentials/` | ... | `example.md` | ... | Loading |
ROW_PATTERN = re.compile(
    r"^\| `(\d{2}_[a-z_]+|_rules_lazy_load)/` \|[^|]+\| `([^`]+)` \|[^|]+\| ([^|]+) \|$",
    re.MULTILINE,
)
# Matches any config-dir name (~/.claude/, ~/claude/, ...) per portable_paths.md.
IMPORT_PATTERN = re.compile(r"^@~/[^/]+/(_?rules\S*)$", re.MULTILINE)
LAZY_FOLDER = "_rules_lazy_load"
PATH_SCOPED_TIER = "04_path_scoped"
# paths: frontmatter (5 lines) + version, created, updated, miss_cost
HEADER_LINES = 9
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
    """Return the numbered tier folders under ``rules/``.

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
    """The heading promises five folders, so the table must have five rows."""
    assert "## 📁 The five rule folders" in _content(), "'The five rule folders' heading removed"
    assert len(_rows()) == 5, (
        f"Expected 5 folder rows, parsed {len(_rows())} — check the table format"
    )


def folder(tier: str):
    """Return the folder a table row names: a rules/ tier, or the lazy folder beside rules/."""
    return LAZY_RULES_DIR if tier == LAZY_FOLDER else RULES_DIR / tier


def test_every_table_tier_exists_on_disk():
    """Every folder named in the table must exist."""
    for tier, _example, _loading in _rows():
        assert folder(tier).is_dir(), f"Table names '{tier}/' but no such folder exists"


def test_every_disk_tier_is_in_table():
    """Every numbered ``rules/`` folder must have a row in the table."""
    in_table = {tier for tier, _example, _loading in _rows()}
    missing = set(_tiers_on_disk()) - in_table
    assert not missing, f"Tier folders missing from the table: {sorted(missing)}"


def test_table_tiers_in_numeric_order():
    """Table rows must list the numbered tiers in folder order, with the lazy folder last."""
    tiers = [tier for tier, _example, _loading in _rows()]
    assert tiers[-1] == LAZY_FOLDER, f"{LAZY_FOLDER}/ should be the last row: {tiers}"
    tiers = tiers[:-1]
    assert tiers == sorted(tiers), f"Tier rows out of order: {tiers}"


def test_example_files_exist():
    """Each row's example rule must exist inside that tier."""
    for tier, example, _loading in _rows():
        target = folder(tier) / example
        assert target.is_file(), (
            f"Example '{example}' for tier '{tier}/' no longer exists — update the table"
        )


def test_loading_column_matches_tier():
    """Tiers 01–03 say always-on, 04_path_scoped/ says path-scoped, and the lazy folder says never automatic."""
    for tier, _example, loading in _rows():
        if tier == LAZY_FOLDER:
            assert "never loaded automatically" in loading, f"{tier} loading should say never loaded automatically"
        elif tier == PATH_SCOPED_TIER:
            assert loading.startswith("Path-scoped"), f"{tier} loading should start Path-scoped"
        else:
            assert loading.startswith("Always-on"), f"{tier} loading should start Always-on"


def test_claude_md_imports_no_rules():
    """Rules load natively from rules/, so CLAUDE.md imports none, as the table says."""
    imported = IMPORT_PATTERN.findall(CLAUDE_MD.read_text())
    assert not imported, f"CLAUDE.md imports rules the native loader already loads: {imported}"


def test_pointers_resolve():
    """The overview README and on-demand children examples must point at real paths."""
    content = _content()
    assert "`_rules_lazy_load/_tier_readmes/00_rules_overview.md`" in content, "Pointer to the rules overview removed"
    assert (LAZY_RULES_DIR / "_tier_readmes" / "00_rules_overview.md").is_file(), "the rules overview is missing"
    assert "`_rules_lazy_load/authoring_skills/`" in content, "On-demand children example removed"
    assert (LAZY_RULES_DIR / "authoring_skills").is_dir(), "On-demand children example folder is missing"


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


def test_paths_guidance_survives():
    """The 'When paths: fits' guidance keeps its four conditions, so path-scoping decisions stay checkable."""
    content = RULE.read_text()
    assert "## 🎯 When `paths:` fits" in content, "the path-scoping section is missing"
    assert "**Clear file type:**" in content, "the file-type condition is missing"
    assert "**Read before write:**" in content, "the read-before-write condition is missing"
    assert "**New-file gap:**" in content, "the new-file pointer advice is missing"
    assert "**Backstop for high cost:**" in content, "the high-cost backstop condition is missing"


def test_paths_trial_outcome_is_recorded():
    """The path-scoping decision keeps its evidence and its exception, and the evidence file exists."""
    content = RULE.read_text()
    assert "**Proven:** `test_path_scoped_rules_live.py`" in content, "the live evidence for paths: is missing"
    assert "**Stays pointer-based:**" in content, "the pointer-based exception is missing"
    live = RULES_DIR.parent / "_tests" / "rules" / "05_lazy_load" / "test_path_scoped_rules_live.py"
    assert live.is_file(), "the live test named as evidence no longer exists"
