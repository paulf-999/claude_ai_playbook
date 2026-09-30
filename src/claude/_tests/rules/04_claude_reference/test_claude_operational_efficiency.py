# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# Date created:      2026-09-30
# Version:           1.0.0
# Date updated:      2026-09-30
# ─────────────────────────────────────────────────────────

"""Content-regression tests for _rules/04_claude_reference/claude_operational_efficiency.md.

Tier 04 is instructional, so these tests don't prove compliance. They catch
a section, child import or key phrase that gets silently dropped in an edit,
since the rule's four children moved into a subfolder on 2026-09-30.
"""
import re

from _shared_paths import RULES_DIR

TIER_DIR = RULES_DIR / "04_claude_reference"
RULE = TIER_DIR / "claude_operational_efficiency.md"
CHILD_DIR = TIER_DIR / "claude_operational_efficiency"

EXPECTED_SECTIONS = [
    "Token awareness",
    "Default behaviours",
    "When to delegate",
    "Turn budgets",
    "Intervention mode",
    "External system access",
    "Task request conventions",
    "MCP server toggling",
]

EXPECTED_CHILDREN = {
    "_claude_when_to_delegate.md",
    "_external_system_access.md",
    "_task_request_conventions.md",
    "_mcp_server_toggling.md",
}

# Matches any config-dir name (~/.claude/, ~/claude/, ...) per portable_paths.md.
IMPORT_PATTERN = re.compile(r"^@~/[^/]+/_rules/(\S+)$", re.MULTILINE)
HEADER_LINES = 3
LINE_LIMIT = 110


def _content():
    """Return the rule file's text.

    :return: the full content of ``claude_operational_efficiency.md``
    """
    return RULE.read_text()


def _imports():
    """Return every ``@``-import in the rule, relative to ``_rules/``.

    :return: import paths such as ``04_claude_reference/.../_x.md``
    """
    return IMPORT_PATTERN.findall(_content())


def _headings():
    """Return the text of every ``##`` heading, emoji stripped.

    :return: heading titles such as ``Token awareness``
    """
    raw = re.findall(r"^## (.+)$", _content(), re.MULTILINE)
    return [re.sub(r"^[^\w]+", "", heading).strip() for heading in raw]


def test_rule_file_exists():
    """The rule file must be present at its tier 04 path."""
    assert RULE.is_file(), f"Rule missing: {RULE}"


def test_child_directory_exists():
    """The children must live in a subfolder named after the parent."""
    assert CHILD_DIR.is_dir(), f"Child folder missing: {CHILD_DIR}"


def test_expected_sections_present():
    """Each of the 8 expected sections must keep its ``##`` heading."""
    headings = _headings()
    for section in EXPECTED_SECTIONS:
        assert section in headings, (
            f"Section '{section}' missing from {RULE.name} — restore its ## heading"
        )


def test_exactly_four_child_imports():
    """The rule must import exactly its 4 children, with no duplicates."""
    imports = _imports()
    names = [path.rsplit("/", 1)[-1] for path in imports]
    assert len(imports) == len(EXPECTED_CHILDREN), (
        f"Expected {len(EXPECTED_CHILDREN)} @imports, found {len(imports)}: {names}"
    )
    assert set(names) == EXPECTED_CHILDREN, (
        f"Child imports drifted — missing {EXPECTED_CHILDREN - set(names)}, "
        f"unexpected {set(names) - EXPECTED_CHILDREN}"
    )


def test_child_imports_resolve_inside_child_directory():
    """Every import must point at an existing file in the child folder."""
    for path in _imports():
        target = RULES_DIR / path
        assert target.is_file(), f"@import does not resolve: {path}"
        assert target.parent == CHILD_DIR, (
            f"@import {path} points outside {CHILD_DIR.name}/"
        )


def test_no_orphaned_children():
    """Every ``.md`` file in the child folder must be imported by the parent."""
    imported = {path.rsplit("/", 1)[-1] for path in _imports()}
    on_disk = {child.name for child in CHILD_DIR.glob("*.md")}
    orphans = on_disk - imported
    assert not orphans, (
        f"Children never imported (silently unreachable): {sorted(orphans)}"
    )


def test_children_use_underscore_prefix():
    """Child files must start with ``_`` per the directory naming standard."""
    for child in CHILD_DIR.glob("*.md"):
        assert child.name.startswith("_"), f"Child file lacks _ prefix: {child.name}"


def test_turn_budgets_pointer_resolves():
    """The turn budgets section must point at an existing lazy-load file."""
    content = _content()
    assert "**Read on demand:**" in content, "Turn budgets read-on-demand pointer removed"
    assert "05_lazy_load/turn_budgets.md" in content, (
        "Turn budgets pointer no longer names 05_lazy_load/turn_budgets.md"
    )
    target = RULES_DIR / "05_lazy_load" / "turn_budgets.md"
    assert target.is_file(), f"Turn budgets pointer target missing: {target}"


def test_key_phrases_survive():
    """The sub-agent and intervention guidance must keep their core wording."""
    content = _content()
    assert "context isolation" in content, "Sub-agent 'context isolation' justification lost"
    assert "Flag, don't block" in content, "Intervention mode 'Flag, don't block' lost"


def test_contents_entries_match_headings():
    """Every Contents entry must name a real ``##`` heading."""
    entries = re.findall(r"^- \[([^\]]+)\]\(#", _content(), re.MULTILINE)
    assert entries, "Contents section has no entries"
    headings = _headings()
    for entry in entries:
        assert entry in headings, f"Contents entry '{entry}' has no matching ## heading"


def test_line_limit():
    """The rule must stay within 110 lines, excluding the metadata header."""
    body = _content().splitlines()[HEADER_LINES:]
    assert len(body) <= LINE_LIMIT, (
        f"{RULE.name}: {len(body)} lines exceeds {LINE_LIMIT} — split into more children"
    )


def test_ends_with_single_newline():
    """The rule must end with exactly one newline."""
    raw = RULE.read_bytes()
    assert raw.endswith(b"\n"), f"{RULE.name} does not end with a newline"
    assert not raw.endswith(b"\n\n"), f"{RULE.name} ends with multiple newlines"
