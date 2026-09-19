# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 7/10
# Date created:      2026-08-28
# Version:           1.0.0
# Date updated:      2026-09-17
# ─────────────────────────────────────────────────────────

"""
Test suite for rule directory organization patterns.

Validates:
1. Top-level files in 01_essentials/ are simple/foundational concepts
2. Child files use underscore prefix (_filename.md)
3. Subdirectories only exist when 2+ child files present
4. No orphaned child files at top level
5. All top-level files imported in CLAUDE.md
"""

import re

from _shared_paths import CLAUDE_DIR, CLAUDE_MD, RULES_DIR

ESSENTIALS_DIR = RULES_DIR / "01_essentials"

# Top-level files expected in 01_essentials
# These are parent files that are imported in CLAUDE.md. Per the 5-tier reorg,
# behaviour.md/security.md/testing.md moved to 02_claude_standards/, and
# authoring_rules.md/authoring_skills.md moved to 03_authoring_guidelines/ —
# 01_essentials now holds only the foundational, user-facing files.
EXPECTED_TOP_LEVEL = {
    "README.md",
    "claude_response_standards.md",
    "claude_usage_standards.md",
    "guiding_principles.md",
}

# Top-level directories expected (compound rules with children)
EXPECTED_DIRECTORIES = {
    "claude_response_standards",  # Has children (_enforcement.md, _response_timing.md)
    "claude_usage_standards",  # Grouping directory for naming, writing_style, claude_directory_structure
}

# Parent files within claude_usage_standards/ subdirectory
CLAUDE_USAGE_STANDARDS_PARENTS = {
    "naming_standards.md",
    "writing_style.md",
    "claude_directory_structure.md",
}

# Subdirectories within claude_usage_standards/
CLAUDE_USAGE_STANDARDS_SUBDIRS = {
    "naming_standards",
    "writing_style",
    "claude_directory_structure",
}


def test_01_essentials_directory_exists():
    """Verify 01_essentials/ directory exists."""
    assert ESSENTIALS_DIR.exists(), f"Directory not found: {ESSENTIALS_DIR}"
    assert ESSENTIALS_DIR.is_dir(), f"Not a directory: {ESSENTIALS_DIR}"


def test_top_level_files_are_expected():
    """Verify top-level files in 01_essentials/ match expected set."""
    files = {f.name for f in ESSENTIALS_DIR.glob("*.md")}
    assert files == EXPECTED_TOP_LEVEL, (
        f"Unexpected top-level files.\n"
        f"Expected: {EXPECTED_TOP_LEVEL}\n"
        f"Got: {files}\n"
        f"Missing: {EXPECTED_TOP_LEVEL - files}\n"
        f"Extra: {files - EXPECTED_TOP_LEVEL}"
    )


def test_top_level_directories_are_expected():
    """Verify top-level directories in 01_essentials/ match expected set."""
    dirs = {d.name for d in ESSENTIALS_DIR.iterdir() if d.is_dir() and not d.name.startswith(".")}
    assert dirs == EXPECTED_DIRECTORIES, (
        f"Unexpected top-level directories.\n"
        f"Expected: {EXPECTED_DIRECTORIES}\n"
        f"Got: {dirs}\n"
        f"Missing: {EXPECTED_DIRECTORIES - dirs}\n"
        f"Extra: {dirs - EXPECTED_DIRECTORIES}"
    )


def test_claude_usage_standards_directory_exists():
    """Verify claude_usage_standards/ subdirectory exists."""
    claude_usage_standards_dir = ESSENTIALS_DIR / "claude_usage_standards"
    assert claude_usage_standards_dir.exists(), f"Directory not found: {claude_usage_standards_dir}"
    assert claude_usage_standards_dir.is_dir(), f"Not a directory: {claude_usage_standards_dir}"


def test_claude_usage_standards_parent_files():
    """Verify parent files in claude_usage_standards/ directory."""
    claude_usage_standards_dir = ESSENTIALS_DIR / "claude_usage_standards"
    files = {f.name for f in claude_usage_standards_dir.glob("*.md")}
    assert files == CLAUDE_USAGE_STANDARDS_PARENTS, (
        f"Unexpected parent files in claude_usage_standards/.\n"
        f"Expected: {CLAUDE_USAGE_STANDARDS_PARENTS}\n"
        f"Got: {files}\n"
        f"Missing: {CLAUDE_USAGE_STANDARDS_PARENTS - files}\n"
        f"Extra: {files - CLAUDE_USAGE_STANDARDS_PARENTS}"
    )


def test_claude_usage_standards_subdirectories():
    """Verify subdirectories in claude_usage_standards/ match expected set."""
    claude_usage_standards_dir = ESSENTIALS_DIR / "claude_usage_standards"
    dirs = {d.name for d in claude_usage_standards_dir.iterdir() if d.is_dir() and not d.name.startswith(".")}
    assert dirs == CLAUDE_USAGE_STANDARDS_SUBDIRS, (
        f"Unexpected subdirectories in claude_usage_standards/.\n"
        f"Expected: {CLAUDE_USAGE_STANDARDS_SUBDIRS}\n"
        f"Got: {dirs}\n"
        f"Missing: {CLAUDE_USAGE_STANDARDS_SUBDIRS - dirs}\n"
        f"Extra: {dirs - CLAUDE_USAGE_STANDARDS_SUBDIRS}"
    )


def test_child_files_have_underscore_prefix():
    """Verify all child files in subdirectories use underscore prefix."""
    errors = []

    for subdir in EXPECTED_DIRECTORIES:
        if subdir == "claude_usage_standards":
            continue  # claude_usage_standards is a special case

        subdir_path = ESSENTIALS_DIR / subdir
        if not subdir_path.exists():
            continue

        for md_file in subdir_path.glob("*.md"):
            if not md_file.name.startswith("_"):
                errors.append(f"Child file missing underscore prefix: {md_file.relative_to(ESSENTIALS_DIR)}")

    # Check claude_usage_standards subdirectory children
    claude_usage_standards_dir = ESSENTIALS_DIR / "claude_usage_standards"
    for subdir in CLAUDE_USAGE_STANDARDS_SUBDIRS:
        subdir_path = claude_usage_standards_dir / subdir
        if not subdir_path.exists():
            continue

        for md_file in subdir_path.glob("*.md"):
            if not md_file.name.startswith("_"):
                errors.append(f"Child file missing underscore prefix: {md_file.relative_to(ESSENTIALS_DIR)}")

    assert not errors, "Child file naming violations:\n" + "\n".join(errors)


def test_no_orphaned_child_files():
    """Verify no orphaned child files at top level of 01_essentials/."""
    errors = []

    for md_file in ESSENTIALS_DIR.glob("_*.md"):
        errors.append(f"Orphaned child file at top level: {md_file.name}")

    assert not errors, "Orphaned child files found:\n" + "\n".join(errors)


def test_two_plus_rule_for_subdirectories():
    """Verify subdirectories only exist when 2+ child files present."""
    errors = []

    for subdir in ESSENTIALS_DIR.iterdir():
        if not subdir.is_dir() or subdir.name.startswith("."):
            continue

        if subdir.name == "claude_usage_standards":
            continue  # claude_usage_standards has special structure

        child_files = list(subdir.glob("_*.md"))
        if len(child_files) == 1:
            errors.append(
                f"Subdirectory with only 1 child file violates 2+ rule: "
                f"{subdir.name}/ (contains {child_files[0].name})"
            )

    assert not errors, "2+ rule violations:\n" + "\n".join(errors)


def test_claude_md_imports():
    """Verify all top-level files are imported in CLAUDE.md."""
    if not CLAUDE_MD.exists():
        return  # Skip if CLAUDE.md doesn't exist

    claude_content = CLAUDE_MD.read_text()
    errors = []

    for file in EXPECTED_TOP_LEVEL:
        if file == "README.md":
            continue  # README is not imported

        # Match any "@~/<config-dir-name>/_rules/01_essentials/<file>" import,
        # regardless of whether the config-dir is named .claude or claude.
        stem = file.replace(".md", "")
        import_pattern = re.compile(
            rf"@~/[^/]+/_rules/01_essentials/{re.escape(stem)}(?:\.md)?\b"
        )
        if not import_pattern.search(claude_content):
            errors.append(f"Missing import for {file}: expected a pattern like .../01_essentials/{stem}")

    assert not errors, "Missing imports in CLAUDE.md:\n" + "\n".join(errors)


def test_claude_usage_standards_parent_files_imported():
    """Verify claude_usage_standards parent files are reachable from CLAUDE.md (directly or via a hub file).

    CLAUDE.md imports claude_usage_standards.md, which is the actual entry
    point for these 3 grouped files — not CLAUDE.md directly. Checking only
    CLAUDE.md's own text would miss this legitimate indirection.
    """
    usage_standards = CLAUDE_DIR / "_rules" / "01_essentials" / "claude_usage_standards.md"
    if not CLAUDE_MD.exists() or not usage_standards.exists():
        return  # Skip if either entry point doesn't exist

    combined_content = CLAUDE_MD.read_text() + "\n" + usage_standards.read_text()
    errors = []

    expected_imports = [
        "naming_standards",
        "writing_style",
        "claude_directory_structure",
    ]

    for import_name in expected_imports:
        pattern = re.compile(
            rf"@~/[^/]+/_rules/01_essentials/claude_usage_standards/{re.escape(import_name)}(?:\.md)?\b"
        )
        if not pattern.search(combined_content):
            errors.append(f"Missing import for claude_usage_standards/{import_name}")

    assert not errors, (
        "Missing claude_usage_standards imports in CLAUDE.md or claude_usage_standards.md:\n" +
        "\n".join(errors)
    )


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
