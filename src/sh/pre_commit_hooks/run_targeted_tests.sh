#!/bin/bash
set -e
#================================================================
## HEADER
#================================================================
## Overview:    Targeted pytest runner for Claude config validation.
##
## Description: Inspects staged files and runs only the pytest
##              test modules that cover the affected areas of
##              src/claude/. Exits cleanly if no testable files
##              are staged.
##
## Usage: Invoked automatically by pre-commit. Not intended to
##        be run directly.
##
#================================================================

#=======================================================================
# Variables
#=======================================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
COLOUR_OFF='\033[0m'

TESTS_TO_RUN=()

#=======================================================================
# Functions
#=======================================================================

add_test() {
    local test_file="$1"
    # Only add if not already in the list
    for existing in "${TESTS_TO_RUN[@]+"${TESTS_TO_RUN[@]}"}"; do
        [[ "$existing" == "$test_file" ]] && return
    done
    TESTS_TO_RUN+=("$test_file")
}

#=======================================================================
# Main script logic
#=======================================================================

# Get staged files
STAGED_FILES=$(git diff --cached --name-only)

if [[ -z "$STAGED_FILES" ]]; then
    exit 0
fi

# Map staged paths to test modules
while IFS= read -r file; do
    case "$file" in
        src/claude/agents/*)
            add_test "tests/test_agents.py" ;;
        src/claude/skills/*)
            add_test "tests/test_skills.py" ;;
        src/claude/process/*)
            add_test "tests/test_process.py" ;;
        src/claude/commands/*)
            add_test "tests/test_commands.py" ;;
        src/claude/rules/*)
            add_test "tests/test_rules.py" ;;
        src/claude/style_guide_standards/*)
            add_test "tests/test_style_guide_standards.py" ;;
        tests/* | requirements.txt | pytest.ini)
            add_test "tests/" ;;
    esac
done <<< "$STAGED_FILES"

if [[ ${#TESTS_TO_RUN[@]} -eq 0 ]]; then
    exit 0
fi

echo -e "\nRunning targeted tests for staged files: ${TESTS_TO_RUN[*]}\n"

if pytest "${TESTS_TO_RUN[@]}"; then
    echo -e "\n${GREEN}Claude config validation passed.${COLOUR_OFF}\n"
else
    echo -e "\n${RED}Claude config validation failed. Fix the issues above before committing.${COLOUR_OFF}\n"
    exit 1
fi
