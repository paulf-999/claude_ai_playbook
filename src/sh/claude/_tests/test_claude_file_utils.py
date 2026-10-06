# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-05
# Version:           2.0.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────
"""Tests for ``flatten_skills`` in ``claude_file_utils.sh``.

Goal: after install or update, every grouped skill sits flat at
``skills/<name>`` with its latest content, and no ``_<group>_skills/`` folder
is left behind. Regression for the update path (found 2026-10-01): ``cp -R``
into an existing ``skills/<name>`` nested the new copy as ``<name>/<name>``
and left the stale copy in place.
"""

import os
import subprocess
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[4]
UTILS_SCRIPT = "src/sh/claude/helpers/claude_file_utils.sh"


def flatten(target: Path) -> subprocess.CompletedProcess:
    """Source the real helper script and run ``flatten_skills`` against ``target``.

    :param target: The config dir whose ``skills/`` folder is flattened.
    :return: The finished process, stdout and stderr merged.
    """
    env = {**os.environ, "CLAUDE_CONFIG_DIR": str(target)}
    return subprocess.run(
        ["bash", "-c", f"source {UTILS_SCRIPT} && flatten_skills"],
        cwd=REPO_ROOT, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        text=True, timeout=30,
    )


def make_skill(parent: Path, name: str, body: str = "# skill") -> Path:
    """Create ``parent/name/SKILL.md`` and return the skill folder.

    :param parent: Folder to create the skill in.
    :param name: Skill folder name.
    :param body: SKILL.md content.
    :return: The skill folder.
    """
    skill = parent / name
    skill.mkdir(parents=True, exist_ok=True)
    (skill / "SKILL.md").write_text(body)
    return skill


@pytest.fixture
def skills(tmp_path: Path) -> Path:
    """Return an empty ``skills/`` folder inside a temp config dir.

    :param tmp_path: pytest's per-test temp directory.
    :return: The ``skills/`` folder.
    """
    folder = tmp_path / "skills"
    folder.mkdir()
    return folder


def test_script_exits_cleanly(skills: Path):
    """Flattening an empty skills/ folder succeeds."""
    result = flatten(skills.parent)
    assert result.returncode == 0, f"flatten_skills failed: {result.stdout}"


def test_grouped_skill_is_promoted(skills: Path):
    """A skill in a group folder ends up at skills/<name>."""
    make_skill(skills / "_demo_skills", "demo_one", "v1")
    flatten(skills.parent)
    assert (skills / "demo_one" / "SKILL.md").read_text() == "v1", "Grouped skill was not promoted to skills/"


def test_group_folder_is_removed(skills: Path):
    """No _<group>_skills/ folder is left after flattening."""
    make_skill(skills / "_demo_skills", "demo_one")
    flatten(skills.parent)
    assert not (skills / "_demo_skills").exists(), "Group folder should be removed after flattening"


def test_group_readme_is_removed_with_group(skills: Path):
    """A loose README.md in a group folder goes with the group, not into skills/."""
    make_skill(skills / "_demo_skills", "demo_one")
    (skills / "_demo_skills" / "README.md").write_text("group readme")
    flatten(skills.parent)
    assert not (skills / "_demo_skills" / "README.md").exists(), "Group README should be removed with its folder"
    assert not (skills / "README.md").exists(), "Group README must not be promoted into skills/"


def test_existing_flat_copy_is_replaced(skills: Path):
    """Regression: an update replaces the old flat copy instead of keeping it."""
    make_skill(skills, "demo_one", "old")
    make_skill(skills / "_demo_skills", "demo_one", "new")
    flatten(skills.parent)
    assert (skills / "demo_one" / "SKILL.md").read_text() == "new", "Stale flat copy was not replaced on update"


def test_existing_flat_copy_is_not_nested(skills: Path):
    """Regression: an update never creates skills/<name>/<name>."""
    make_skill(skills, "demo_one", "old")
    make_skill(skills / "_demo_skills", "demo_one", "new")
    flatten(skills.parent)
    assert not (skills / "demo_one" / "demo_one").exists(), "cp -R nested the new copy inside the old one"


def test_nested_skill_files_are_copied(skills: Path):
    """Sub-folders inside a skill (reference/, tests/) come along."""
    skill = make_skill(skills / "_demo_skills", "demo_one")
    (skill / "reference").mkdir()
    (skill / "reference" / "_implementation.md").write_text("impl")
    flatten(skills.parent)
    copied = skills / "demo_one" / "reference" / "_implementation.md"
    assert copied.is_file(), "Nested reference/ file was not copied"
    assert copied.read_text() == "impl", "Nested file content changed during copy"


def test_multiple_groups_are_all_flattened(skills: Path):
    """Skills from every group folder are promoted, and every group goes."""
    make_skill(skills / "_alpha_skills", "alpha_one")
    make_skill(skills / "_beta_skills", "beta_one")
    flatten(skills.parent)
    assert (skills / "alpha_one" / "SKILL.md").is_file(), "Skill from the first group is missing"
    assert (skills / "beta_one" / "SKILL.md").is_file(), "Skill from the second group is missing"
    leftover = sorted(p.name for p in skills.iterdir() if p.name.startswith("_"))
    assert leftover == [], f"Group folders left behind: {leftover}"


def test_flat_only_skill_is_untouched(skills: Path):
    """A skill that already sits flat with no grouped original is left alone."""
    make_skill(skills, "solo_skill", "keep")
    flatten(skills.parent)
    assert (skills / "solo_skill" / "SKILL.md").read_text() == "keep", "Flat-only skill should not be touched"


def test_top_level_readme_is_untouched(skills: Path):
    """The skills/README.md index survives flattening."""
    (skills / "README.md").write_text("index")
    make_skill(skills / "_demo_skills", "demo_one")
    flatten(skills.parent)
    assert (skills / "README.md").read_text() == "index", "skills/README.md should not be touched"


def test_empty_group_folder_is_removed(skills: Path):
    """A group folder with no skills is still cleaned up."""
    (skills / "_empty_skills").mkdir()
    result = flatten(skills.parent)
    assert result.returncode == 0, f"flatten_skills failed on an empty group: {result.stdout}"
    assert not (skills / "_empty_skills").exists(), "Empty group folder should be removed"
