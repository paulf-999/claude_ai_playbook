# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-10
# Date updated:      2026-10-10
# Version:           1.1.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────
"""Validates that ``make install`` moves on-demand rules from ``rules/`` to beside it.

The repo keeps every rule under ``rules/``, with the on-demand set in ``rules/_rules_lazy_load/``.
Claude Code loads every ``.md`` under ``rules/`` by itself, so leaving that folder there once
installed would load ~100 on-demand files every session. Each test runs the real copy, flatten,
relocate and prune steps from ``claude_file_utils.sh`` against a fake source and a temp target.
"""

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
UTILS = REPO_ROOT / "src" / "sh" / "claude" / "helpers" / "claude_file_utils.sh"
INSTALL_SCRIPT = REPO_ROOT / "src" / "sh" / "claude" / "install_claude_files.sh"
WINDOWS_SCRIPT = REPO_ROOT / "src" / "sh" / "claude" / "install_claude_files_windows.sh"
LAZY = "_rules_lazy_load"

SOURCE_FILES = {
    "rules/01_essentials/core.md": "core\n",
    f"rules/{LAZY}/org.md": "org\n",
    f"rules/{LAZY}/pointer.md": "See `~/.claude/_rules_lazy_load/org.md` and `~/.claude/` itself.\n",
    f"rules/{LAZY}/style/_sql.md": "sql\n",
}


def make_tree(root: Path, files: dict[str, str]):
    """Write a dict of relative paths and contents under a folder.

    :param root: Folder to write into.
    :param files: Relative path to file content.
    """
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)


def install(tmp_path: Path, extra: str = "") -> str:
    """Run the install's copy, flatten, relocate and prune steps from the fake source into the target.

    :param tmp_path: Test folder holding ``src/``, ``target/`` and ``home/``.
    :param extra: More steps to run afterwards, e.g. ``" && rewrite_config_paths"``.
    :return: The steps' combined output.
    """
    env = {**os.environ, "HOME": str(tmp_path / "home"), "CLAUDE_CONFIG_DIR": str(tmp_path / "target")}
    steps = (f'source "{UTILS}" && SOURCE_DIR="{tmp_path / "src"}" && copy_claude_files && flatten_skills'
             f" && relocate_lazy_rules && prune_removed_files{extra}")
    done = subprocess.run(["bash", "-c", steps], cwd=REPO_ROOT, env=env,
                          capture_output=True, text=True, timeout=60, check=True)
    return done.stdout + done.stderr


def setup(tmp_path: Path) -> Path:
    """Create the fake source and an empty target, and run a first install.

    :param tmp_path: pytest's temp folder.
    :return: The target folder.
    """
    make_tree(tmp_path / "src", SOURCE_FILES)
    (tmp_path / "home").mkdir()
    (tmp_path / "target").mkdir()
    install(tmp_path)
    return tmp_path / "target"


def test_relocation_is_logged(tmp_path: Path):
    """The install says it moved the folder, so the step is visible in its output."""
    make_tree(tmp_path / "src", SOURCE_FILES)
    (tmp_path / "home").mkdir()
    (tmp_path / "target").mkdir()
    output = install(tmp_path)
    assert f"Moved rules/{LAZY}/ beside rules/" in output, output


def test_nothing_to_move_is_a_no_op(tmp_path: Path):
    """With no lazy folder in the source, the step succeeds and creates nothing."""
    make_tree(tmp_path / "src", {"rules/01_essentials/core.md": "core\n"})
    (tmp_path / "home").mkdir()
    (tmp_path / "target").mkdir()
    output = install(tmp_path)
    assert not (tmp_path / "target" / LAZY).exists(), "an empty lazy folder was created"
    assert "Moved rules/" not in output, "the step claimed a move with nothing to move"


def test_leftover_copy_under_rules_is_moved_next_time(tmp_path: Path):
    """If an install stopped before relocating, the next one moves the leftover copy and clears rules/."""
    target = setup(tmp_path)
    make_tree(target, {f"rules/{LAZY}/stray.md": "stray\n"})
    install(tmp_path)
    assert (target / LAZY / "stray.md").is_file(), "the leftover file wasn't moved beside rules/"
    assert not (target / "rules" / LAZY).exists(), "the leftover copy is still under rules/"


def test_pointers_in_moved_rules_are_rewritten(tmp_path: Path):
    """Paths in the relocated folder point at the real config folder, though the repo has no top-level copy."""
    make_tree(tmp_path / "src", SOURCE_FILES)
    (tmp_path / "home").mkdir()
    (tmp_path / "home" / "claude").mkdir()
    env_target = tmp_path / "home" / "claude"
    env = {**os.environ, "HOME": str(tmp_path / "home"), "CLAUDE_CONFIG_DIR": str(env_target)}
    steps = (f'source "{UTILS}" && SOURCE_DIR="{tmp_path / "src"}" && copy_claude_files && flatten_skills'
             " && relocate_lazy_rules && rewrite_config_paths")
    subprocess.run(["bash", "-c", steps], cwd=REPO_ROOT, env=env,
                   capture_output=True, text=True, timeout=60, check=True)
    text = (env_target / LAZY / "pointer.md").read_text()
    assert "`~/claude/_rules_lazy_load/org.md`" in text, f"pointer not rewritten: {text}"
    assert "`~/.claude/` itself" in text, "prose about Claude Code's own folder was changed"


def test_lazy_rules_sit_beside_rules(tmp_path: Path):
    """On-demand rules land at the target's top level, and rules/ keeps only always-on rules."""
    target = setup(tmp_path)
    assert (target / LAZY / "org.md").read_text() == "org\n", "org.md missing from the top-level lazy folder"
    assert (target / LAZY / "style/_sql.md").is_file(), "nested lazy file missing"
    assert not (target / "rules" / LAZY).exists(), "the lazy folder is still under rules/"
    assert (target / "rules/01_essentials/core.md").is_file(), "an always-on rule went missing"


def test_manifest_lists_lazy_rules_at_their_installed_path(tmp_path: Path):
    """The manifest names lazy files where the install leaves them, not where the repo keeps them."""
    lines = (setup(tmp_path) / ".install_manifest").read_text().splitlines()
    assert f"{LAZY}/org.md" in lines, f"installed lazy path missing: {lines}"
    assert not any(line.startswith(f"rules/{LAZY}/") for line in lines), "repo-layout lazy paths listed"


def test_reinstall_keeps_lazy_rules(tmp_path: Path):
    """A second install prunes nothing the repo still ships."""
    target = setup(tmp_path)
    output = install(tmp_path)
    assert "Removed (no longer in the repo)" not in output, output
    assert (target / LAZY / "org.md").is_file(), "a re-install removed a lazy rule"


def test_reinstall_merges_into_existing_folder(tmp_path: Path):
    """A file you added to the installed lazy folder survives, and nothing nests inside it."""
    target = setup(tmp_path)
    make_tree(target, {f"{LAZY}/mine.md": "mine\n"})
    install(tmp_path)
    assert (target / LAZY / "mine.md").is_file(), "a file the user added was removed"
    assert not (target / LAZY / LAZY).exists(), "the copy nested a second lazy folder inside the first"


def test_lazy_rule_removed_from_repo_is_pruned(tmp_path: Path):
    """Deleting a lazy rule in the repo removes it from its installed path."""
    target = setup(tmp_path)
    (tmp_path / f"src/rules/{LAZY}/org.md").unlink()
    install(tmp_path)
    assert not (target / LAZY / "org.md").exists(), "a lazy rule the repo deleted is still installed"


def test_install_relocates_after_flattening_and_before_pruning():
    """The install moves the lazy folder once skills are flattened, before anything else reads the layout."""
    script = INSTALL_SCRIPT.read_text()
    flatten, relocate, prune = (script.index(f"    {step}") for step in
                                ("flatten_skills", "relocate_lazy_rules", "prune_removed_files"))
    assert flatten < relocate < prune, "relocate_lazy_rules must run between flatten_skills and prune_removed_files"


def test_windows_install_relocates_and_clears_the_old_folder():
    """The Windows sync moves the folder too, and clears the installed copy first, since it isn't a source item."""
    windows = WINDOWS_SCRIPT.read_text()
    flatten, relocate = windows.index("    flatten_skills"), windows.index("    relocate_lazy_rules")
    assert flatten < relocate, "the Windows install must move the lazy folder after flattening skills"
    assert '"${RETIRED_ITEMS[@]}" "${LAZY_RULES_NAME}"' in windows, "Windows sync no longer clears the lazy folder"
