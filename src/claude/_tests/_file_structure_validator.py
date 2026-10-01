"""Checks file and directory names in the Claude config against its naming conventions.

``FileStructureValidator`` scans the whole config directory (``CLAUDE_CONFIG_DIR``) and
collects violations: names that aren't snake_case, nested markdown without the ``_``
child prefix, and missing ``_rules/`` tiers.

``check_new_path`` applies the same file checks to one path that doesn't exist yet. The
naming hook (``hooks/hook_enforcement_naming_convention.sh``) calls it through the
``--check`` command-line mode, so the hook and the scan always agree.

Tests: ``test_file_structure_compliance.py`` runs the scan over the real config, and
``test_file_structure_validator.py`` proves it on small fake config trees.
"""

import json
import re
import sys
from pathlib import Path


from _shared_paths import CLAUDE_DIR as CLAUDE_HOME

# Directories that are auto-generated, third-party, or out-of-scope and
# should be skipped entirely (not scanned for naming compliance)
AUTO_GENERATED_DIRS = {
    "backups",
    "memory",
    "sessions",
    "projects",
    "plugins",
    ".git",
    "__pycache__",
    "graphify-out",  # third-party tool's own generated cache/output, not Claude-authored
    "_admin",  # personal audit/decision-log scratch area with its own ALL-CAPS convention
    "file-history",  # Claude Code's own version-history store — UUID/hash@vN filenames
    ".trash",  # Claude Code's own sync-cleanup holding area (see syncClaudeAiSkills)
    "cache",  # Claude Code's own cache (model catalog, GitHub issue exports, etc.)
    "chrome",  # Claude Code's own Chrome extension host binary
    "daemon",  # Claude Code's own background daemon state (roster.json, control.key)
    "feedback",  # Claude Code's own feedback queue
    "ide",  # Claude Code's own IDE integration lock files (PID-named)
    "jobs",  # Claude Code's own scheduled-job state
    "mcp",  # Claude Code's own MCP server state
    "paste-cache",  # Claude Code's own pasted-content cache (hash-named)
    "plans",  # Claude Code's own plan-mode scratch files (ephemeral; see claude_plans.md)
    "security",  # Claude Code's own security-warning state (UUID-named)
    "session-env",  # Claude Code's own per-session environment state
    "shell-snapshots",  # Claude Code's own shell state snapshots
    "state",  # Claude Code's own persisted state (e.g. mcp-discover-verdicts.json)
    "tasks",  # Claude Code's own background-task state
    "telemetry",  # Claude Code's own telemetry queue
}

# Root-level files Claude Code itself generates — not authored content
AUTO_GENERATED_FILES = {
    "mcp-needs-auth-cache.json",
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
        "subdirs": [
            "01_essentials",
            "02_claude_standards",
            "03_authoring_guidelines",
            "04_claude_reference",
            "05_lazy_load",
        ],
        "rule": (
            "Rules organized by tier (01_essentials=blocking, 02_claude_standards=how Claude works, "
            "03_authoring_guidelines=authoring standards, 04_claude_reference=reference material, "
            "05_lazy_load=domain-specific)"
        ),
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
    """Validates file structure compliance in the configured Claude directory."""

    def __init__(self, claude_home: Path = CLAUDE_HOME):
        """Start a validator with no violations.

        :param claude_home: Root of the Claude config directory.
        :type claude_home: Path
        """
        self.claude_home = claude_home
        self.violations = []

    def scan(self) -> list[dict]:
        """Scan the configured Claude directory and collect all violations.

        :return: Violation dicts with keys path, rule, severity and message.
        :rtype: list[dict]
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

    def _scan_directory(self, directory: Path, depth: int = 0):
        """Scan a directory and everything below it for violations.

        :param directory: Directory to scan.
        :type directory: Path
        :param depth: How many levels below the config root ``directory``'s children sit.
        :type depth: int
        """
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

    def _validate_directory(self, directory: Path, depth: int):
        """Check a directory has the subdirectories its ``DIR_RULES`` entry expects.

        :param directory: Directory to check.
        :type directory: Path
        :param depth: Depth of the directory below the config root.
        :type depth: int
        """
        # Check directory-specific rules
        if directory.name in DIR_RULES:
            rules = DIR_RULES[directory.name]
            if "subdirs" in rules:
                self._validate_subdirs(directory, rules["subdirs"])

    def _validate_subdirs(self, directory: Path, expected_subdirs: list[str]):
        """Record a warning for each expected subdirectory that is missing.

        :param directory: Directory that should hold the subdirectories.
        :type directory: Path
        :param expected_subdirs: Names of the subdirectories it should hold.
        :type expected_subdirs: list[str]
        """
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

    def _validate_file(self, file: Path, depth: int):
        """Check one file's name and record any violations.

        :param file: File to check.
        :type file: Path
        :param depth: Depth of the file below the config root.
        :type depth: int
        """
        rel_path = file.relative_to(self.claude_home)
        filename = file.name

        # Check if filename is valid (exceptions for special files)
        if filename in [
            "CLAUDE.md", "README.md", "SKILL.md", "AGENT.md", "TODO.md",
            "settings.json", "aliases.md", "keybindings.json",
            "skill.contract.yaml",  # required exact name, see authoring_skills.md
            "__init__.py",  # Python package marker, not a naming-convention target
            # Eval fixture deliberately named after a real external repo slug
            # (Payroc's own repos use hyphens) — see payroc_engineering_naming_standards.md
            "dmt-scripts-claude_ai_playbook.yaml",
        ] or filename in AUTO_GENERATED_FILES:
            return

        # Dotfiles (.gitkeep, .coverage, etc.) are tooling artifacts, not
        # naming-convention targets
        if filename.startswith("."):
            return

        # Template files mirror the exact target filename they template
        # (e.g. AGENT.md.template, skill.contract.yaml.template) — validate
        # the part before ".template" instead of the literal template name
        if filename.endswith(".template"):
            filename = filename[: -len(".template")]
            if filename in ["AGENT.md", "RULE.md", "SKILL.md", "TODO.md", "skill.contract.yaml"]:
                return

        # Check if child file (should start with underscore)
        is_child_file = depth > 1 and filename.startswith("_")

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
        """Say whether a file name is snake_case.

        :param filename: File name to check.
        :type filename: str
        :return: ``True`` when the name is lowercase snake_case with an extension.
        :rtype: bool
        """
        # Allow special files
        if filename in ["CLAUDE.md", "README.md", "SKILL.md", "settings.json", "keybindings.json"]:
            return True

        # Check pattern: lowercase, underscore-separated, valid extension.
        # A leading underscore is allowed and expected for child files
        # (see _claude_directory_naming.md: "_<aspect>.md" for children).
        pattern = r"^_?[a-z0-9][a-z0-9_]*(\.[a-z0-9]+)$"
        return bool(re.match(pattern, filename))


def check_new_path(file_path: Path, claude_home: Path = CLAUDE_HOME) -> list[dict]:
    """Return the violations a new file at ``file_path`` would cause.

    Paths outside ``claude_home``, or inside a skipped directory (auto-generated or hidden),
    return an empty list — the same files the full scan never looks at.

    :param file_path: Absolute path of the file about to be created.
    :type file_path: Path
    :param claude_home: Root of the Claude config directory.
    :type claude_home: Path
    :return: Violation dicts with keys path, rule, severity and message.
    :rtype: list[dict]
    """
    try:
        rel_path = file_path.relative_to(claude_home)
    except ValueError:
        return []
    parent_dirs = rel_path.parts[:-1]
    if any(part in AUTO_GENERATED_DIRS or part.startswith(".") or part == "node_modules" for part in parent_dirs):
        return []
    validator = FileStructureValidator(claude_home)
    validator._validate_file(file_path, len(parent_dirs))
    return validator.violations


if __name__ == "__main__":
    # --check <claude_home> <file_path>: print one path's violations as JSON (used by the naming hook)
    if len(sys.argv) == 4 and sys.argv[1] == "--check":
        print(json.dumps(check_new_path(Path(sys.argv[3]), Path(sys.argv[2]))))
    else:
        sys.exit("usage: _file_structure_validator.py --check <claude_home> <file_path>")
