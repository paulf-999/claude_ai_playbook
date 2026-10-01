# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-01
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Proves the skill authoring gate's walk checks (W1–W6) on fake skills.

The gate linter reports a walk check that fails a skill as FAIL, which blocks the
commit, and one that needs a human to judge as WARN, which doesn't. Each test builds
a fake skill that trips one check and confirms where it lands. Real skills are held
to these checks by ``test_skill_structure_compliance.py``'s crawl-gate test.
"""
from __future__ import annotations

from pathlib import Path

from _gate_fixtures import codes
from _gate_fixtures import make_skill
from _gate_fixtures import walk_run


def test_clean_skill_has_no_walk_findings(tmp_path: Path):
    """A short, emoji-headed skill with evals and no jargon passes every walk check."""
    failures, warnings = walk_run(make_skill(tmp_path), tmp_path)
    assert failures == [], f"a clean skill should have no failures, got {failures}"
    assert warnings == [], f"a clean skill should have no warnings, got {warnings}"


def test_w1_long_opening_fails(tmp_path: Path):
    """An opening of 100+ lines before the first ## section fails W1."""
    failures, _ = walk_run(make_skill(tmp_path, opening="line\n" * 110), tmp_path)
    assert "W1" in codes(failures), f"a 100+ line opening should fail W1, got {failures}"


def test_w1_unexplained_maturity_warns(tmp_path: Path):
    """'maturity' in the opening without its explanation is a W1 warning, not a failure."""
    skill = make_skill(tmp_path, opening="A skill at the draft maturity.")
    failures, warnings = walk_run(skill, tmp_path)
    assert "W1" in codes(warnings), f"unexplained maturity should warn W1, got {warnings}"
    assert "W1" not in codes(failures), "an unexplained term alone shouldn't block"


def test_w2_heading_without_emoji_warns(tmp_path: Path):
    """A ## heading with no emoji is a W2 warning."""
    _, warnings = walk_run(make_skill(tmp_path, extra="\n## Notes\n\nPlain heading.\n"), tmp_path)
    assert "W2" in codes(warnings), f"a bare ## heading should warn W2, got {warnings}"


def test_w2_long_skill_md_warns(tmp_path: Path):
    """A SKILL.md over 150 lines is a W2 warning."""
    _, warnings = walk_run(make_skill(tmp_path, extra="detail\n" * 160), tmp_path)
    assert any(w.startswith("W2: SKILL.md is") for w in warnings), f"a long file should warn W2, got {warnings}"


def test_w3_false_tested_claim_fails(tmp_path: Path):
    """Claiming tags.tested: true with no tests or evals fails W3."""
    skill = make_skill(tmp_path, tested=True, evals=False)
    failures, _ = walk_run(skill, tmp_path)
    assert any("claims tags.tested: true" in f for f in failures), f"a false claim should fail W3, got {failures}"


def test_w3_disclosed_gap_warns(tmp_path: Path):
    """No tests, no evals and an honest tested: false is a W3 warning only."""
    failures, warnings = walk_run(make_skill(tmp_path, tested=False, evals=False), tmp_path)
    assert "W3" in codes(warnings), f"an honest untested skill should warn W3, got {warnings}"
    assert "W3" not in codes(failures), "an honest, disclosed gap shouldn't block"


def test_w3_test_count_outside_maturity_range_fails(tmp_path: Path):
    """A tactical skill with only 2 test functions fails W3's 5–12 range."""
    tests_dir = tmp_path / "tests_dir"
    tests_dir.mkdir()
    (tests_dir / "test_demo_skill.py").write_text("def test_a():\n    pass\n\ndef test_b():\n    pass\n")
    failures, _ = walk_run(make_skill(tmp_path, maturity="tactical"), tests_dir)
    assert any(f.startswith("W3: tactical skill has 2 tests") for f in failures), f"got {failures}"


def test_w4_jargon_in_opening_prose_fails(tmp_path: Path):
    """MCP named in the opening prose without explanation fails W4."""
    failures, _ = walk_run(make_skill(tmp_path, opening="Calls the MCP server."), tmp_path)
    assert any(f.startswith("W4:") and "MCP" in f for f in failures), f"MCP jargon should fail W4, got {failures}"


def test_w4_ignores_frontmatter_keys(tmp_path: Path):
    """'maturity' as a frontmatter key isn't jargon in the prose."""
    failures, _ = walk_run(make_skill(tmp_path, maturity="draft"), tmp_path)
    assert "W4" not in codes(failures), f"frontmatter keys must not trip W4, got {failures}"


def test_w5_todo_blocks_tactical_but_not_draft(tmp_path: Path):
    """An open TODO fails W5 for a tactical skill and is allowed in a draft one."""
    tactical, _ = walk_run(make_skill(tmp_path / "t", maturity="tactical", extra="TODO: finish\n"), tmp_path)
    draft, _ = walk_run(make_skill(tmp_path / "d", maturity="draft", extra="TODO: finish\n"), tmp_path)
    assert "W5" in codes(tactical), f"a tactical TODO should fail W5, got {tactical}"
    assert "W5" not in codes(draft), f"a draft TODO is allowed, got {draft}"


def test_w6_short_phase_file_fails(tmp_path: Path):
    """A phase file under 100 characters fails W6."""
    skill = make_skill(tmp_path)
    (skill / "phase1.md").write_text("# Phase 1\n")
    failures, _ = walk_run(skill, tmp_path)
    assert any(f.startswith("W6: phase1.md") for f in failures), f"a stub phase file should fail W6, got {failures}"
