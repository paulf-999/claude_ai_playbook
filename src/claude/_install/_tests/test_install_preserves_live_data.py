# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-02
# Version:           1.1.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────
"""Validates that installing over a live config keeps its runtime data and user-owned files.

``make install`` used to move the whole config dir into a backup before copying the repo in,
which stranded transcripts, history and app state in the backup, and it overwrote the user's
``memory/`` and ``TODO.md``. Each test runs the real backup and copy steps from
``claude_file_utils.sh`` against a temp ``HOME`` and ``CLAUDE_CONFIG_DIR``.
"""

import os
import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[4]
UTILS = REPO_ROOT / "src" / "sh" / "claude" / "helpers" / "claude_file_utils.sh"
INSTALL_SCRIPT = REPO_ROOT / "src" / "sh" / "claude" / "install_claude_files.sh"
SOURCE_DIR = REPO_ROOT / "src" / "claude"
INSTALL_STEPS = "backup_target_dir copy && copy_claude_files && flatten_skills"

# Files a live config holds that the repo never ships, or that the user owns once installed
SEEDED = {
    "projects/-repo/session.jsonl": '{"type": "user"}\n',
    ".claude.json": '{"mcpServers": {}}\n',
    "history.jsonl": '{"display": "hi"}\n',
    "memory/MEMORY.md": "# My memory\n",
    "memory/feedback_extra.md": "kept\n",
    "TODO.md": "# My TODOs\n",
    "_plans/2026_10_01_plan.md": "# Plan\n",
    "settings.local.json": '{"permissions": {}}\n',
}


def run_install_steps(home: Path, target: Path) -> subprocess.CompletedProcess:
    """Source the helpers and run the install's backup and copy steps.

    :param home: Temp ``HOME``, where the backup lands.
    :param target: Temp ``CLAUDE_CONFIG_DIR``.
    :return: The finished process.
    """
    env = {**os.environ, "HOME": str(home), "CLAUDE_CONFIG_DIR": str(target)}
    return subprocess.run(
        ["bash", "-c", f'source "{UTILS}" && {INSTALL_STEPS}'],
        cwd=REPO_ROOT, env=env, capture_output=True, text=True, timeout=60, check=True,
    )


@pytest.fixture(scope="module")
def live(tmp_path_factory) -> dict[str, Path]:
    """Install over a seeded live config once, for every test in this module.

    :param tmp_path_factory: pytest's module-scoped temp factory.
    :return: ``home`` and ``target`` paths after the install.
    """
    root = tmp_path_factory.mktemp("live")
    home, target = root / "home", root / "claude"
    home.mkdir()
    for rel, text in SEEDED.items():
        (target / rel).parent.mkdir(parents=True, exist_ok=True)
        (target / rel).write_text(text)
    (target / "settings.json").write_text('{"stale": true}\n')
    run_install_steps(home, target)
    return {"home": home, "target": target}


def is_user_owned(name: str) -> bool:
    """Ask the shell helper whether a top-level entry is user-owned.

    :param name: Top-level entry name.
    :return: True when ``is_user_owned`` returns 0.
    """
    result = subprocess.run(
        ["bash", "-c", f'source "{UTILS}" && is_user_owned "{name}"'],
        cwd=REPO_ROOT, env={**os.environ, "CLAUDE_CONFIG_DIR": "/tmp/unused"}, timeout=30,
    )
    return result.returncode == 0


# --- Runtime data survives ---

def test_transcripts_survive(live: dict[str, Path]):
    """Session transcripts the usage audit reads are still in place, unchanged."""
    path = live["target"] / "projects/-repo/session.jsonl"
    assert path.read_text() == SEEDED["projects/-repo/session.jsonl"], "transcripts were moved or changed"


def test_app_state_survives(live: dict[str, Path]):
    """Claude Code's own state files stay where they were."""
    for rel in (".claude.json", "history.jsonl"):
        assert (live["target"] / rel).read_text() == SEEDED[rel], f"{rel} was moved or changed"


# --- User-owned files are kept ---

def test_memory_is_kept_whole(live: dict[str, Path]):
    """The user's memory files are neither overwritten nor reduced to the repo's one file."""
    memory = live["target"] / "memory"
    assert (memory / "MEMORY.md").read_text() == SEEDED["memory/MEMORY.md"], "MEMORY.md was overwritten"
    assert (memory / "feedback_extra.md").is_file(), "a memory file only the user has was lost"


def test_todo_plans_and_local_settings_are_kept(live: dict[str, Path]):
    """TODO.md, _plans/ and settings.local.json keep the user's content."""
    for rel in ("TODO.md", "_plans/2026_10_01_plan.md", "settings.local.json"):
        assert (live["target"] / rel).read_text() == SEEDED[rel], f"{rel} was overwritten"


# --- Repo files are installed ---

def test_repo_managed_files_are_updated(live: dict[str, Path]):
    """Files the repo manages replace the stale live copies."""
    target = live["target"]
    for rel in ("settings.json", "CLAUDE.md"):
        assert (target / rel).read_text() == (SOURCE_DIR / rel).read_text(), f"{rel} was not updated from the repo"


def test_skills_are_flattened(live: dict[str, Path]):
    """Skill group folders are flattened, as before."""
    groups = [p.name for p in (live["target"] / "skills").glob("_*") if p.is_dir()]
    assert not groups, f"skill group folders left behind: {groups}"


def test_reinstall_does_not_nest_skills(tmp_path: Path):
    """Installing over already-flattened skills merges them, never nesting skills/<name>/<name>/.

    GNU cp copies ``src/`` into an existing ``dest`` as ``dest/src``, so on Linux every reinstall
    used to add another nested copy of each skill.
    """
    home, target = tmp_path / "home", tmp_path / "claude"
    home.mkdir()
    target.mkdir()
    run_install_steps(home, target)
    run_install_steps(home, target)
    skills = [p for p in (target / "skills").iterdir() if p.is_dir() and not p.name.startswith(".")]
    assert skills, "no skills were installed"
    nested = [p.name for p in skills if (p / p.name).is_dir()]
    assert not nested, f"skills nested inside themselves after a reinstall: {nested}"


def test_backup_is_a_copy_not_a_move(live: dict[str, Path]):
    """The backup holds a copy of the live data, and the target keeps the original."""
    backups = list(live["home"].glob(".claude_backup_*"))
    assert len(backups) == 1, f"expected one backup, found {len(backups)}"
    assert (backups[0] / "projects/-repo/session.jsonl").is_file(), "the backup is missing the transcripts"
    assert (live["target"] / "projects").is_dir(), "the target lost its transcripts to the backup"


def test_first_install_gets_the_repo_defaults(tmp_path: Path):
    """With nothing installed yet, user-owned files come from the repo."""
    home, target = tmp_path / "home", tmp_path / "claude"
    home.mkdir()
    target.mkdir()
    run_install_steps(home, target)
    assert (target / "memory" / "MEMORY.md").is_file(), "a first install should get the repo's MEMORY.md"
    todo = (SOURCE_DIR / "TODO.md").read_text()
    assert (target / "TODO.md").read_text() == todo, "a first install should get the repo's TODO.md"


# --- The user-owned list and the scripts ---

def test_user_owned_names_are_recognised():
    """is_user_owned accepts each listed name and rejects repo-managed ones."""
    for name in ("memory", "TODO.md", "_plans", "settings.local.json"):
        assert is_user_owned(name), f"{name} should be user-owned"
    for name in ("_rules", "settings.json", "memory_extra"):
        assert not is_user_owned(name), f"{name} should be repo-managed"


def test_install_never_moves_the_target():
    """The install backs up by copy, and the helpers no longer offer a move mode."""
    assert 'backup_target_dir "copy"' in INSTALL_SCRIPT.read_text(), "install must back up by copy"
    assert not re.search(r'^\s*mv "\$\{TARGET_DIR\}"', UTILS.read_text(), re.M), "a mv of TARGET_DIR is back"
