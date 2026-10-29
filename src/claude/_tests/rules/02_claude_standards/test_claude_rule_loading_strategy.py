# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-30
# Date updated:      2026-10-28
# Version:           4.0.2
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Drift tests for rules/02_claude_standards/path_scoped_rules/claude_rule_loading_strategy.md.

The rule's folder table describes the real ``rules/`` and ``_rules_lazy_load/`` layout. These tests
fail when the table and the folders on disk stop matching, or when the table's
example files or loading claims quietly go stale.
"""
import re

from _shared_paths import CLAUDE_DIR, LAZY_RULES_DIR, RULES_DIR, resolve_config_path

RULE = RULES_DIR / "02_claude_standards" / "path_scoped_rules" / "claude_rule_loading_strategy.md"

# A table row: | `01_essentials/` | ... | `example.md` | ... | Loading |
ROW_PATTERN = re.compile(
    r"^\| `(\d{2}_[a-z_]+(?:/[a-z_]+)?|_rules_lazy_load)/` \|[^|]+\| `([^`]+)` \|[^|]+\| ([^|]+) \|$",
    re.MULTILINE,
)
LAZY_FOLDER = "_rules_lazy_load"
PATH_SCOPED_TIER = "02_claude_standards/path_scoped_rules"
# paths: frontmatter (7 lines) + version, created, updated, miss_cost, loading
HEADER_LINES = 12
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
    """The rule file must be present in path_scoped_rules/."""
    assert RULE.is_file(), f"Rule missing: {RULE}"


def test_table_has_five_rows():
    """The heading promises five folders, so the table must have five rows."""
    assert "## 📁 The five rule folders" in _content(), (  # wording-check: heading states the row count
        "'The five rule folders' heading removed"
    )
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
        # Map the installed path, since the repo keeps style guides in their own folder
        target = resolve_config_path(CLAUDE_DIR, f"{tier if tier == LAZY_FOLDER else f'rules/{tier}'}/{example}")
        assert target.is_file(), (
            f"Example '{example}' for tier '{tier}/' no longer exists — update the table"
        )


def test_loading_column_matches_tier():
    """Tiers 01–03 say always-on, path_scoped_rules/ says path-scoped, and the lazy folder says never automatic."""
    for tier, _example, loading in _rows():
        if tier == LAZY_FOLDER:
            assert "never loaded automatically" in loading, (  # wording-check: cell checked against its tier
                f"{tier} loading should say never loaded automatically"
            )
        elif tier == PATH_SCOPED_TIER:
            assert loading.startswith("Path-scoped"), f"{tier} loading should start Path-scoped"
        else:
            assert loading.startswith("Always-on"), f"{tier} loading should start Always-on"


def test_pointers_resolve():
    """The on-demand children example must point at a real folder."""
    content = _content()
    children_pointer = "`_rules_lazy_load/authoring_guidelines_lazy_load/authoring_skills/`"
    assert children_pointer in content, "On-demand children example removed"
    children_example = LAZY_RULES_DIR / "authoring_guidelines_lazy_load" / "authoring_skills"
    assert children_example.is_dir(), "On-demand children example folder is missing"


def test_line_limit():
    """The rule must stay within 110 lines, excluding the metadata header."""
    body = _content().splitlines()[HEADER_LINES:]
    assert len(body) <= LINE_LIMIT, f"{RULE.name}: {len(body)} lines exceeds {LINE_LIMIT}"


def test_ends_with_single_newline():
    """The rule must end with exactly one newline."""
    raw = RULE.read_bytes()
    assert raw.endswith(b"\n"), f"{RULE.name} does not end with a newline"
    assert not raw.endswith(b"\n\n"), f"{RULE.name} ends with multiple newlines"
