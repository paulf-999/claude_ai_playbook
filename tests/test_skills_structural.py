"""Structural tests for Claude skill definition files.

Validates that every skill directory in src/claude/skills/ and src/claude/wip/skills/ has:
- A SKILL.md file
- Valid YAML frontmatter with non-empty name and description
- A name that matches the directory name
- All referenced ~/.claude/skills/... file paths exist in the repo

Discovers skills by finding all SKILL.md files at any depth under both directories,
so both stable skills and WIP skills (which are merged into ~/.claude/skills/ at install time)
are covered. Archived skills under wip/skills/archive/ are excluded from discovery.
"""

import re
from pathlib import Path

import frontmatter
import pytest

SKILLS_DIR = Path(__file__).parent.parent / "src" / "claude" / "skills"
SKILLS_WIP_DIR = Path(__file__).parent.parent / "src" / "claude" / "wip" / "skills"
CLAUDE_CONFIG_DIR = Path(__file__).parent.parent / "src" / "claude"
TESTS_SKILLS_DIR = Path(__file__).parent / "skills"

CLAUDE_HOME_ALIAS = "~/.claude/"
CLAUDE_HOME_REPO = str(CLAUDE_CONFIG_DIR) + "/"

# Discover all skill directories by locating every SKILL.md at any depth under both trees
_stable_skill_dirs = [(d, SKILLS_DIR) for d in (skill_md.parent for skill_md in SKILLS_DIR.rglob("SKILL.md"))]
_wip_skill_dirs = [
    (d, SKILLS_WIP_DIR)
    for d in (skill_md.parent for skill_md in SKILLS_WIP_DIR.rglob("SKILL.md"))
    if SKILLS_WIP_DIR / "archive" not in d.parents and d != SKILLS_WIP_DIR / "archive"
]
_all_skill_entries = _stable_skill_dirs + _wip_skill_dirs

skill_dirs = [entry[0] for entry in _all_skill_entries]

# Stable-only lists — used where WIP skills should be excluded (e.g. test file enforcement)
stable_skill_dirs = [entry[0] for entry in _stable_skill_dirs]
stable_skill_ids = [str(d.relative_to(SKILLS_DIR)) for d in stable_skill_dirs]

# Use relative paths as IDs (e.g. "commit", "wip/manage_jira") for clear test output
skill_ids = [
    str(d.relative_to(root))
    if d.is_relative_to(SKILLS_DIR)
    else "wip/" + str(d.relative_to(SKILLS_WIP_DIR))
    for d, root in _all_skill_entries
]

# Skills that pre-date the test-file enforcement rule and have not yet had tests written.
# Remove a skill from this set when its test file is added — the structural test will then
# enforce the contract automatically.
_TEST_COVERAGE_EXEMPT: set[str] = {
    "_data_engineering_skills/review_dbt_pr",
    "_data_engineering_skills/file_template_update",
    "_meetings_skills/sprint_planning_dpe_team",
    "_atlassian_skills/populate_jira_business_value",
}


def _load_skill_md(skill_dir: Path) -> frontmatter.Post:
    """Load the SKILL.md from a skill directory.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    :return: Parsed frontmatter post object.
    :rtype: frontmatter.Post
    """
    return frontmatter.load(str(skill_dir / "SKILL.md"))


def _extract_claude_home_references(content: str) -> list[str]:
    """Extract all ~/.claude/... file path references from skill content.

    :param content: Raw markdown content of a SKILL.md file.
    :type content: str
    :return: List of resolved absolute file paths.
    :rtype: list[str]
    """
    pattern = r"~/.claude/[^\s`'\"\)>]+"  # stop at whitespace or common delimiters (backtick, quotes, brackets)
    matches = re.findall(pattern, content)
    resolved = []
    for match in matches:
        # Strip trailing punctuation that may have been captured as part of the surrounding prose
        match = match.rstrip(".,;:")
        # Skip dynamic template placeholders (e.g. {chosen_style}) — not statically resolvable
        if "{" in match or "}" in match or "<" in match:
            continue
        # Skip directory references (e.g. ~/.claude/sessions/) — runtime dirs, not repo files
        if match.endswith("/"):
            continue
        absolute = match.replace(CLAUDE_HOME_ALIAS, CLAUDE_HOME_REPO)
        resolved.append(absolute)
    return resolved


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_skill_has_skill_md(skill_dir: Path) -> None:
    """Every skill directory must contain a SKILL.md file.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    """
    skill_md = skill_dir / "SKILL.md"
    assert skill_md.exists(), f"{skill_dir.name}: missing SKILL.md"


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_skill_md_has_valid_frontmatter(skill_dir: Path) -> None:
    """SKILL.md must have parseable YAML frontmatter.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    """
    post = _load_skill_md(skill_dir)
    assert post.metadata, f"{skill_dir.name}/SKILL.md: missing or empty frontmatter"


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_skill_md_frontmatter_has_name_and_description(skill_dir: Path) -> None:
    """SKILL.md frontmatter must have non-empty name and description fields.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    """
    post = _load_skill_md(skill_dir)
    assert "name" in post.metadata, f"{skill_dir.name}/SKILL.md: frontmatter missing 'name'"
    assert post.metadata["name"], f"{skill_dir.name}/SKILL.md: frontmatter 'name' is empty"
    assert "description" in post.metadata, f"{skill_dir.name}/SKILL.md: frontmatter missing 'description'"
    assert post.metadata["description"], f"{skill_dir.name}/SKILL.md: frontmatter 'description' is empty"


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_skill_name_matches_directory(skill_dir: Path) -> None:
    """SKILL.md frontmatter name must match the skill directory name.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    """
    post = _load_skill_md(skill_dir)
    assert post.metadata.get("name") == skill_dir.name, (
        f"{skill_dir.name}/SKILL.md: frontmatter name '{post.metadata.get('name')}' "
        f"does not match directory name '{skill_dir.name}'"
    )


def _path_exists_in_repo(path_str: str) -> bool:
    """Check whether a resolved repo path exists, with a wip/skills/ fallback.

    WIP skills reference ``~/.claude/skills/<name>/...`` at runtime because ``merge_skills_wip``
    copies them into ``skills/`` at install time. In the repo, those files live under
    ``wip/skills/``. Resolve against ``wip/skills/`` as a fallback before reporting missing.

    :param path_str: Absolute repo-relative path (``CLAUDE_HOME_ALIAS`` already substituted).
    :type path_str: str
    :return: True if the path exists under ``skills/`` or ``wip/skills/`` fallback.
    :rtype: bool
    """
    primary = Path(path_str)
    if primary.exists():
        return True
    # WIP fallback: swap skills/ for wip/skills/ when the primary path is absent
    skills_prefix = CLAUDE_HOME_REPO + "skills/"
    if path_str.startswith(skills_prefix):
        wip_fallback = Path(path_str.replace(skills_prefix, CLAUDE_HOME_REPO + "wip/skills/", 1))
        if wip_fallback.exists():
            return True
    return False


@pytest.mark.parametrize("skill_dir", skill_dirs, ids=skill_ids)
def test_skill_file_references_exist(skill_dir: Path) -> None:
    """All ~/.claude/skills/... paths referenced in SKILL.md must exist in the repo.

    WIP skills that reference ``~/.claude/skills/<name>/...`` are resolved against
    ``wip/skills/`` as a fallback, since those files are merged into ``skills/`` at install
    time but live under ``wip/skills/`` in the source tree.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    """
    post = _load_skill_md(skill_dir)
    references = _extract_claude_home_references(post.content)

    missing = [ref for ref in references if not _path_exists_in_repo(ref)]
    assert not missing, (
        f"{skill_dir.name}/SKILL.md: referenced files not found in repo:\n"
        + "\n".join(f"  {ref}" for ref in missing)
    )


@pytest.mark.parametrize("skill_dir", stable_skill_dirs, ids=stable_skill_ids)
def test_tested_true_implies_test_file_exists(skill_dir: Path) -> None:
    """A stable skill with tags.tested: true must have a corresponding test file.

    When a skill's frontmatter is updated to ``tested: true``, this test enforces
    that a test file actually exists. Skills in ``_TEST_COVERAGE_EXEMPT`` are
    grandfathered — remove a skill from that set when its test file is added.

    The expected test file is resolved by searching ``tests/skills/`` for any file
    matching ``test_<skill_name>_skill.py`` at any depth. This handles both grouped
    (e.g. ``tests/skills/_git_skills/``) and flat layouts.

    :param skill_dir: Path to the skill directory.
    :type skill_dir: Path
    """
    post = _load_skill_md(skill_dir)
    tags = post.metadata.get("tags") or {}
    tested = tags.get("tested", False)

    if not tested:
        pytest.skip(f"{skill_dir.name}: tags.tested is false — skipping")

    skill_id = str(skill_dir.relative_to(SKILLS_DIR))
    if skill_id in _TEST_COVERAGE_EXEMPT:
        pytest.skip(f"{skill_dir.name}: grandfathered in _TEST_COVERAGE_EXEMPT — skipping")

    expected_filename = f"test_{skill_dir.name}_skill.py"
    matches = list(TESTS_SKILLS_DIR.rglob(expected_filename))

    assert matches, (
        f"{skill_dir.name}/SKILL.md sets tags.tested: true but no test file found.\n"
        f"Expected a file named '{expected_filename}' somewhere under tests/skills/.\n"
        f"Either add the test file or set tags.tested: false in SKILL.md."
    )
