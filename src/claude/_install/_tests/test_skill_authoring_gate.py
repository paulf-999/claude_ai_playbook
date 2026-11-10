# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-11-10
# Date updated:      2026-11-10
# Version:           1.0.0
# Test quality score: 8/10
# Test complexity score: 4/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────
"""Validates which Python the skill authoring gate runs, and that a scorer crash is shown.

``skill_authoring_gate.sh`` used to run bare ``python3`` and discard the complexity scorer's output,
so a Python without PyYAML failed every skill with no reason given. Each test copies the real hook
into a throwaway tree with stub scripts and a fake ``venv/bin/python``, then runs it.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[4]
HOOK = REPO_ROOT / "src" / "sh" / "pre_commit_hooks" / "skill_authoring_gate.sh"


@pytest.fixture
def tree(tmp_path: Path) -> Path:
    """Build a throwaway repo tree holding the hook, stub linter and scorer, and one skill.

    :param tmp_path: pytest's temp folder.
    :return: The tree's root folder.
    """
    hook_dir = tmp_path / "src" / "sh" / "pre_commit_hooks"
    hook_dir.mkdir(parents=True)
    shutil.copy(HOOK, hook_dir / HOOK.name)
    for script in ("_lint_scripts/lint_skill_authoring_gate.py", "_audit_scripts/audit_skill_complexity.py"):
        stub = tmp_path / "src" / "claude" / "scripts" / script
        stub.parent.mkdir(parents=True)
        stub.write_text("")
    skill = tmp_path / "src" / "claude" / "skills" / "_demo" / "demo_skill"
    skill.mkdir(parents=True)
    (skill / "skill.contract.yaml").write_text("name: demo_skill\n")
    return tmp_path


def add_fake_venv_python(tree: Path, body: str) -> None:
    """Write an executable ``venv/bin/python`` that runs the given bash body.

    :param tree: The throwaway tree.
    :param body: Bash lines the fake interpreter runs, given the script path as ``$1``.
    """
    python = tree / "venv" / "bin" / "python"
    python.parent.mkdir(parents=True)
    python.write_text(f"#!/bin/bash\n{body}\n")
    python.chmod(0o755)


def run_gate(tree: Path) -> subprocess.CompletedProcess[str]:
    """Run the copied hook and capture its output."""
    hook = tree / "src" / "sh" / "pre_commit_hooks" / HOOK.name
    return subprocess.run(["bash", str(hook)], capture_output=True, text=True, check=False)


def test_gate_uses_venv_python_when_present(tree: Path) -> None:
    """The gate runs both scripts with the repo venv's Python and passes when they succeed."""
    calls = tree / "calls.txt"
    add_fake_venv_python(tree, f'echo "$1" >> "{calls}"\nexit 0')

    result = run_gate(tree)

    assert result.returncode == 0, result.stdout
    ran = calls.read_text()
    assert "lint_skill_authoring_gate.py" in ran
    assert "audit_skill_complexity.py" in ran


def test_scorer_crash_is_shown_not_hidden(tree: Path) -> None:
    """A scorer that crashes blocks the commit and its error reaches the output."""
    add_fake_venv_python(
        tree,
        'case "$1" in *audit_skill_complexity.py) echo "ModuleNotFoundError: No module named \'yaml\'"; exit 1;; esac',
    )

    result = run_gate(tree)

    assert result.returncode == 1
    assert "Complexity check failed for demo_skill" in result.stdout
    assert "No module named 'yaml'" in result.stdout
