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

# Top-level entries that only make sense in the repo and are never installed: the installer itself
REPO_ONLY_ENTRIES=("_install")

# Lists every file the last install put in the target, so the next one can remove what the repo dropped
MANIFEST_NAME=".install_manifest"

# On-demand rules sit under rules/ in the repo but beside it once installed,
# since Claude Code loads every .md under rules/ by itself
LAZY_RULES_NAME="_rules_lazy_load"

# Style guides sit in one folder, in the repo and once installed, except their entry files (with paths:
# frontmatter), which the install moves under rules/ so Claude Code loads them on matching files
STYLE_GUIDES_NAME="_style_guide_standards"
STYLE_GUIDES_PATH_SCOPED="rules/04_path_scoped/style_guide_standards"

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
# Tell whether a top-level entry stays in the repo and is never copied to the target
is_repo_only() {
    local NAME="$1"  # top-level entry name, e.g. "_install"
    local ENTRY
    for ENTRY in "${REPO_ONLY_ENTRIES[@]}"; do
        [[ "${ENTRY}" == "${NAME}" ]] && return 0
    done
    return 1
}

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
        is_repo_only "${NAME}" && continue
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

# Set settings.json's plansDirectory to the target's own plans/ folder, where plan mode keeps its drafts.
# Saved plans live apart in _plans/, so drafts never mix with them.
set_plans_directory() {
    local SETTINGS="${TARGET_DIR}/settings.json"
    [[ -f "${SETTINGS}" ]] || return 0
    PLANS="${TARGET_DIR}/plans" perl -pi -e 's{("plansDirectory":\s*)"[^"]*"}{$1"$ENV{PLANS}"}' "${SETTINGS}"
}

# Flatten skill group directories in ~/.claude/skills/.
# Group dirs are identified by a leading underscore (e.g. _meetings_skills/).
# Each skill subdirectory is promoted directly to ~/.claude/skills/;
# then the group dir is removed.
flatten_skills() {
    local SKILLS_DIR="${TARGET_DIR}/skills"
    local SKILL_COUNT=0 GROUP_COUNT=0

    for GROUP_DIR in "${SKILLS_DIR}"/_*/; do
        [[ -d "${GROUP_DIR}" ]] || continue
        for SKILL_DIR in "${GROUP_DIR}"*/; do
            [[ -d "${SKILL_DIR}" ]] || continue
            local SKILL_NAME
            SKILL_NAME=$(basename "${SKILL_DIR}")
            # Copy the contents (dir/.) so an existing skill folder is merged into, not nested, on GNU and BSD cp
            mkdir -p "${SKILLS_DIR}/${SKILL_NAME}"
            cp -R "${SKILL_DIR}." "${SKILLS_DIR}/${SKILL_NAME}/"
            SKILL_COUNT=$((SKILL_COUNT + 1))
        done
        rm -rf "${GROUP_DIR}"
        GROUP_COUNT=$((GROUP_COUNT + 1))
    done
    # One summary line rather than one per skill and group, to keep the install output short
    [[ "${GROUP_COUNT}" -gt 0 ]] && log_message "${INFO}" "Flattened ${SKILL_COUNT} skills from ${GROUP_COUNT} groups"
    return 0
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

# Return 0 when a file's opening frontmatter has a paths: key, meaning Claude Code loads it on matching files
is_path_scoped() {
    local FILE="$1"  # file to check
    awk 'NR == 1 { if ($0 != "---") exit; next } $0 == "---" { exit } /^paths:/ { found = 1; exit } END { exit !found }' "${FILE}"
}

# Print where a style-guide file installs, relative to the target: under rules/ when path-scoped, else in place
style_guide_install_path() {
    local FILE="$1"  # the file itself, to read its frontmatter
    local REL="$2"   # its path inside _style_guide_standards/
    if is_path_scoped "${FILE}"; then
        echo "${STYLE_GUIDES_PATH_SCOPED}/${REL}"
    else
        echo "${STYLE_GUIDES_NAME}/${REL}"
    fi
}

# Move the style guides' entry files from _style_guide_standards/ into rules/, where Claude Code loads them
# on matching files, overwriting the last install's copy. Every other file stays put and is read on demand.
split_style_guides() {
    local FROM_DIR="${TARGET_DIR}/${STYLE_GUIDES_NAME}"
    local FROM TO COUNT=0
    [[ -d "${FROM_DIR}" ]] || return 0
    while IFS= read -r FROM; do
        is_path_scoped "${FROM}" || continue
        TO="${TARGET_DIR}/${STYLE_GUIDES_PATH_SCOPED}/${FROM#"${FROM_DIR}/"}"
        mkdir -p "$(dirname "${TO}")"
        mv -f "${FROM}" "${TO}"
        COUNT=$((COUNT + 1))
    done < <(find "${FROM_DIR}" -type f)
    find "${FROM_DIR}" -depth -type d -empty -delete
    [[ "${COUNT}" -gt 0 ]] && log_message "${INFO}" "Moved ${COUNT} style-guide entry files into ${STYLE_GUIDES_PATH_SCOPED}/"
    return 0
}

# Print the files an install puts in the target, relative to it and sorted, laid out as
# flatten_skills, relocate_lazy_rules and split_style_guides leave them.
# User-owned entries are left out, so pruning can never remove them.
list_installed_files() {
    local REL
    (cd "${SOURCE_DIR}" && find . -type f) | sed 's#^\./##' | while IFS= read -r REL; do
        is_user_owned "${REL%%/*}" && continue
        is_repo_only "${REL%%/*}" && continue
        if [[ "${REL}" == "${STYLE_GUIDES_NAME}/"* ]]; then
            style_guide_install_path "${SOURCE_DIR}/${REL}" "${REL#"${STYLE_GUIDES_NAME}/"}"
        elif [[ "${REL}" == "rules/${LAZY_RULES_NAME}/"* ]]; then
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

# Tell whether a file's exact content is something this repo has stored, i.e. a copy an install shipped.
# A file you edited has content the repo never stored, so it never matches. Without git, nothing matches.
shipped_by_repo() {
    local HASH
    HASH=$(git -C "${ROOT_DIR}" hash-object "$1" 2>/dev/null) || return 1
    git -C "${ROOT_DIR}" cat-file -e "${HASH}^{blob}" 2>/dev/null
}

# Remove old shipped copies from _rules_lazy_load/: files this install doesn't ship but whose content the
# repo once shipped. The first version of migrate_old_rules_layout (2026-10-06) moved every old _rules/ file
# in here, and no manifest lists them, so pruning can't see them. Compares against this install's files
# rather than the manifest, so the Windows sync (which keeps none) is covered too. A file you edited never
# matches, so it stays. The install's backup holds a copy of everything removed here.
remove_stale_lazy_copies() {
    local LAZY_DIR="${TARGET_DIR}/${LAZY_RULES_NAME}"
    local CURRENT FILE REL
    local COUNT=0
    [[ -d "${LAZY_DIR}" ]] || return 0
    CURRENT=$(list_installed_files)
    while IFS= read -r FILE; do
        REL="${FILE#"${TARGET_DIR}/"}"
        grep -qxF "${REL}" <<< "${CURRENT}" && continue
        shipped_by_repo "${FILE}" || continue
        rm "${FILE}"
        remove_empty_parents "$(dirname "${FILE}")"
        COUNT=$((COUNT + 1))
    done < <(find "${LAZY_DIR}" -type f | LC_ALL=C sort)
    # One summary line rather than one per file, to keep the install output short
    [[ "${COUNT}" -gt 0 ]] && log_message "${INFO}" "Removed old shipped copies from ${LAZY_RULES_NAME}/: ${COUNT} (the backup keeps them)"
    return 0
}

# Clear what the old _rules/ layout left behind (replaced 2026-10-06 by rules/ and _rules_lazy_load/):
# the links earlier installs put in rules/, then each file left under _rules/. A file whose content the
# repo shipped is a stale copy — installs before the manifest existed left them, so pruning can't see
# them — and is removed. Anything else is yours and moves to the same place in _rules_lazy_load/ (whose
# root was _rules/05_lazy_load/). Never overwrites: if the new path is taken, your file stays in _rules/
# and a warning names it. The install's backup holds a copy of everything removed here.
migrate_old_rules_layout() {
    local OLD_DIR="${TARGET_DIR}/_rules"
    local NEW_DIR="${TARGET_DIR}/_rules_lazy_load"
    local LINK FROM REL TO
    local SHIPPED_COUNT=0
    remove_stale_lazy_copies
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
        if shipped_by_repo "${FROM}"; then
            rm "${FROM}"
            SHIPPED_COUNT=$((SHIPPED_COUNT + 1))
            continue
        fi
        if [[ -e "${TO}" ]]; then
            log_message "${WARNING}" "Kept _rules/${REL}: ${TO#"${TARGET_DIR}/"} already exists — merge it by hand"
            continue
        fi
        mkdir -p "$(dirname "${TO}")"
        mv "${FROM}" "${TO}"
        log_message "${INFO}" "Moved your file: _rules/${REL} -> ${TO#"${TARGET_DIR}/"}"
    done < <(find "${OLD_DIR}" -type f | LC_ALL=C sort)
    # One summary line rather than one per file, to keep the install output short
    [[ "${SHIPPED_COUNT}" -gt 0 ]] && log_message "${INFO}" "Removed old shipped copies from _rules/: ${SHIPPED_COUNT} (the backup keeps them)"
    find "${OLD_DIR}" -depth -type d -empty -delete
    if [[ -d "${OLD_DIR}" ]]; then
        log_message "${WARNING}" "_rules/ still holds files that clash with the new layout — review: ${OLD_DIR}"
    fi
    return 0
}

# File saved plans and plan-mode drafts into their status folders (see clean_plans.py).
# Runs without its own prompt: the install was already confirmed and backed up, and filing
# only moves files — never deletes or overwrites — so it stays safe on a config you own.
file_plans() {
    local SCRIPT="${SOURCE_DIR}/_scripts/_clean_scripts/clean_plans.py"
    local OUTPUT
    if ! command -v python3 >/dev/null 2>&1; then
        log_message "${WARNING}" "python3 not found — skipped filing plans; run: make clean_plans"
        return 0
    fi
    OUTPUT=$(CLAUDE_CONFIG_DIR="${TARGET_DIR}" python3 "${SCRIPT}" --yes 2>&1) \
        || { log_message "${WARNING}" "Filing plans failed — run: make clean_plans"; return 0; }
    [[ -n "${OUTPUT}" ]] && log_message "${INFO}" "${OUTPUT}"
    return 0
}

# Print summary of Claude file operation (install/update)
print_operation_summary() {
    local OPERATION="$1"  # operation type: "installation" or "update"

    print_section_header "${DEBUG}" "Claude file ${OPERATION} complete."
}
