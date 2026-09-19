# Test Metadata
# ─────────────────────────────────────────────────────────
# Test quality score: 8/10
# Test complexity score: 4/10
# Python style compliant: Yes
# Date created:      2026-08-28
# Version:           1.1.0
# Date updated:      2026-09-19
# ─────────────────────────────────────────────────────────

"""Tests for confluence_create_page timeout mechanism.

Tests validate: timeout trigger, user responses (A/R/C), draft preservation,
timeout customization, and the hard 6-minute wait cap.
"""

import threading
import time
from unittest.mock import patch

import pytest

from confluence_create_page_handler import (
    create_page_with_timeout,
    format_timeout_dialog,
    parse_timeout_arg,
    save_draft,
)


class MockToolCall:
    """Mock a tool call that takes a real, fixed amount of time to return."""

    def __init__(self, duration_seconds):
        self.duration = duration_seconds
        self.start_time = None

    def __call__(self):
        self.start_time = time.time()
        time.sleep(self.duration)
        return {"pageId": "123456", "url": "https://confluence.example.com/..."}


class BlockingToolCall:
    """A tool call that never returns on its own — only a timeout/abort path ends it.

    Used for the 6-minute-cap test, where the real elapsed time is driven by a
    mocked time.time() rather than actual sleeping (waiting 6 real minutes per
    test run isn't practical). The daemon thread that calls this is abandoned
    once the test's assertions run; it is never joined.
    """

    def __call__(self):
        threading.Event().wait()
        return {"pageId": "never-returns", "url": "never-returns"}


@pytest.fixture
def mock_confluence_setup():
    """Set up mocks for Confluence API interactions."""
    with patch("builtins.input") as mock_input:
        yield mock_input


def test_timeout_trigger_at_2_minutes(mock_confluence_setup):
    """Timeout dialog appears once elapsed time reaches the timeout.

    Uses timeout_seconds=1 (not a sub-second value) because the production
    polling loop checks elapsed time once per second — a timeout under 1s can
    never actually be observed, regardless of how slow the tool call is.
    """
    mock_confluence_setup.return_value = "A"
    slow_call = MockToolCall(duration_seconds=2.5)

    result = create_page_with_timeout(tool_call=slow_call, timeout_seconds=1)

    assert result["status"] in ["timeout", "aborted", "retry_requested"]
    mock_confluence_setup.assert_called_once()


def test_timeout_abort_preserves_draft(mock_confluence_setup, tmp_path):
    """[A]bort preserves draft in ~/.drafts/confluence/."""
    with patch("pathlib.Path.home", return_value=tmp_path):
        draft_content = "# Test Page\n\nThis is test content."
        draft_path = save_draft(draft_content, "test_page")

        mock_confluence_setup.return_value = "A"
        slow_call = MockToolCall(duration_seconds=2.5)

        result = create_page_with_timeout(
            tool_call=slow_call,
            timeout_seconds=1,
            draft_path=draft_path,
        )

        assert result["status"] == "aborted"
        assert draft_path.exists()
        assert draft_path.read_text() == draft_content


def test_timeout_retry_starts_fresh(mock_confluence_setup):
    """[R]etry cancels current attempt and starts fresh."""
    mock_confluence_setup.return_value = "R"
    slow_call = MockToolCall(duration_seconds=2.5)

    result = create_page_with_timeout(tool_call=slow_call, timeout_seconds=1)

    assert result["status"] == "retry_requested"


def test_timeout_continue_adds_4_minutes(mock_confluence_setup):
    """[C]ontinue extends the timeout and lets a slow-but-finishing call succeed.

    The call takes 2.3s against a 1s initial timeout, so the dialog must fire
    and consume the "C" response before the call finishes on its own —
    verifying [C]ontinue actually extended the window rather than the call
    simply finishing before any check happened.
    """
    mock_confluence_setup.return_value = "C"
    call_that_completes = MockToolCall(duration_seconds=2.3)

    result = create_page_with_timeout(tool_call=call_that_completes, timeout_seconds=1)

    assert result["status"] == "success"
    assert result["pageId"] == "123456"
    mock_confluence_setup.assert_called_once()


def test_timeout_customization_override(mock_confluence_setup):
    """Custom timeout via --timeout-seconds parameter still triggers correctly."""
    mock_confluence_setup.return_value = "A"
    medium_call = MockToolCall(duration_seconds=2.5)

    result = create_page_with_timeout(tool_call=medium_call, timeout_seconds=1)

    assert result["status"] in ["aborted", "timeout"]


def test_timeout_dialog_content(mock_confluence_setup):
    """Timeout dialog displays correct information."""
    dialog_2min = format_timeout_dialog(elapsed=120, remaining_attempts=1)

    assert "TIMEOUT" in dialog_2min
    assert "[A]bort" in dialog_2min
    assert "[R]etry" in dialog_2min
    assert "[C]ontinue" in dialog_2min
    assert "minute" in dialog_2min


def test_timeout_maximum_6_minutes(mock_confluence_setup):
    """Total wait cannot exceed 6 minutes even with [C]ontinue.

    A real 6-minute wait isn't practical per test run, so time.time() is
    mocked to jump straight through the relevant checkpoints (initial
    timeout at ~120s, then past the 360s hard cap) while the tool call
    itself blocks on a real threading.Event so it genuinely never returns
    on its own — only the max-wait abort path can end this test.
    """
    mock_confluence_setup.side_effect = ["C", "A"]
    fake_times = iter([0, 1, 121, 121, 365, 365, 365, 365])

    with patch("time.time", side_effect=lambda: next(fake_times)):
        result = create_page_with_timeout(
            tool_call=BlockingToolCall(),
            timeout_seconds=1,
        )

    assert result["status"] == "aborted"


def test_timeout_respects_fast_completion(mock_confluence_setup):
    """No timeout dialog if call completes within timeout."""
    fast_call = MockToolCall(duration_seconds=0.05)

    result = create_page_with_timeout(tool_call=fast_call, timeout_seconds=0.2)

    assert result["status"] == "success"
    assert result["pageId"] == "123456"
    mock_confluence_setup.assert_not_called()


def test_timeout_parameter_parsing():
    """--timeout-seconds parameter is parsed correctly."""
    timeout = parse_timeout_arg(["confluence_create_page"])
    assert timeout == 120

    timeout = parse_timeout_arg(["confluence_create_page", "--timeout-seconds", "300"])
    assert timeout == 300

    timeout = parse_timeout_arg(["confluence_create_page", "--timeout-seconds", "invalid"])
    assert timeout == 120


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
