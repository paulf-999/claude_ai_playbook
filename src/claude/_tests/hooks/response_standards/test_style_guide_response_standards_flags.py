# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-01
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Proves hook_style_guide_response_standards.sh flags each response-format gap.

The hook is reserved, not registered (see response_standards_enforcement.md), so
these tests keep it working for the day it's wired in as a Stop hook. Each test
sends a substantive response (50+ words) missing one part of the standard: the
Summary, the offer line, the timing footer, or a clean ending after the footer.
``test_style_guide_response_standards_waivers.py`` covers the responses it skips.
"""
import subprocess

from _shared_paths import HOOKS_DIR

HOOK_PATH = HOOKS_DIR / "hook_style_guide_response_standards.sh"
FLAG_HEADER = "🚩 Response Standards Check"
SUMMARY_FLAG = "Missing **Summary** block"
OFFER_FLAG = "Missing offer line"
TIMING_FLAG = "Missing response timing footer"
AFTER_TIMING_FLAG = "Content found after timing footer"
BODY = (
    "This paragraph pads the response past the fifty word threshold so the hook treats it as "
    "substantive and applies every check. It talks about the change, why it matters, what was "
    "verified and what is left to do, which is the normal shape of a real answer from Claude."
)
SUMMARY = "**Summary**\n\n🎯 **Theme**\n- ✅ One point\n- 🔁 Another point"
OFFER = "More detail? (Y/N)"
FOOTER = "Response time: 45s"


def run_hook(response: str) -> subprocess.CompletedProcess:
    """Run the hook on one response.

    :param response: Response text sent on stdin.
    :type response: str
    :return: The completed hook run.
    :rtype: subprocess.CompletedProcess
    """
    return subprocess.run(["bash", str(HOOK_PATH)], input=response, text=True, capture_output=True)


def build(*parts: str) -> str:
    """Join response parts with blank lines.

    :param parts: Pieces of the response, in order.
    :type parts: str
    :return: The full response.
    :rtype: str
    """
    return "\n\n".join(parts)


def test_compliant_response_passes():
    """A response with every part gives no flags."""
    result = run_hook(build(SUMMARY, BODY, OFFER, FOOTER))
    assert FLAG_HEADER not in result.stdout, f"compliant response should pass, got {result.stdout}"


def test_missing_summary_is_flagged():
    """A substantive response without **Summary** is flagged."""
    result = run_hook(build(BODY, OFFER, FOOTER))
    assert SUMMARY_FLAG in result.stdout, f"should flag the missing Summary, got {result.stdout}"
    assert OFFER_FLAG not in result.stdout, f"only the Summary is missing, got {result.stdout}"


def test_missing_offer_line_is_flagged():
    """A substantive response without the offer line is flagged."""
    result = run_hook(build(SUMMARY, BODY, FOOTER))
    assert OFFER_FLAG in result.stdout, f"should flag the missing offer line, got {result.stdout}"
    assert SUMMARY_FLAG not in result.stdout, f"only the offer line is missing, got {result.stdout}"


def test_offer_line_inside_a_sentence_is_flagged():
    """The offer line must sit on its own line, not inside other text."""
    result = run_hook(build(SUMMARY, BODY + " More detail? (Y/N) is the usual question.", FOOTER))
    assert OFFER_FLAG in result.stdout, f"an inline offer line should be flagged, got {result.stdout}"


def test_offer_line_with_next_steps_suffix_passes():
    """The offer line may carry the 'pick a next step' suffix."""
    result = run_hook(build(SUMMARY, BODY, "More detail? (Y/N), or pick a next step (1–3)", FOOTER))
    assert OFFER_FLAG not in result.stdout, f"the next-steps suffix should be allowed, got {result.stdout}"


def test_missing_timing_footer_is_flagged():
    """A substantive response without the timing footer is flagged."""
    result = run_hook(build(SUMMARY, BODY, OFFER))
    assert TIMING_FLAG in result.stdout, f"should flag the missing footer, got {result.stdout}"
    assert "Response time: Xs" in result.stdout, f"the fix should show the current footer format, got {result.stdout}"


def test_minutes_footer_passes():
    """A footer over a minute, like 'Response time: 1min 15s', is accepted."""
    result = run_hook(build(SUMMARY, BODY, OFFER, "Response time: 1min 15s"))
    assert TIMING_FLAG not in result.stdout, f"the minutes format should pass, got {result.stdout}"
    assert AFTER_TIMING_FLAG not in result.stdout, f"nothing follows the footer, got {result.stdout}"


def test_content_after_footer_is_flagged():
    """Text after the timing footer is flagged, since the footer must be last."""
    result = run_hook(build(SUMMARY, BODY, OFFER, FOOTER, "One more thought."))
    assert AFTER_TIMING_FLAG in result.stdout, f"text after the footer should be flagged, got {result.stdout}"


def test_trailing_blank_lines_after_footer_pass():
    """Blank lines after the footer don't count as content."""
    result = run_hook(build(SUMMARY, BODY, OFFER, FOOTER) + "\n\n   \n")
    assert AFTER_TIMING_FLAG not in result.stdout, f"trailing whitespace should be ignored, got {result.stdout}"


def test_every_gap_is_reported_together():
    """A response missing all three parts gets all three flags in one report."""
    result = run_hook(build(BODY, BODY))
    assert SUMMARY_FLAG in result.stdout, f"should flag the Summary, got {result.stdout}"
    assert OFFER_FLAG in result.stdout, f"should flag the offer line, got {result.stdout}"
    assert TIMING_FLAG in result.stdout, f"should flag the footer, got {result.stdout}"
    assert result.stdout.count(FLAG_HEADER) == 1, f"flags should share one report header, got {result.stdout}"


def test_flags_never_block():
    """The hook warns without blocking, so it always exits 0."""
    result = run_hook(build(BODY, BODY))
    assert result.returncode == 0, f"the hook must never block, got exit {result.returncode}"
