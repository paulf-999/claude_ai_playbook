#!/bin/bash

# Load generic shell utilities (logging, helpers, ROOT_DIR, TIMESTAMP)
source src/sh/shell_utils.sh

#=======================================================================
# Variables
#=======================================================================

SOURCE_DIR="${ROOT_DIR}/src/claude"        # repo-managed Claude files (source of truth)
# Live Claude config dir: CLAUDE_CONFIG_DIR when set, otherwise Claude Code's default ~/.claude.
# The install copies over the target and keeps its runtime data, so the default folder is safe to use.
TARGET_DIR="${CLAUDE_CONFIG_DIR:-${HOME}/.claude}"
BACKUP_DIR="${HOME}/.claude_backup_${TIMESTAMP}"  # timestamped backup location

# Top-level entries the user owns once installed: copied on first install only, never overwritten
USER_OWNED_ENTRIES=("memory" "TODO.md" "_plans" "settings.local.json")

# Lists every file the last install put in the target, so the next one can remove what the repo dropped
MANIFEST_NAME=".install_manifest"

# On-demand rules sit under rules/ in the repo but beside it once installed,
# since Claude Code loads every .md under rules/ by itself
LAZY_RULES_NAME="_rules_lazy_load"

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

# Point ~/.claude/ paths in the installed markdown at the real config folder (e.g. ~/claude).
# @ imports can't read environment variables, so this is the only way they resolve elsewhere.
# Only paths into an entry that exists in the target are rewritten, so prose about Claude Code's
# own ~/.claude/ state folder is left alone, and user-owned entries are never touched.
rewrite_config_paths() {
    local PREFIX NAMES ENTRY NAME
    set_plans_directory
    if [[ "${TARGET_DIR}" == "${HOME}/.claude" ]]; then
        return 0
    elif [[ "${TARGET_DIR}" == "${HOME}/"* ]]; then
        # shellcheck disable=SC2088  # a literal ~ is intended: it's text written into markdown, not a path
        PREFIX="~/${TARGET_DIR#"${HOME}/"}/"
    else
        PREFIX="${TARGET_DIR}/"
    fi
    NAMES=$(find "${TARGET_DIR}" -mindepth 1 -maxdepth 1 -exec basename {} \; | perl -ne 'chomp; push @n, quotemeta; END { print join("|", @n) }')
    for ENTRY in "${SOURCE_DIR}"/* "${LAZY_RULES_NAME}"; do
        NAME=$(basename "${ENTRY}")
        is_user_owned "${NAME}" && continue
        [[ -e "${TARGET_DIR}/${NAME}" ]] || continue
        PREFIX="${PREFIX}" NAMES="${NAMES}" find "${TARGET_DIR}/${NAME}" -type f -name "*.md" \
            -exec perl -pi -e 's{~/\.claude/(?=(?:$ENV{NAMES})\b)}{$ENV{PREFIX}}g' {} +
    done
    log_message "${INFO}" "Pointed ~/.claude/ paths at: ${PREFIX}"
}

# Set settings.json's plansDirectory to the target's own _plans/ folder
set_plans_directory() {
    local SETTINGS="${TARGET_DIR}/settings.json"
    [[ -f "${SETTINGS}" ]] || return 0
    PLANS="${TARGET_DIR}/_plans" perl -pi -e 's{("plansDirectory":\s*)"[^"]*"}{$1"$ENV{PLANS}"}' "${SETTINGS}"
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
            # Copy the contents (dir/.) so an existing skill folder is merged into, not nested, on GNU and BSD cp
            mkdir -p "${SKILLS_DIR}/${SKILL_NAME}"
            cp -R "${SKILL_DIR}." "${SKILLS_DIR}/${SKILL_NAME}/"
            log_message "${INFO}" "Flattened skill: ${SKILL_NAME}"
        done
        rm -rf "${GROUP_DIR}"
        log_message "${INFO}" "Removed skill group dir: $(basename "${GROUP_DIR}")"
    done
}

# Move rules/_rules_lazy_load/ up to the target's top level, beside rules/, so Claude Code doesn't load it every session.
# Copies the contents (dir/.) so an existing folder is merged into, not nested, on GNU and BSD cp.
relocate_lazy_rules() {
    local FROM="${TARGET_DIR}/rules/${LAZY_RULES_NAME}"
    [[ -d "${FROM}" ]] || return 0
    mkdir -p "${TARGET_DIR}/${LAZY_RULES_NAME}"
    cp -R "${FROM}/." "${TARGET_DIR}/${LAZY_RULES_NAME}/"
    rm -rf "${FROM}"
    log_message "${INFO}" "Moved rules/${LAZY_RULES_NAME}/ beside rules/"
}

# Print the files an install puts in the target, relative to it and sorted, laid out as
# flatten_skills and relocate_lazy_rules leave them.
# User-owned entries are left out, so pruning can never remove them.
list_installed_files() {
    local REL
    (cd "${SOURCE_DIR}" && find . -type f) | sed 's#^\./##' | while IFS= read -r REL; do
        is_user_owned "${REL%%/*}" && continue
        if [[ "${REL}" == "rules/${LAZY_RULES_NAME}/"* ]]; then
            echo "${REL#rules/}"
        elif [[ "${REL}" =~ ^skills/_[^/]+/([^/]+/.+)$ ]]; then
            echo "skills/${BASH_REMATCH[1]}"
        elif [[ ! "${REL}" =~ ^skills/_[^/]+/[^/]+$ ]]; then  # a group's own files go with its folder
            echo "${REL}"
        fi
    done | LC_ALL=C sort -u
}

# Remove empty folders from a path upwards, stopping at the target itself
remove_empty_parents() {
    local DIR="$1"  # folder a file was just removed from
    while [[ "${DIR}" != "${TARGET_DIR}" && "${DIR}" == "${TARGET_DIR}/"* ]] && rmdir "${DIR}" 2>/dev/null; do
        DIR=$(dirname "${DIR}")
    done
}

# Remove files the last install put in the target that the repo no longer ships, then record this install.
# Only paths on the previous manifest are candidates, so files the user added to the target are never touched.
# The first install with this step has no manifest yet: it removes nothing and just writes one.
prune_removed_files() {
    local MANIFEST="${TARGET_DIR}/${MANIFEST_NAME}"
    local CURRENT REL
    CURRENT=$(list_installed_files)
    if [[ -f "${MANIFEST}" ]]; then
        LC_ALL=C comm -23 <(LC_ALL=C sort -u "${MANIFEST}") <(echo "${CURRENT}") | while IFS= read -r REL; do
            [[ -z "${REL}" || "${REL}" == /* || "/${REL}/" == */../* ]] && continue  # stay inside the target
            is_user_owned "${REL%%/*}" && continue
            [[ -f "${TARGET_DIR}/${REL}" ]] || continue
            rm "${TARGET_DIR}/${REL}"
            log_message "${INFO}" "Removed (no longer in the repo): ${REL}"
            remove_empty_parents "$(dirname "${TARGET_DIR}/${REL}")"
        done
    else
        log_message "${INFO}" "No install manifest yet — nothing removed; the next install can prune"
    fi
    echo "${CURRENT}" > "${MANIFEST}"
}

# Clear what the old _rules/ layout left behind (replaced 2026-10-06 by rules/ and _rules_lazy_load/):
# the links earlier installs put in rules/, and files you added under _rules/, which move to the same
# place in _rules_lazy_load/ (whose root was _rules/05_lazy_load/). Runs after pruning, which already
# removed the files earlier installs shipped there, so whatever is left in _rules/ is yours.
# Never overwrites: if the new path is taken, the old file stays in _rules/ and a warning names it.
migrate_old_rules_layout() {
    local OLD_DIR="${TARGET_DIR}/_rules"
    local NEW_DIR="${TARGET_DIR}/_rules_lazy_load"
    local LINK FROM REL TO
    # Links into the old _rules/ would dangle, and Claude Code would still try to load them
    if [[ -d "${TARGET_DIR}/rules" ]]; then
        while IFS= read -r LINK; do
            [[ "$(readlink "${LINK}")" == ../_rules/* ]] || continue
            rm "${LINK}"
            log_message "${INFO}" "Removed old rule link: rules/$(basename "${LINK}")"
        done < <(find "${TARGET_DIR}/rules" -maxdepth 1 -type l -name "*.md")
    fi
    [[ -d "${OLD_DIR}" ]] || return 0
    while IFS= read -r FROM; do
        REL="${FROM#"${OLD_DIR}/"}"
        TO="${NEW_DIR}/${REL#05_lazy_load/}"
        if [[ -e "${TO}" ]]; then
            log_message "${WARNING}" "Kept _rules/${REL}: ${TO#"${TARGET_DIR}/"} already exists — merge it by hand"
            continue
        fi
        mkdir -p "$(dirname "${TO}")"
        mv "${FROM}" "${TO}"
        log_message "${INFO}" "Moved your file: _rules/${REL} -> ${TO#"${TARGET_DIR}/"}"
    done < <(find "${OLD_DIR}" -type f | LC_ALL=C sort)
    find "${OLD_DIR}" -depth -type d -empty -delete
    if [[ -d "${OLD_DIR}" ]]; then
        log_message "${WARNING}" "_rules/ still holds files that clash with the new layout — review: ${OLD_DIR}"
    fi
    return 0
}

# Print summary of Claude file operation (install/update)
print_operation_summary() {
    local OPERATION="$1"  # operation type: "installation" or "update"

    print_section_header "${DEBUG}" "Claude file ${OPERATION} complete."
}
