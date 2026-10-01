# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-08-28
# Date updated:      2026-10-01
# Version:           2.0.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Content tests for _rules/02_claude_standards/behaviour/_decision_making.md.

Each test guards one clause of the intentionality gate — present 2–3 options with
one recommended, wait for the choice, and skip options when the path is clear —
so a lost clause fails by name. The two rules it defers to (the artefact gates
and the naming-candidate exception) are checked to still exist and agree.
"""
from __future__ import annotations

from _shared_paths import RULES_DIR

DECISION_MAKING = RULES_DIR / "02_claude_standards" / "behaviour" / "_decision_making.md"
ARTEFACT_GATES = RULES_DIR / "02_claude_standards" / "behaviour" / "_artefact_proposal_gates.md"
NAMING_PRINCIPLES = RULES_DIR / "01_essentials" / "claude_usage_standards" / "naming_standards"
NAMING_PRINCIPLES = NAMING_PRINCIPLES / "_naming_principles.md"


def content() -> str:
    """Read _decision_making.md.

    :return: The rule's text.
    :rtype: str
    """
    return DECISION_MAKING.read_text()


def test_core_principle():
    """The rule leads with 'present options, don't decide unilaterally'."""
    assert "**Present options, don't decide unilaterally.**" in content(), "core principle sentence is missing"


def test_two_to_three_options():
    """Options come in twos or threes, never four or more."""
    assert "**2–3 options:** Never 4+" in content(), "the 2–3 option limit is missing"


def test_one_option_recommended():
    """One option is marked recommended, and it leads."""
    assert '"Option Name (Recommended)"' in content(), "the (Recommended) label format is missing"
    assert "**One marked recommended:** Lead with the recommended option" in content(), (
        "the rule must say the recommended option leads"
    )


def test_uses_ask_user_question():
    """Options are presented with the AskUserQuestion tool."""
    assert "Use `AskUserQuestion` tool to present options" in content(), "AskUserQuestion is no longer named"


def test_waits_for_selection():
    """Claude waits for the user's choice and treats it as final."""
    assert "**Wait for selection:** Do not proceed until user has selected" in content(), (
        "wait-for-selection is missing"
    )


def test_user_direction_skips_options():
    """When the user has already chosen, Claude just executes."""
    assert "**User explicitly directs an approach:** User has already decided; just execute" in content(), (
        "the 'user explicitly directs' exemption is missing"
    )


def test_clear_bug_fixes_skip_options():
    """Bug fixes with one clear solution and typos don't need options."""
    assert "**Bug fixes with one clear solution:**" in content(), "the clear bug-fix exemption is missing"
    assert "**Typo fixes, single-line changes:**" in content(), "the typo exemption is missing"


def test_execution_signal():
    """The 'how to execute vs what to build' signal survives."""
    assert 'If the decision is about "how to execute" (not "what to build")' in content(), (
        "the execution signal is missing"
    )


def test_artefact_gates_come_first():
    """New artefacts pass the three gates before options, and that rule still exists."""
    assert "run the three gates in `_artefact_proposal_gates.md`" in content(), "the gates prerequisite is missing"
    assert ARTEFACT_GATES.is_file(), f"the rule it defers to is gone: {ARTEFACT_GATES}"


def test_naming_exception_matches_naming_rule():
    """The 3–4 name-candidate exception still matches _naming_principles.md."""
    assert "name candidates use the 3–4 range set in `_naming_principles.md`" in content(), "naming exception missing"
    assert "3–4 name candidates" in NAMING_PRINCIPLES.read_text(), (
        "_naming_principles.md no longer says 3–4 candidates, so the exception is out of date"
    )


def test_do_and_dont_examples():
    """The rule keeps both a DO and a DON'T example."""
    assert "**✅ DO:**" in content(), "the rule needs at least one DO example"
    assert "**❌ DON'T:**" in content(), "the rule needs at least one DON'T example"


def test_line_limit():
    """The rule stays within the 110-line limit."""
    lines = len(content().splitlines())
    assert lines <= 110, f"_decision_making.md has {lines} lines — split it into a parent and children"
