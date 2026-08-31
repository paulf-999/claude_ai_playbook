"""
Test suite for rule directory organization patterns.

Validates:
1. Top-level files in 01_essentials/ are simple/foundational concepts
2. Child files use underscore prefix (_filename.md)
3. Subdirectories only exist when 2+ child files present
4. No orphaned child files at top level
5. All top-level files imported in CLAUDE.md
"""

import os
from pathlib import Path


# Use project repo paths
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent  # Go up to project root
RULES_DIR = PROJECT_ROOT / "src" / "claude" / "_rules"
ESSENTIALS_DIR = RULES_DIR / "01_essentials"
CLAUDE_MD = PROJECT_ROOT / "src" / "claude" / "CLAUDE.md"

# Top-level files expected in 01_essentials
# These are parent files that are imported in CLAUDE.md
EXPECTED_TOP_LEVEL = {
    "README.md",
    "authoring_rules.md",
    "authoring_skills.md",
    "behaviour.md",
    "conventions.md",
    "guiding_principles.md",
    "security.md",
    "testing.md",
}

# Top-level directories expected (compound rules with children)
EXPECTED_DIRECTORIES = {
    "behaviour",  # Has children
    "conventions",  # Grouping directory for naming, writing_style, claude_directory_structure
    "skill_authoring",  # Has children
    "testing",  # Has children
}

# Parent files within conventions/ subdirectory
CONVENTIONS_PARENTS = {
    "naming_standards.md",
    "writing_style.md",
    "claude_directory_structure.md",
}

# Subdirectories within conventions/
CONVENTIONS_SUBDIRS = {
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


def test_conventions_directory_exists():
    """Verify conventions/ subdirectory exists."""
    conventions_dir = ESSENTIALS_DIR / "conventions"
    assert conventions_dir.exists(), f"Directory not found: {conventions_dir}"
    assert conventions_dir.is_dir(), f"Not a directory: {conventions_dir}"


def test_conventions_parent_files():
    """Verify parent files in conventions/ directory."""
    conventions_dir = ESSENTIALS_DIR / "conventions"
    files = {f.name for f in conventions_dir.glob("*.md")}
    assert files == CONVENTIONS_PARENTS, (
        f"Unexpected parent files in conventions/.\n"
        f"Expected: {CONVENTIONS_PARENTS}\n"
        f"Got: {files}\n"
        f"Missing: {CONVENTIONS_PARENTS - files}\n"
        f"Extra: {files - CONVENTIONS_PARENTS}"
    )


def test_conventions_subdirectories():
    """Verify subdirectories in conventions/ match expected set."""
    conventions_dir = ESSENTIALS_DIR / "conventions"
    dirs = {d.name for d in conventions_dir.iterdir() if d.is_dir() and not d.name.startswith(".")}
    assert dirs == CONVENTIONS_SUBDIRS, (
        f"Unexpected subdirectories in conventions/.\n"
        f"Expected: {CONVENTIONS_SUBDIRS}\n"
        f"Got: {dirs}\n"
        f"Missing: {CONVENTIONS_SUBDIRS - dirs}\n"
        f"Extra: {dirs - CONVENTIONS_SUBDIRS}"
    )


def test_child_files_have_underscore_prefix():
    """Verify all child files in subdirectories use underscore prefix."""
    errors = []

    for subdir in EXPECTED_DIRECTORIES:
        if subdir == "conventions":
            continue  # conventions is a special case

        subdir_path = ESSENTIALS_DIR / subdir
        if not subdir_path.exists():
            continue

        for md_file in subdir_path.glob("*.md"):
            if not md_file.name.startswith("_"):
                errors.append(f"Child file missing underscore prefix: {md_file.relative_to(ESSENTIALS_DIR)}")

    # Check conventions subdirectory children
    conventions_dir = ESSENTIALS_DIR / "conventions"
    for subdir in CONVENTIONS_SUBDIRS:
        subdir_path = conventions_dir / subdir
        if not subdir_path.exists():
            continue

        for md_file in subdir_path.glob("*.md"):
            if not md_file.name.startswith("_"):
                errors.append(f"Child file missing underscore prefix: {md_file.relative_to(ESSENTIALS_DIR)}")

    assert not errors, f"Child file naming violations:\n" + "\n".join(errors)


def test_no_orphaned_child_files():
    """Verify no orphaned child files at top level of 01_essentials/."""
    errors = []

    for md_file in ESSENTIALS_DIR.glob("_*.md"):
        errors.append(f"Orphaned child file at top level: {md_file.name}")

    assert not errors, f"Orphaned child files found:\n" + "\n".join(errors)


def test_two_plus_rule_for_subdirectories():
    """Verify subdirectories only exist when 2+ child files present."""
    errors = []

    for subdir in ESSENTIALS_DIR.iterdir():
        if not subdir.is_dir() or subdir.name.startswith("."):
            continue

        if subdir.name == "conventions":
            continue  # conventions has special structure

        child_files = list(subdir.glob("_*.md"))
        if len(child_files) == 1:
            errors.append(f"Subdirectory with only 1 child file violates 2+ rule: {subdir.name}/ (contains {child_files[0].name})")

    assert not errors, f"2+ rule violations:\n" + "\n".join(errors)


def test_claude_md_imports():
    """Verify all top-level files are imported in CLAUDE.md."""
    if not CLAUDE_MD.exists():
        return  # Skip if CLAUDE.md doesn't exist

    claude_content = CLAUDE_MD.read_text()
    errors = []

    for file in EXPECTED_TOP_LEVEL:
        if file == "README.md":
            continue  # README is not imported

        # Check for import pattern: @~/.claude/_rules/01_essentials/<file>
        import_pattern = f"@~/.claude/_rules/01_essentials/{file.replace('.md', '')}"
        if import_pattern not in claude_content:
            errors.append(f"Missing import for {file}: expected pattern like {import_pattern}")

    assert not errors, f"Missing imports in CLAUDE.md:\n" + "\n".join(errors)


def test_conventions_parent_files_imported():
    """Verify conventions parent files are referenced in CLAUDE.md."""
    if not CLAUDE_MD.exists():
        return  # Skip if CLAUDE.md doesn't exist

    claude_content = CLAUDE_MD.read_text()
    errors = []

    # Check that convention files are imported via their new conventions/ path
    expected_imports = [
        "naming_standards",
        "writing_style",
        "claude_directory_structure",
    ]

    for import_name in expected_imports:
        pattern = f"@~/.claude/_rules/01_essentials/conventions/{import_name}"
        if pattern not in claude_content:
            errors.append(f"Missing import for conventions/{import_name}: expected pattern {pattern}")

    assert not errors, f"Missing convention imports in CLAUDE.md:\n" + "\n".join(errors)


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
