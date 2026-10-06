# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-08-28
# Date updated:      2026-10-06
# Version:           2.2.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Content tests for rules/03_authoring_guidelines/authoring_rules.md.

Each test guards one part of the rule-authoring guide — the five checklist
questions, the five creation steps and the key quality gates — so a lost
clause fails by name. Every file the guide sends an author to (template,
tiers, scorecard README, on-demand children, the structure test) must exist,
so the guide can't point at something that was moved or deleted.
"""
from __future__ import annotations

import re

from _shared_paths import CLAUDE_DIR, RULES_DIR

AUTHORING_RULES = RULES_DIR / "03_authoring_guidelines" / "authoring_rules.md"
TIERS = ("01_essentials", "02_claude_standards", "03_authoring_guidelines", "04_path_scoped")


def content() -> str:
    """Read authoring_rules.md.

    :return: The guide's text.
    :rtype: str
    """
    return AUTHORING_RULES.read_text()


def numbered_items(heading: str) -> list[str]:
    """List the bold titles of a section's numbered items.

    :param heading: Text of the ``##`` heading that starts the section.
    :type heading: str
    :return: The bold text of each ``1. **...**`` line, in order.
    :rtype: list[str]
    """
    section = content().split(heading, 1)[1].split("\n## ", 1)[0]
    return re.findall(r"^\d\. \*\*([^*]+)\*\*", section, re.M)


def test_checklist_has_five_questions():
    """The pre-creation checklist asks its five questions in order."""
    items = numbered_items("## ✅ Pre-Creation Checklist")
    assert len(items) == 5, f"expected 5 checklist questions, found {items}"
    assert items[0] == "Mechanical enforcement or instructional?", f"question 1 changed: {items[0]}"
    assert items[1] == "Always-on or lazy-loaded?", f"question 2 changed: {items[1]}"


def test_evidence_of_need_required():
    """Authors must show evidence of need, not a hypothetical."""
    assert "**Evidence of need** (not hypothetical)" in content(), "the evidence-of-need question is missing"


def test_creation_has_five_steps():
    """Rule creation keeps its five steps, ending with the scorecard."""
    steps = numbered_items("## 🚀 Rule Creation (5 Steps)")
    assert len(steps) == 5, f"expected 5 creation steps, found {steps}"
    assert steps[-1].startswith("Create a quality scorecard"), f"the last step should be the scorecard, got {steps[-1]}"


def test_template_exists():
    """The rule template the guide names exists."""
    assert "_templates/rule.md.template" in content(), "the guide no longer names the rule template"
    assert (CLAUDE_DIR / "_templates" / "rule.md.template").is_file(), "_templates/rule.md.template is missing"


def test_every_tier_named_exists():
    """Each tier the guide offers is a real folder."""
    missing = [t for t in TIERS if f"`{t}/`" not in content() or not (RULES_DIR / t).is_dir()]
    assert not missing, f"tiers missing from the guide or from rules/: {missing}"


def test_scorecard_template_exists():
    """The scorecard README the guide points to exists."""
    readme = CLAUDE_DIR / "_admin" / "_quality_scorecards" / "rules" / "README.md"
    assert readme.is_file(), f"the guide points to a scorecard template that's gone: {readme}"


def test_read_on_demand_children_exist():
    """Every on-demand child the guide names exists."""
    paths = re.findall(r"\*\*Read on demand:\*\* `~/[^/]+/([^`]+)`", content())
    assert len(paths) == 2, f"expected the common-mistakes and hard-gates pointers, found {paths}"
    missing = [p for p in paths if not (CLAUDE_DIR / p).is_file()]
    assert not missing, f"Read-on-demand pointers to missing files: {missing}"


def test_structure_test_exists():
    """The structural test every rule must pass is where the guide says."""
    assert "test_rules_structure.py" in content(), "the guide no longer names test_rules_structure.py"
    assert (CLAUDE_DIR / "_tests" / "rules" / "test_rules_structure.py").is_file(), "test_rules_structure.py is gone"


def test_children_must_be_placed_by_load_mode():
    """The guide says children under rules/ load natively and on-demand ones go in _rules_lazy_load/."""
    assert "**Place every child by how it should load**" in content(), "the child-placement gate is missing"
    assert "put them in `_rules_lazy_load/<topic>/`" in content(), "the on-demand children rule is missing"


def test_metadata_header_gate():
    """Rules carry the version/created/updated header and point to its standard."""
    assert "**Metadata header**" in content(), "the metadata-header gate is missing"
    pointer = "`rules/03_authoring_guidelines/shared_standards/_claude_config_metadata.md`"
    assert pointer in content(), "the guide must point to _claude_config_metadata.md"


def test_line_limit():
    """The guide stays within the 110-line rule limit."""
    lines = len(content().splitlines())
    assert lines <= 110, f"authoring_rules.md has {lines} lines — split it into a parent and children"
