# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-01
# Version:           1.0.0
# Test quality score: 9/10
# Test complexity score: 9/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests the confluence_create_page timeout's options, with no threads or waiting.

Covers parsing ``--timeout-seconds``, the dialog's wording, and how each
[A]bort, [R]etry or [C]ontinue answer resolves, including the 6-minute cap on
[C]ontinue. ``test_confluence_create_page_timeout.py`` covers the timed behaviour.
"""
from pathlib import Path

from .confluence_create_page_handler import _handle_timeout_choice
from .confluence_create_page_handler import format_timeout_dialog
from .confluence_create_page_handler import parse_timeout_arg

MAX_WAIT = 360


def test_timeout_defaults_to_two_minutes():
    """With no --timeout-seconds flag the timeout is 120 seconds."""
    assert parse_timeout_arg(["confluence_create_page"]) == 120, "the default timeout should be 120 seconds"


def test_timeout_flag_overrides_default():
    """--timeout-seconds sets the timeout."""
    assert parse_timeout_arg(["confluence_create_page", "--timeout-seconds", "300"]) == 300, "300 should be used"


def test_non_numeric_timeout_falls_back_to_default():
    """A non-numeric value is ignored in favour of the default."""
    assert parse_timeout_arg(["x", "--timeout-seconds", "soon"]) == 120, "a bad value should fall back to 120"


def test_flag_without_value_falls_back_to_default():
    """A trailing --timeout-seconds with no value is ignored."""
    assert parse_timeout_arg(["x", "--timeout-seconds"]) == 120, "a missing value should fall back to 120"


def test_dialog_offers_all_three_choices():
    """The dialog names the timeout and offers [A]bort, [R]etry and [C]ontinue."""
    dialog = format_timeout_dialog(elapsed=120, remaining_attempts=1)
    assert "CONFLUENCE PUBLISH TIMEOUT" in dialog, "the dialog should say it timed out"
    for option in ("[A]bort", "[R]etry", "[C]ontinue"):
        assert option in dialog, f"the dialog should offer {option}"


def test_dialog_states_the_six_minute_cap():
    """The dialog tells the user [C]ontinue stops at 6 minutes in total."""
    assert "max 6 minutes total" in format_timeout_dialog(elapsed=120, remaining_attempts=1), "cap should be stated"


def test_dialog_uses_singular_for_one_minute():
    """At 60 seconds the dialog says '1 minute', not '1 minutes'."""
    dialog = format_timeout_dialog(elapsed=60, remaining_attempts=1)
    assert "for 1 minute (60 seconds)" in dialog, f"expected singular minute, got {dialog!r}"


def test_dialog_uses_plural_for_two_minutes():
    """At 120 seconds the dialog says '2 minutes'."""
    dialog = format_timeout_dialog(elapsed=120, remaining_attempts=1)
    assert "for 2 minutes (120 seconds)" in dialog, f"expected plural minutes, got {dialog!r}"


def test_retry_ends_the_wait():
    """[R]etry ends this attempt and asks for a fresh one."""
    result, new_timeout = _handle_timeout_choice("R", 120, MAX_WAIT, None)
    assert result == {"status": "retry_requested", "elapsed": 120}, f"got {result}"
    assert new_timeout is None, "retry shouldn't extend the timeout"


def test_continue_adds_four_minutes():
    """[C]ontinue keeps waiting for another 240 seconds."""
    result, new_timeout = _handle_timeout_choice("C", 60, MAX_WAIT, None)
    assert result is None, "continue should keep polling, not return a result"
    assert new_timeout == 300, f"60s + 240s should give 300, got {new_timeout}"


def test_continue_is_capped_at_six_minutes():
    """[C]ontinue never extends the wait past 360 seconds."""
    _, new_timeout = _handle_timeout_choice("C", 200, MAX_WAIT, None)
    assert new_timeout == MAX_WAIT, f"200s + 240s should be capped at {MAX_WAIT}, got {new_timeout}"


def test_abort_keeps_the_draft_path():
    """[A]bort ends the wait and reports where the draft was kept."""
    result, _ = _handle_timeout_choice("A", 130, MAX_WAIT, Path("/drafts/page.md"))
    assert result == {"status": "aborted", "elapsed": 130, "draft_path": "/drafts/page.md"}, f"got {result}"


def test_unknown_answer_aborts():
    """Any answer other than A, R or C is treated as [A]bort."""
    result, new_timeout = _handle_timeout_choice("X", 130, MAX_WAIT, None)
    assert result == {"status": "aborted", "elapsed": 130, "draft_path": None}, f"got {result}"
    assert new_timeout is None, "an unknown answer shouldn't extend the timeout"
