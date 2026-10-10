# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-10
# Version:           2.2.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests where rules/ files live and what CLAUDE.md still imports.

- **Layout:** no files at the ``rules/`` root, no retired ``04_claude_reference/`` tier,
  ``aliases.md`` at the config root, and no paths dissolved in the 2026-08 restructure.
- **Import graph:** every import in CLAUDE.md or ``rules/`` resolves, and no import chain
  from CLAUDE.md reaches ``_reference/``.

Rules load natively from ``rules/``, so CLAUDE.md imports only memory and aliases; a stray
``@`` import elsewhere never loads.
``test_rules_structure.py`` covers the per-file format checks.
"""
from __future__ import annotations

import re
from pathlib import Path

from _shared_paths import CLAUDE_DIR, CLAUDE_MD, LAZY_RULES_NAME, RULES_DIR, native_rule_files

REFERENCE_DIR = CLAUDE_DIR / "_reference"
IMPORT_LINE = re.compile(r"^@~/[^/\s]+/(\S+)$", re.M)

# rules/ root holds only tier folders — any file there would load every session
EXPECTED_ROOT_FILES: set[str] = set()

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
    RULES_DIR / "speculative_features.md",
    RULES_DIR / "claude_internal.md",
    # Tier 04 was retired on 2026-10-06 (#330); its one rule moved to 02_claude_standards/
    RULES_DIR / "04_claude_reference",
]




def import_targets(text: str) -> list[str]:
    """Return the config-relative path of every ``@~/<config-dir>/...`` import line.

    Detects any config-dir name (.claude, claude, a repo checkout) — see portable_paths.md.

    :param text: Markdown content.
    :type text: str
    :return: Import paths with the ``@~/<config-dir>/`` prefix removed.
    :rtype: list[str]
    """
    return IMPORT_LINE.findall(text)


def extract_import_paths(md_file: Path) -> list[Path]:
    """Return resolved paths for all @import lines in a markdown file.

    :param md_file: The markdown file to parse for import lines.
    :type md_file: Path
    :return: Resolved file paths corresponding to each @-import line found.
    :rtype: list[Path]
    """
    return [CLAUDE_DIR / target for target in import_targets(md_file.read_text())]


def importing_files() -> list[Path]:
    """Return CLAUDE.md and every rules/ file.

    :return: The files whose imports Claude Code can follow.
    :rtype: list[Path]
    """
    return [CLAUDE_MD] + native_rule_files(RULES_DIR)


def test_rules_root_contains_only_expected_files():
    """rules/ root must contain no files — all rules live in tier subdirectories."""
    actual = {rule_file.name for rule_file in RULES_DIR.iterdir() if rule_file.is_file()}
    assert actual == EXPECTED_ROOT_FILES, (
        f"rules/ root mismatch — expected: {EXPECTED_ROOT_FILES}, got: {actual}"
    )



def test_rules_holds_exactly_the_four_tiers():
    """rules/ holds tiers 01–03 and 04_path_scoped/ only — tier 04 was retired on 2026-10-06 (#330).

    The repo also keeps the on-demand rules there, which the install moves beside rules/.
    """
    tiers = {d.name for d in RULES_DIR.iterdir() if d.is_dir() and d.name != LAZY_RULES_NAME}
    expected = {"01_essentials", "02_claude_standards", "03_authoring_guidelines", "04_path_scoped"}
    assert tiers == expected, f"rules/ tier folders drifted — missing {expected - tiers}, extra {tiers - expected}"


def test_aliases_at_claude_root():
    """aliases.md must exist at the Claude directory root, not inside rules/."""
    assert (CLAUDE_DIR / "aliases.md").exists(), f"aliases.md missing from {CLAUDE_DIR} root"
    assert not (RULES_DIR / "aliases.md").exists(), "aliases.md must not be inside rules/"


def test_behaviour_subdir_dissolved():
    """rules/behaviour/ subdir was dissolved and must not exist."""
    assert not (RULES_DIR / "behaviour").is_dir(), "rules/behaviour/ should not exist"


def test_dissolved_paths_absent():
    """Paths removed during restructure must not reappear."""
    for path in DISSOLVED_PATHS:
        assert not path.exists(), f"Dissolved path has reappeared: {path}"


def test_import_files_found():
    """CLAUDE.md still carries its memory and aliases imports, so the checks below can't pass on nothing."""
    assert import_targets(CLAUDE_MD.read_text()), "CLAUDE.md has no @~/ import lines"


def test_all_imports_resolve():
    """Every @import in CLAUDE.md or rules/ points to a real file."""
    broken = [
        f"{f.relative_to(CLAUDE_DIR)} -> {p.relative_to(CLAUDE_DIR)}"
        for f in importing_files() for p in extract_import_paths(f) if not p.exists()
    ]
    assert not broken, f"unresolved imports: {broken}"


def test_import_parser_reads_any_config_dir():
    """The parser handles .claude and claude prefixes, and skips inline mentions."""
    text = "@~/.claude/rules/a.md\n@~/claude/rules/b.md\nsee @~/claude/c.md\n"
    assert import_targets(text) == ["rules/a.md", "rules/b.md"], f"got {import_targets(text)}"


def always_on_import_graph() -> dict[Path, Path | None]:
    """Walk every @import chain from CLAUDE.md and return each reached file with its importer.

    :return: Map of each reachable file to the file that imported it (None for CLAUDE.md).
    :rtype: dict[Path, Path | None]
    """
    reached: dict[Path, Path | None] = {CLAUDE_MD: None}
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
