#!/bin/bash
# version: 2.0.0
# created: 2026-08-31
# updated: 2026-10-01
# UserPromptSubmit hook — warns once when the MCP servers in settings.json change mid-session.
# Claude Code reads deniedMcpServers at startup only, so a toggle made during a session
# (e.g. `make enable_mcp`) doesn't apply until restart. Silent unless the list has changed.
#
# How it works:
# 1. On a session's first prompt, snapshot the sorted deniedMcpServers list.
# 2. On later prompts, compare the current list with the snapshot.
# 3. If it differs, warn once for that list; reverting to the snapshot goes quiet again.
# State lives in $TMPDIR, keyed by session_id, never in the config dir.
set -eu

CLAUDE_HOOKS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_ROOT_DIR="$(dirname "${CLAUDE_HOOKS_DIR}")"
SETTINGS_FILE="${CLAUDE_ROOT_DIR}/settings.json"
STATE_DIR="${TMPDIR:-/tmp}/claude_mcp_stale_settings"

#=======================================================================
# Variables
#=======================================================================

# Read full hook payload from stdin — provided by Claude Code on every prompt.
INPUT=$(cat)

#=======================================================================
# Main script logic
#=======================================================================

# Fail open: without a session id or a readable settings file there is nothing to compare.
SESSION_ID=$(echo "${INPUT}" | jq -r '.session_id // empty' 2>/dev/null || true)
[[ -z "${SESSION_ID}" || ! "${SESSION_ID}" =~ ^[A-Za-z0-9_-]+$ ]] && exit 0
[[ -f "${SETTINGS_FILE}" ]] || exit 0
CURRENT=$(jq -c '[.deniedMcpServers // [] | .[].serverName] | sort' "${SETTINGS_FILE}" 2>/dev/null) || exit 0

mkdir -p "${STATE_DIR}"
SNAPSHOT_FILE="${STATE_DIR}/${SESSION_ID}.snapshot"
WARNED_FILE="${STATE_DIR}/${SESSION_ID}.warned"

# First prompt of the session: record what the session started with.
if [[ ! -f "${SNAPSHOT_FILE}" ]]; then
    echo "${CURRENT}" > "${SNAPSHOT_FILE}"
    exit 0
fi

SNAPSHOT=$(cat "${SNAPSHOT_FILE}")
[[ "${CURRENT}" == "${SNAPSHOT}" ]] && exit 0
[[ -f "${WARNED_FILE}" && "$(cat "${WARNED_FILE}")" == "${CURRENT}" ]] && exit 0
echo "${CURRENT}" > "${WARNED_FILE}"

MESSAGE="⚠️ MCP servers changed since this session started (disabled at start: ${SNAPSHOT}; disabled now: ${CURRENT}). The change won't take effect until you restart Claude Code."
jq -n --arg message "${MESSAGE}" \
  '{"systemMessage": $message, "hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": $message}}'
