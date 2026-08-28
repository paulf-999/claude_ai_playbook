#!/usr/bin/env python3
"""PreToolUse hook — redundant read guard.

Denies a Read call when the exact same content (by sha256 hash, scoped to the
requested offset/limit window) was already read earlier in the same session.
Claude already has that content in context in that case, so blocking the
re-read and telling Claude to reuse it costs zero information.

Input:  JSON on stdin — {"session_id": "...", "tool_name": "Read",
        "tool_input": {"file_path": "...", "offset": int|None, "limit": int|None}}
Output: JSON on stdout — {"hookSpecificOutput": {"hookEventName": "PreToolUse",
        "permissionDecision": "deny", "permissionDecisionReason": "..."}} to
        block the call, or nothing (exit 0) to allow it.

Grep, Bash, and other tools are deliberately out of scope for this hook —
result-equivalence for those depends on more than byte-identical output, and
a hard block risks disrupting a legitimate re-run (e.g. checking whether a
fix landed). Read is the one case where a byte-identical re-read is always
safe to block outright.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

_STATE_PATH = Path.home() / ".claude" / "wip" / "hooks" / ".redundant_read_state.json"
_MAX_FINGERPRINT_BYTES = 5 * 1024 * 1024  # skip fingerprinting above this size
_SESSION_TTL_SECONDS = 3 * 24 * 60 * 60  # prune sessions untouched for this long


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

def _read_hook_input() -> dict:
    """Parse JSON from stdin.

    :return: Parsed hook input dict, or empty dict on failure.
    :rtype: dict
    """
    try:
        return json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        return {}


def _format_window(offset: int | None, limit: int | None) -> str:
    """Build the read-window portion of a state file key.

    :param offset: The 1-indexed starting line requested, or None for a full read.
    :type offset: int | None
    :param limit: The number of lines requested, or None for no limit.
    :type limit: int | None
    :return: A string of the form "<offset>:<limit>", empty either side if unset.
    :rtype: str
    """
    return f"{offset if offset is not None else ''}:{limit if limit is not None else ''}"


# ---------------------------------------------------------------------------
# State
# ---------------------------------------------------------------------------

def _default_state() -> dict:
    """Build an empty state document.

    :return: A fresh state dict with no sessions recorded.
    :rtype: dict
    """
    return {"sessions": {}}


def _load_state(path: Path) -> dict:
    """Load session state from disk.

    :param path: Path to the state JSON file.
    :type path: Path
    :return: Parsed state dict, or a fresh default state if the file is
        missing or corrupt.
    :rtype: dict
    """
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError, ValueError):
        return _default_state()


def _save_state(path: Path, state: dict) -> None:
    """Persist session state to disk.

    :param path: Path to the state JSON file.
    :type path: Path
    :param state: State dict to write.
    :type state: dict
    """
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(state))
    except OSError:
        pass


def _prune_stale_sessions(state: dict, now: float, ttl_seconds: float = _SESSION_TTL_SECONDS) -> None:
    """Drop sessions that have not been touched within the TTL window.

    Keeps the state file bounded without a separate cleanup job — there is no
    natural calendar rollover for this hook, unlike month-to-date state.

    :param state: State dict to prune in place.
    :type state: dict
    :param now: The current time, as a Unix timestamp.
    :type now: float
    :param ttl_seconds: Sessions untouched for longer than this are dropped.
    :type ttl_seconds: float
    """
    sessions = state.get("sessions", {})
    stale = [sid for sid, data in sessions.items() if now - data.get("last_touched", 0) > ttl_seconds]
    for sid in stale:
        del sessions[sid]


# ---------------------------------------------------------------------------
# Fingerprinting
# ---------------------------------------------------------------------------

def _read_window_bytes(file_path: str, offset: int | None, limit: int | None) -> bytes:
    """Read only the requested line window from a file, as bytes.

    :param file_path: Absolute path to the file being read.
    :type file_path: str
    :param offset: The 1-indexed starting line, or None to start at line 1.
    :type offset: int | None
    :param limit: The number of lines to read, or None to read to EOF.
    :type limit: int | None
    :return: The raw bytes of the requested line window.
    :rtype: bytes
    """
    start_index = max(offset - 1, 0) if offset else 0
    end_index = start_index + limit if limit is not None else None
    chunks: list[bytes] = []
    with open(file_path, "rb") as fh:
        for index, line in enumerate(fh):
            if index < start_index:
                continue
            if end_index is not None and index >= end_index:
                break
            chunks.append(line)
    return b"".join(chunks)


def _fingerprint_file(
    file_path: str,
    offset: int | None,
    limit: int | None,
    max_bytes: int = _MAX_FINGERPRINT_BYTES,
) -> str | None:
    """Compute a content hash for a file, or the requested window within it.

    Uses sha256 content hashing rather than mtime+size — mtime is not a sound
    signal for this check (touch, in-place rewrites, and WSL2/network-FS mtime
    granularity quirks can all produce a false "unchanged" verdict).

    :param file_path: Absolute path to the file being read.
    :type file_path: str
    :param offset: The 1-indexed starting line requested, or None for a full read.
    :type offset: int | None
    :param limit: The number of lines requested, or None for no limit.
    :type limit: int | None
    :param max_bytes: Skip fingerprinting for files larger than this, on disk.
    :type max_bytes: int
    :return: Hex-encoded sha256 digest, or None if fingerprinting was skipped
        or the file could not be read.
    :rtype: str | None
    """
    try:
        size = os.path.getsize(file_path)
    except OSError:
        return None
    if size > max_bytes:
        return None

    try:
        if offset is None and limit is None:
            with open(file_path, "rb") as fh:
                data = fh.read()
        else:
            data = _read_window_bytes(file_path, offset, limit)
    except OSError:
        return None

    return hashlib.sha256(data).hexdigest()


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def _emit_deny(file_path: str) -> None:
    """Write the PreToolUse deny envelope to stdout.

    :param file_path: The file path being denied, named in the reason text.
    :type file_path: str
    """
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": (
                f"Redundant read blocked: {file_path} is unchanged since it was already read "
                "earlier in this session. Reuse the content already in your context instead of "
                "re-reading it."
            ),
        }
    }
    print(json.dumps(output))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def _process() -> None:
    """Check the incoming Read call against session state and act on it.

    Denies via stdout if the exact content was already read this session;
    otherwise records the new fingerprint and returns, allowing the call.
    """
    hook_data = _read_hook_input()
    if hook_data.get("tool_name") != "Read":
        return

    tool_input = hook_data.get("tool_input") or {}
    file_path = tool_input.get("file_path")
    session_id = hook_data.get("session_id")
    if not file_path or not session_id:
        return

    offset = tool_input.get("offset")
    limit = tool_input.get("limit")
    new_hash = _fingerprint_file(file_path, offset, limit)
    if new_hash is None:
        return

    now = time.time()
    state = _load_state(_STATE_PATH)
    _prune_stale_sessions(state, now)

    session = state["sessions"].setdefault(session_id, {"last_touched": now, "files": {}})
    session["last_touched"] = now

    read_key = f"{file_path}|{_format_window(offset, limit)}"
    prior_hash = session["files"].get(read_key)

    if prior_hash == new_hash:
        _emit_deny(file_path)
    else:
        session["files"][read_key] = new_hash

    _save_state(_STATE_PATH, state)


def main() -> None:
    """Run the redundant-read check, failing open on any unexpected error.

    A bug in this hook must never accidentally block all reads, so the whole
    check is wrapped in one outer catch-all — any exception falls through to
    allow.
    """
    try:
        _process()
    except Exception:
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()
