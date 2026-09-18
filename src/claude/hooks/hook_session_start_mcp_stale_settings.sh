#!/bin/bash
# Hook: Detect stale MCP settings after toggle changes.
#
# Purpose: Remind user if ~/.claude/settings.json was modified in a recent
# session but the current session hasn't restarted yet. Helps catch cases
# where the mcp_toggle.py exit code signal was missed.
#
# Lifecycle: onSessionStart
#
# How it works:
# 1. On session start, check if ~/.claude/settings.json exists
# 2. Compare file mtime against session start time
# 3. If modified < 5 minutes ago, show a gentle reminder
# 4. Only show once per session to avoid spam

set -eu

SETTINGS_FILE="${HOME}/.claude/settings.json"
STALE_FLAG_FILE="${HOME}/.claude/.stale_settings_warning_shown"

# Settings file must exist
if [[ ! -f "$SETTINGS_FILE" ]]; then
    exit 0
fi

# Check if we've already shown the warning in this session
if [[ -f "$STALE_FLAG_FILE" ]]; then
    exit 0
fi

# Get file modification time and current time
SETTINGS_MTIME=$(stat -c %Y "$SETTINGS_FILE" 2>/dev/null || stat -f %m "$SETTINGS_FILE" 2>/dev/null || echo 0)
CURRENT_TIME=$(date +%s)
TIME_DIFF=$((CURRENT_TIME - SETTINGS_MTIME))

# If settings were modified less than 5 minutes (300 seconds) ago, show reminder
if [[ $TIME_DIFF -lt 300 ]]; then
    cat <<'EOF'

⚠️  Note: MCP settings were changed recently.
    If you see MCP tool calls hanging (2–6 minutes), restart Claude Code.

EOF
    # Mark that we've shown the warning so we don't spam this session
    # The flag file will persist for the session (Claude Code clears ~/.claude on exit)
    touch "$STALE_FLAG_FILE"
fi

exit 0
