#!/bin/bash
# hook_style_guide_response_standards.sh
#
# Enforce Response Standards hook: validates response format compliance
# Checks for Summary structure, offer line, response timing footer
# Flags deviations but does not block execution
#
# Lifecycle event: PostResponse

set -euo pipefail

# Input: response content from stdin or environment
RESPONSE="${RESPONSE:-$(cat)}"

# Color codes for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ============================================================================
# Helper: Check if response is substantive (not waived)
# ============================================================================
is_substantive() {
    local response="$1"

    # Waive short answers (<50 words)
    local word_count=$(echo "$response" | wc -w)
    if [[ $word_count -lt 50 ]]; then
        return 1  # Not substantive
    fi

    # Waive skill output (contains skill markers)
    if [[ "$response" =~ "⎿" ]] || [[ "$response" =~ "⎪" ]]; then
        return 1
    fi

    # Waive code blocks (contains triple backticks at start)
    if [[ "$response" =~ ^'```' ]]; then
        return 1
    fi

    # Waive error messages (starts with "Error:" or "❌")
    if [[ "$response" =~ ^"Error:" ]] || [[ "$response" =~ ^"❌" ]]; then
        return 1
    fi

    # Waive plan mode (contains plan file link)
    if [[ "$response" =~ "Planning: " ]]; then
        return 1
    fi

    return 0  # Is substantive
}

# ============================================================================
# Helper: Check for Summary structure
# ============================================================================
has_summary() {
    local response="$1"
    if [[ "$response" =~ \*\*Summary\*\* ]]; then
        return 0  # Has Summary
    fi
    return 1  # Missing Summary
}

# ============================================================================
# Helper: Check for offer line
# ============================================================================
has_offer_line() {
    local response="$1"
    # Check for offer line on its own line (not part of other text)
    if [[ "$response" =~ $'\n''More detail\?'$'\n' ]] || \
       [[ "$response" =~ $'^More detail\?' ]] || \
       [[ "$response" =~ $'\n''More detail\?'$ ]]; then
        return 0  # Has offer line
    fi
    return 1  # Missing offer line
}

# ============================================================================
# Helper: Check for response timing footer
# ============================================================================
has_timing_footer() {
    local response="$1"
    if [[ "$response" =~ Response\ time.*[0-9]+s ]]; then
        return 0  # Has timing footer
    fi
    return 1  # Missing timing footer
}

# ============================================================================
# Helper: Check if content comes after timing footer (should not)
# ============================================================================
has_content_after_timing() {
    local response="$1"
    # Extract everything after timing footer
    local after_timing=$(echo "$response" | sed -n '/Response time.*[0-9]*s/,$p' | tail -n +2)
    if [[ -n "$after_timing" ]] && [[ ! "$after_timing" =~ ^[[:space:]]*$ ]]; then
        return 0  # Has content after timing (violation)
    fi
    return 1  # Clean (no content after timing)
}

# ============================================================================
# Main validation
# ============================================================================

FLAGS=()

if is_substantive "$RESPONSE"; then
    # Response is substantive; apply full validation

    if ! has_summary "$RESPONSE"; then
        FLAGS+=("❌ Missing **Summary** block. Expected: **Summary** + 3–4 bullets with bold keywords")
    fi

    if ! has_offer_line "$RESPONSE"; then
        FLAGS+=("❌ Missing offer line. Expected: 'More detail? (Y/N)' or similar on its own line")
    fi

    if ! has_timing_footer "$RESPONSE"; then
        FLAGS+=("❌ Missing response timing footer. Expected: 'Response time (post-reasoning): Xs' as final line")
    fi

    if has_content_after_timing "$RESPONSE"; then
        FLAGS+=("❌ Content found after timing footer. Timing footer must be the final line.")
    fi
fi

# ============================================================================
# Report flags (if any)
# ============================================================================

if [[ ${#FLAGS[@]} -gt 0 ]]; then
    echo ""
    echo -e "${YELLOW}🚩 Response Standards Check${NC}"
    for flag in "${FLAGS[@]}"; do
        echo -e "${RED}${flag}${NC}"
    done
    echo ""
fi

exit 0
