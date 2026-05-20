#!/bin/bash

# Load generic shell utilities (logging, helpers, ROOT_DIR, TIMESTAMP)
source src/sh/shell_utils.sh

#=======================================================================
# Variables
#=======================================================================

SOURCE_DIR="${ROOT_DIR}/src/claude"        # repo-managed Claude files (source of truth)
TARGET_DIR="${HOME}/.claude"              # local runtime directory for Claude
BACKUP_DIR="${HOME}/.claude_backup_${TIMESTAMP}"  # timestamped backup location

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

# Backup ~/.claude using specified mode: "move" (install) or "copy" (update)
backup_target_dir() {
    local MODE="$1"  # backup strategy: move (clean install) or copy (safe update)

    # Only backup if directory exists and is not empty
    if dir_exists "${TARGET_DIR}" && [[ -n "$(ls -A "${TARGET_DIR}" 2>/dev/null)" ]]; then

        if [[ "${MODE}" == "move" ]]; then
            mv "${TARGET_DIR}" "${BACKUP_DIR}"   # move entire directory (install behaviour)
            mkdir -p "${TARGET_DIR}"             # recreate clean target directory
            log_message "${INFO}" "Backed up (move) Claude directory to: ${BACKUP_DIR}"

        elif [[ "${MODE}" == "copy" ]]; then
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

# Copy all managed Claude files from repo into target directory
copy_claude_files() {
    cp -R "${SOURCE_DIR}/." "${TARGET_DIR}/"
    find "${TARGET_DIR}" -name "*.sh" -exec chmod +x {} \;
    log_message "${INFO}" "Copied Claude files to: ${TARGET_DIR}"
}

# Merge wip/skills subdirectories into ~/.claude/skills/ so WIP skills are invokable.
# Top-level skill dirs are copied directly. The archive/ dir is excluded.
# Non-directory items (e.g. README.md) are skipped.
merge_skills_wip() {
    local WIP_DIR="${SOURCE_DIR}/wip/skills"
    local SKILLS_DIR="${TARGET_DIR}/skills"

    for ITEM in "${WIP_DIR}"/*/; do
        [[ -d "${ITEM}" ]] || continue
        local ITEM_NAME
        ITEM_NAME=$(basename "${ITEM}")
        if [[ "${ITEM_NAME}" == "archive" ]]; then
            continue  # skip archived skills
        fi
        cp -R "${ITEM}" "${SKILLS_DIR}/${ITEM_NAME}"
        log_message "${INFO}" "Merged wip/skills/${ITEM_NAME} into skills/"
    done
}

# Print summary of Claude file operation (install/update)
print_operation_summary() {
    local OPERATION="$1"  # operation type: "installation" or "update"

    print_section_header "${DEBUG}" "Claude file ${OPERATION} complete."
}
