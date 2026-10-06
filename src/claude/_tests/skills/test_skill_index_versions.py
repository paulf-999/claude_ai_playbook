# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-05
# Date updated:      2026-10-05
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Every skill group README lists each of its skills at the version in that skill's SKILL.md header.

The group indexes (``skills/_<group>_skills/README.md``) drifted from the real
versions on 2026-10-05 — four skills showed stale numbers — so this suite fails
the build whenever an index row and a SKILL.md header disagree.
"""
import re
from pathlib import Path

import pytest

from _metadata_header import header_version_after_frontmatter as header_version
from _shared_paths import SKILLS_DIR

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
SKILL_CELL = re.compile(r"^`/([a-z0-9_]+)`$")
SAMPLE_INDEX = """\
| Skill | Description | Version | Tested |
|---|---|---|---|
| `/git_create_pr` | Create a PR, with a pipe-free description | 1.3.1 | yes |
| `/git_review_pr` | Review a PR | 0.4.1 | no |
| `/demo_unversioned` | Has no version yet | — | no |
"""


def index_versions(readme: str) -> dict[str, str]:
    """Map each `/skill` row in a group README to the first semver cell after its name."""
    versions = {}
    for line in readme.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        match = SKILL_CELL.match(cells[0]) if cells else None
        if not match:
            continue
        version = next((cell for cell in cells[1:] if SEMVER.match(cell)), None)
        if version:
            versions[match.group(1)] = version
    return versions


def version_drift(skill_versions: dict[str, str], indexed: dict[str, str]) -> list[str]:
    """Return one error per skill whose index version is missing, stale or orphaned."""
    errors = []
    for name, version in sorted(skill_versions.items()):
        if name not in indexed:
            errors.append(f"{name}: missing from the group README (SKILL.md is {version})")
        elif indexed[name] != version:
            errors.append(f"{name}: README says {indexed[name]} but SKILL.md is {version}")
    orphaned = sorted(set(indexed) - set(skill_versions))
    errors += [f"{name}: listed in the README but has no SKILL.md" for name in orphaned]
    return errors


def group_dirs() -> list[Path]:
    """Return every `_<group>_skills` folder that has a README index."""
    return sorted(path.parent for path in SKILLS_DIR.glob("_*_skills/README.md"))


def group_skill_versions(group: Path) -> dict[str, str]:
    """Map each skill folder in a group to the version in its SKILL.md header."""
    return {skill.parent.name: header_version(skill.read_text()) for skill in sorted(group.glob("*/SKILL.md"))}


# --- Parser ---

def test_index_row_version_is_read():
    """A skill row yields its name and the version cell."""
    versions = index_versions(SAMPLE_INDEX)
    assert versions["git_create_pr"] == "1.3.1", f"wrong version read: {versions}"
    assert versions["git_review_pr"] == "0.4.1", f"second row not read: {versions}"


def test_header_and_separator_rows_ignored():
    """Table header and separator lines aren't mistaken for skills."""
    versions = index_versions(SAMPLE_INDEX)
    assert "Skill" not in versions, "header row parsed as a skill"
    assert len(versions) == 2, f"expected 2 versioned rows, got {versions}"


def test_row_without_version_skipped():
    """A row whose version cell isn't semver is left out, so drift reports it as missing."""
    assert "demo_unversioned" not in index_versions(SAMPLE_INDEX), "non-semver cell accepted as a version"


def test_prose_lines_ignored():
    """Text outside the table yields nothing."""
    assert index_versions("# Git skills\n\nSee `/git_create_pr` 1.0.0 for details.\n") == {}, "prose parsed as a row"


# --- Drift rules ---

def test_matching_versions_pass():
    """Identical versions produce no errors."""
    assert version_drift({"a_skill": "1.0.0"}, {"a_skill": "1.0.0"}) == [], "matching versions reported as drift"


def test_stale_version_caught():
    """A README version that differs from SKILL.md is reported with both numbers."""
    errors = version_drift({"a_skill": "1.1.0"}, {"a_skill": "1.2.0"})
    assert len(errors) == 1, f"expected one error, got {errors}"
    assert "1.2.0" in errors[0] and "1.1.0" in errors[0], f"error doesn't name both versions: {errors}"


def test_unindexed_skill_caught():
    """A skill with no README row is reported."""
    errors = version_drift({"a_skill": "0.1.0"}, {})
    assert len(errors) == 1, f"expected one error, got {errors}"
    assert "missing from the group README" in errors[0], f"missing row not caught: {errors}"


def test_orphaned_index_row_caught():
    """A README row for a skill that doesn't exist is reported."""
    errors = version_drift({}, {"gone_skill": "1.0.0"})
    assert errors and "has no SKILL.md" in errors[0], f"orphaned row not caught: {errors}"


# --- Real config ---

def test_skill_groups_exist():
    """The real checks below only mean something if group folders are found."""
    if not group_dirs():
        pytest.skip(f"no _<group>_skills folders under {SKILLS_DIR} — flat live install")
    assert all(group.name.endswith("_skills") for group in group_dirs()), "a non-group folder was picked up"


def test_every_group_index_matches_its_skills():
    """Each group README lists every skill in its folder at its SKILL.md version, and nothing else."""
    groups = group_dirs()
    if not groups:
        pytest.skip(f"no _<group>_skills folders under {SKILLS_DIR} — flat live install")
    for group in groups:
        errors = version_drift(group_skill_versions(group), index_versions((group / "README.md").read_text()))
        assert not errors, f"{group.name}/README.md is out of date — update its Version column: {errors}"


def test_every_skill_header_has_a_version():
    """Each grouped SKILL.md exposes a semver header version for the index to match."""
    groups = group_dirs()
    if not groups:
        pytest.skip(f"no _<group>_skills folders under {SKILLS_DIR} — flat live install")
    for group in groups:
        for name, version in group_skill_versions(group).items():
            assert version and SEMVER.match(version), f"{group.name}/{name}: SKILL.md header has no semver version"
