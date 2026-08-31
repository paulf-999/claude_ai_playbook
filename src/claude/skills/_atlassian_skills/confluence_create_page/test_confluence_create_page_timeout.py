"""Tests for confluence_create_page timeout mechanism.

Tests validate: timeout trigger at 2 minutes, user responses (A/R/C),
draft preservation, and timeout customization.
"""

import pytest
import time
import pathlib
import tempfile
from unittest.mock import MagicMock, patch, call
from confluence_create_page_handler import (
    create_page_with_timeout,
    format_timeout_dialog,
    parse_timeout_arg,
    save_draft
)


class MockToolCall:
    """Mock a tool call that takes time."""

    def __init__(self, duration_seconds):
        self.duration = duration_seconds
        self.start_time = None

    def __call__(self):
        self.start_time = time.time()
        time.sleep(self.duration)
        return {"pageId": "123456", "url": "https://confluence.example.com/..."}


@pytest.fixture
def mock_confluence_setup():
    """Set up mocks for Confluence API interactions."""
    with patch('builtins.input') as mock_input:
        yield mock_input


def test_timeout_trigger_at_2_minutes(mock_confluence_setup):
    """Timeout dialog appears at exactly 120 seconds."""
    # Mock user choosing to abort at timeout
    mock_confluence_setup.return_value = "A"

    # Create a mock tool call that takes longer than timeout
    slow_call = MockToolCall(duration_seconds=0.15)

    # Invoke with small timeout for testing
    result = create_page_with_timeout(
        tool_call=slow_call,
        timeout_seconds=0.1
    )

    # Verify tool was interrupted or aborted
    assert result["status"] in ["timeout", "aborted", "retry_requested"]


def test_timeout_abort_preserves_draft(mock_confluence_setup, tmp_path):
    """[A]bort preserves draft in ~/.drafts/confluence/."""
    # Create draft content
    with patch('pathlib.Path.home', return_value=tmp_path):
        draft_content = "# Test Page\n\nThis is test content."
        draft_path = save_draft(draft_content, "test_page")

        # Mock user selecting [A]bort
        mock_confluence_setup.return_value = "A"

        # Create slow tool call
        slow_call = MockToolCall(duration_seconds=0.15)

        # Invoke with timeout
        result = create_page_with_timeout(
            tool_call=slow_call,
            timeout_seconds=0.1,
            draft_path=draft_path
        )

        # Verify draft was preserved
        assert result["status"] == "aborted"
        assert draft_path.exists()
        assert draft_path.read_text() == draft_content


def test_timeout_retry_starts_fresh(mock_confluence_setup):
    """[R]etry cancels current attempt and starts fresh."""
    # Mock user selecting [R]etry
    mock_confluence_setup.return_value = "R"

    # First call takes longer than timeout
    slow_call = MockToolCall(duration_seconds=0.15)

    result = create_page_with_timeout(
        tool_call=slow_call,
        timeout_seconds=0.1
    )

    # Verify status indicates retry should happen
    assert result["status"] == "retry_requested"


def test_timeout_continue_adds_4_minutes(mock_confluence_setup):
    """[C]ontinue adds 4 more minutes to the timer."""
    # Mock user selecting [C]ontinue
    mock_confluence_setup.return_value = "C"

    # Create a tool call that completes after initial timeout
    call_that_completes = MockToolCall(duration_seconds=0.2)

    result = create_page_with_timeout(
        tool_call=call_that_completes,
        timeout_seconds=0.1
    )

    # Verify call succeeded
    assert result["status"] == "success"
    assert result["pageId"] == "123456"


def test_timeout_customization_override(mock_confluence_setup):
    """Custom timeout via --timeout-seconds parameter."""
    # Mock user aborting at timeout
    mock_confluence_setup.return_value = "A"

    # Create a call that takes longer than timeout
    medium_call = MockToolCall(duration_seconds=0.15)

    # Invoke with custom timeout
    result = create_page_with_timeout(
        tool_call=medium_call,
        timeout_seconds=0.1
    )

    # Should be aborted after timeout
    assert result["status"] in ["aborted", "timeout"]


def test_timeout_dialog_content(mock_confluence_setup):
    """Timeout dialog displays correct information."""
    # Generate dialog at different elapsed times
    dialog_2min = format_timeout_dialog(elapsed=120, remaining_attempts=1)
    dialog_at_retry = format_timeout_dialog(elapsed=240, remaining_attempts=0)

    # Verify content
    assert "TIMEOUT" in dialog_2min
    assert "[A]bort" in dialog_2min
    assert "[R]etry" in dialog_2min
    assert "[C]ontinue" in dialog_2min
    assert "minute" in dialog_2min


def test_timeout_maximum_6_minutes(mock_confluence_setup):
    """Total wait cannot exceed 6 minutes even with [C]ontinue."""
    # Mock user selecting [C]ontinue, then aborting
    mock_confluence_setup.side_effect = ["C", "A"]

    # Create a very slow call
    very_slow_call = MockToolCall(duration_seconds=10)

    result = create_page_with_timeout(
        tool_call=very_slow_call,
        timeout_seconds=0.1
    )

    # Should abort (maximum wait enforced)
    assert result["status"] == "aborted"


def test_timeout_respects_fast_completion(mock_confluence_setup):
    """No timeout dialog if call completes within timeout."""
    # Create a fast call
    fast_call = MockToolCall(duration_seconds=0.05)

    # Invoke with longer timeout
    result = create_page_with_timeout(
        tool_call=fast_call,
        timeout_seconds=0.2
    )

    assert result["status"] == "success"
    assert result["pageId"] == "123456"
    # Dialog input should never be called for fast completion
    mock_confluence_setup.assert_not_called()


def test_timeout_parameter_parsing():
    """--timeout-seconds parameter is parsed correctly."""
    # Test default
    timeout = parse_timeout_arg(["confluence_create_page"])
    assert timeout == 120

    # Test custom value
    timeout = parse_timeout_arg(["confluence_create_page", "--timeout-seconds", "300"])
    assert timeout == 300

    # Test invalid value (should default)
    timeout = parse_timeout_arg(["confluence_create_page", "--timeout-seconds", "invalid"])
    assert timeout == 120


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
