# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 9/10
# Test complexity score: 4/10
# Python style compliant: Yes
# Date created:      2026-08-28
# Version:           1.4.1
# Date updated:      2026-09-30
# ─────────────────────────────────────────────────────────

"""Tests for _rules/ directory structure and content standards.

Verifies the design goals for the _rules/ layout in the configured Claude directory:
- Human-readable files at root, Claude-specific internals in claude_internal/
- All @import paths resolve to real files
- File quality standards (line limits, H1 headings, trailing newlines)
- CLAUDE.md import priority order
- No always-on bloat: no Related sections, Contents only when earned
- _reference/ is never reached from CLAUDE.md's import graph
"""
import re
from pathlib import Path
from typing import Optional

from _shared_paths import CLAUDE_DIR, CLAUDE_MD, RULES_DIR

# Human-readable theme files permitted at _rules/ root — no others allowed
EXPECTED_ROOT_FILES = {
    "README.md",
}

# Claude Code-specific files expected in claude_internal/ — no others allowed
EXPECTED_CLAUDE_REFERENCE_FILES = {
    "claude_operational_efficiency.md",
    "claude_rule_loading_strategy.md",
    "README.md",
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
    under 05_lazy_load/ (different standards apply there).

    :return: List of rule markdown files to validate.
    :rtype: list[Path]
    """
    return [
        rule_file for rule_file in RULES_DIR.rglob("*.md")
        if rule_file.name != "README.md" and "05_lazy_load" not in rule_file.parts
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
    """_rules/ root must contain nothing but README.md — all rules live in tier subdirectories."""
    actual = {rule_file.name for rule_file in RULES_DIR.iterdir() if rule_file.is_file()}
    assert actual == EXPECTED_ROOT_FILES, (
        f"_rules/ root mismatch — expected: {EXPECTED_ROOT_FILES}, got: {actual}"
    )


def test_claude_reference_contains_expected_files():
    """04_claude_reference/ top level must contain exactly the expected files.

    02_claude_internal/ (this test's original target) was retired across two
    reorgs — its contents were redistributed: git.md -> 02_claude_standards/,
    claude_efficiency.md -> renamed and consolidated here as
    claude_operational_efficiency.md, automation_controls.md -> 05_lazy_load/,
    memory.md / security_guardrails.md -> folded into other files.
    """
    reference_dir = RULES_DIR / "04_claude_reference"
    actual = {rule_file.name for rule_file in reference_dir.iterdir() if rule_file.is_file()}
    assert actual == EXPECTED_CLAUDE_REFERENCE_FILES, (
        f"04_claude_reference/ mismatch — expected: {EXPECTED_CLAUDE_REFERENCE_FILES}, got: {actual}"
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
    """No _rules/ file (excluding README and lazy_load) may exceed 110 lines.

    The 3-line metadata header doesn't count — see _claude_config_metadata.md.
    """
    for rule_file in rule_files():
        lines = rule_file.read_text().splitlines()
        if lines and lines[0].startswith("<!-- version:"):
            lines = lines[3:]
        assert len(lines) <= 110, f"{rule_file.name}: {len(lines)} lines exceeds 110-line limit"


def test_h1_heading_present():
    """Every _rules/ file must have an H1 heading."""
    for rule_file in rule_files():
        assert re.search(r"^# .+", rule_file.read_text(), re.MULTILINE), (
            f"{rule_file.name}: missing H1 heading"
        )


def test_h1_heading_has_emoji():
    """Every _rules/ file H1 heading must include an emoji."""
    for rule_file in rule_files():
        content = rule_file.read_text()
        h1_match = re.search(r"^# (.+)", content, re.MULTILINE)
        assert h1_match, f"{rule_file.name}: missing H1 heading"
        heading_text = h1_match.group(1)
        has_non_ascii = any(ord(char) > 127 for char in heading_text)
        assert has_non_ascii, f"{rule_file.name}: H1 heading has no emoji — got: '# {heading_text}'"


def test_files_end_with_single_newline():
    """Every _rules/ file must end with exactly one newline."""
    for rule_file in rule_files():
        raw = rule_file.read_bytes()
        assert raw.endswith(b"\n"), f"{rule_file.name}: does not end with a newline"
        assert not raw.endswith(b"\n\n"), f"{rule_file.name}: ends with multiple newlines"


# --- Always-on context budget (#120, #121) ---

REFERENCE_DIR = CLAUDE_DIR / "_reference"
RELATED_HEADING = re.compile(r"^## .*Related", re.MULTILINE)
REFERENCES_SECTION = re.compile(r"^## .*References.*\n(?:(?!## ).*\n?)*", re.MULTILINE)


def has_internal_link_section(text: str) -> bool:
    """Return True for a Related section, or a References section that lists config files.

    A References section of external URLs (e.g. vendor docs) is legitimate
    content; one that names other .md files is a Related section by another name.

    :param text: The markdown file's content.
    :type text: str
    :return: Whether the file carries parent/sibling links that belong in a README.
    :rtype: bool
    """
    if RELATED_HEADING.search(text):
        return True
    return any(".md" in section for section in REFERENCES_SECTION.findall(text))
H2_HEADING = re.compile(r"^## (.+)$", re.MULTILINE)
CONTENTS_MIN_HEADINGS = 3


def imported_content_files() -> list[Path]:
    """Return every .md file under _rules/ and _reference/ that can be @import-ed.

    Wider than rule_files(): includes 05_lazy_load/ and _reference/, since a
    lazy-loaded rule costs the same context once it is read. Excludes READMEs
    (never imported — they are where Related links now live).

    :return: Markdown files subject to the context-budget checks.
    :rtype: list[Path]
    """
    return [
        md_file
        for base in (RULES_DIR, REFERENCE_DIR)
        for md_file in base.rglob("*.md")
        if md_file.name != "README.md"
    ]


def test_no_related_section_outside_readmes():
    """Related links live in the tier README, not the always-on rule file (#121)."""
    offenders = [
        str(md_file.relative_to(CLAUDE_DIR))
        for md_file in imported_content_files()
        if has_internal_link_section(md_file.read_text())
    ]
    assert not offenders, (
        f"{len(offenders)} file(s) have a Related section (or a References section of .md links) — "
        f"move the links to the tier README under '🔗 Related rules': {sorted(offenders)}"
    )


def test_contents_section_only_with_three_real_headings():
    """A Contents section must only appear when the file has 3+ other ## headings (#120)."""
    offenders = []
    for md_file in imported_content_files():
        headings = H2_HEADING.findall(md_file.read_text())
        if not any("Contents" in heading for heading in headings):
            continue
        real = [h for h in headings if "Contents" not in h and "Related" not in h]
        if len(real) < CONTENTS_MIN_HEADINGS:
            offenders.append(f"{md_file.relative_to(CLAUDE_DIR)} ({len(real)} headings)")
    assert not offenders, (
        f"Contents section on file(s) with fewer than {CONTENTS_MIN_HEADINGS} real ## headings "
        f"— drop the Contents block: {sorted(offenders)}"
    )


def always_on_import_graph() -> dict[Path, Optional[Path]]:
    """Walk every @import chain from CLAUDE.md and return each reached file with its importer.

    :return: Map of each reachable file to the file that imported it (None for CLAUDE.md).
    :rtype: dict[Path, Optional[Path]]
    """
    reached: dict[Path, Optional[Path]] = {CLAUDE_MD: None}
    queue = [CLAUDE_MD]
    while queue:
        current = queue.pop()
        for target in extract_import_paths(current):
            if target not in reached and target.exists():
                reached[target] = current
                queue.append(target)
    return reached


def test_always_on_files_do_not_import_reference():
    """_reference/ is read on demand — no @import chain from CLAUDE.md may reach it.

    Its architecture docs are background reading, and every import adds the full
    file to every session's context.
    """
    reached = always_on_import_graph()
    offenders = sorted(
        f"{reached[path].relative_to(CLAUDE_DIR)} -> {path.relative_to(CLAUDE_DIR)}"
        for path in reached
        if REFERENCE_DIR in path.parents
    )
    assert not offenders, (
        f"{len(offenders)} @import(s) pull _reference/ into every session — replace each with a "
        f"'Read on demand' pointer: {offenders}"
    )


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

    tier_positions = [TIER_ORDER.index(tier_name) for tier_name in tier_sequence]
    assert tier_positions == sorted(tier_positions), (
        f"CLAUDE.md _rules/ imports out of tier order — expected ascending {TIER_ORDER}, "
        f"found sequence: {tier_sequence}"
    )
