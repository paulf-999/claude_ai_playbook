# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-02
# Date updated:      2026-10-02
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────
"""Validates that ``make install`` removes files the repo has deleted or moved since the last install.

The install only ever copied files over the target, so renamed rules, moved tests and deleted skills
stayed behind. On 2026-10-02 a leftover duplicate test broke the live test run, and a stale
``hooks/README.md`` claimed there were no active hooks. Each install now writes ``.install_manifest``
and the next one removes paths on it that the repo no longer ships. Each test runs the real copy,
flatten and prune steps from ``claude_file_utils.sh`` against a fake source and a temp target.
"""

import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[4]
UTILS = REPO_ROOT / "src" / "sh" / "claude" / "helpers" / "claude_file_utils.sh"
INSTALL_SCRIPT = REPO_ROOT / "src" / "sh" / "claude" / "install_claude_files.sh"

SOURCE_FILES = {
    "_rules/a/keep.md": "keep\n",
    "_rules/a/gone.md": "gone\n",
    "_tests/old/test_old.py": "old\n",
    "skills/_g_skills/README.md": "group readme\n",
    "skills/_g_skills/demo/SKILL.md": "demo\n",
    "skills/_g_skills/demo/reference/_phases.md": "phases\n",
    "memory/MEMORY.md": "repo memory\n",
    "TODO.md": "repo todo\n",
}


def make_tree(root: Path, files: dict) -> None:
    """Write a dict of relative paths and contents under a folder.

    :param root: Folder to write into.
    :param files: Relative path to file content.
    """
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text)


def install(tmp_path: Path) -> str:
    """Run the install's copy, flatten and prune steps from the fake source into the target.

    :param tmp_path: Test folder holding ``src/``, ``target/`` and ``home/``.
    :return: The steps' combined output.
    """
    env = {**os.environ, "HOME": str(tmp_path / "home"), "CLAUDE_CONFIG_DIR": str(tmp_path / "target")}
    steps = f'source "{UTILS}" && SOURCE_DIR="{tmp_path / "src"}" && copy_claude_files && flatten_skills'
    done = subprocess.run(
        ["bash", "-c", f"{steps} && prune_removed_files"],
        cwd=REPO_ROOT, env=env, capture_output=True, text=True, timeout=60, check=True,
    )
    return done.stdout + done.stderr


def setup(tmp_path: Path) -> Path:
    """Create the fake source and an empty target, and run a first install.

    :param tmp_path: pytest's temp folder.
    :return: The target folder.
    """
    make_tree(tmp_path / "src", SOURCE_FILES)
    (tmp_path / "home").mkdir()
    (tmp_path / "target").mkdir(exist_ok=True)
    install(tmp_path)
    return tmp_path / "target"


def manifest(target: Path) -> list:
    """Read the target's install manifest.

    :param target: The installed target.
    :return: Its lines.
    """
    return (target / ".install_manifest").read_text().splitlines()


def test_first_install_writes_manifest_and_removes_nothing(tmp_path: Path) -> None:
    """With no manifest yet, a stray file already in the target stays and a manifest is written."""
    make_tree(tmp_path / "target", {"_rules/a/stray.md": "from an older install\n"})
    target = setup(tmp_path)
    assert (target / "_rules/a/stray.md").is_file(), "a first install must not remove anything"
    assert "_rules/a/keep.md" in manifest(target), "the manifest should list installed files"


def test_manifest_maps_skills_to_their_flattened_paths(tmp_path: Path) -> None:
    """Grouped skills are listed where flatten_skills puts them, and a group's own files aren't listed."""
    lines = manifest(setup(tmp_path))
    assert "skills/demo/SKILL.md" in lines, f"flattened skill path missing: {lines}"
    assert not any(line.startswith("skills/_g_skills/") for line in lines), "group paths should not be listed"


def test_manifest_is_sorted_and_leaves_out_user_owned_files(tmp_path: Path) -> None:
    """User-owned entries are never on the manifest, so pruning can't reach them."""
    lines = manifest(setup(tmp_path))
    assert lines == sorted(lines), "the manifest should be sorted"
    assert not any(line.split("/")[0] in ("memory", "TODO.md") for line in lines), f"user-owned listed: {lines}"


def test_file_deleted_from_repo_is_removed(tmp_path: Path) -> None:
    """A file the repo dropped since the last install is removed from the target."""
    target = setup(tmp_path)
    (tmp_path / "src/_rules/a/gone.md").unlink()
    output = install(tmp_path)
    assert not (target / "_rules/a/gone.md").exists(), "a file the repo deleted is still installed"
    assert "Removed (no longer in the repo): _rules/a/gone.md" in output, "the removal should be logged"
    assert (target / "_rules/a/keep.md").is_file(), "a file the repo still ships was removed"


def test_moved_file_leaves_no_copy_behind(tmp_path: Path) -> None:
    """A file moved in the repo ends up only at its new path, so pytest can't collect both."""
    target = setup(tmp_path)
    (tmp_path / "src/_tests/new").mkdir()
    (tmp_path / "src/_tests/old/test_old.py").rename(tmp_path / "src/_tests/new/test_old.py")
    install(tmp_path)
    assert (target / "_tests/new/test_old.py").is_file(), "the moved file is missing at its new path"
    assert not (target / "_tests/old").exists(), "the old copy, or its empty folder, is still there"


def test_removed_skill_is_removed_from_flattened_path(tmp_path: Path) -> None:
    """Deleting a skill from its group removes its flattened folder from the target."""
    target = setup(tmp_path)
    for rel in ("SKILL.md", "reference/_phases.md"):
        (tmp_path / "src/skills/_g_skills/demo" / rel).unlink()
    install(tmp_path)
    assert not (target / "skills/demo").exists(), "the removed skill's folder is still installed"


def test_files_the_user_added_are_kept(tmp_path: Path) -> None:
    """A file the install never wrote survives, even in a folder the repo manages."""
    target = setup(tmp_path)
    make_tree(target, {"_rules/a/mine.md": "mine\n", "projects/-repo/session.jsonl": "{}\n"})
    (tmp_path / "src/_rules/a/gone.md").unlink()
    install(tmp_path)
    assert (target / "_rules/a/mine.md").is_file(), "a file the user added was removed"
    assert (target / "projects/-repo/session.jsonl").is_file(), "runtime data was removed"


def test_user_owned_paths_on_an_old_manifest_are_kept(tmp_path: Path) -> None:
    """Even if an old manifest lists a user-owned file, pruning leaves it alone."""
    target = setup(tmp_path)
    (target / ".install_manifest").write_text("TODO.md\nmemory/MEMORY.md\n")
    install(tmp_path)
    assert (target / "memory/MEMORY.md").is_file(), "pruning removed the user's memory"
    assert (target / "TODO.md").is_file(), "pruning removed the user's TODO.md"


def test_manifest_paths_outside_the_target_are_ignored(tmp_path: Path) -> None:
    """A manifest line that climbs out of the target, or is absolute, never deletes anything."""
    target = setup(tmp_path)
    outside = tmp_path / "home" / "precious.txt"
    outside.write_text("keep\n")
    (target / ".install_manifest").write_text(f"../home/precious.txt\n{outside}\n")
    install(tmp_path)
    assert outside.is_file(), "pruning followed a path outside the target"


def test_folders_still_holding_files_are_kept(tmp_path: Path) -> None:
    """Only folders left empty are removed, never one that still holds files."""
    target = setup(tmp_path)
    (tmp_path / "src/_rules/a/gone.md").unlink()
    install(tmp_path)
    assert (target / "_rules/a").is_dir(), "a folder that still has files was removed"


def test_manifest_is_rewritten_each_install(tmp_path: Path) -> None:
    """After a removal the manifest no longer lists the dropped file."""
    target = setup(tmp_path)
    (tmp_path / "src/_rules/a/gone.md").unlink()
    install(tmp_path)
    assert "_rules/a/gone.md" not in manifest(target), "the manifest still lists a removed file"


def test_install_prunes_after_flattening_and_before_rewriting_paths() -> None:
    """The install runs prune_removed_files once skills are flattened and before paths are rewritten."""
    script = INSTALL_SCRIPT.read_text()
    flatten, prune, rewrite = (script.index(f"    {step}") for step in
                               ("flatten_skills", "prune_removed_files", "rewrite_config_paths"))
    assert flatten < prune < rewrite, "prune_removed_files must run between flatten_skills and rewrite_config_paths"
    assert "Remove files an earlier install added" in script, "the install preview should say it removes files"
