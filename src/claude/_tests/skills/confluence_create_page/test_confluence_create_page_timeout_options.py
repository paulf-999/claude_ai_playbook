# Test Metadata
# ─────────────────────────────────────────────────────────
# Date created:      2026-10-01
# Date updated:      2026-10-01
# Version:           1.2.0
# Test quality score: 9/10
# Test complexity score: 8/10
# Python style compliant: Yes
# ─────────────────────────────────────────────────────────

"""Tests the confluence_create_page timeout's options, with no threads or waiting.

Covers parsing ``--timeout-seconds``, the dialog's wording, how each [A]bort,
[R]etry or [C]ontinue answer resolves, including the 6-minute cap on [C]ontinue,
and where [A]bort's draft is kept: ``~/_drafts/confluence/``, not the config folder.
``test_confluence_create_page_timeout.py`` covers the timed behaviour.
"""
import time
from pathlib import Path
from unittest.mock import patch

from .confluence_create_page_handler import _handle_timeout_choice
from .confluence_create_page_handler import format_timeout_dialog
from .confluence_create_page_handler import parse_timeout_arg
from .confluence_create_page_handler import save_draft

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


def test_draft_is_saved_in_home_drafts_folder(tmp_path: Path):
    """A draft lands in ~/_drafts/confluence/ with its content, never under the config folder."""
    with patch("pathlib.Path.home", return_value=tmp_path):
        draft = save_draft("# Page\n\nBody.", "Q3 Roadmap")
    assert draft.parent == tmp_path / "_drafts" / "confluence", f"draft saved in the wrong folder: {draft}"
    assert ".claude" not in draft.parts, f"drafts must not depend on the config folder: {draft}"
    assert draft.read_text() == "# Page\n\nBody.", "the draft should hold the content unchanged"


def test_dialog_names_the_drafts_folder():
    """[A]bort's line in the dialog names the same folder the draft is saved in."""
    dialog = format_timeout_dialog(elapsed=120, remaining_attempts=1)
    assert "preserve draft in ~/_drafts/confluence/" in dialog, f"dialog should name the drafts folder, got {dialog!r}"


def test_draft_name_is_date_first_slug(tmp_path: Path):
    """A draft is named YYYY_MM_DD_<slug>.md, with the title folded to a clean slug."""
    with patch("pathlib.Path.home", return_value=tmp_path):
        draft = save_draft("Body.", "Q3 Roadmap -- 2026!")
    expected = f"{time.strftime('%Y_%m_%d')}_q3_roadmap_2026.md"
    assert draft.name == expected, f"expected {expected}, got {draft.name}"


def test_redraft_on_the_same_day_replaces_the_draft(tmp_path: Path):
    """Saving the same page twice in a day updates one draft rather than adding a copy."""
    with patch("pathlib.Path.home", return_value=tmp_path):
        first = save_draft("First.", "Q3 Roadmap")
        second = save_draft("Second.", "Q3 Roadmap")
    assert first == second, f"same-day drafts of one page should share a file, got {first} and {second}"
    assert second.read_text() == "Second.", "the later draft should replace the earlier one"
