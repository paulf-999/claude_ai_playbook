# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 9/10
# Test complexity score: 10/10
# Python style compliant: Yes
# Date created:      2026-09-16
# Version:           3.0.0
# Date updated:      2026-09-30
# ─────────────────────────────────────────────────────────

"""Tests for plan-mode phase approval gates in claude_plans/_plan_mode_phase_gates.md.

Verifies the rule still requires a stop and explicit approval between plan
phases, uses the parent's Summary-format phase report (no separate
template, per a 2026-09-30 decision), and keeps its plan-approval exceptions.
Checks behaviour-bearing text, not emphasis words: the 2026-09-30 prompt audit
removed the stacked MANDATORY/CRITICAL/BLOCKING register and three duplicate
examples, so asserting those would lock in the style it replaced.
"""
import re

from _shared_paths import CLAUDE_DIR

RULE_FILE = CLAUDE_DIR / "_rules" / "02_claude_standards" / "claude_plans" / "_plan_mode_phase_gates.md"
PARENT_FILE = CLAUDE_DIR / "_rules" / "02_claude_standards" / "claude_plans.md"

PRESSURE_WORDS = ["MANDATORY", "CRITICAL", "BLOCKING", "non-negotiable", "absolute requirement"]


def _content() -> str:
    """Return the rule file's text.

    :return: Full rule content.
    """
    return RULE_FILE.read_text()


def test_title_names_plan_mode_phase_gates():
    """Rule keeps its H1 title so imports and README links stay meaningful."""
    assert "# 🗂️ Plan-Mode Phase Gates" in _content(), "Rule missing its H1 title"


def test_states_stop_after_each_phase():
    """Rule must tell Claude to stop after each phase in plan mode."""
    content = _content()
    assert re.search(r"In plan mode, stop after each phase", content), (
        "Rule must state that plan mode stops after each phase"
    )
    assert re.search(r"explicit approval before starting the next", content), (
        "Rule must require explicit approval before the next phase starts"
    )


def test_requires_waiting_for_explicit_response():
    """Rule must say to wait for an explicit user response, not auto-proceed."""
    content = _content()
    assert re.search(r"Wait for the user's explicit response", content), (
        "Rule must state to wait for the user's explicit response"
    )
    assert "silence as no approval" in content, (
        "Rule must state that silence is not approval"
    )


def test_explains_why_plans_require_gates():
    """Rule must keep its rationale so the gate isn't applied blindly."""
    content = _content()
    assert "**Why plans require gates:**" in content, "Rule missing its rationale heading"
    assert "decision boundaries" in content, "Rationale must name phases as decision boundaries"
    assert "wasted effort" in content, "Rationale must name wasted effort as the cost avoided"


def test_report_format_points_to_parent():
    """The child defers to the parent's phase report instead of defining its own."""
    content = _content()
    assert "**Report format:**" in content, "Rule must say which report format to use"
    assert "`claude_plans.md` → How to apply" in content, "Rule must point at the parent's How to apply"


def test_no_separate_report_template():
    """No standalone template competes with the Summary format (2026-09-30 decision)."""
    for name, text in (("child", _content()), ("parent", PARENT_FILE.read_text())):
        assert "Proceed? (yes/no/adjust)" not in text, f"{name} still carries the old template"
        assert "**Ready for Phase N+1:**" not in text, f"{name} still carries the old template"


def test_parent_report_uses_summary_format():
    """The parent's report is built from the normal Summary + Next steps format."""
    parent = PARENT_FILE.read_text()
    assert "claude_response_standards.md" in parent, "Parent must reference the response standards"
    assert "(Summary, then Next steps)" in parent, "Parent must name the Summary + Next steps shape"


def test_parent_report_lists_required_contents():
    """The report must still carry deliverables, the next phase, and an approve/adjust choice."""
    parent = PARENT_FILE.read_text()
    assert "one bullet per deliverable" in parent, "Report must list each deliverable"
    assert "names the next phase" in parent, "Report must name the next phase"
    assert "says work has stopped" in parent, "Report must say work has stopped"
    assert '"Start Phase N+1" as the recommended option' in parent, "Report must offer to start the next phase"
    assert '"Adjust first"' in parent, "Report must offer an adjust option"


def test_no_stacked_pressure_language():
    """Rule states the gate plainly, without all-caps emphasis markers."""
    content = _content()
    for word in PRESSURE_WORDS:
        assert word not in content, f"Rule reintroduced pressure wording: '{word}'"


def test_plan_approval_is_not_confirmation():
    """'Implement the following plan:' must still require an explicit go-ahead."""
    content = _content()
    assert '"Implement the following plan:" is not confirmation' in content, (
        "Rule must state that 'Implement the following plan:' is not confirmation"
    )


def test_keeps_todo_exception():
    """Exception 1 (TODO.md editing in plan mode) must survive."""
    assert "**Exception 1:**" in _content(), "Rule lost Exception 1 (TODO.md)"


def test_slash_command_exception_runs_without_prompt():
    """Exception 2 lets explicit slash commands run without a confirmation prompt."""
    content = _content()
    assert "**Exception 2:**" in content, "Rule lost Exception 2 (slash commands)"
    assert "run without a confirmation prompt" in content, (
        "Exception 2 must say slash commands run without a confirmation prompt"
    )


def test_keeps_plan_persistence_section():
    """The persist-to-_plans section and its incident note must survive."""
    content = _content()
    assert "## 📁 Persist the plan to `_plans/`" in content, "Rule lost the persistence section"
    assert "Incident (2026-09-19)" in content, "Rule lost the literal-~ incident note"


def test_rule_line_limit():
    """Rule must stay within the ~110-line rule-file limit (writing_style.md)."""
    lines = _content().splitlines()
    assert len(lines) <= 110, (
        f"Rule exceeds 110 lines ({len(lines)}). Split into parent + child if needed."
    )


def test_rule_ends_with_newline():
    """Rule must end with exactly one newline."""
    raw = RULE_FILE.read_bytes()
    assert raw.endswith(b"\n"), "Rule does not end with a newline"
    assert not raw.endswith(b"\n\n"), "Rule ends with multiple newlines"
