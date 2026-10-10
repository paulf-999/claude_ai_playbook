# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-10
# Version:           1.2.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────
"""Validates that installing into a config folder other than ``~/.claude`` leaves it working.

``@`` imports can't read ``CLAUDE_CONFIG_DIR``, so the repo's ``@~/.claude/`` imports break in a
config at ``~/claude``. The install now rewrites paths into the installed folder to its real
prefix, and sets ``plansDirectory`` to its ``_plans/``. Each test runs the real install steps
from ``claude_file_utils.sh`` against a temp ``HOME``.
"""

import json
import os
import re
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[4]
UTILS = REPO_ROOT / "src" / "sh" / "claude" / "helpers" / "claude_file_utils.sh"
SCRIPTS = REPO_ROOT / "src" / "sh" / "claude"
TESTS_DIR = REPO_ROOT / "src" / "claude" / "_tests"
REACHABILITY_TEST = TESTS_DIR / "rules" / "02_claude_standards" / "test_always_on_reachability.py"
# The same order install_claude_files runs; creating the target first matters, since cp -R into a
# missing folder behaves differently on macOS and Linux
STEPS = (
    "create_target_dir_if_missing && backup_target_dir copy && copy_claude_files && flatten_skills"
    " && relocate_lazy_rules && rewrite_config_paths"
)
IMPORT = re.compile(r"^@(\S+\.md)\s*$", re.M)
SQL_GUIDE = Path("rules/04_path_scoped/style_guide_standards/sql.md")
PORTABLE = Path("rules/02_claude_standards/portable_paths.md")
BARE_PROSE = "`~/.claude/` exists (Claude Code's own state dir"


def install(home: Path, target: Path, steps: str = STEPS):
    """Run the install steps from ``claude_file_utils.sh`` into ``target``.

    :param home: Temp ``HOME``.
    :param target: Temp ``CLAUDE_CONFIG_DIR``.
    :param steps: Shell functions to run after sourcing the helpers.
    """
    env = {**os.environ, "HOME": str(home), "CLAUDE_CONFIG_DIR": str(target)}
    subprocess.run(["bash", "-c", f'source "{UTILS}" && {steps}'], cwd=REPO_ROOT, env=env,
                   capture_output=True, text=True, timeout=60, check=True)


@pytest.fixture(scope="module")
def custom(tmp_path_factory) -> dict[str, Path]:
    """Install into ``$HOME/claude`` once, with a seeded user-owned file and runtime file.

    :param tmp_path_factory: pytest's module-scoped temp factory.
    :return: ``home`` and ``target`` paths.
    """
    home = tmp_path_factory.mktemp("custom")
    target = home / "claude"
    (target / "memory").mkdir(parents=True)
    (target / "memory" / "MEMORY.md").write_text("see ~/.claude/_rules/x.md\n")
    (target / "projects").mkdir()
    (target / "projects" / "note.md").write_text("see ~/.claude/_rules/x.md\n")
    install(home, target)
    return {"home": home, "target": target}


def imports(path: Path) -> list[str]:
    """Return the ``@`` import targets in a file.

    :param path: A markdown file.
    :return: Import paths, without the ``@``.
    """
    return IMPORT.findall(path.read_text())


# --- Imports resolve in a custom folder ---

def test_no_default_prefix_imports_left(custom: dict[str, Path]):
    """No installed file has an import line that still points at ``~/.claude/``."""
    left = [str(p) for p in custom["target"].rglob("*.md") if any(i.startswith("~/.claude/") for i in imports(p))]
    assert not left, f"files still importing from ~/.claude/: {left[:5]}"


def test_every_import_resolves(custom: dict[str, Path]):
    """Each import in CLAUDE.md points at a real file in the installed folder."""
    found = imports(custom["target"] / "CLAUDE.md")
    assert len(found) >= 2, f"expected the memory and aliases imports, found {len(found)}"
    missing = [i for i in found if not (custom["home"] / i.removeprefix("~/")).is_file()]
    assert not missing, f"imports that don't resolve: {missing}"


def test_always_on_rules_reachable(custom: dict[str, Path]):
    """The repo's reachability test passes against the installed folder."""
    env = {**os.environ, "CLAUDE_CONFIG_DIR": str(custom["target"])}
    command = ["python3", "-m", "pytest", str(REACHABILITY_TEST), "-q", "--no-cov", "-p", "no:cacheprovider"]
    result = subprocess.run(command, cwd=REPO_ROOT, env=env, capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stdout[-1500:]


def test_pointers_use_the_real_folder(custom: dict[str, Path]):
    """Read-on-demand pointers in rules point at the installed folder too."""
    text = (custom["target"] / SQL_GUIDE).read_text()
    pointer = "`~/claude/_rules_lazy_load/style_guide_standards/sql/formatting.md`"
    assert pointer in text, "sql.md pointer not rewritten"
    assert "`~/.claude/_rules_lazy_load/" not in text, "sql.md still points at ~/.claude/"


# --- What the rewrite leaves alone ---

def test_prose_about_the_default_folder_is_kept(custom: dict[str, Path]):
    """A bare mention of Claude Code's own ``~/.claude/`` folder isn't rewritten."""
    assert BARE_PROSE in (REPO_ROOT / "src" / "claude" / PORTABLE).read_text(), "fixture text changed in the repo"
    assert BARE_PROSE in (custom["target"] / PORTABLE).read_text(), "prose about ~/.claude/ itself was rewritten"


def test_user_owned_and_runtime_files_untouched(custom: dict[str, Path]):
    """The rewrite never edits memory/ or runtime data."""
    for rel in ("memory/MEMORY.md", "projects/note.md"):
        assert (custom["target"] / rel).read_text() == "see ~/.claude/_rules/x.md\n", f"{rel} was rewritten"


def test_plans_directory_is_the_targets(custom: dict[str, Path]):
    """plansDirectory points at the installed folder's own _plans/."""
    settings = json.loads((custom["target"] / "settings.json").read_text())
    assert settings["plansDirectory"] == str(custom["target"] / "_plans"), settings["plansDirectory"]


def test_rewrite_is_idempotent(custom: dict[str, Path]):
    """Running the rewrite again changes nothing."""
    before = (custom["target"] / "CLAUDE.md").read_text()
    install(custom["home"], custom["target"], "rewrite_config_paths")
    assert (custom["target"] / "CLAUDE.md").read_text() == before, "a second rewrite changed CLAUDE.md"


# --- Other locations ---

def test_default_folder_is_left_as_shipped(tmp_path: Path):
    """In ``~/.claude`` imports stay as shipped, and plansDirectory is still made absolute."""
    target = tmp_path / ".claude"
    install(tmp_path, target)
    shipped = (REPO_ROOT / "src" / "claude" / "CLAUDE.md").read_text()
    assert (target / "CLAUDE.md").read_text() == shipped, "CLAUDE.md changed in the default folder"
    settings = json.loads((target / "settings.json").read_text())
    assert settings["plansDirectory"] == str(target / "_plans"), settings["plansDirectory"]


def test_folder_outside_home_uses_absolute_paths(tmp_path: Path):
    """A config outside HOME gets absolute import paths."""
    home, target = tmp_path / "home", tmp_path / "elsewhere" / "cfg"
    home.mkdir()
    target.mkdir(parents=True)
    install(home, target)
    found = imports(target / "CLAUDE.md")
    assert found and all(i.startswith(f"{target}/") for i in found), found[:3]


def test_scripts_that_rewrite():
    """Install and update rewrite paths, while the Windows sync, which targets another machine's folder, doesn't."""
    for name in ("install_claude_files.sh", "update_claude_files.sh"):
        assert "rewrite_config_paths" in (SCRIPTS / name).read_text(), f"{name} doesn't rewrite paths"
    assert "rewrite_config_paths" not in (SCRIPTS / "install_claude_files_windows.sh").read_text()
