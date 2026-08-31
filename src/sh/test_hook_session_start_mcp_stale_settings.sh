#!/bin/bash
# Tests for hook_session_start_mcp_stale_settings.sh
#
# Tests: Hook detects stale settings, outputs reminder, doesn't spam sessions
# Run from repo root: bash src/sh/test_hook_session_start_mcp_stale_settings.sh

set -eu

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

TESTS_PASSED=0
TESTS_FAILED=0

test_hook_detects_recent_modification() {
    echo ""
    echo -e "${YELLOW}[TEST]${NC} Hook detects settings modified recently"

    # Create test HOME
    local TEST_HOME="/tmp/hook_test_$$"
    mkdir -p "$TEST_HOME/.claude"

    # Create settings.json and modify it now (< 5 minutes ago)
    echo '{"deniedMcpServers": []}' > "$TEST_HOME/.claude/settings.json"
    touch "$TEST_HOME/.claude/settings.json"

    # Run hook
    export HOME="$TEST_HOME"
    output=$(bash src/claude/hooks/hook_session_start_mcp_stale_settings.sh 2>&1 || true)

    # Check output
    if echo "$output" | grep -q "MCP settings were changed recently"; then
        echo -e "${GREEN}✓ PASS${NC}: Hook detected recent modification"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}: Hook did not detect recent modification"
        echo "Output was: $output"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    # Cleanup
    rm -rf "$TEST_HOME"
}

test_hook_ignores_old_modification() {
    echo ""
    echo -e "${YELLOW}[TEST]${NC} Hook ignores settings modified long ago"

    # Create test HOME
    local TEST_HOME="/tmp/hook_test_$$"
    mkdir -p "$TEST_HOME/.claude"

    # Create settings.json and backdate it (> 5 minutes ago)
    echo '{"deniedMcpServers": []}' > "$TEST_HOME/.claude/settings.json"
    touch -t 202301010000 "$TEST_HOME/.claude/settings.json"  # January 2023

    # Run hook
    export HOME="$TEST_HOME"
    output=$(bash src/claude/hooks/hook_session_start_mcp_stale_settings.sh 2>&1 || true)

    # Check no warning (output should be empty or minimal)
    if [[ -z "$output" ]] || ! echo "$output" | grep -q "MCP settings were changed"; then
        echo -e "${GREEN}✓ PASS${NC}: Hook ignored old modification"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}: Hook warned about old modification"
        echo "Output was: $output"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    # Cleanup
    rm -rf "$TEST_HOME"
}

test_hook_no_warning_if_no_settings() {
    echo ""
    echo -e "${YELLOW}[TEST]${NC} Hook doesn't warn if settings.json doesn't exist"

    # Create test HOME without settings
    local TEST_HOME="/tmp/hook_test_$$"
    mkdir -p "$TEST_HOME/.claude"

    # Run hook (no settings.json)
    export HOME="$TEST_HOME"
    output=$(bash src/claude/hooks/hook_session_start_mcp_stale_settings.sh 2>&1 || true)

    # Check no error or warning
    if [[ -z "$output" ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Hook exited cleanly without settings.json"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}: Hook output when settings.json missing"
        echo "Output was: $output"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    # Cleanup
    rm -rf "$TEST_HOME"
}

test_hook_no_spam() {
    echo ""
    echo -e "${YELLOW}[TEST]${NC} Hook creates flag file to prevent repeat warnings"

    # Create test HOME
    local TEST_HOME="/tmp/hook_test_$$"
    mkdir -p "$TEST_HOME/.claude"

    # Create recent settings.json
    echo '{"deniedMcpServers": []}' > "$TEST_HOME/.claude/settings.json"
    touch "$TEST_HOME/.claude/settings.json"

    # Run hook once
    export HOME="$TEST_HOME"
    bash src/claude/hooks/hook_session_start_mcp_stale_settings.sh > /dev/null 2>&1 || true

    # Check if flag file was created
    FLAG_FILE="$TEST_HOME/.claude/.stale_settings_warning_shown"
    if [[ -f "$FLAG_FILE" ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Hook created flag file to prevent spam"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}: Hook did not create flag file"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    # Cleanup
    rm -rf "$TEST_HOME"
}

test_hook_exit_code_success() {
    echo ""
    echo -e "${YELLOW}[TEST]${NC} Hook always exits with code 0"

    # Create test HOME
    local TEST_HOME="/tmp/hook_test_$$"
    mkdir -p "$TEST_HOME/.claude"
    echo '{"deniedMcpServers": []}' > "$TEST_HOME/.claude/settings.json"

    # Run hook
    export HOME="$TEST_HOME"
    if bash src/claude/hooks/hook_session_start_mcp_stale_settings.sh > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}: Hook exited with code 0"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        exit_code=$?
        echo -e "${RED}✗ FAIL${NC}: Hook exited with code $exit_code (expected 0)"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    # Cleanup
    rm -rf "$TEST_HOME"
}

main() {
    echo "================================"
    echo "Hook: session_start_mcp_stale_settings Tests"
    echo "================================"

    test_hook_detects_recent_modification
    test_hook_ignores_old_modification
    test_hook_no_warning_if_no_settings
    test_hook_no_spam
    test_hook_exit_code_success

    # Summary
    echo ""
    echo "================================"
    echo -e "Results: ${GREEN}$TESTS_PASSED passed${NC}, ${RED}$TESTS_FAILED failed${NC}"
    echo "================================"

    if [[ $TESTS_FAILED -gt 0 ]]; then
        exit 1
    fi
    exit 0
}

main "$@"
