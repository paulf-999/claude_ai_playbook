# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-01
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Proves hook_style_guide_response_standards.sh skips the responses the standard waives.

Short answers, skill output, code blocks, errors and plan-mode output are exempt
from the format checks. Each waiver test uses a response long enough to be checked
(50+ words) and pairs it with a control that has the marker removed and is flagged,
so a waiver can't pass just because its sample text is short.
``test_style_guide_response_standards_flags.py`` covers the checks themselves.
"""
import subprocess

from _shared_paths import HOOKS_DIR

HOOK_PATH = HOOKS_DIR / "hook_style_guide_response_standards.sh"
FLAG_HEADER = "🚩 Response Standards Check"
LONG_TEXT = (
    "This text is long enough to count as a substantive response under the fifty word rule, "
    "so without a waiver the hook would check it and flag the missing Summary, offer line and "
    "timing footer. It describes a change, the reasons for it, how it was verified, and what "
    "is still left to do afterwards."
)


def flagged(response: str) -> bool:
    """Run the hook and say whether it flagged the response.

    :param response: Response text sent on stdin.
    :type response: str
    :return: ``True`` when the hook printed its flag report.
    :rtype: bool
    """
    result = subprocess.run(["bash", str(HOOK_PATH)], input=response, text=True, capture_output=True)
    return FLAG_HEADER in result.stdout


def words(count: int) -> str:
    """Build a response of exactly ``count`` words.

    :param count: Number of words.
    :type count: int
    :return: The words joined by spaces.
    :rtype: str
    """
    return " ".join(["word"] * count)


def test_control_text_is_flagged():
    """The shared long text is flagged on its own, so every waiver below is meaningful."""
    assert len(LONG_TEXT.split()) >= 50, "LONG_TEXT must be at least 50 words to be checked"
    assert flagged(LONG_TEXT), "LONG_TEXT without a waiver marker must be flagged"


def test_answer_under_fifty_words_is_waived():
    """A 49-word answer is a short answer and isn't checked."""
    assert not flagged(words(49)), "49 words is a short answer and should be waived"


def test_answer_of_fifty_words_is_checked():
    """At 50 words an answer is substantive and gets checked."""
    assert flagged(words(50)), "50 words is substantive and should be checked"


def test_skill_output_marker_is_waived():
    """Skill output carrying the ⎿ marker isn't checked."""
    assert not flagged("⎿  Done (3 tool uses)\n\n" + LONG_TEXT), "⎿ skill output should be waived"
    assert flagged("Done (3 tool uses)\n\n" + LONG_TEXT), "the same text without ⎿ should be checked"


def test_skill_continuation_marker_is_waived():
    """Skill output carrying the ⎪ marker isn't checked."""
    assert not flagged(LONG_TEXT + "\n⎪ more skill output"), "⎪ skill output should be waived"


def test_leading_code_block_is_waived():
    """A response that starts with a code block isn't checked."""
    assert not flagged("```python\nprint('x')\n```\n\n" + LONG_TEXT), "a leading code block should be waived"
    assert flagged(LONG_TEXT + "\n\n```python\nprint('x')\n```"), "a code block later on should not waive"


def test_error_prefix_is_waived():
    """A response starting with 'Error:' isn't checked."""
    assert not flagged("Error: " + LONG_TEXT), "an 'Error:' response should be waived"
    assert flagged("Note: " + LONG_TEXT), "the same text with another prefix should be checked"


def test_cross_mark_prefix_is_waived():
    """A response starting with ❌ isn't checked."""
    assert not flagged("❌ " + LONG_TEXT), "a ❌ response should be waived"


def test_error_word_mid_response_does_not_waive():
    """'Error:' only waives at the very start of the response."""
    assert flagged(LONG_TEXT + " Error: this came later."), "a mid-response 'Error:' should not waive"


def test_plan_mode_marker_is_waived():
    """A response carrying a 'Planning: ' plan file link isn't checked."""
    assert not flagged("Planning: plans/example.md\n\n" + LONG_TEXT), "plan-mode output should be waived"
    assert flagged("Plan: plans/example.md\n\n" + LONG_TEXT), "without 'Planning: ' it should be checked"


def test_empty_response_is_waived():
    """An empty response is a short answer and gives no report."""
    assert not flagged(""), "an empty response should be waived"
