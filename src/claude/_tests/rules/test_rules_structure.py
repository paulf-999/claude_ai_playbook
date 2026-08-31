"""Tests for _rules/ directory structure and content standards.

Verifies the design goals for the ~/.claude/_rules/ layout:
- Human-readable files at root, Claude-specific internals in claude_internal/
- All @import paths resolve to real files
- File quality standards (line limits, H1 headings, trailing newlines)
- CLAUDE.md import priority order
"""
import re
from pathlib import Path

CLAUDE_DIR = Path.home() / ".claude"
RULES_DIR = CLAUDE_DIR / "_rules"
CLAUDE_MD = CLAUDE_DIR / "CLAUDE.md"

# Human-readable theme files permitted at _rules/ root — no others allowed
EXPECTED_ROOT_FILES = {
    "behaviour.md",
    "naming_standards.md",
    "security.md",
    "writing_style.md",
    "README.md",
}

# Claude Code-specific files expected in claude_internal/ — no others allowed
EXPECTED_INTERNAL_FILES = {
    "automation_controls.md",
    "claude_efficiency.md",
    "git.md",
    "memory.md",
    "security_guardrails.md",
}

# Paths removed during the 2026-08 restructure that must never reappear
DISSOLVED_PATHS = [
    RULES_DIR / "behaviour" / "general.md",
    RULES_DIR / "behaviour" / "risky_actions.md",
    RULES_DIR / "behaviour" / "memory.md",
    RULES_DIR / "behaviour" / "git.md",
    RULES_DIR / "security_guardrails.md",
    RULES_DIR / "git.md",
    RULES_DIR / "optimisation.md",
    RULES_DIR / "aliases.md",
    RULES_DIR / "lazy_load" / "security.md",
    RULES_DIR / "lazy_load" / "speculative_features.md",
    RULES_DIR / "lazy_load" / "style_guide_standards" / "payroc_engineering_naming_standards.md",
    RULES_DIR / "speculative_features.md",
    RULES_DIR / "claude_internal.md",
]

# Imports in CLAUDE.md must appear in this exact priority order
EXPECTED_IMPORT_ORDER = [
    "MEMORY.md",
    "behaviour.md",
    "security.md",
    "claude_efficiency.md",
    "automation_controls.md",
    "memory.md",
    "security_guardrails.md",
    "git.md",
    "writing_style.md",
    "naming_standards.md",
    "aliases.md",
]


def extract_import_paths(md_file: Path) -> list[Path]:
    """Return resolved paths for all @~/.claude/ imports in a markdown file.

    :param md_file: The markdown file to parse for import lines.
    :type md_file: Path
    :return: Resolved file paths corresponding to each @-import line found.
    :rtype: list[Path]
    """
    paths = []
    for line in md_file.read_text().splitlines():
        stripped = line.strip()
        if stripped.startswith("@~/.claude/"):
            paths.append(Path(stripped[1:]).expanduser())
    return paths


def rule_files() -> list[Path]:
    """Return all .md files in _rules/ eligible for quality checks.

    Excludes README.md (documentation, not a rule file) and anything
    under lazy_load/ (different standards apply there).

    :return: List of rule markdown files to validate.
    :rtype: list[Path]
    """
    return [
        f for f in RULES_DIR.rglob("*.md")
        if f.name != "README.md" and "lazy_load" not in f.parts
    ]


# --- Import resolution ---

def test_all_imports_resolve():
    """Every @import path in any ~/.claude/ .md file must point to a real file."""
    for md_file in CLAUDE_DIR.rglob("*.md"):
        if "lazy_load" in md_file.parts:
            continue
        for path in extract_import_paths(md_file):
            assert path.exists(), (
                f"{md_file.relative_to(CLAUDE_DIR)}: unresolved import → {path}"
            )


# --- Structure ---

def test_rules_root_contains_only_expected_files():
    """_rules/ root must only contain human-readable theme files."""
    actual = {f.name for f in RULES_DIR.iterdir() if f.is_file()}
    assert actual == EXPECTED_ROOT_FILES, (
        f"_rules/ root mismatch — expected: {EXPECTED_ROOT_FILES}, got: {actual}"
    )


def test_claude_internal_contains_expected_files():
    """02_claude_internal/ must contain exactly the expected files."""
    internal_dir = RULES_DIR / "02_claude_internal"
    actual = {f.name for f in internal_dir.iterdir() if f.is_file()}
    assert actual == EXPECTED_INTERNAL_FILES, (
        f"claude_internal/ mismatch — expected: {EXPECTED_INTERNAL_FILES}, got: {actual}"
    )


def test_aliases_at_claude_root():
    """aliases.md must exist at ~/.claude/ root, not inside _rules/."""
    assert (CLAUDE_DIR / "aliases.md").exists(), "aliases.md missing from ~/.claude/ root"
    assert not (RULES_DIR / "aliases.md").exists(), "aliases.md must not be inside _rules/"


def test_behaviour_subdir_dissolved():
    """_rules/behaviour/ subdir was dissolved and must not exist."""
    assert not (RULES_DIR / "behaviour").is_dir(), "_rules/behaviour/ should not exist"


def test_dissolved_paths_absent():
    """Paths removed during restructure must not reappear."""
    for path in DISSOLVED_PATHS:
        assert not path.exists(), f"Dissolved path has reappeared: {path}"


# --- File quality ---

def test_line_limits():
    """No _rules/ file (excluding README and lazy_load) may exceed 110 lines."""
    for f in rule_files():
        lines = f.read_text().splitlines()
        assert len(lines) <= 110, f"{f.name}: {len(lines)} lines exceeds 110-line limit"


def test_h1_heading_present():
    """Every _rules/ file must have an H1 heading."""
    for f in rule_files():
        assert re.search(r"^# .+", f.read_text(), re.MULTILINE), (
            f"{f.name}: missing H1 heading"
        )


def test_h1_heading_has_emoji():
    """Every _rules/ file H1 heading must include an emoji."""
    for f in rule_files():
        content = f.read_text()
        h1_match = re.search(r"^# (.+)", content, re.MULTILINE)
        assert h1_match, f"{f.name}: missing H1 heading"
        heading_text = h1_match.group(1)
        has_non_ascii = any(ord(c) > 127 for c in heading_text)
        assert has_non_ascii, f"{f.name}: H1 heading has no emoji — got: '# {heading_text}'"


def test_files_end_with_single_newline():
    """Every _rules/ file must end with exactly one newline."""
    for f in rule_files():
        raw = f.read_bytes()
        assert raw.endswith(b"\n"), f"{f.name}: does not end with a newline"
        assert not raw.endswith(b"\n\n"), f"{f.name}: ends with multiple newlines"


# --- Import order ---

def test_claude_md_import_order():
    """CLAUDE.md imports must appear in the defined priority order."""
    content = CLAUDE_MD.read_text()
    import_names = [
        Path(line.strip()[1:]).expanduser().name
        for line in content.splitlines()
        if line.strip().startswith("@~/.claude/")
    ]
    positions = []
    for name in EXPECTED_IMPORT_ORDER:
        assert name in import_names, f"Expected import missing from CLAUDE.md: {name}"
        positions.append(import_names.index(name))
    assert positions == sorted(positions), (
        f"CLAUDE.md imports out of priority order — expected: {EXPECTED_IMPORT_ORDER}, "
        f"found sequence: {import_names}"
    )
