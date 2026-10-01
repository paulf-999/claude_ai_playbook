#!/bin/bash

# Load generic shell utilities (logging, helpers, ROOT_DIR, TIMESTAMP)
source src/sh/shell_utils.sh

#=======================================================================
# Variables
#=======================================================================

SOURCE_DIR="${ROOT_DIR}/src/claude"        # repo-managed Claude files (source of truth)
# Live Claude config dir — never ~/.claude, which holds Claude Code's own state
TARGET_DIR="${CLAUDE_CONFIG_DIR:?CLAUDE_CONFIG_DIR is not set — export it (e.g. export CLAUDE_CONFIG_DIR=\"\$HOME/claude\") and re-run}"
BACKUP_DIR="${HOME}/.claude_backup_${TIMESTAMP}"  # timestamped backup location

# Top-level entries the user owns once installed: copied on first install only, never overwritten
USER_OWNED_ENTRIES=("memory" "TODO.md" "_plans" "settings.local.json")

#=======================================================================
# Shared functions
#=======================================================================

# Ensure source directory exists before proceeding
validate_source_dir() {
    if ! dir_exists "${SOURCE_DIR}"; then
        log_message "${ERROR}" "ERROR: source directory not found: ${SOURCE_DIR}"
        exit 1
    fi
}

# Ensure target directory exists (used for update flow)
validate_target_dir() {
    if ! dir_exists "${TARGET_DIR}"; then
        log_message "${ERROR}" "ERROR: target directory not found: ${TARGET_DIR}"
        exit 1
    fi
}

# Back up the target. Only "copy" exists: moving the target away would strand its runtime data
# (transcripts, history, app state) in the backup, so there is deliberately no "move" mode.
backup_target_dir() {
    local MODE="$1"  # backup strategy: copy (the target stays in place)

    # Only backup if directory exists and is not empty
    if dir_exists "${TARGET_DIR}" && [[ -n "$(ls -A "${TARGET_DIR}" 2>/dev/null)" ]]; then

        if [[ "${MODE}" == "copy" ]]; then
            cp -R "${TARGET_DIR}" "${BACKUP_DIR}"  # copy directory (update safety)
            log_message "${INFO}" "Backed up (copy) Claude directory to: ${BACKUP_DIR}"

        else
            log_message "${ERROR}" "Invalid backup mode: ${MODE}"  # guard against misuse
            exit 1
        fi
    fi
}

# Create target directory if it does not already exist
create_target_dir_if_missing() {
    if ! dir_exists "${TARGET_DIR}"; then
        mkdir -p "${TARGET_DIR}"
        log_message "${INFO}" "Created target directory: ${TARGET_DIR}"
    fi
}

# Return 0 when a top-level entry name is in USER_OWNED_ENTRIES
is_user_owned() {
    local NAME="$1"  # top-level entry name, e.g. "memory"
    local ENTRY
    for ENTRY in "${USER_OWNED_ENTRIES[@]}"; do
        [[ "${ENTRY}" == "${NAME}" ]] && return 0
    done
    return 1
}

# Copy the repo's Claude files over the target, entry by entry.
# Anything already in the target that the repo doesn't ship (transcripts, app state) is left alone,
# and user-owned entries are copied only when the target doesn't have them yet.
copy_claude_files() {
    local ENTRY NAME
    for ENTRY in "${SOURCE_DIR}"/* "${SOURCE_DIR}"/.[!.]*; do
        [[ -e "${ENTRY}" ]] || continue
        NAME=$(basename "${ENTRY}")
        if is_user_owned "${NAME}" && [[ -e "${TARGET_DIR}/${NAME}" ]]; then
            log_message "${INFO}" "Kept user-owned: ${NAME}"
            continue
        fi
        cp -R "${ENTRY}" "${TARGET_DIR}/"
    done
    find "${TARGET_DIR}" -name "*.sh" -exec chmod +x {} \;
    log_message "${INFO}" "Copied Claude files to: ${TARGET_DIR}"
}

# Flatten skill group directories in ~/.claude/skills/.
# Group dirs are identified by a leading underscore (e.g. _meetings_skills/).
# Each skill subdirectory is promoted directly to ~/.claude/skills/;
# then the group dir is removed.
flatten_skills() {
    local SKILLS_DIR="${TARGET_DIR}/skills"

    for GROUP_DIR in "${SKILLS_DIR}"/_*/; do
        [[ -d "${GROUP_DIR}" ]] || continue
        for SKILL_DIR in "${GROUP_DIR}"*/; do
            [[ -d "${SKILL_DIR}" ]] || continue
            local SKILL_NAME
            SKILL_NAME=$(basename "${SKILL_DIR}")
            cp -R "${SKILL_DIR}" "${SKILLS_DIR}/${SKILL_NAME}"
            log_message "${INFO}" "Flattened skill: ${SKILL_NAME}"
        done
        rm -rf "${GROUP_DIR}"
        log_message "${INFO}" "Removed skill group dir: $(basename "${GROUP_DIR}")"
    done
}

# Print summary of Claude file operation (install/update)
print_operation_summary() {
    local OPERATION="$1"  # operation type: "installation" or "update"

    print_section_header "${DEBUG}" "Claude file ${OPERATION} complete."
}
