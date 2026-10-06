# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-06
# Version:           1.1.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests authoring_skills.md's maturity levels, scope boundaries and maintenance design.

The maturity table states eval counts and complexity caps that two other files repeat:
the hard-gates checklist and the shared complexity formula. Each pair must agree, so
editing one copy can't silently contradict another. The anti-patterns and the five
low-maintenance principles are checked clause by clause.
``test_authoring_skills.py`` covers what a skill must contain.
"""
from __future__ import annotations

import re

from _resolved_rule import resolved_content
from _shared_paths import LAZY_RULES_DIR, RULES_DIR

GUIDELINES = RULES_DIR / "03_authoring_guidelines"
RULE_FILE = GUIDELINES / "authoring_skills.md"
CHECKLIST = LAZY_RULES_DIR / "authoring_skills" / "_hard_gates_checklist.md"
COMPLEXITY_FORMULA = GUIDELINES / "shared_standards" / "_complexity_scoring.md"
LEVELS = ("Draft", "Tactical", "Strategic")


def content() -> str:
    """Read authoring_skills.md with every child inlined.

    :return: The full resolved rule text.
    :rtype: str
    """
    return resolved_content(RULE_FILE)


def table_row(label: str) -> list[str]:
    """Return the Draft, Tactical and Strategic cells of one maturity-table row.

    :param label: The bold row label, e.g. ``Test coverage``.
    :type label: str
    :return: The three level cells, in table order.
    :rtype: list[str]
    """
    row = re.search(rf"^\| \*\*{re.escape(label)}\*\* \|(.+)\|$", content(), re.M)
    assert row, f"the maturity table has no '{label}' row"
    return [cell.strip() for cell in row.group(1).split("|")]


def test_maturity_table_has_three_levels():
    """The maturity table's columns are Draft, Tactical and Strategic, in that order."""
    assert "| Evidence | Draft | Tactical | Strategic |" in content(), "the maturity table header changed"


def test_maturity_rests_on_evidence():
    """Each level is tied to a real problem and a use frequency."""
    assert table_row("Real problem")[1] == "Recurring, observed need", "tactical should need a recurring, observed need"
    assert table_row("Use frequency")[2] == "20+/month or always-on", "strategic should need heavy use"


def test_eval_counts_match_checklist():
    """The table's eval counts per level match the hard-gates checklist."""
    counts = [re.match(r"(\d+(?:–\d+|\+)) evals", cell).group(1) for cell in table_row("Test coverage")]
    assert counts == ["5–8", "8–12", "12+"], f"maturity eval counts changed: {counts}"
    expected = ", ".join(f"{level} {count} evals" for level, count in zip(LEVELS, counts))
    assert expected in CHECKLIST.read_text(), f"the checklist should say '{expected}'"


def test_eval_coverage_grows_with_maturity():
    """Higher levels add error cases, then edge cases and adversarial input."""
    coverage = table_row("Test coverage")
    assert "happy paths" in coverage[0], "draft evals should cover happy paths"
    assert "error cases" in coverage[1], "tactical evals should add error cases"
    assert "adversarial" in coverage[2], "strategic evals should add adversarial input"


def test_complexity_caps_match_shared_formula():
    """The table's complexity caps match the shared complexity formula."""
    caps = [re.match(r"≤(\d)", cell).group(1) for cell in table_row("Complexity (raw sum)")]
    assert caps == ["4", "6", "8"], f"maturity complexity caps changed: {caps}"
    expected = f"Draft ≤{caps[0]}, Tactical ≤{caps[1]}, Strategic ≤{caps[2]}"
    assert expected in COMPLEXITY_FORMULA.read_text(), f"_complexity_scoring.md should say '{expected}'"


def test_maturity_justified_in_best_for():
    """The chosen maturity is justified in one sentence on SKILL.md's Best For line."""
    rule = "**Where to justify it:** one sentence in SKILL.md's **Best For** line"
    assert rule in content(), "the maturity justification rule is missing"


def test_not_for_declares_scope():
    """Scope boundaries go in the contract's dispatch.not_for."""
    assert "## 🚪 Scope Boundaries [REQUIRED]" in content(), "the scope-boundaries section is missing"
    assert "list them under `dispatch.not_for`" in content(), "not_for is no longer the home for boundaries"


def test_anti_pattern_handle_everything():
    """The rule warns against one skill that tries to handle everything."""
    assert "**❌ Don't try to handle everything**" in content(), "the handle-everything anti-pattern is missing"


def test_anti_pattern_evals_not_replaced_by_pytest():
    """evals.yaml stays mandatory, and pytest is an addition rather than a replacement."""
    assert "`evals.yaml` is mandatory for every skill" in content(), "evals.yaml is no longer mandatory"
    assert "is a welcome *addition*, not a replacement" in content(), "pytest's role as an addition is missing"


def test_low_maintenance_principles():
    """The five low-maintenance principles are all present."""
    section = content().split("## 🛠️ Low-Maintenance Design [CRITICAL]", 1)[1]
    principles = re.findall(r"^- \*\*([^:*]+):\*\*", section, re.M)
    expected = [
        "Design for immutability",
        "Isolate dependencies",
        "Battle-tested tools only",
        "Freeze scope with `not_for`",
    ]
    assert principles[:4] == expected, f"low-maintenance principles changed: {principles}"
    assert "Evals are the contract" in principles, "the 'evals are the contract' principle is missing"


def test_no_skill_to_skill_calls():
    """Skills stay isolated, with no skill-to-skill calls."""
    assert "no skill-to-skill calls" in content(), "the isolation principle is missing"
