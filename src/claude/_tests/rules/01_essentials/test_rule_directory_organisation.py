# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-08-28
# Date updated:      2026-10-11
# Version:           2.4.1
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests the folder layout of the always-on rule tiers.

- **01_essentials/:** holds exactly the expected top-level files and folders.
- **Parent and children:** across tiers 01–03, per ``multifile_document_organisation.md``,
  children sit in a ``<topic>/`` folder beside their ``<topic>.md`` parent, use the ``_``
  prefix, come two or more to a folder, and never sit loose at a tier's root.
- **Style guides:** installed path-scoped guides (``sql.md``, ``infra/terraform.md``) are standalone
  entry files grouped by domain, so their folders are exempt from the parent-and-children checks.

Whether CLAUDE.md imports these files is checked by ``test_always_on_reachability.py``.
"""
from __future__ import annotations

from pathlib import Path

from _shared_paths import RULES_DIR

ESSENTIALS_DIR = RULES_DIR / "01_essentials"
USAGE_STANDARDS_DIR = ESSENTIALS_DIR / "claude_usage_standards"
ALWAYS_ON_TIERS = ("01_essentials", "02_claude_standards", "03_authoring_guidelines")

# Top-level files and folders expected in 01_essentials/
EXPECTED_TOP_LEVEL = {"claude_response_standards.md", "claude_usage_standards.md", "guiding_principles.md"}
EXPECTED_DIRECTORIES = {"claude_usage_standards"}

# claude_usage_standards/ groups three rules, one of which keeps a children folder
USAGE_STANDARDS_PARENTS = {
    "naming_standards.md",
    "writing_style.md",
    "multifile_document_organisation.md",
}
USAGE_STANDARDS_SUBDIRS = {"naming_standards"}

# Folders that group parents or shared children rather than one parent's children
GROUPING_DIRS = {
    "01_essentials/claude_usage_standards",
    "02_claude_standards/claude_working_practices",
    "02_claude_standards/path_scoped_rules",
    "03_authoring_guidelines/shared_standards",
}
# Installed path-scoped style guides: standalone entry files grouped by domain, at any depth.
# Only the live install has this folder (the repo keeps guides in _reference/), so it isn't stale-checked.
STYLE_GUIDES_DIR = "02_claude_standards/path_scoped_rules/style_guide_standards"


def child_folders() -> list[Path]:
    """List the children folders in tiers 01–03, leaving out grouping folders.

    :return: Every folder under the always-on tiers that holds one parent's children.
    :rtype: list[Path]
    """
    return sorted(
        folder for tier in ALWAYS_ON_TIERS for folder in (RULES_DIR / tier).rglob("*")
        if folder.is_dir() and not is_grouping(str(folder.relative_to(RULES_DIR)))
    )


def is_grouping(rel: str) -> bool:
    """Say whether a folder groups parents rather than holding one parent's children.

    :param rel: The folder's path relative to ``rules/``.
    :return: True for a listed grouping folder or anything in the style-guide tree.
    """
    return rel in GROUPING_DIRS or rel == STYLE_GUIDES_DIR or rel.startswith(f"{STYLE_GUIDES_DIR}/")


def children(folder: Path) -> list[Path]:
    """List the rule files in a children folder.

    :param folder: A children folder.
    :type folder: Path
    :return: Its markdown files, README.md excluded.
    :rtype: list[Path]
    """
    return sorted(f for f in folder.glob("*.md") if f.name != "README.md")


def test_01_essentials_directory_exists():
    """01_essentials/ exists and is a folder."""
    assert ESSENTIALS_DIR.exists(), f"Directory not found: {ESSENTIALS_DIR}"
    assert ESSENTIALS_DIR.is_dir(), f"Not a directory: {ESSENTIALS_DIR}"


def test_top_level_files_are_expected():
    """01_essentials/ holds exactly the expected top-level files."""
    files = {f.name for f in ESSENTIALS_DIR.glob("*.md")}
    assert files == EXPECTED_TOP_LEVEL, f"missing {EXPECTED_TOP_LEVEL - files}, extra {files - EXPECTED_TOP_LEVEL}"


def test_top_level_directories_are_expected():
    """01_essentials/ holds exactly the expected folders."""
    dirs = {d.name for d in ESSENTIALS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")}
    assert dirs == EXPECTED_DIRECTORIES, f"missing {EXPECTED_DIRECTORIES - dirs}, extra {dirs - EXPECTED_DIRECTORIES}"


def test_usage_standards_parent_files():
    """claude_usage_standards/ holds exactly its four rule files."""
    files = {f.name for f in USAGE_STANDARDS_DIR.glob("*.md")}
    expected = USAGE_STANDARDS_PARENTS
    assert files == expected, f"missing {expected - files}, extra {files - expected}"


def test_usage_standards_subdirectories():
    """claude_usage_standards/ holds exactly the children folders its rules need."""
    dirs = {d.name for d in USAGE_STANDARDS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")}
    expected = USAGE_STANDARDS_SUBDIRS
    assert dirs == expected, f"missing {expected - dirs}, extra {dirs - expected}"


def test_child_files_have_underscore_prefix():
    """Every child file in tiers 01–03 starts with an underscore."""
    files = [f for folder in child_folders() for f in children(folder)]
    assert files, "expected child files in the always-on tiers"
    bad = [str(f.relative_to(RULES_DIR)) for f in files if not f.name.startswith("_")]
    assert not bad, f"child files missing the _ prefix: {bad}"


def test_no_loose_child_files_at_tier_roots():
    """No _child.md sits loose at a tier's root, away from its parent's folder."""
    loose = [str(f.relative_to(RULES_DIR)) for tier in ALWAYS_ON_TIERS for f in (RULES_DIR / tier).glob("_*.md")]
    assert not loose, f"child files at a tier root — move them into their parent's folder: {loose}"


def test_two_plus_rule_for_child_folders():
    """Every children folder holds two or more children."""
    folders = child_folders()
    assert folders, "expected children folders in the always-on tiers"
    single = [str(f.relative_to(RULES_DIR)) for f in folders if len(children(f)) == 1]
    assert not single, f"folders with one child — flatten each to a top-level file: {single}"


def test_child_folders_sit_beside_their_parent():
    """Every children folder has its <topic>.md parent beside it."""
    orphans = [
        str(f.relative_to(RULES_DIR)) for f in child_folders()
        if f.name != "_lazy_load" and not (f.parent / f"{f.name}.md").is_file()
    ]
    assert not orphans, f"children folders with no <topic>.md parent beside them: {orphans}"


def test_no_lazy_load_folders_in_always_on_tiers():
    """On-demand children live in _rules_lazy_load/, since every file under rules/ auto-loads."""
    lazy = [str(f.relative_to(RULES_DIR)) for f in child_folders() if f.name == "_lazy_load"]
    assert not lazy, f"move these children to _rules_lazy_load/<topic>/: {lazy}"


def test_grouping_dirs_still_exist():
    """Every grouping folder exempted above still exists, so no exemption goes stale."""
    stale = [d for d in GROUPING_DIRS if not (RULES_DIR / d).is_dir()]
    assert not stale, f"grouping exemptions for folders that no longer exist — remove them: {stale}"
    shared = [f.name for f in (RULES_DIR / "03_authoring_guidelines" / "shared_standards").glob("*.md")]
    assert len(shared) >= 2, f"shared_standards/ should group 2+ shared children, found {shared}"


def test_style_guide_entry_files_are_grouped_not_children():
    """Style guides like sql.md sit unprefixed in the style-guide tree, which counts as grouping, not children."""
    assert is_grouping(STYLE_GUIDES_DIR), "the style-guide root should count as a grouping folder"
    assert is_grouping(f"{STYLE_GUIDES_DIR}/infra"), "style-guide subfolders should count as grouping folders"
    assert not is_grouping("02_claude_standards/behaviour"), "a parent's children folder is not a grouping folder"
    assert not is_grouping(f"{STYLE_GUIDES_DIR}_extra"), "a sibling with a matching prefix is not exempt"
