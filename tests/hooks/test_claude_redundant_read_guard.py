"""Unit tests for src/claude/wip/hooks/claude_redundant_read_guard.py.

Covers fingerprint stability/size-cap/windowed-vs-full-read behaviour, state
load/save/corruption handling, TTL pruning, and the full main() entry point
(first read allows, immediate identical re-read denies, re-read after an edit
allows, a different offset/limit window allows, and malformed input always
fails open).
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src" / "claude" / "wip" / "hooks"))

from claude_redundant_read_guard import (  # noqa: E402
    _default_state,
    _fingerprint_file,
    _format_window,
    _load_state,
    _prune_stale_sessions,
    _read_hook_input,
    _save_state,
    main,
)


# ---------------------------------------------------------------------------
# _read_hook_input
# ---------------------------------------------------------------------------


class TestReadHookInput:
    """Tests for stdin JSON parsing."""

    def test_parses_valid_json(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Returns parsed dict for valid JSON input."""
        payload = {"session_id": "abc", "tool_name": "Read", "tool_input": {"file_path": "/tmp/f.py"}}
        monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(payload)))
        assert _read_hook_input() == payload

    def test_returns_empty_dict_on_invalid_json(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Returns empty dict when stdin contains invalid JSON."""
        monkeypatch.setattr("sys.stdin", io.StringIO("not json"))
        assert _read_hook_input() == {}

    def test_returns_empty_dict_on_empty_stdin(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Returns empty dict when stdin is empty."""
        monkeypatch.setattr("sys.stdin", io.StringIO(""))
        assert _read_hook_input() == {}


# ---------------------------------------------------------------------------
# _format_window
# ---------------------------------------------------------------------------


class TestFormatWindow:
    """Tests for the read-window key fragment."""

    def test_full_read_has_empty_window(self) -> None:
        """A read with no offset/limit produces an empty window fragment."""
        assert _format_window(None, None) == ":"

    def test_windowed_read_includes_both_values(self) -> None:
        """A read with offset and limit encodes both in the fragment."""
        assert _format_window(10, 50) == "10:50"

    def test_offset_only(self) -> None:
        """A read with only an offset encodes it, leaving limit empty."""
        assert _format_window(10, None) == "10:"


# ---------------------------------------------------------------------------
# _fingerprint_file
# ---------------------------------------------------------------------------


class TestFingerprintFile:
    """Tests for content fingerprinting."""

    def test_same_content_produces_same_hash(self, tmp_path: Path) -> None:
        """Identical content yields identical hashes across separate calls."""
        f = tmp_path / "a.py"
        f.write_text("print('hello')\n")
        assert _fingerprint_file(str(f), None, None) == _fingerprint_file(str(f), None, None)

    def test_edit_changes_hash(self, tmp_path: Path) -> None:
        """Editing the file changes the resulting hash."""
        f = tmp_path / "a.py"
        f.write_text("print('hello')\n")
        before = _fingerprint_file(str(f), None, None)
        f.write_text("print('goodbye')\n")
        after = _fingerprint_file(str(f), None, None)
        assert before != after

    def test_over_size_cap_returns_none(self, tmp_path: Path) -> None:
        """Files larger than max_bytes are skipped entirely."""
        f = tmp_path / "big.py"
        f.write_text("x" * 100)
        assert _fingerprint_file(str(f), None, None, max_bytes=10) is None

    def test_missing_file_returns_none(self, tmp_path: Path) -> None:
        """A nonexistent file fails open rather than raising."""
        assert _fingerprint_file(str(tmp_path / "missing.py"), None, None) is None

    def test_windowed_read_differs_from_full_read(self, tmp_path: Path) -> None:
        """A windowed read of part of a file hashes differently from a full read."""
        f = tmp_path / "a.py"
        f.write_text("line1\nline2\nline3\nline4\n")
        full = _fingerprint_file(str(f), None, None)
        windowed = _fingerprint_file(str(f), 1, 2)
        assert full != windowed

    def test_windowed_read_at_different_range_differs(self, tmp_path: Path) -> None:
        """Two windowed reads at different ranges of the same file hash differently."""
        f = tmp_path / "a.py"
        f.write_text("line1\nline2\nline3\nline4\n")
        first_window = _fingerprint_file(str(f), 1, 2)
        second_window = _fingerprint_file(str(f), 3, 2)
        assert first_window != second_window

    def test_same_windowed_range_hashes_identically(self, tmp_path: Path) -> None:
        """Repeated reads of the same window hash identically."""
        f = tmp_path / "a.py"
        f.write_text("line1\nline2\nline3\nline4\n")
        assert _fingerprint_file(str(f), 2, 2) == _fingerprint_file(str(f), 2, 2)


# ---------------------------------------------------------------------------
# _load_state / _save_state
# ---------------------------------------------------------------------------


class TestLoadState:
    """Tests for state loading, including corruption handling."""

    def test_returns_default_state_when_file_missing(self, tmp_path: Path) -> None:
        """A missing state file yields a fresh empty state."""
        assert _load_state(tmp_path / "missing.json") == _default_state()

    def test_returns_default_state_on_corrupt_json(self, tmp_path: Path) -> None:
        """Corrupt JSON on disk is treated as no prior state."""
        state_path = tmp_path / "state.json"
        state_path.write_text("not json")
        assert _load_state(state_path) == _default_state()

    def test_loads_existing_state(self, tmp_path: Path) -> None:
        """Existing valid state is loaded as-is."""
        state_path = tmp_path / "state.json"
        existing = {"sessions": {"abc": {"last_touched": 100.0, "files": {"f.py|:": "deadbeef"}}}}
        state_path.write_text(json.dumps(existing))
        assert _load_state(state_path) == existing


class TestSaveState:
    """Tests for state persistence."""

    def test_round_trips_through_disk(self, tmp_path: Path) -> None:
        """State written by _save_state is read back identically, creating parent dirs."""
        state_path = tmp_path / "sub" / "state.json"
        state = {"sessions": {"abc": {"last_touched": 1.0, "files": {}}}}
        _save_state(state_path, state)
        assert json.loads(state_path.read_text()) == state


# ---------------------------------------------------------------------------
# _prune_stale_sessions
# ---------------------------------------------------------------------------


class TestPruneStaleSessions:
    """Tests for TTL-based session pruning."""

    def test_keeps_recently_touched_session(self) -> None:
        """A session touched within the TTL window is retained."""
        state = {"sessions": {"abc": {"last_touched": 100.0, "files": {}}}}
        _prune_stale_sessions(state, now=200.0, ttl_seconds=1000.0)
        assert "abc" in state["sessions"]

    def test_drops_stale_session(self) -> None:
        """A session untouched beyond the TTL window is removed."""
        state = {"sessions": {"abc": {"last_touched": 100.0, "files": {}}}}
        _prune_stale_sessions(state, now=2000.0, ttl_seconds=1000.0)
        assert "abc" not in state["sessions"]

    def test_only_drops_stale_sessions(self) -> None:
        """Fresh sessions survive pruning alongside removed stale ones."""
        state = {
            "sessions": {
                "stale": {"last_touched": 100.0, "files": {}},
                "fresh": {"last_touched": 1900.0, "files": {}},
            }
        }
        _prune_stale_sessions(state, now=2000.0, ttl_seconds=1000.0)
        assert "stale" not in state["sessions"]
        assert "fresh" in state["sessions"]


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def _payload(session_id: str, file_path: str, offset: int | None = None, limit: int | None = None) -> str:
    """Build a PreToolUse Read hook payload as a JSON string.

    :param session_id: The session identifier.
    :type session_id: str
    :param file_path: The file path being read.
    :type file_path: str
    :param offset: The requested offset, if any.
    :type offset: int | None
    :param limit: The requested limit, if any.
    :type limit: int | None
    :return: JSON-encoded hook input.
    :rtype: str
    """
    tool_input = {"file_path": file_path}
    if offset is not None:
        tool_input["offset"] = offset
    if limit is not None:
        tool_input["limit"] = limit
    return json.dumps({"session_id": session_id, "tool_name": "Read", "tool_input": tool_input})


class TestMain:
    """Integration tests for the main() entry point."""

    def test_first_read_allows(self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture,
                                tmp_path: Path) -> None:
        """The first read of a file in a session is always allowed."""
        f = tmp_path / "a.py"
        f.write_text("print('hi')\n")
        monkeypatch.setattr("sys.stdin", io.StringIO(_payload("sess-1", str(f))))
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0
        assert capsys.readouterr().out == ""

    def test_identical_reread_denies(self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture,
                                      tmp_path: Path) -> None:
        """An immediate identical re-read of the same file is denied."""
        f = tmp_path / "a.py"
        f.write_text("print('hi')\n")

        monkeypatch.setattr("sys.stdin", io.StringIO(_payload("sess-1", str(f))))
        with pytest.raises(SystemExit):
            main()

        monkeypatch.setattr("sys.stdin", io.StringIO(_payload("sess-1", str(f))))
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0
        out = json.loads(capsys.readouterr().out)
        assert out["hookSpecificOutput"]["hookEventName"] == "PreToolUse"
        assert out["hookSpecificOutput"]["permissionDecision"] == "deny"
        assert str(f) in out["hookSpecificOutput"]["permissionDecisionReason"]

    def test_reread_after_edit_allows(self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture,
                                       tmp_path: Path) -> None:
        """A re-read after the file changed is allowed, not denied."""
        f = tmp_path / "a.py"
        f.write_text("print('hi')\n")

        monkeypatch.setattr("sys.stdin", io.StringIO(_payload("sess-1", str(f))))
        with pytest.raises(SystemExit):
            main()

        f.write_text("print('bye')\n")
        monkeypatch.setattr("sys.stdin", io.StringIO(_payload("sess-1", str(f))))
        with pytest.raises(SystemExit):
            main()
        assert capsys.readouterr().out == ""

    def test_different_window_allows(self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture,
                                      tmp_path: Path) -> None:
        """A read of a different offset/limit window is allowed, not denied."""
        f = tmp_path / "a.py"
        f.write_text("line1\nline2\nline3\nline4\n")

        monkeypatch.setattr("sys.stdin", io.StringIO(_payload("sess-1", str(f), offset=1, limit=2)))
        with pytest.raises(SystemExit):
            main()

        monkeypatch.setattr("sys.stdin", io.StringIO(_payload("sess-1", str(f), offset=3, limit=2)))
        with pytest.raises(SystemExit):
            main()
        assert capsys.readouterr().out == ""

    def test_cross_session_isolation(self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture,
                                      tmp_path: Path) -> None:
        """A read already seen in one session does not affect a different session."""
        f = tmp_path / "a.py"
        f.write_text("print('hi')\n")

        monkeypatch.setattr("sys.stdin", io.StringIO(_payload("sess-1", str(f))))
        with pytest.raises(SystemExit):
            main()

        monkeypatch.setattr("sys.stdin", io.StringIO(_payload("sess-2", str(f))))
        with pytest.raises(SystemExit):
            main()
        assert capsys.readouterr().out == ""

    def test_non_read_tool_allows_without_recording(self, monkeypatch: pytest.MonkeyPatch,
                                                      capsys: pytest.CaptureFixture, tmp_path: Path) -> None:
        """A non-Read tool call is ignored, as a defense-in-depth check on tool_name."""
        payload = json.dumps({"session_id": "sess-1", "tool_name": "Grep", "tool_input": {"file_path": "x"}})
        monkeypatch.setattr("sys.stdin", io.StringIO(payload))
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0
        assert capsys.readouterr().out == ""

    def test_missing_file_path_allows(self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
        """A payload with no file_path fails open."""
        payload = json.dumps({"session_id": "sess-1", "tool_name": "Read", "tool_input": {}})
        monkeypatch.setattr("sys.stdin", io.StringIO(payload))
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0
        assert capsys.readouterr().out == ""

    def test_missing_session_id_allows(self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture,
                                        tmp_path: Path) -> None:
        """A payload with no session_id fails open."""
        f = tmp_path / "a.py"
        f.write_text("hi\n")
        payload = json.dumps({"tool_name": "Read", "tool_input": {"file_path": str(f)}})
        monkeypatch.setattr("sys.stdin", io.StringIO(payload))
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0
        assert capsys.readouterr().out == ""

    def test_bad_json_allows(self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
        """Malformed stdin JSON fails open."""
        monkeypatch.setattr("sys.stdin", io.StringIO("not json"))
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0
        assert capsys.readouterr().out == ""

    def test_nonexistent_file_allows(self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture,
                                      tmp_path: Path) -> None:
        """A file_path that does not exist on disk fails open."""
        monkeypatch.setattr("sys.stdin", io.StringIO(_payload("sess-1", str(tmp_path / "missing.py"))))
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0
        assert capsys.readouterr().out == ""

    def test_unexpected_exception_allows(self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture,
                                          tmp_path: Path) -> None:
        """Any unexpected exception during processing fails open rather than crashing."""
        import claude_redundant_read_guard

        f = tmp_path / "a.py"
        f.write_text("hi\n")
        monkeypatch.setattr(claude_redundant_read_guard, "_fingerprint_file",
                             lambda *a, **k: (_ for _ in ()).throw(RuntimeError("boom")))
        monkeypatch.setattr("sys.stdin", io.StringIO(_payload("sess-1", str(f))))
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 0
        assert capsys.readouterr().out == ""


@pytest.fixture(autouse=True)
def _no_real_state_file(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Ensure no test can accidentally write to the real state file."""
    import claude_redundant_read_guard

    monkeypatch.setattr(claude_redundant_read_guard, "_STATE_PATH", tmp_path / ".redundant_read_state.json")
