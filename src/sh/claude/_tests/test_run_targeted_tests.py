# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-02
# Date updated:      2026-10-02
# Version:           1.0.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────
"""Validates which tests the pre-commit targeted-test hook runs for each kind of staged file.

``run_targeted_tests.sh`` used to map only ``src/claude/`` paths, so changing an installer helper
under ``src/sh/`` ran no tests until CI. Each test stages files in a throwaway git repo and runs the
real hook with a fake ``pytest`` on ``PATH`` that records the paths it was given.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[4]
HOOK = REPO_ROOT / "src" / "sh" / "pre_commit_hooks" / "run_targeted_tests.sh"
WHOLE, SH = "src/claude/_tests/", "src/sh/claude/_tests/"

# git commit sets GIT_INDEX_FILE and friends for its hooks; drop them so the throwaway repo is used
CLEAN_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """Create a throwaway git repo and a fake ``pytest`` that records its arguments.

    :param tmp_path: pytest's temp folder.
    :return: The repo folder.
    """
    root = tmp_path / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "-q", str(root)], env=CLEAN_ENV, check=True)
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake = bin_dir / "pytest"
    fake.write_text(f'#!/bin/bash\necho "$@" > "{tmp_path / "args.txt"}"\nexit "${{FAKE_PYTEST_EXIT:-0}}"\n')
    fake.chmod(0o755)
    return root


def run_hook(repo: Path, *staged: str, pytest_exit: int = 0) -> tuple[int, list[str] | None]:
    """Stage the given files and run the hook.

    :param repo: The throwaway repo.
    :param staged: Repo-relative paths to create and stage.
    :param pytest_exit: Exit code for the fake pytest.
    :return: ``(exit code, list of paths pytest was given, or None if it never ran)``.
    """
    for rel in staged:
        (repo / rel).parent.mkdir(parents=True, exist_ok=True)
        (repo / rel).write_text("x\n")
        subprocess.run(["git", "-C", str(repo), "add", rel], env=CLEAN_ENV, check=True)
    env = {**CLEAN_ENV, "PATH": f"{repo.parent / 'bin'}:{os.environ['PATH']}", "FAKE_PYTEST_EXIT": str(pytest_exit)}
    done = subprocess.run(["bash", str(HOOK)], cwd=repo, env=env, capture_output=True, text=True, timeout=60)
    args_file = repo.parent / "args.txt"
    return done.returncode, (args_file.read_text().split() if args_file.exists() else None)


def test_nothing_staged_runs_nothing(repo: Path):
    """With nothing staged the hook exits cleanly without running pytest."""
    assert run_hook(repo) == (0, None), "an empty commit should run no tests"


def test_untested_file_runs_nothing(repo: Path):
    """A staged file no test covers, such as a doc, runs no tests."""
    assert run_hook(repo, "docs/readme.md") == (0, None), "a doc change should run no tests"


def test_installer_change_runs_sh_tests(repo: Path):
    """Changing an installer helper runs the shell tooling tests."""
    code, args = run_hook(repo, "src/sh/claude/helpers/claude_file_utils.sh")
    assert code == 0, "the hook should pass when pytest passes"
    assert args == [SH], f"expected only the shell tooling tests, got {args}"


def test_skill_change_runs_skill_tests(repo: Path):
    """Changing a skill runs only the skill tests, as before."""
    assert run_hook(repo, "src/claude/skills/demo/SKILL.md")[1] == ["src/claude/_tests/skills/"]


def test_rule_and_hook_changes_run_their_folders(repo: Path):
    """A rule and a hook together queue both their test folders."""
    args = run_hook(repo, "src/claude/_rules/a.md", "src/claude/hooks/h.sh")[1]
    assert sorted(args) == ["src/claude/_tests/hooks/", "src/claude/_tests/rules/"], f"got {args}"


def test_whole_suite_replaces_its_own_subfolders(repo: Path):
    """Once the whole config suite is queued, its subfolders are dropped so pytest still runs everything."""
    args = run_hook(repo, "src/claude/_rules/a.md", "src/claude/_tests/test_x.py")[1]
    assert args == [WHOLE], f"subfolders alongside the whole suite make pytest skip tests, got {args}"


def test_whole_suite_keeps_the_sh_tests(repo: Path):
    """The whole config suite never swallows the shell tooling tests, which live outside it."""
    args = run_hook(repo, "src/sh/claude/helpers/mcp_toggle.py", "src/claude/_tests/test_x.py")[1]
    assert sorted(args) == sorted([SH, WHOLE]), f"the shell tooling tests were dropped, got {args}"


def test_sh_tests_survive_whole_suite_queued_first(repo: Path):
    """Order doesn't matter: a later src/sh change still adds its tests after the whole suite."""
    args = run_hook(repo, "src/claude/_tests/a_first.py", "src/sh/z_last.sh")[1]
    assert SH in args and WHOLE in args, f"got {args}"
    assert len(args) == 2, f"each suite should be passed once, got {args}"


def test_pytest_config_change_runs_both_suites(repo: Path):
    """Changing pytest.ini or requirements.txt runs every test, config and shell tooling alike."""
    for staged in ("pytest.ini", "requirements.txt"):
        args = run_hook(repo, staged)[1]
        assert sorted(args) == sorted([SH, WHOLE]), f"{staged} should run both suites, got {args}"


def test_duplicate_paths_are_passed_once(repo: Path):
    """Several staged files in one area queue its tests only once."""
    args = run_hook(repo, "src/sh/a.sh", "src/sh/b.sh", "src/sh/claude/c.py")[1]
    assert args == [SH], f"got {args}"


def test_failing_tests_block_the_commit(repo: Path):
    """When pytest fails the hook exits non-zero, so pre-commit blocks the commit."""
    code, args = run_hook(repo, "src/sh/a.sh", pytest_exit=1)
    assert args == [SH], "pytest should still have run"
    assert code == 1, "a failing test run must block the commit"


def test_hook_points_pytest_at_the_repo_config(repo: Path, tmp_path: Path):
    """The hook sets CLAUDE_CONFIG_DIR to the repo's own src/claude before running pytest."""
    fake = tmp_path / "bin" / "pytest"
    fake.write_text(f'#!/bin/bash\necho "$CLAUDE_CONFIG_DIR" > "{tmp_path / "config.txt"}"\n')
    run_hook(repo, "src/sh/a.sh")
    toplevel = subprocess.run(["git", "-C", str(repo), "rev-parse", "--show-toplevel"],
                              env=CLEAN_ENV, capture_output=True, text=True, check=True).stdout.strip()
    expected = Path(toplevel) / "src" / "claude"
    assert (tmp_path / "config.txt").read_text().strip() == str(expected), "pytest should check the repo's config"
