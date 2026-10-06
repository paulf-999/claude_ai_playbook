# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-08-28
# Date updated:      2026-10-06
# Version:           2.0.3
# Test quality score: 9/10
# Test complexity score: 7/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests confluence_create_page's timeout wrapper while a real call is running.

Covers when the dialog fires, what each answer does to a live call, the 6-minute
cap, draft preservation, and the result for a call that errors or returns nothing.
The tool call runs on a real thread; only the 6-minute test fakes the clock.
``test_confluence_create_page_timeout_options.py`` covers the dialog and its answers.
"""
from __future__ import annotations

import threading
import time
from unittest.mock import patch

import pytest

from . import confluence_create_page_handler as handler
from .confluence_create_page_handler import create_page_with_timeout, save_draft


class MockToolCall:
    """A tool call that takes a real, fixed time to return a page."""

    def __init__(self, duration_seconds: float, result: dict | None = None):
        """Set how long the call takes and what it returns.

        :param duration_seconds: Seconds to sleep before returning.
        :param result: What to return, or None for the default page.
        """
        self.duration = duration_seconds
        self.result = {"pageId": "123456", "url": "https://confluence.example.com/x"} if result is None else result

    def __call__(self):
        """Sleep, then return the result.

        :return: The configured result.
        """
        time.sleep(self.duration)
        return self.result


class BlockingToolCall:
    """A tool call that never returns, so only the timeout path can end the test."""

    def __call__(self):
        """Block forever on an event nothing sets.

        :return: Never returns.
        """
        threading.Event().wait()
        return {}


@pytest.fixture
def answers():
    """Patch input() so each test can script the user's answers to the dialog.

    :return: The mock standing in for input().
    """
    with patch("builtins.input") as mock_input:
        yield mock_input


def test_dialog_fires_once_the_timeout_passes(answers):
    """A call still running after the timeout shows the dialog once, and [A]bort ends it."""
    answers.return_value = "A"
    result = create_page_with_timeout(tool_call=MockToolCall(2.5), timeout_seconds=1)
    assert result["status"] == "aborted", f"[A]bort should end the wait, got {result}"
    assert result["elapsed"] >= 1, f"the dialog shouldn't appear before the timeout, got {result['elapsed']}s"
    answers.assert_called_once()


def test_abort_keeps_the_draft(answers, tmp_path):
    """[A]bort reports the draft's path, and the draft is still there with its content."""
    with patch.object(handler, "CLAUDE_DIR", tmp_path):
        draft = save_draft("# Test Page\n\nBody.", "test_page")
        answers.return_value = "A"
        result = create_page_with_timeout(tool_call=MockToolCall(2.5), timeout_seconds=1, draft_path=draft)
    assert result["draft_path"] == str(draft), f"the result should point at the draft, got {result}"
    assert draft.read_text() == "# Test Page\n\nBody.", "the draft should be kept unchanged"


def test_retry_ends_the_live_call(answers):
    """[R]etry ends the running call and asks for a fresh attempt."""
    answers.return_value = "R"
    result = create_page_with_timeout(tool_call=MockToolCall(2.5), timeout_seconds=1)
    assert result["status"] == "retry_requested", f"[R]etry should end the call, got {result}"


def test_continue_lets_a_slow_call_finish(answers):
    """[C]ontinue extends the wait, so a call that finishes later still succeeds."""
    answers.return_value = "C"
    result = create_page_with_timeout(tool_call=MockToolCall(2.3), timeout_seconds=1)
    assert result["status"] == "success", f"the call should finish after [C]ontinue, got {result}"
    assert result["pageId"] == "123456", "the page from the call should come back"
    answers.assert_called_once()


def test_longer_custom_timeout_avoids_the_dialog(answers):
    """A 3-second timeout lets a 1.5-second call finish without asking, where 1 second would ask."""
    result = create_page_with_timeout(tool_call=MockToolCall(1.5), timeout_seconds=3)
    assert result["status"] == "success", f"the call should finish inside the custom timeout, got {result}"
    answers.assert_not_called()


def test_wait_never_passes_six_minutes(answers):
    """Even after [C]ontinue, a call still running at 360 seconds is aborted."""
    answers.side_effect = ["C", "A"]
    fake_times = iter([0, 1, 121, 121, 365, 365, 365, 365])
    with patch("time.time", side_effect=lambda: next(fake_times)):
        result = create_page_with_timeout(tool_call=BlockingToolCall(), timeout_seconds=1)
    assert result["status"] == "aborted", f"the 6-minute cap should abort, got {result}"
    assert result["elapsed"] >= 360, f"the abort should come at or after 360s, got {result['elapsed']}"


def test_fast_call_never_asks(answers):
    """A call that finishes inside the timeout returns its page without a dialog."""
    result = create_page_with_timeout(tool_call=MockToolCall(0.05), timeout_seconds=1)
    assert result["status"] == "success", f"a fast call should succeed, got {result}"
    answers.assert_not_called()


def test_failing_call_reports_its_error(answers):
    """A call that raises is reported as an error with its message."""

    def failing_call():
        raise ConnectionError("network down")

    result = create_page_with_timeout(tool_call=failing_call, timeout_seconds=1)
    assert result["status"] == "error", f"a raising call should be an error, got {result}"
    assert result["error"] == "network down", f"the error message should come through, got {result}"


def test_empty_result_is_unknown(answers):
    """A call that returns nothing is reported as unknown, not success."""
    result = create_page_with_timeout(tool_call=MockToolCall(0.05, result={}), timeout_seconds=1)
    assert result["status"] == "unknown", f"an empty result shouldn't count as success, got {result}"


def test_closed_input_aborts(answers):
    """If the user closes input (Ctrl-D) at the dialog, the wait aborts."""
    answers.side_effect = EOFError
    result = create_page_with_timeout(tool_call=MockToolCall(2.5), timeout_seconds=1)
    assert result["status"] == "aborted", f"closed input should abort, got {result}"
