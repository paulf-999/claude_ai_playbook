"""Tests for the Claude component Tier 1 tag lint validator.

Covers validation logic (validate_component) and file discovery (find_components).
Validation tests use in-memory metadata dicts — no file system access required.
Discovery tests use pytest's tmp_path fixture to create minimal SKILL.md fixtures.
"""

from datetime import date, timedelta
from pathlib import Path

import frontmatter
import pytest

from src.sh.claude.claude_tag_lint import STALENESS_WARN_DAYS, find_components, validate_component

# ── helpers ───────────────────────────────────────────────────────────────────

VALID_METADATA: dict = {
    "name": "test-skill",
    "maturity": "draft",
    "tags": {
        "criticality": "could",  # 'could' avoids tested/last-reviewed warnings — use must/should explicitly in warn tests
        "status": "active",
        "tested": False,
    },
}


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


def _write_skill(tmp_path: Path, skill_name: str, metadata: dict) -> Path:
    """Write a minimal SKILL.md to a temp directory and return its path.

    :param tmp_path: pytest tmp_path fixture.
    :type tmp_path: Path
    :param skill_name: Skill directory name.
    :type skill_name: str
    :param metadata: Frontmatter metadata dict.
    :type metadata: dict
    :return: Path to the created SKILL.md.
    :rtype: Path
    """
    skill_dir = tmp_path / skill_name
    skill_dir.mkdir()
    skill_file = skill_dir / "SKILL.md"
    post = frontmatter.Post("skill body", **metadata)
    skill_file.write_text(frontmatter.dumps(post))
    return skill_file


# ── validate_component — clean pass ──────────────────────────────────────────


def test_validate_component_all_valid_returns_no_issues():
    """A fully valid metadata dict produces no failures or warnings."""
    failures, warnings = validate_component(VALID_METADATA)
    assert failures == [], f"unexpected failures: {failures}"
    assert warnings == [], f"unexpected warnings: {warnings}"


def test_validate_component_tested_true_returns_no_issues():
    """tested: true is a valid value with no warnings."""
    failures, warnings = validate_component(_meta(**{"tags.tested": True}))
    assert failures == []
    assert warnings == []


def test_validate_component_all_maturity_values_accepted():
    """All three valid maturity values pass without failure."""
    for value in ("draft", "tactical", "strategic"):
        failures, _ = validate_component(_meta(maturity=value))
        assert not any("maturity" in f for f in failures), f"maturity '{value}' unexpectedly failed"


def test_validate_component_all_criticality_values_accepted():
    """All four valid criticality values pass without failure."""
    for value in ("must", "should", "could", "want"):
        failures, _ = validate_component(_meta(**{"tags.criticality": value}))
        assert not any("criticality" in f for f in failures), f"criticality '{value}' unexpectedly failed"


def test_validate_component_all_status_values_accepted():
    """All four valid status values pass without failure."""
    for value in ("active", "dormant", "deprecated", "wip"):
        failures, _ = validate_component(_meta(**{"tags.status": value}))
        assert not any("status" in f for f in failures), f"status '{value}' unexpectedly failed"


# ── validate_component — FAIL cases ──────────────────────────────────────────


def test_validate_component_missing_maturity_fails():
    """Missing maturity key produces a FAIL."""
    failures, _ = validate_component(_meta(maturity=None))
    assert any("maturity" in f and "missing" in f for f in failures), f"expected maturity missing FAIL, got: {failures}"


def test_validate_component_invalid_maturity_fails():
    """An unrecognised maturity value produces a FAIL."""
    failures, _ = validate_component(_meta(maturity="production"))
    assert any("maturity" in f and "invalid" in f for f in failures), f"expected maturity invalid FAIL, got: {failures}"


def test_validate_component_missing_criticality_fails():
    """Missing tags.criticality produces a FAIL."""
    failures, _ = validate_component(_meta(**{"tags.criticality": None}))
    assert any("criticality" in f and "missing" in f for f in failures), f"expected criticality FAIL, got: {failures}"


def test_validate_component_invalid_criticality_fails():
    """An unrecognised criticality value produces a FAIL."""
    failures, _ = validate_component(_meta(**{"tags.criticality": "nice-to-have"}))
    assert any("criticality" in f and "invalid" in f for f in failures)


def test_validate_component_missing_status_fails():
    """Missing tags.status produces a FAIL."""
    failures, _ = validate_component(_meta(**{"tags.status": None}))
    assert any("status" in f and "missing" in f for f in failures), f"expected status FAIL, got: {failures}"


def test_validate_component_invalid_status_fails():
    """An unrecognised status value produces a FAIL."""
    failures, _ = validate_component(_meta(**{"tags.status": "retired"}))
    assert any("status" in f and "invalid" in f for f in failures)


def test_validate_component_missing_tested_fails():
    """Missing tags.tested produces a FAIL."""
    failures, _ = validate_component(_meta(**{"tags.tested": None}))
    assert any("tested" in f and "missing" in f for f in failures), f"expected tested FAIL, got: {failures}"


def test_validate_component_invalid_tested_fails():
    """A non-boolean tested value produces a FAIL."""
    failures, _ = validate_component(_meta(**{"tags.tested": "yes"}))
    assert any("tested" in f and "invalid" in f for f in failures)


def test_validate_component_missing_tags_block_fails_all_tag_fields():
    """A missing tags block causes criticality, status, and tested to all fail."""
    meta = {k: v for k, v in VALID_METADATA.items() if k != "tags"}
    failures, _ = validate_component(meta)
    assert any("criticality" in f for f in failures)
    assert any("status" in f for f in failures)
    assert any("tested" in f for f in failures)


def test_validate_component_non_dict_tags_block_fails():
    """A tags value that is not a dict causes all tag sub-fields to fail."""
    failures, _ = validate_component(_meta(tags="active"))
    assert any("criticality" in f for f in failures)
    assert any("status" in f for f in failures)
    assert any("tested" in f for f in failures)


# ── validate_component — WARN cases ──────────────────────────────────────────


def test_validate_component_must_untested_warns():
    """criticality:must + tested:false produces a warning."""
    _, warnings = validate_component(_meta(**{"tags.criticality": "must", "tags.tested": False}))
    assert any("tested" in w for w in warnings), f"expected tested warning, got: {warnings}"


def test_validate_component_should_untested_warns():
    """criticality:should + tested:false produces a warning."""
    _, warnings = validate_component(_meta(**{"tags.criticality": "should", "tags.tested": False}))
    assert any("tested" in w for w in warnings)


def test_validate_component_could_untested_no_warn():
    """criticality:could + tested:false does NOT produce a tested warning."""
    _, warnings = validate_component(_meta(**{"tags.criticality": "could", "tags.tested": False}))
    assert not any("tested" in w for w in warnings)


def test_validate_component_want_untested_no_warn():
    """criticality:want + tested:false does NOT produce a tested warning."""
    _, warnings = validate_component(_meta(**{"tags.criticality": "want", "tags.tested": False}))
    assert not any("tested" in w for w in warnings)


def test_validate_component_must_missing_last_reviewed_warns():
    """criticality:must without last-reviewed warns."""
    _, warnings = validate_component(_meta(**{"tags.criticality": "must"}))
    assert any("last-reviewed" in w for w in warnings)


def test_validate_component_should_missing_last_reviewed_warns():
    """criticality:should without last-reviewed warns."""
    _, warnings = validate_component(_meta(**{"tags.criticality": "should"}))
    assert any("last-reviewed" in w for w in warnings)


def test_validate_component_could_missing_last_reviewed_no_warn():
    """criticality:could without last-reviewed does NOT warn."""
    _, warnings = validate_component(_meta(**{"tags.criticality": "could"}))
    assert not any("last-reviewed" in w for w in warnings)


def test_validate_component_stale_last_reviewed_warns():
    """A last-reviewed date older than STALENESS_WARN_DAYS produces a warning."""
    stale = date.today() - timedelta(days=STALENESS_WARN_DAYS + 1)
    _, warnings = validate_component(_meta(**{"last-reviewed": stale}))
    assert any("last-reviewed" in w for w in warnings), f"expected staleness warning, got: {warnings}"


def test_validate_component_recent_last_reviewed_no_warn():
    """A last-reviewed date within STALENESS_WARN_DAYS does not warn."""
    recent = date.today() - timedelta(days=STALENESS_WARN_DAYS - 1)
    _, warnings = validate_component(_meta(**{"last-reviewed": recent}))
    assert not any("last-reviewed" in w and "days ago" in w for w in warnings)


def test_validate_component_tested_string_true_accepted():
    """tested: 'true' (string) is accepted as a valid boolean equivalent."""
    failures, _ = validate_component(_meta(**{"tags.tested": "true"}))
    assert not any("tested" in f for f in failures)


def test_validate_component_tested_string_false_accepted():
    """tested: 'false' (string) is accepted as a valid boolean equivalent."""
    failures, _ = validate_component(_meta(**{"tags.tested": "false"}))
    assert not any("tested" in f for f in failures)


# ── find_components ───────────────────────────────────────────────────────────


def test_find_components_returns_skill_md_files(tmp_path: Path):
    """SKILL.md files are always discovered."""
    _write_skill(tmp_path, "my-skill", VALID_METADATA)
    results = find_components(tmp_path)
    assert any(p.name == "SKILL.md" for p in results), "SKILL.md not found by find_components"


def test_find_components_skips_readme(tmp_path: Path):
    """README.md files are excluded from results."""
    _write_skill(tmp_path, "my-skill", VALID_METADATA)
    readme = tmp_path / "README.md"
    readme.write_text("# readme")
    results = find_components(tmp_path)
    assert not any(p.name == "README.md" for p in results)


def test_find_components_picks_up_tagged_non_skill_md(tmp_path: Path):
    """A non-SKILL.md file with a maturity key is included."""
    tagged = tmp_path / "agent.md"
    post = frontmatter.Post("agent body", **VALID_METADATA)
    tagged.write_text(frontmatter.dumps(post))
    results = find_components(tmp_path)
    assert tagged in results


def test_find_components_ignores_untagged_md(tmp_path: Path):
    """A .md file without a maturity key is silently excluded."""
    untagged = tmp_path / "docs.md"
    untagged.write_text("# no frontmatter here")
    results = find_components(tmp_path)
    assert untagged not in results


def test_find_components_returns_sorted(tmp_path: Path):
    """Results are returned in sorted order."""
    for name in ("z-skill", "a-skill", "m-skill"):
        _write_skill(tmp_path, name, VALID_METADATA)
    results = find_components(tmp_path)
    assert results == sorted(results)


def test_find_components_empty_dir_returns_empty_list(tmp_path: Path):
    """An empty directory returns an empty list."""
    assert find_components(tmp_path) == []
