# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 9/10
# Date created:      2026-08-28
# Version:           1.0.0
# Date updated:      2026-09-17
# ─────────────────────────────────────────────────────────

"""Tests for _rules/ directory structure and content standards.

Verifies the design goals for the _rules/ layout in the configured Claude directory:
- Human-readable files at root, Claude-specific internals in claude_internal/
- All @import paths resolve to real files
- File quality standards (line limits, H1 headings, trailing newlines)
- CLAUDE.md import priority order
"""
import re
from pathlib import Path

from _claude_dir import CLAUDE_DIR

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

# CLAUDE.md's _rules/ imports must appear in ascending tier order (01 before 02 before 03 before 04).
# Tier-based rather than a fixed filename list, so adding/removing files within a tier
# never requires updating this test — only a tier reassignment would.
TIER_ORDER = [
    "01_essentials",
    "02_claude_standards",
    "03_authoring_guidelines",
    "04_claude_reference",
]


def extract_import_paths(md_file: Path) -> list[Path]:
    """Return resolved paths for all @import lines in a markdown file.

    Detects any "@~/<config-dir-name>/" prefix generically (.claude, claude, a
    repo checkout) rather than hardcoding one convention — see portable_paths.md.

    :param md_file: The markdown file to parse for import lines.
    :type md_file: Path
    :return: Resolved file paths corresponding to each @-import line found.
    :rtype: list[Path]
    """
    paths = []
    for line in md_file.read_text().splitlines():
        stripped = line.strip()
        if not stripped.startswith("@~/") or "/" not in stripped[len("@~/"):]:
            continue
        rest = stripped[len("@~/"):].split("/", 1)[1]
        paths.append(CLAUDE_DIR / rest)
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
    """aliases.md must exist at the Claude directory root, not inside _rules/."""
    assert (CLAUDE_DIR / "aliases.md").exists(), f"aliases.md missing from {CLAUDE_DIR} root"
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
    """CLAUDE.md's _rules/ imports must appear in ascending tier order (01 → 02 → 03 → 04)."""
    content = CLAUDE_MD.read_text()
    tier_sequence = []
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped.startswith("@~/") or "/" not in stripped[len("@~/"):]:
            continue
        # "@~/<config-dir-name>/_rules/<tier>/..." — skip both leading segments
        # generically (see portable_paths.md), then require a _rules/ import.
        after_config_dir = stripped[len("@~/"):].split("/", 1)[1]
        if not after_config_dir.startswith("_rules/"):
            continue
        tier = after_config_dir[len("_rules/"):].split("/")[0]
        if tier in TIER_ORDER:
            tier_sequence.append(tier)

    tier_positions = [TIER_ORDER.index(t) for t in tier_sequence]
    assert tier_positions == sorted(tier_positions), (
        f"CLAUDE.md _rules/ imports out of tier order — expected ascending {TIER_ORDER}, "
        f"found sequence: {tier_sequence}"
    )
