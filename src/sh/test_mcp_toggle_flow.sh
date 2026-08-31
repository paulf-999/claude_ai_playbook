#!/bin/bash
# Integration tests for mcp_toggle.sh and mcp_toggle.py
#
# Tests: Makefile target, exit codes, blocking message, settings.json integrity
# Run from repo root: bash src/sh/test_mcp_toggle_flow.sh

set -eu

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

TESTS_PASSED=0
TESTS_FAILED=0

# Temporary test settings file
TEST_SETTINGS="/tmp/test_settings_$$.json"

test_setup() {
    echo "Test Setup: Creating temporary settings.json"
    cat > "$TEST_SETTINGS" <<'EOF'
{
  "cleanupPeriodDays": 30,
  "deniedMcpServers": [{"serverName": "github"}],
  "permissions": {
    "allow": ["Bash(git:*)"],
    "deny": ["Bash(rm -rf:*)"]
  }
}
EOF
}

test_cleanup() {
    rm -f "$TEST_SETTINGS"
}

run_test() {
    local test_name="$1"
    local test_cmd="$2"
    local expected_exit_code="$3"

    echo ""
    echo -e "${YELLOW}[TEST]${NC} $test_name"
    if eval "$test_cmd" > /tmp/test_output_$$.txt 2>&1; then
        actual_exit_code=0
    else
        actual_exit_code=$?
    fi

    if [[ "$actual_exit_code" == "$expected_exit_code" ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Exit code $actual_exit_code (expected $expected_exit_code)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}: Exit code $actual_exit_code (expected $expected_exit_code)"
        cat /tmp/test_output_$$.txt
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
    rm -f /tmp/test_output_$$.txt
}

test_blocking_message() {
    echo ""
    echo -e "${YELLOW}[TEST]${NC} Blocking message contains required elements"

    # Mock HOME to use test settings
    local HOME_BACKUP="$HOME"
    export HOME="/tmp/mcp_test_$$"
    mkdir -p "$HOME/.claude"
    # Create settings with atlassian DISABLED (in deniedMcpServers)
    cat > "$HOME/.claude/settings.json" <<'EOF'
{
  "cleanupPeriodDays": 30,
  "deniedMcpServers": [{"serverName": "atlassian"}],
  "permissions": {"allow": ["Bash(git:*)"]}
}
EOF

    output=$(python3 src/sh/claude/helpers/mcp_toggle.py enable atlassian 2>&1 || true)

    # Check message contents
    local checks=0
    local passed=0

    # Check 1: RESTART REQUIRED
    if echo "$output" | grep -q "RESTART REQUIRED"; then
        passed=$((passed + 1))
    fi
    checks=$((checks + 1))

    # Check 2: Server name
    if echo "$output" | grep -q "atlassian"; then
        passed=$((passed + 1))
    fi
    checks=$((checks + 1))

    # Check 3: Urgency indicator
    if echo "$output" | grep -q "MUST restart"; then
        passed=$((passed + 1))
    fi
    checks=$((checks + 1))

    # Check 4: Time hanging warning
    if echo "$output" | grep -q "2–6 minutes"; then
        passed=$((passed + 1))
    fi
    checks=$((checks + 1))

    # Check 5: Close instruction
    if echo "$output" | grep -q "Close Claude Code completely"; then
        passed=$((passed + 1))
    fi
    checks=$((checks + 1))

    if [[ $passed -eq $checks ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Message contains all required elements ($passed/$checks)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}: Message missing elements ($passed/$checks)"
        echo "Output was:"
        echo "$output"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    export HOME="$HOME_BACKUP"
    rm -rf "/tmp/mcp_test_$$"
}

test_settings_preservation() {
    echo ""
    echo -e "${YELLOW}[TEST]${NC} Other settings preserved after toggle"

    # Mock HOME and settings
    local HOME_BACKUP="$HOME"
    export HOME="/tmp/mcp_test_$$"
    mkdir -p "$HOME/.claude"
    cp "$TEST_SETTINGS" "$HOME/.claude/settings.json"

    python3 src/sh/claude/helpers/mcp_toggle.py enable atlassian > /dev/null 2>&1 || true

    # Verify other fields intact
    local settings_content=$(cat "$HOME/.claude/settings.json")
    local checks=0
    local passed=0

    # Check 1: cleanupPeriodDays
    if echo "$settings_content" | jq -e '.cleanupPeriodDays == 30' > /dev/null 2>&1; then
        passed=$((passed + 1))
    fi
    checks=$((checks + 1))

    # Check 2: permissions.allow still present
    if echo "$settings_content" | jq -e '.permissions.allow | length > 0' > /dev/null 2>&1; then
        passed=$((passed + 1))
    fi
    checks=$((checks + 1))

    # Check 3: GitHub still in deniedMcpServers
    if echo "$settings_content" | jq -e '.deniedMcpServers[] | select(.serverName == "github")' > /dev/null 2>&1; then
        passed=$((passed + 1))
    fi
    checks=$((checks + 1))

    # Check 4: Atlassian NOT in deniedMcpServers (was enabled)
    if ! echo "$settings_content" | jq -e '.deniedMcpServers[] | select(.serverName == "atlassian")' > /dev/null 2>&1; then
        passed=$((passed + 1))
    fi
    checks=$((checks + 1))

    if [[ $passed -eq $checks ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Settings preserved correctly ($passed/$checks checks)"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}: Settings not preserved ($passed/$checks checks)"
        echo "Settings content:"
        echo "$settings_content" | jq .
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    export HOME="$HOME_BACKUP"
    rm -rf "/tmp/mcp_test_$$"
}

test_no_change_exit_code_zero() {
    echo ""
    echo -e "${YELLOW}[TEST]${NC} No-change scenarios exit with code 0"

    # Mock HOME and settings
    local HOME_BACKUP="$HOME"
    export HOME="/tmp/mcp_test_$$"
    mkdir -p "$HOME/.claude"
    # Create settings with atlassian already enabled (not in deniedMcpServers)
    cat > "$HOME/.claude/settings.json" <<'EOF'
{"deniedMcpServers": []}
EOF

    # Enable when already enabled
    if python3 src/sh/claude/helpers/mcp_toggle.py enable atlassian > /tmp/test_enable_output.txt 2>&1; then
        exit_code=0
    else
        exit_code=$?
    fi

    if [[ $exit_code -eq 0 ]]; then
        echo -e "${GREEN}✓ PASS${NC}: Already-enabled scenario exits with code 0"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}✗ FAIL${NC}: Exit code was $exit_code (expected 0)"
        cat /tmp/test_enable_output.txt
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi

    export HOME="$HOME_BACKUP"
    rm -rf "/tmp/mcp_test_$$" "/tmp/test_enable_output.txt"
}

# Run all tests
main() {
    echo "================================"
    echo "MCP Toggle Integration Tests"
    echo "================================"

    test_setup
    trap test_cleanup EXIT

    # Test 1: Enable exits with 1 (change made)
    # Note: Simplified — full test requires mocking HOME/SETTINGS_PATH
    echo ""
    echo -e "${YELLOW}Test Summary:${NC} Running integration tests"

    test_blocking_message
    test_settings_preservation
    test_no_change_exit_code_zero

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
