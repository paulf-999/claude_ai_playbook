# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-28
# Date updated:      2026-10-01
# Version:           2.1.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Structural tests for _rules/05_lazy_load/authoring_agents.md.

Verifies the agent authoring guide and its 5 child files are present and
well-formed. Filed after a 2026-09-28 rule audit found authoring_agents.md
had zero test coverage, unlike its two siblings in the same tier
(authoring_rules.md, authoring_skills.md). Moved to 05_lazy_load/ on
2026-09-29 to stay under Claude Code's 150k-char limit, then back to
03_authoring_guidelines/ on 2026-09-30 so agent work is detected. Moved to
05_lazy_load/ again on 2026-10-01, once ``paths:`` scoping proved it loads
whenever an agent file is read; it was used in 2 of 115 sessions. Its children
sit in `authoring_agents/_lazy_load/` and are only read on demand.
"""
from pathlib import Path

from _shared_paths import CLAUDE_DIR

TIER_DIR = CLAUDE_DIR / "_rules" / "05_lazy_load"
AUTHORING_RULES = CLAUDE_DIR / "_rules" / "03_authoring_guidelines" / "authoring_rules.md"
SCOPED_LINK = CLAUDE_DIR / "rules" / "authoring_agents.md"
AUTHORING_AGENTS = TIER_DIR / "authoring_agents.md"
CHILDREN_DIR = TIER_DIR / "authoring_agents" / "_lazy_load"
TIER_README = TIER_DIR / "README.md"

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


def test_parent_points_to_every_child_on_demand():
    """Every child must be named in one of the parent's `**Read on demand:**` pointers."""
    pointers = [
        line for line in AUTHORING_AGENTS.read_text().splitlines()
        if line.startswith("- **Read on demand:**")
    ]
    for child in EXPECTED_CHILDREN:
        assert any(f"authoring_agents/_lazy_load/{child}" in p for p in pointers), (
            f"authoring_agents.md has no read-on-demand pointer to: {child}"
        )


def test_parent_never_imports_a_child():
    """No child may be @imported — that would load it every session."""
    imports = [
        line for line in AUTHORING_AGENTS.read_text().splitlines()
        if line.lstrip().startswith("@") and "authoring_agents/" in line
    ]
    assert not imports, f"authoring_agents.md @imports a child it should read on demand: {imports}"


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
        entry = readme_related_entry(TIER_README, f"authoring_agents/_lazy_load/{child}")
        assert "authoring_agents.md" in entry, (
            f"{child}: 03_authoring_guidelines/README.md Related entry doesn't name "
            f"authoring_agents.md as its parent"
        )


def test_parent_loads_with_agent_files():
    """The agent guide loads through paths: whenever an agents/ file is read, not at startup."""
    text = AUTHORING_AGENTS.read_text()
    frontmatter = text.split("\n---", 1)[0] if text.startswith("---\n") else ""
    assert '"**/agents/**"' in frontmatter, "authoring_agents.md lost its paths: trigger for agents/**"
    # make install builds rules/ from paths: frontmatter, so only an installed config has the link
    if SCOPED_LINK.parent.is_dir():
        assert SCOPED_LINK.is_symlink(), "rules/authoring_agents.md symlink is missing, so paths: never loads"
        assert SCOPED_LINK.resolve() == AUTHORING_AGENTS.resolve(), "rules/authoring_agents.md points somewhere else"
    imports = [
        line.strip() for line in (CLAUDE_DIR / "CLAUDE.md").read_text().splitlines()
        if line.strip().startswith("@")
    ]
    assert not any(i.endswith("/authoring_agents.md") for i in imports), (
        "CLAUDE.md still @imports authoring_agents.md, so it loads every session"
    )


def test_always_on_pointer_exists():
    """authoring_rules.md's tier list must point readers to the agent guide's current home."""
    rules = AUTHORING_RULES.read_text()
    assert "05_lazy_load/authoring_agents.md" in rules, (
        "authoring_rules.md lost its pointer to 05_lazy_load/authoring_agents.md, needed for new agents"
    )
    assert "03_authoring_guidelines/authoring_agents.md" not in rules, (
        "authoring_rules.md still points to the old 03_authoring_guidelines/ location"
    )
