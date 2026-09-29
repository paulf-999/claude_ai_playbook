# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# Date created:      2026-09-28
# Version:           1.2.0
# Date updated:      2026-09-29
# ─────────────────────────────────────────────────────────

"""Structural tests for _rules/05_lazy_load/authoring_agents.md.

Verifies the agent authoring guide and its 5 child files are present and
well-formed. Filed after a 2026-09-28 rule audit found authoring_agents.md
had zero test coverage, unlike its two siblings in the same tier
(authoring_rules.md, authoring_skills.md). Moved to 05_lazy_load/ on
2026-09-29 to bring always-on instructions under Claude Code's 150k-char
limit; test_parent_is_not_always_on guards against it being re-imported.
"""
from pathlib import Path

from _shared_paths import CLAUDE_DIR

AUTHORING_AGENTS = CLAUDE_DIR / "_rules" / "05_lazy_load" / "authoring_agents.md"
CHILDREN_DIR = CLAUDE_DIR / "_rules" / "05_lazy_load" / "authoring_agents"
TIER_README = CLAUDE_DIR / "_rules" / "05_lazy_load" / "README.md"

EXPECTED_SECTIONS = [
    "Quick Navigation",
    "Core Standards",
    "Decision Tree",
    "Scope Boundaries",
    "Hard Gates Checklist",
    "Common Mistakes",
]

EXPECTED_PATTERNS = [
    "Naming pattern",
    "maturity levels",
    "Decision Tree",
    "Scope Boundaries",
    "Hard Gates Checklist",
]

EXPECTED_CHILDREN = [
    "_core_standards.md",
    "_decision_tree_and_process.md",
    "_scope_and_maturity.md",
    "_hard_gates_checklist.md",
    "_common_mistakes.md",
]



def readme_related_entry(readme: Path, rel_path: str) -> str:
    """Return one file's block from a tier README's "🔗 Related rules" section.

    Related links moved out of rule files into tier READMEs (#121), so each
    file's parent/sibling links now live under a ``### `<rel_path>` `` heading.

    :param readme: The tier README holding the Related rules section.
    :type readme: Path
    :param rel_path: The rule's path relative to the README's directory.
    :type rel_path: str
    :return: The block's text, or an empty string if the heading is absent.
    :rtype: str
    """
    lines = readme.read_text().splitlines()
    heading = f"### `{rel_path}`"
    if heading not in lines:
        return ""
    start = lines.index(heading) + 1
    end = next(
        (idx for idx in range(start, len(lines)) if lines[idx].startswith(("### ", "## "))),
        len(lines),
    )
    return "\n".join(lines[start:end])


def test_authoring_agents_file_exists():
    """authoring_agents.md must be present at the expected path."""
    assert AUTHORING_AGENTS.exists(), f"authoring_agents.md missing: {AUTHORING_AGENTS}"


def test_authoring_agents_has_expected_sections():
    """authoring_agents.md must contain all required section headings."""
    content = AUTHORING_AGENTS.read_text()
    for section in EXPECTED_SECTIONS:
        assert section.lower() in content.lower(), (
            f"authoring_agents.md missing expected section: '{section}'"
        )


def test_authoring_agents_contains_key_patterns():
    """authoring_agents.md must reference its own core concepts by name."""
    content = AUTHORING_AGENTS.read_text()
    for pattern in EXPECTED_PATTERNS:
        assert pattern.lower() in content.lower(), (
            f"authoring_agents.md missing expected pattern: '{pattern}'"
        )


def test_authoring_agents_line_limit():
    """authoring_agents.md must not exceed 110 lines."""
    lines = AUTHORING_AGENTS.read_text().splitlines()
    assert len(lines) <= 110, f"authoring_agents.md: {len(lines)} lines exceeds 110-line limit"


def test_authoring_agents_ends_with_newline():
    """authoring_agents.md must end with exactly one newline."""
    raw = AUTHORING_AGENTS.read_bytes()
    assert raw.endswith(b"\n"), "authoring_agents.md does not end with a newline"
    assert not raw.endswith(b"\n\n"), "authoring_agents.md ends with multiple newlines"


def test_authoring_agents_imports_every_declared_child():
    """Every file the parent's Quick Navigation names must have a real @import line."""
    content = AUTHORING_AGENTS.read_text()
    for child in EXPECTED_CHILDREN:
        assert f"authoring_agents/{child}" in content, (
            f"authoring_agents.md does not @import its declared child: {child}"
        )


def test_all_expected_children_exist_on_disk():
    """Every child file named in the parent must actually exist on disk."""
    for child in EXPECTED_CHILDREN:
        child_path = CHILDREN_DIR / child
        assert child_path.exists(), f"Declared child file missing on disk: {child_path}"


def test_no_undeclared_children_on_disk():
    """The children directory must not contain files the parent never mentions."""
    actual = {p.name for p in CHILDREN_DIR.glob("*.md")}
    assert actual == set(EXPECTED_CHILDREN), (
        f"authoring_agents/ has a mismatch between files on disk and declared "
        f"children: on disk only={actual - set(EXPECTED_CHILDREN)}, "
        f"declared only={set(EXPECTED_CHILDREN) - actual}"
    )


def test_each_child_has_an_emoji_h1():
    """Every child file must open with an emoji-prefixed H1 (after any metadata header)."""
    for child in EXPECTED_CHILDREN:
        lines = (CHILDREN_DIR / child).read_text().splitlines()
        # Skip the metadata header, if present — see _claude_config_metadata.md
        first_line = lines[3] if lines[0].startswith("<!-- version:") else lines[0]
        assert first_line.startswith("# "), f"{child}: first line is not an H1: {first_line!r}"
        assert len(first_line) > 2 and not first_line[2].isalnum(), (
            f"{child}: H1 does not appear to start with an emoji: {first_line!r}"
        )


def test_each_child_has_a_purpose_statement():
    """Every child file must state its purpose near the top, per writing_style.md."""
    for child in EXPECTED_CHILDREN:
        content = (CHILDREN_DIR / child).read_text()
        assert "**Purpose:**" in content, f"{child}: missing a '**Purpose:**' statement"


def test_each_child_ends_with_newline():
    """Every child file must end with exactly one newline."""
    for child in EXPECTED_CHILDREN:
        raw = (CHILDREN_DIR / child).read_bytes()
        assert raw.endswith(b"\n"), f"{child}: does not end with a newline"
        assert not raw.endswith(b"\n\n"), f"{child}: ends with multiple newlines"


def test_each_child_links_back_to_parent():
    """Every child's tier README Related entry must name authoring_agents.md as its parent."""
    for child in EXPECTED_CHILDREN:
        entry = readme_related_entry(TIER_README, f"authoring_agents/{child}")
        assert "authoring_agents.md" in entry, (
            f"{child}: 05_lazy_load/README.md Related entry doesn't name "
            f"authoring_agents.md as its parent"
        )


def test_parent_is_not_always_on():
    """CLAUDE.md must not @import the agent guide — it is read on demand only."""
    claude_md = (CLAUDE_DIR / "CLAUDE.md").read_text()
    assert "authoring_agents.md" not in claude_md, (
        "CLAUDE.md imports authoring_agents.md — it was moved to 05_lazy_load/ "
        "to stay under the 150k always-on char limit; remove the import"
    )


def test_always_on_pointer_exists():
    """authoring_rules.md (always-on) must point readers to the lazy-loaded agent guide."""
    rules = (CLAUDE_DIR / "_rules" / "03_authoring_guidelines" / "authoring_rules.md").read_text()
    assert "05_lazy_load/authoring_agents.md" in rules, (
        "authoring_rules.md lost its read-on-demand pointer to "
        "05_lazy_load/authoring_agents.md — agents would become undiscoverable"
    )
