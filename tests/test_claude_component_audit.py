"""Tests for the Claude component audit health checker.

Covers health signal detection (check_health) and file discovery (find_all_components).
Health tests use in-memory metadata dicts — no file system access required.
Discovery tests use pytest's tmp_path fixture to create minimal component fixtures.
"""

from datetime import date, timedelta
from pathlib import Path

import frontmatter
import pytest

from src.sh.claude.claude_component_audit import (
    STALENESS_WARN_DAYS,
    check_health,
    find_all_components,
)

# ── helpers ───────────────────────────────────────────────────────────────────

VALID_METADATA: dict = {
    "name": "test-skill",
    "maturity": "draft",
    "tags": {
        "criticality": "could",  # 'could' avoids must/should-gated signals — set explicitly in those tests
        "status": "active",
        "tested": False,
    },
}

KNOWN_NAMES: set[str] = {"test-skill", "other-skill"}


def _meta(**overrides) -> dict:
    """Return a copy of VALID_METADATA with the given overrides applied.

    Supports nested overrides via dot notation for the tags block, e.g.
    ``_meta(**{"tags.criticality": "must"})``.

    :return: Modified metadata dict.
    :rtype: dict
    """
    import copy

    m = copy.deepcopy(VALID_METADATA)
    for key, value in overrides.items():
        if key.startswith("tags."):
            tag_key = key[len("tags."):]
            if value is None:
                m["tags"].pop(tag_key, None)
            else:
                m["tags"][tag_key] = value
        elif value is None:
            m.pop(key, None)
        else:
            m[key] = value
    return m


def _write_component(tmp_path: Path, name: str, metadata: dict, filename: str = "SKILL.md") -> Path:
    """Write a component .md file to a temp directory and return its path.

    :param tmp_path: pytest tmp_path fixture.
    :type tmp_path: Path
    :param name: Component directory name.
    :type name: str
    :param metadata: Frontmatter metadata dict.
    :type metadata: dict
    :param filename: File name to write (default: SKILL.md).
    :type filename: str
    :return: Path to the created file.
    :rtype: Path
    """
    comp_dir = tmp_path / name
    comp_dir.mkdir(exist_ok=True)
    comp_file = comp_dir / filename
    post = frontmatter.Post("component body", **metadata)
    comp_file.write_text(frontmatter.dumps(post))
    return comp_file


# ── check_health — DORMANT ────────────────────────────────────────────────────


def test_dormant_must_criticality_flagged():
    """status:dormant + criticality:must produces DORMANT signal."""
    signals = check_health(_meta(**{"tags.status": "dormant", "tags.criticality": "must"}), KNOWN_NAMES)
    assert signals["DORMANT"] is not None


def test_dormant_should_criticality_flagged():
    """status:dormant + criticality:should produces DORMANT signal."""
    signals = check_health(_meta(**{"tags.status": "dormant", "tags.criticality": "should"}), KNOWN_NAMES)
    assert signals["DORMANT"] is not None


def test_dormant_could_criticality_clean():
    """status:dormant + criticality:could does NOT produce DORMANT signal."""
    signals = check_health(_meta(**{"tags.status": "dormant", "tags.criticality": "could"}), KNOWN_NAMES)
    assert signals["DORMANT"] is None


def test_dormant_want_criticality_clean():
    """status:dormant + criticality:want does NOT produce DORMANT signal."""
    signals = check_health(_meta(**{"tags.status": "dormant", "tags.criticality": "want"}), KNOWN_NAMES)
    assert signals["DORMANT"] is None


def test_active_high_criticality_no_dormant_signal():
    """status:active + criticality:must does NOT produce DORMANT signal."""
    signals = check_health(_meta(**{"tags.status": "active", "tags.criticality": "must"}), KNOWN_NAMES)
    assert signals["DORMANT"] is None


# ── check_health — UNTESTED ───────────────────────────────────────────────────


def test_untested_must_criticality_flagged():
    """tested:false + criticality:must produces UNTESTED signal."""
    signals = check_health(_meta(**{"tags.criticality": "must", "tags.tested": False}), KNOWN_NAMES)
    assert signals["UNTESTED"] is not None


def test_untested_should_criticality_flagged():
    """tested:false + criticality:should produces UNTESTED signal."""
    signals = check_health(_meta(**{"tags.criticality": "should", "tags.tested": False}), KNOWN_NAMES)
    assert signals["UNTESTED"] is not None


def test_untested_could_criticality_clean():
    """tested:false + criticality:could does NOT produce UNTESTED signal."""
    signals = check_health(_meta(**{"tags.criticality": "could", "tags.tested": False}), KNOWN_NAMES)
    assert signals["UNTESTED"] is None


def test_tested_true_must_no_untested_signal():
    """tested:true + criticality:must does NOT produce UNTESTED signal."""
    signals = check_health(_meta(**{"tags.criticality": "must", "tags.tested": True}), KNOWN_NAMES)
    assert signals["UNTESTED"] is None


# ── check_health — NO_REVIEW ──────────────────────────────────────────────────


def test_missing_review_must_criticality_flagged():
    """Absent last-reviewed + criticality:must produces NO_REVIEW signal."""
    signals = check_health(_meta(**{"tags.criticality": "must"}), KNOWN_NAMES)
    assert signals["NO_REVIEW"] is not None


def test_missing_review_should_criticality_flagged():
    """Absent last-reviewed + criticality:should produces NO_REVIEW signal."""
    signals = check_health(_meta(**{"tags.criticality": "should"}), KNOWN_NAMES)
    assert signals["NO_REVIEW"] is not None


def test_missing_review_could_criticality_clean():
    """Absent last-reviewed + criticality:could does NOT produce NO_REVIEW signal."""
    signals = check_health(_meta(**{"tags.criticality": "could"}), KNOWN_NAMES)
    assert signals["NO_REVIEW"] is None


def test_present_review_date_suppresses_no_review_signal():
    """A last-reviewed date present clears NO_REVIEW even for must/should."""
    recent = date.today() - timedelta(days=10)
    signals = check_health(
        _meta(**{"tags.criticality": "must", "last-reviewed": recent}),
        KNOWN_NAMES,
    )
    assert signals["NO_REVIEW"] is None


# ── check_health — STALE ──────────────────────────────────────────────────────


def test_stale_last_reviewed_flagged():
    """A last-reviewed date older than STALENESS_WARN_DAYS produces STALE signal."""
    stale = date.today() - timedelta(days=STALENESS_WARN_DAYS + 1)
    signals = check_health(_meta(**{"last-reviewed": stale}), KNOWN_NAMES)
    assert signals["STALE"] is not None


def test_fresh_last_reviewed_clean():
    """A last-reviewed date within STALENESS_WARN_DAYS does NOT produce STALE signal."""
    recent = date.today() - timedelta(days=STALENESS_WARN_DAYS - 1)
    signals = check_health(_meta(**{"last-reviewed": recent}), KNOWN_NAMES)
    assert signals["STALE"] is None


# ── check_health — DEPRECATED ─────────────────────────────────────────────────


def test_deprecated_status_flagged():
    """status:deprecated produces DEPRECATED signal."""
    signals = check_health(_meta(**{"tags.status": "deprecated"}), KNOWN_NAMES)
    assert signals["DEPRECATED"] is not None


def test_active_status_no_deprecated_signal():
    """status:active does NOT produce DEPRECATED signal."""
    signals = check_health(_meta(**{"tags.status": "active"}), KNOWN_NAMES)
    assert signals["DEPRECATED"] is None


# ── check_health — BROKEN_DEP ────────────────────────────────────────────────


def test_broken_depends_on_flagged():
    """A depends-on entry not in known_names produces BROKEN_DEP signal."""
    meta = _meta(**{"depends-on": ["nonexistent-skill"]})
    signals = check_health(meta, KNOWN_NAMES)
    assert signals["BROKEN_DEP"] is not None
    assert "nonexistent-skill" in signals["BROKEN_DEP"]


def test_valid_depends_on_clean():
    """A depends-on entry that exists in known_names does NOT produce BROKEN_DEP."""
    meta = _meta(**{"depends-on": ["other-skill"]})
    signals = check_health(meta, KNOWN_NAMES)
    assert signals["BROKEN_DEP"] is None


def test_empty_depends_on_clean():
    """No depends-on field does NOT produce BROKEN_DEP signal."""
    signals = check_health(VALID_METADATA, KNOWN_NAMES)
    assert signals["BROKEN_DEP"] is None


# ── find_all_components ───────────────────────────────────────────────────────


def test_find_all_components_tagged_file_in_skills(tmp_path: Path):
    """A SKILL.md with maturity key is placed in the tagged list."""
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    _write_component(skills_dir, "my-skill", VALID_METADATA, "SKILL.md")

    tagged, untagged = find_all_components(tmp_path)
    assert any(p.name == "SKILL.md" for p in tagged)
    assert not any(p.name == "SKILL.md" for p in untagged)


def test_find_all_components_untagged_file_in_agents(tmp_path: Path):
    """A .md without maturity key is placed in the untagged list."""
    agents_dir = tmp_path / "agents"
    agents_dir.mkdir()
    untagged_file = agents_dir / "my-agent.md"
    untagged_file.write_text("# no frontmatter")

    tagged, untagged = find_all_components(tmp_path)
    assert untagged_file not in tagged
    assert untagged_file in untagged


def test_find_all_components_skips_readme(tmp_path: Path):
    """README.md files are excluded from both lists."""
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    readme = skills_dir / "README.md"
    readme.write_text("# readme")

    tagged, untagged = find_all_components(tmp_path)
    assert readme not in tagged
    assert readme not in untagged


def test_find_all_components_both_lists_sorted(tmp_path: Path):
    """Both returned lists are in sorted order."""
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    for name in ("z-skill", "a-skill", "m-skill"):
        _write_component(skills_dir, name, VALID_METADATA, "SKILL.md")

    tagged, _ = find_all_components(tmp_path)
    assert tagged == sorted(tagged)


def test_find_all_components_empty_root_returns_empty_lists(tmp_path: Path):
    """An empty directory returns two empty lists."""
    tagged, untagged = find_all_components(tmp_path)
    assert tagged == []
    assert untagged == []


def test_find_all_components_excludes_skills_wip(tmp_path: Path):
    """Files under skills_wip/ are excluded from both lists."""
    wip_dir = tmp_path / "skills_wip"
    wip_dir.mkdir()
    wip_file = wip_dir / "draft-skill.md"
    post = frontmatter.Post("wip body", **VALID_METADATA)
    wip_file.write_text(frontmatter.dumps(post))

    tagged, untagged = find_all_components(tmp_path)
    assert wip_file not in tagged
    assert wip_file not in untagged
