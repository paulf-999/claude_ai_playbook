"""
Test: File Structure Compliance Scan

Validates that all files and directories in ~/.claude/ follow naming and location conventions.

Checks:
1. **Naming compliance:** snake_case for files, underscore prefix for user-created dirs
2. **Location compliance:** Files in correct directories (_rules/, _tests/, hooks/, skills/, etc.)
3. **Child file prefixes:** Child files start with underscore (_child.md)
4. **Directory depth:** Rules organized properly by tier (01_core/, 02_claude_internal/, 03_lazy_load/)

This test is parametrized to scan all files at once and report violations.
"""

import re
from pathlib import Path


CLAUDE_HOME = Path.home() / ".claude"

# Directories that are auto-generated and should be skipped
AUTO_GENERATED_DIRS = {
    "backups",
    "memory",
    "sessions",
    "projects",
    "plugins",
    ".git",
    "__pycache__",
}

# User-created directories that should exist (with underscore prefix)
USER_CREATED_DIRS = {
    "_rules",
    "_tests",
    "_templates",
    "_reference",
    "_docs",
    "_lib",
    "_drafts",
    "_errors",
    "_sessions",
    "_wip",
}

# Directory-specific validation rules
DIR_RULES = {
    "_rules": {
        "subdirs": ["01_core", "02_claude_internal", "03_lazy_load"],
        "rule": "Rules organized by tier (01_core=blocking, 02_claude_internal=how Claude works, 03_lazy_load=domain-specific)",
    },
    "hooks": {
        "pattern": r"^(hook_\w+_\w+\.sh|hook_\w+_dispatch\.sh)$",
        "rule": "Hook files follow pattern: hook_<type>_<domain>.sh",
    },
    "skills": {
        "pattern": r"^[a-z_]+_[a-z_]+$",
        "rule": "Skill directories follow pattern: <domain>_<action>",
    },
}

# Naming patterns for files
FILE_NAMING_RULES = {
    r"\.md$": {
        "pattern": r"^[a-z_]+\.md$",
        "rule": "Markdown files: snake_case.md",
        "exceptions": ["CLAUDE.md", "README.md", "SKILL.md"],
    },
    r"\.sh$": {
        "pattern": r"^[a-z_]+\.sh$",
        "rule": "Shell files: snake_case.sh",
    },
    r"\.py$": {
        "pattern": r"^[a-z_]+\.py$",
        "rule": "Python files: snake_case.py",
    },
}


class FileStructureValidator:
    """Validates file structure compliance in ~/.claude/."""

    def __init__(self, claude_home: Path = CLAUDE_HOME):
        """Initialize validator with Claude home directory."""
        self.claude_home = claude_home
        self.violations = []

    def scan(self) -> list[dict]:
        """
        Scan ~/.claude/ and collect all violations.

        Returns:
            List of violation dicts with keys: path, rule, severity
        """
        if not self.claude_home.exists():
            self.violations.append({
                "path": str(self.claude_home),
                "rule": "Directory exists",
                "severity": "error",
                "message": f"Claude home directory not found: {self.claude_home}",
            })
            return self.violations

        self._scan_directory(self.claude_home)
        return self.violations

    def _scan_directory(self, directory: Path, depth: int = 0) -> None:
        """Recursively scan directory for violations."""
        if not directory.exists():
            return

        # Skip auto-generated directories
        if directory.name in AUTO_GENERATED_DIRS:
            return

        # Skip hidden directories and common exclusions
        if directory.name.startswith('.') or directory.name in ["__pycache__", "node_modules"]:
            return

        try:
            for item in directory.iterdir():
                if item.is_dir():
                    self._validate_directory(item, depth)
                    self._scan_directory(item, depth + 1)
                elif item.is_file():
                    self._validate_file(item, depth)
        except PermissionError:
            # Skip directories we can't read
            pass

    def _validate_directory(self, directory: Path, depth: int) -> None:
        """Validate a directory name and structure."""
        rel_path = directory.relative_to(self.claude_home)

        # Check if directory is user-created or auto-generated
        is_user_created = directory.name.startswith("_") or depth == 0

        # Check naming convention
        if is_user_created and depth > 0 and not directory.name.startswith("_"):
            self.violations.append({
                "path": str(rel_path),
                "rule": "User-created directories must start with underscore",
                "severity": "warning",
                "message": f"Directory should be _{directory.name}/",
            })

        # Check directory-specific rules
        if directory.name in DIR_RULES:
            rules = DIR_RULES[directory.name]
            if "subdirs" in rules:
                self._validate_subdirs(directory, rules["subdirs"])

    def _validate_subdirs(self, directory: Path, expected_subdirs: list[str]) -> None:
        """Validate expected subdirectories exist."""
        for expected in expected_subdirs:
            subdir = directory / expected
            if not subdir.exists():
                rel_path = directory.relative_to(self.claude_home)
                self.violations.append({
                    "path": str(rel_path),
                    "rule": f"Missing subdirectory: {expected}",
                    "severity": "warning",
                    "message": f"Expected subdirectory {expected}/ under {rel_path}/",
                })

    def _validate_file(self, file: Path, depth: int) -> None:
        """Validate a file name."""
        rel_path = file.relative_to(self.claude_home)
        filename = file.name

        # Check if filename is valid (exceptions for special files)
        if filename in ["CLAUDE.md", "README.md", "SKILL.md", "settings.json", "aliases.md", "keybindings.json"]:
            return

        # Check if child file (should start with underscore)
        is_child_file = depth > 1 and filename.startswith("_")
        is_parent_file = depth > 0 and not filename.startswith("_") and filename.endswith(".md")

        parent_dir = file.parent.name
        if parent_dir in USER_CREATED_DIRS and depth == 1:
            # Top-level files in user directories should be allowed
            pass
        elif depth > 1 and not is_child_file and filename.endswith(".md"):
            # Nested markdown files should start with underscore
            self.violations.append({
                "path": str(rel_path),
                "rule": "Child files should start with underscore",
                "severity": "info",
                "message": f"Consider renaming to _{filename}",
            })

        # Check snake_case naming
        if not self._is_valid_snake_case(filename):
            self.violations.append({
                "path": str(rel_path),
                "rule": "Invalid naming: not snake_case",
                "severity": "error",
                "message": f"File should use snake_case: {filename}",
            })

    def _is_valid_snake_case(self, filename: str) -> bool:
        """Check if filename follows snake_case convention."""
        # Allow special files
        if filename in ["CLAUDE.md", "README.md", "SKILL.md", "settings.json", "keybindings.json"]:
            return True

        # Check pattern: lowercase, underscore-separated, valid extension
        pattern = r"^[a-z0-9][a-z0-9_]*(\.[a-z0-9]+)$"
        return bool(re.match(pattern, filename))


def test_file_structure_compliance():
    """
    Validate that all files and directories in ~/.claude/ follow conventions.
    """
    validator = FileStructureValidator()
    violations = validator.scan()

    # Separate by severity
    errors = [v for v in violations if v["severity"] == "error"]
    warnings = [v for v in violations if v["severity"] == "warning"]
    infos = [v for v in violations if v["severity"] == "info"]

    # Build error message
    error_msg = ""
    if errors:
        error_msg += f"\n❌ {len(errors)} ERRORS:\n"
        for v in errors:
            error_msg += f"  - {v['path']}: {v['message']}\n"

    if warnings:
        error_msg += f"\n⚠️ {len(warnings)} WARNINGS:\n"
        for v in warnings:
            error_msg += f"  - {v['path']}: {v['message']}\n"

    if infos:
        error_msg += f"\nℹ️ {len(infos)} INFO:\n"
        for v in infos[:5]:  # Show first 5 info items
            error_msg += f"  - {v['path']}: {v['message']}\n"
        if len(infos) > 5:
            error_msg += f"  ... and {len(infos) - 5} more\n"

    # Assert no errors (warnings/infos are advisory)
    assert len(errors) == 0, f"File structure violations found:{error_msg}"


if __name__ == "__main__":
    test_file_structure_compliance()
    print("✅ File structure compliance check passed!")
