# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-09-30
# Date updated:      2026-10-01
# Version:           1.0.1
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Keeps skill_domains.yaml and the real skills/ layout in step.

Goal: every installed skill's name starts with a registered domain prefix,
and the skill sits in the folder that domain names — so drift like the
retired ``_confluence_skills`` folder fails the build instead of going
unnoticed (found 2026-09-30, fixed in #162).

The folder checks only apply to the repo's grouped layout (CI sets
CLAUDE_CONFIG_DIR to src/claude). A live install lays skills out flat, with
no group folders, so those two checks skip there instead of failing.
"""
from pathlib import Path

import pytest
import yaml

from _shared_paths import RULES_DIR, SKILLS_DIR

DOMAINS_FILE = RULES_DIR / "03_authoring_guidelines" / "authoring_skills" / "skill_domains.yaml"
REQUIRED_FIELDS = {"id", "prefix", "directory", "description", "stable"}


def load_domains(path: Path = DOMAINS_FILE) -> list:
    """Return the domain entries from a skill_domains.yaml file.

    :param path: The YAML file to read.
    :type path: Path
    :return: One dict per domain.
    :rtype: list
    """
    return yaml.safe_load(path.read_text())["domains"]


def installed_skills(skills_dir: Path = SKILLS_DIR) -> list:
    """Return the folder of every installed skill (any folder holding a SKILL.md).

    :param skills_dir: The skills/ directory to scan.
    :type skills_dir: Path
    :return: Skill folders, sorted by path.
    :rtype: list
    """
    return sorted(path.parent for path in skills_dir.rglob("SKILL.md"))


def has_group_folders(skills_dir: Path = SKILLS_DIR) -> bool:
    """Return True when skills sit in ``_<group>_skills/`` folders, as in the repo.

    :param skills_dir: The skills/ directory to inspect.
    :type skills_dir: Path
    :return: Whether any underscore-prefixed group folder exists.
    :rtype: bool
    """
    return any(path.is_dir() and path.name.startswith("_") for path in skills_dir.iterdir())


def misplaced_skills(domains: list, skills: list) -> list:
    """Describe every skill with an unregistered prefix or in the wrong folder.

    :param domains: Domain entries, as returned by :func:`load_domains`.
    :type domains: list
    :param skills: Skill folders, as returned by :func:`installed_skills`.
    :type skills: list
    :return: One human-readable problem per bad skill; empty when all is well.
    :rtype: list
    """
    problems = []
    for skill in skills:
        matches = [d for d in domains if skill.name.startswith(d["prefix"])]
        if not matches:
            problems.append(f"{skill.name}: no domain in skill_domains.yaml has a matching prefix")
        elif skill.parent.name != matches[0]["directory"]:
            expected = matches[0]["directory"]
            problems.append(f"{skill.name}: sits in {skill.parent.name}/, but its domain names {expected}/")
    return problems


def test_domains_file_exists():
    """skill_domains.yaml is where the naming rules say it is."""
    assert DOMAINS_FILE.is_file(), (
        f"Missing {DOMAINS_FILE} — _claude_naming_patterns.md and _core_standards.md point here"
    )


def test_domains_list_is_not_empty():
    """The file registers at least one domain."""
    assert load_domains(), "skill_domains.yaml has no domains — every skill would be unregistered"


def test_every_domain_has_required_fields():
    """Each entry has id, prefix, directory, description and stable."""
    for domain in load_domains():
        missing = REQUIRED_FIELDS - domain.keys()
        assert not missing, f"Domain {domain.get('id', '?')} is missing {sorted(missing)}"


def test_prefix_is_id_plus_underscore():
    """A domain's prefix is always its id followed by an underscore."""
    for domain in load_domains():
        assert domain["prefix"] == f"{domain['id']}_", (
            f"Domain {domain['id']} has prefix {domain['prefix']!r}; expected {domain['id']}_"
        )


def test_domain_ids_are_unique():
    """No domain is registered twice."""
    ids = [domain["id"] for domain in load_domains()]
    assert len(ids) == len(set(ids)), f"Duplicate domain ids in skill_domains.yaml: {ids}"


def test_every_domain_directory_exists():
    """Each named folder exists under skills/."""
    if not has_group_folders():
        pytest.skip("skills/ has no group folders (flat live install) — checked against the repo in CI")
    for domain in load_domains():
        folder = SKILLS_DIR / domain["directory"]
        assert folder.is_dir(), f"Domain {domain['id']} names {domain['directory']}/, which doesn't exist under skills/"


def test_every_domain_directory_is_underscore_prefixed():
    """Skill group folders follow the user-created _<name> convention."""
    for domain in load_domains():
        assert domain["directory"].startswith("_"), (
            f"Domain {domain['id']} names {domain['directory']}; skill group folders start with an underscore"
        )


def test_skills_are_installed():
    """The scan finds skills, so the placement checks aren't passing on an empty list."""
    assert installed_skills(), f"No SKILL.md found under {SKILLS_DIR} — the scan or the path is wrong"


def test_every_skill_sits_in_its_domain_folder():
    """Every installed skill has a registered prefix and sits in its domain's folder."""
    if not has_group_folders():
        pytest.skip("skills/ has no group folders (flat live install) — checked against the repo in CI")
    problems = misplaced_skills(load_domains(), installed_skills())
    assert not problems, "Fix the skill's folder or skill_domains.yaml:\n" + "\n".join(problems)


def test_every_domain_is_used():
    """Every registered domain has at least one skill, so the list doesn't collect dead entries."""
    used = {skill.name.split("_")[0] for skill in installed_skills()}
    unused = [domain["id"] for domain in load_domains() if domain["id"] not in used]
    assert not unused, f"Domains with no skills: {unused} — remove them or add the skill"


def test_detector_flags_skill_in_wrong_folder(tmp_path):
    """Synthetic bad case: a skill in the wrong group folder is reported."""
    skill = tmp_path / "_wrong_skills" / "demo_do_thing"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("# demo")
    domains = [{"id": "demo", "prefix": "demo_", "directory": "_demo_skills"}]
    problems = misplaced_skills(domains, installed_skills(tmp_path))
    assert len(problems) == 1, f"Expected one problem, got {problems}"
    assert "_wrong_skills/" in problems[0], "The problem should name the folder the skill is actually in"


def test_detector_flags_unregistered_prefix(tmp_path):
    """Synthetic bad case: a skill whose prefix matches no domain is reported."""
    skill = tmp_path / "_demo_skills" / "other_do_thing"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("# demo")
    domains = [{"id": "demo", "prefix": "demo_", "directory": "_demo_skills"}]
    problems = misplaced_skills(domains, installed_skills(tmp_path))
    assert problems == ["other_do_thing: no domain in skill_domains.yaml has a matching prefix"], problems


def test_group_folder_detection(tmp_path):
    """The layout check tells the repo's grouped layout from a flat install."""
    (tmp_path / "flat_skill").mkdir()
    assert not has_group_folders(tmp_path), "A flat skills/ folder must not count as grouped"
    (tmp_path / "_demo_skills").mkdir()
    assert has_group_folders(tmp_path), "An _<group>_skills/ folder must count as grouped"


def test_detector_passes_shared_folder(tmp_path):
    """Two domains may share one folder, as confluence and jira share _atlassian_skills."""
    for name in ("alpha_one", "beta_two"):
        skill = tmp_path / "_shared_skills" / name
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("# demo")
    domains = [
        {"id": "alpha", "prefix": "alpha_", "directory": "_shared_skills"},
        {"id": "beta", "prefix": "beta_", "directory": "_shared_skills"},
    ]
    assert misplaced_skills(domains, installed_skills(tmp_path)) == [], "A shared group folder must be allowed"
