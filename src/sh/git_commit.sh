#!/bin/bash
# Interactive commit helper that enforces Conventional Commits v1.0.0
# Format: <type>[(<scope>)][!]: <description>
#
# Usage: git_commit.sh [--no-verify]
# See: https://www.conventionalcommits.org/en/v1.0.0/

set -uo pipefail

# Try to source shell utils; fallback if unavailable
if ! source src/sh/shell_utils.sh 2>/dev/null; then
    DEBUG=""
    DEBUG_DETAILS=""
    COLOUR_OFF=""
    ERROR=""
    log_message() { printf '%b\n' "$2"; }
fi

# Ensure we're inside a git repo
if ! git rev-parse --git-dir >/dev/null 2>&1; then
    log_message "${ERROR}" "Not a git repository."
    exit 1
fi

# -----------------------------
# Configuration
# -----------------------------
COMMON_TYPES=("feat" "fix" "docs" "refactor" "test" "chore")
ADVANCED_TYPES=("build" "ci" "perf" "revert" "style")

# -----------------------------
# Globals
# -----------------------------
STAGED=()
DISPLAY_NAMES=()
TYPE=""
SCOPE=""
BREAKING=false
DESC=""
COMMIT_MSG=""
GIT_FLAGS=()

# -----------------------------
# Helpers
# -----------------------------
to_lower() {
    printf '%s' "$1" | tr '[:upper:]' '[:lower:]'
}

truncate_scope() {
    local name="$1"
    local max_len=30

    local base ext
    if [[ "$name" == *.* && "${name##*.}" != "$name" ]]; then
        base="${name%.*}"
        ext=".${name##*.}"
    else
        base="$name"
        ext=""
    fi

    if ((${#base} > max_len)); then
        printf '%s\n' "${base:0:$max_len}…${ext}"
    else
        printf '%s\n' "${base}${ext}"
    fi
}

build_types_alt() {
    local all_types=("${COMMON_TYPES[@]}" "${ADVANCED_TYPES[@]}")
    local IFS='|'
    echo "${all_types[*]}"
}

is_valid_type() {
    local input="$1"
    local t
    for t in "${COMMON_TYPES[@]}" "${ADVANCED_TYPES[@]}"; do
        [[ "$t" == "$input" ]] && return 0
    done
    return 1
}

is_advanced_type() {
    local input="$1"
    local t
    for t in "${ADVANCED_TYPES[@]}"; do
        [[ "$t" == "$input" ]] && return 0
    done
    return 1
}

# -----------------------------
# Argument parsing
# -----------------------------
parse_args() {
    for arg in "$@"; do
        GIT_FLAGS+=("$arg")
    done
}

# -----------------------------
# Step 1 — commit type
# -----------------------------
select_advanced_type() {
    while true; do
        log_message "${DEBUG}" "More commit types:\n"

        for i in "${!ADVANCED_TYPES[@]}"; do
            local idx=$((i+1))
            echo -e "${DEBUG_DETAILS}${idx}) ${ADVANCED_TYPES[$i]}${COLOUR_OFF}"
        done
        echo -e "${DEBUG_DETAILS}$(( ${#ADVANCED_TYPES[@]} + 1 ))) back${COLOUR_OFF}"
        echo

        # Accept numbers only — prevents common types being entered here,
        # which would be inconsistent with the menu framing.
        read -rp "$(printf '%b' "${DEBUG}Enter number: ${COLOUR_OFF}")" choice

        if [[ "$choice" =~ ^[0-9]+$ ]]; then
            if (( choice >= 1 && choice <= ${#ADVANCED_TYPES[@]} )); then
                TYPE="${ADVANCED_TYPES[$((choice-1))]}"
                return
            elif (( choice == ${#ADVANCED_TYPES[@]} + 1 )); then
                return
            else
                log_message "${ERROR}" "Invalid selection."
            fi
        else
            log_message "${ERROR}" "Invalid selection."
        fi
    done
}

select_type() {
    while true; do
        log_message "${DEBUG}" "Select type of Git commit:\n"

        for i in "${!COMMON_TYPES[@]}"; do
            local idx=$((i+1))
            echo -e "${DEBUG_DETAILS}${idx}) ${COMMON_TYPES[$i]}${COLOUR_OFF}"
        done
        echo -e "${DEBUG_DETAILS}$(( ${#COMMON_TYPES[@]} + 1 ))) More types...${COLOUR_OFF}"
        echo

        read -rp "$(printf '%b' "${DEBUG}Enter number or type (e.g. feat, fix, ci): ${COLOUR_OFF}")" choice
        choice="$(to_lower "$choice")"

        if is_valid_type "$choice"; then
            TYPE="$choice"
            break
        elif [[ "$choice" =~ ^[0-9]+$ ]]; then
            if (( choice >= 1 && choice <= ${#COMMON_TYPES[@]} )); then
                TYPE="${COMMON_TYPES[$((choice-1))]}"
                break
            elif (( choice == ${#COMMON_TYPES[@]} + 1 )); then
                select_advanced_type
                [[ -n "$TYPE" ]] && break
            else
                log_message "${ERROR}" "Invalid selection."
            fi
        else
            log_message "${ERROR}" "Invalid selection."
        fi
    done
}

# -----------------------------
# Step 2 — staged files
# -----------------------------
gather_staged_files() {
    STAGED=()
    while IFS= read -r line; do
        [[ -n "$line" ]] && STAGED+=("$line")
    done < <(git diff --cached --name-only 2>/dev/null || printf '')
}

build_menu_display_names() {
    DISPLAY_NAMES=()

    for i in "${!STAGED[@]}"; do
        local filename
        filename="$(basename -- "${STAGED[$i]}")"
        DISPLAY_NAMES[$i]="$(truncate_scope "$filename")"
    done

    # Handle duplicate filenames
    for i in "${!DISPLAY_NAMES[@]}"; do
        local dup_count=0
        for j in "${!DISPLAY_NAMES[@]}"; do
            [[ "${DISPLAY_NAMES[$j]}" == "${DISPLAY_NAMES[$i]}" ]] && ((dup_count++))
        done

        if (( dup_count > 1 )); then
            local parent
            parent="$(basename -- "$(dirname -- "${STAGED[$i]}")")"
            DISPLAY_NAMES[$i]+=" [${parent}]"
        fi
    done
}

# -----------------------------
# Step 3 — scope (optional)
# -----------------------------
select_scope() {
    log_message "${DEBUG}" "Pick the scope (optional — press Enter to skip):\n"

    if ((${#STAGED[@]} > 0)); then
        build_menu_display_names
        for i in "${!STAGED[@]}"; do
            local idx=$((i+1))
            echo -e "${DEBUG_DETAILS}" "${idx}) ${DISPLAY_NAMES[$i]}"
        done
        echo -e "${DEBUG_DETAILS}" "0) Enter custom scope"
        echo -e "${DEBUG_DETAILS}" "s) Skip scope"
    else
        log_message "${DEBUG_DETAILS}" "(no staged files detected)"
    fi

    while true; do
        read -rp "$(printf '%b' "\n${DEBUG}Choose number, 0 to type, or s to skip: ${COLOUR_OFF}")" scope_choice

        if [[ "$scope_choice" =~ ^[Ss]$ ]] || [[ -z "$scope_choice" ]]; then
            SCOPE=""
            break
        elif ((${#STAGED[@]} > 0)) && [[ "$scope_choice" =~ ^[0-9]+$ ]] &&
             (( scope_choice >= 1 && scope_choice <= ${#STAGED[@]} )); then
            SCOPE="$(truncate_scope "$(basename -- "${STAGED[$((scope_choice-1))]}")")"
            break
        elif [[ "$scope_choice" == "0" || ${#STAGED[@]} -eq 0 ]]; then
            # Re-prompt if custom scope left empty — avoids invalid `type(): desc` subject.
            read -rp "$(printf '%b' "${DEBUG}Enter custom scope: ${COLOUR_OFF}")" SCOPE
            SCOPE="${SCOPE// /-}"
            if [[ -n "$SCOPE" ]]; then
                break
            else
                log_message "${ERROR}" "Scope cannot be empty. Choose a number, 0 to retype, or s to skip."
            fi
        else
            log_message "${ERROR}" "Invalid selection."
        fi
    done
}

# -----------------------------
# Step 4 — breaking change
# -----------------------------
prompt_breaking_change() {
    read -rp "$(printf '%b' "\n${DEBUG}Is this a BREAKING CHANGE? [y/N]: ${COLOUR_OFF}")" bc_choice
    [[ "$bc_choice" =~ ^[Yy]$ ]] && BREAKING=true || BREAKING=false
}

# -----------------------------
# Step 5 — description
# -----------------------------
prompt_description() {
    while true; do
        read -rp "$(printf '%b' "${DEBUG}Enter short description: ${COLOUR_OFF}")" DESC
        [[ -n "$DESC" ]] && break
        log_message "${ERROR}" "Description cannot be empty."
    done
}

# -----------------------------
# Build + commit
# -----------------------------
build_commit_message() {
    local subject="${TYPE}"
    [[ -n "$SCOPE" ]] && subject+="(${SCOPE})"
    $BREAKING && subject+="!"
    subject+=": ${DESC}"
    COMMIT_MSG="$subject"
}

validate_commit_message() {
    local types_alt subject_line
    types_alt="$(build_types_alt)"
    subject_line="${COMMIT_MSG%%$'\n'*}"

    local regex="^(${types_alt})(\([^)]+\))?(!)?: .+"
    if ! [[ "$subject_line" =~ $regex ]]; then
        log_message "${ERROR}" "Invalid commit format."
        log_message "${ERROR}" "Got: $subject_line"
        exit 1
    fi
}

confirm_and_commit() {
    log_message "${DEBUG}" "\nFinal commit message:"
    printf '%s\n%s\n%s\n' "---" "$COMMIT_MSG" "---"

    read -rp "Proceed? [y/N] " confirm
    [[ "$confirm" =~ ^[Yy]$ ]] || exit 0

    # Use + conditional expansion to safely handle an empty GIT_FLAGS array
    # under set -u, which treats empty array expansion as an error in some Bash versions.
    git commit ${GIT_FLAGS[@]+"${GIT_FLAGS[@]}"} -m "$COMMIT_MSG"
}

# -----------------------------
# Main
# -----------------------------
parse_args "$@"
select_type
gather_staged_files
select_scope
prompt_breaking_change
prompt_description
build_commit_message
validate_commit_message
confirm_and_commit
