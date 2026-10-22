# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-22
# Date updated:      2026-10-22
# Version:           1.0.0
# Test quality score: 10/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Validates that every playbook script stops early, with a clear message, on Python older than 3.10.

Each script carries a top-level ``if sys.version_info < (3, 10):`` check that calls
``sys.exit``, placed before every import except ``__future__`` and ``sys``, so an old
Python reports the version instead of failing on a library import or newer syntax.
"""

import ast
from pathlib import Path

from _shared_paths import CLAUDE_DIR

MINIMUM_VERSION = (3, 10)

# The folders the playbook installs its own Python into; plugins/ holds third-party
# plugin code in subfolders, so only its top-level files are the playbook's
RECURSIVE_ROOTS = ("scripts", "skills", "_install/helpers")
TOP_LEVEL_ROOTS = ("plugins",)
SKIPPED_PARTS = {"_tests", "__pycache__"}


def find_scripts(config_dir: Path) -> list[Path]:
    """List the playbook's own Python scripts under config_dir, sorted."""
    found = []
    for root in RECURSIVE_ROOTS:
        found.extend((config_dir / root).rglob("*.py"))
    for root in TOP_LEVEL_ROOTS:
        found.extend((config_dir / root).glob("*.py"))

    def wanted(path: Path) -> bool:
        parts = path.relative_to(config_dir).parts
        # Hidden folders (e.g. skills/.trash/) hold discarded copies, not live scripts
        hidden = any(part.startswith(".") for part in parts)
        return path.name != "__init__.py" and not hidden and not SKIPPED_PARTS.intersection(parts)

    return sorted(path for path in found if wanted(path))


def _is_guard(node: ast.stmt) -> bool:
    """Say whether node is ``if sys.version_info < (3, 10):`` with a ``sys.exit`` call in its body."""
    if not isinstance(node, ast.If) or not isinstance(node.test, ast.Compare):
        return False
    test = node.test
    left_ok = ast.unparse(test.left) == "sys.version_info"
    op_ok = len(test.ops) == 1 and isinstance(test.ops[0], ast.Lt)
    try:
        version_ok = ast.literal_eval(test.comparators[0]) == MINIMUM_VERSION
    except ValueError:
        version_ok = False
    exits = any(
        isinstance(call, ast.Call) and ast.unparse(call.func) == "sys.exit"
        for statement in node.body
        for call in ast.walk(statement)
    )
    return left_ok and op_ok and version_ok and exits


def _is_allowed_early_import(node: ast.stmt) -> bool:
    """Say whether node is an import allowed above the check: ``__future__`` or bare ``sys``."""
    if isinstance(node, ast.ImportFrom):
        return node.module == "__future__"
    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names] == ["sys"]
    return False


def find_guard_problem(script: Path) -> str | None:
    """Explain what is wrong with a script's version check.

    :return: A one-line reason, or None when the check is present and comes before other imports.
    """
    tree = ast.parse(script.read_text(encoding="utf-8"), filename=str(script))
    for node in tree.body:
        if _is_guard(node):
            return None
        if isinstance(node, (ast.Import, ast.ImportFrom)) and not _is_allowed_early_import(node):
            return f"line {node.lineno} imports before the Python {MINIMUM_VERSION[0]}.{MINIMUM_VERSION[1]} check"
    return f"no top-level 'if sys.version_info < {MINIMUM_VERSION}:' check that calls sys.exit"


GUARD = (
    "import sys\n\n"
    "if sys.version_info < (3, 10):  # pragma: no cover\n"
    '    sys.exit("This script needs Python 3.10 or newer.")\n'
)


def write_script(path: Path, body: str) -> Path:
    """Write a fake script made of a docstring followed by body, and return its path."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('"""Fake script."""\n\n' + body, encoding="utf-8")
    return path


# ── live config ───────────────────────────────────────────────────────────────


def test_live_scripts_found():
    """The scan finds the scripts folder's scripts, so a wrong path can't pass vacuously."""
    scripts = find_scripts(CLAUDE_DIR)
    assert any(path.parent.parent.name == "scripts" for path in scripts), f"No scripts found under {CLAUDE_DIR}"


def test_live_scripts_check_python_version():
    """Every playbook script has the version check before its other imports."""
    problems = [
        f"{script.relative_to(CLAUDE_DIR)}: {problem}"
        for script in find_scripts(CLAUDE_DIR)
        if (problem := find_guard_problem(script))
    ]
    assert problems == [], "Scripts missing the Python version check:\n" + "\n".join(problems)


# ── checker behaviour ─────────────────────────────────────────────────────────


def test_guarded_script_passes(tmp_path):
    """A check after the docstring and a __future__ import is accepted."""
    script = write_script(tmp_path / "ok.py", "from __future__ import annotations\n\n" + GUARD + "\nimport json\n")
    assert find_guard_problem(script) is None, "A correctly placed check should pass"


def test_missing_guard_flagged(tmp_path):
    """A script with no check is flagged."""
    script = write_script(tmp_path / "bare.py", "import json\n")
    assert "imports before" in find_guard_problem(script), "An import with no check above it should be flagged"


def test_script_without_imports_flagged(tmp_path):
    """A script with no imports and no check is still flagged."""
    script = write_script(tmp_path / "empty.py", "print('hi')\n")
    assert "no top-level" in find_guard_problem(script), "A script with no check should be flagged"


def test_wrong_version_flagged(tmp_path):
    """A check against an older minimum, such as 3.9, doesn't count."""
    script = write_script(tmp_path / "old.py", GUARD.replace("(3, 10)", "(3, 9)") + "\nimport json\n")
    assert find_guard_problem(script) is not None, "A (3, 9) check should be flagged"


def test_guard_after_other_import_flagged(tmp_path):
    """A check placed after another import comes too late."""
    script = write_script(tmp_path / "late.py", "import json\n" + GUARD)
    assert "line 3 imports before" in find_guard_problem(script), find_guard_problem(script)


def test_guard_without_exit_flagged(tmp_path):
    """A check that only prints, without sys.exit, doesn't count."""
    script = write_script(tmp_path / "soft.py", GUARD.replace("sys.exit", "print") + "\nimport json\n")
    assert find_guard_problem(script) is not None, "A check that doesn't exit should be flagged"


def test_scan_skips_tests_hidden_and_plugin_subfolders(tmp_path):
    """Tests, hidden folders, __init__.py and third-party plugin code are left out of the scan."""
    kept = write_script(tmp_path / "scripts" / "_lint_scripts" / "lint_x.py", "")
    write_script(tmp_path / "skills" / "_tests" / "test_x.py", "")
    write_script(tmp_path / "skills" / ".trash" / "old.py", "")
    write_script(tmp_path / "skills" / "pkg" / "__init__.py", "")
    write_script(tmp_path / "plugins" / "cache" / "vendor.py", "")
    patch = write_script(tmp_path / "plugins" / "patch.py", "")
    assert find_scripts(tmp_path) == sorted([kept, patch]), find_scripts(tmp_path)
