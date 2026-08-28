#!/usr/bin/env bash
# Reset ~/.claude/ to a minimal v2 baseline.
#
# What this script does:
#   1. Archives the current ~/.claude/ content to a versioned release dir
#   2. Removes the archived content from ~/.claude/
#   3. Creates the minimal v2 config files
#
# The release archive is the rollback path — nothing is deleted permanently.
# To restore: cp -r ~/.claude_releases/<release>/ ~/.claude/
#
# Usage: bash src/sh/reset_claude_config.sh
# Recommended: run interactively so you can inspect each step.

set -euo pipefail

RELEASE_DIR="${HOME}/.claude_releases/v1_playbook_baseline"

# ─── Step 1: Create the release archive dir ───────────────────────────────────

mkdir -p "${RELEASE_DIR}"

# ─── Step 2: Archive ~/.claude/ content ───────────────────────────────────────
# Copy all dirs and files that were present in the v1 playbook config.
# Adjust the list below to match what you actually had — run `ls -la ~/.claude/`
# before archiving if unsure.

ARCHIVE_DIRS=(
    skills
    rules
    agents
    hooks
    process
    style_guide_standards
    commands
    wip
    docs
    plans
    memory
    backups
    sessions
    projects
)

for dir in "${ARCHIVE_DIRS[@]}"; do
    src="${HOME}/.claude/${dir}"
    if [[ -d "${src}" ]]; then
        cp -r "${src}" "${RELEASE_DIR}/"
        echo "archived: ${dir}/"
    fi
done

for file in CLAUDE.md settings.json todos.md; do
    src="${HOME}/.claude/${file}"
    if [[ -f "${src}" ]]; then
        cp "${src}" "${RELEASE_DIR}/"
        echo "archived: ${file}"
    fi
done

# ─── Step 3: Remove v1 content from ~/.claude/ ────────────────────────────────
# Only remove user-owned dirs. Leave runtime dirs (backups/, sessions/, projects/)
# in place — Claude Code manages these and will recreate them anyway.

REMOVE_DIRS=(
    skills
    rules
    agents
    hooks
    process
    style_guide_standards
    commands
    wip
    docs
    plans
)

for dir in "${REMOVE_DIRS[@]}"; do
    target="${HOME}/.claude/${dir}"
    if [[ -d "${target}" ]]; then
        rm -rf "${target}"
        echo "removed:  ${dir}/"
    fi
done

# Clear memory files but keep the directory (Claude Code owns it)
find "${HOME}/.claude/memory/" -maxdepth 1 -type f -delete 2>/dev/null || true

# ─── Step 4: Write the v2 minimal config ──────────────────────────────────────

# --- CLAUDE.md ---
cat > "${HOME}/.claude/CLAUDE.md" << 'EOF'
# Global Claude configuration

> ⚠️ **Managed file** — do not edit directly.
> - **Rule:** add behaviour by editing imported files only — never inline
> - **Before importing:** does Claude need this every session?
> - **Remember:** every import grows context — favour deliberate addition

## Core Principles

*Adapted from [Andrej Karpathy's guidelines](https://github.com/multica-ai/andrej-karpathy-skills/)*

1. **Don't assume. Don't hide confusion. Surface tradeoffs.**
2. **Minimum code that solves the problem. Nothing speculative.**
3. **Touch only what you must. Clean up only your own mess.**
4. **Define success criteria. Loop until verified.**

## Imports

<!-- Personal context: memories, preferences, and corrections from prior sessions -->
@~/.claude/memory/MEMORY.md

<!-- Conventions: directory naming and meta-structure for ~/.claude/ -->
@~/.claude/_rules/conventions.md

<!-- File standards: writing and formatting rules for files in _rules/ -->
@~/.claude/_rules/file_standards.md
EOF

# --- settings.json ---
cat > "${HOME}/.claude/settings.json" << 'EOF'
{
  "defaultMode": "plan",
  "autoMemoryEnabled": true,
  "showClearContextOnPlanAccept": true,
  "permissions": {
    "allow": [
      "Bash(git add:*)",
      "Bash(git branch:*)",
      "Bash(git checkout:*)",
      "Bash(git commit:*)",
      "Bash(git diff:*)",
      "Bash(git fetch:*)",
      "Bash(git log:*)",
      "Bash(git merge:*)",
      "Bash(git pull:*)",
      "Bash(git push:*)",
      "Bash(git rebase:*)",
      "Bash(git status:*)",
      "Bash(git -C:*)",
      "Bash(gh:*)",
      "Bash(find:*)"
    ]
  }
}
EOF

# --- memory/MEMORY.md ---
mkdir -p "${HOME}/.claude/memory"
cat > "${HOME}/.claude/memory/MEMORY.md" << 'EOF'
# Global Memory Index

Cross-project memories loaded in every Claude session.
EOF

# --- _rules/ ---
mkdir -p "${HOME}/.claude/_rules"

cat > "${HOME}/.claude/_rules/conventions.md" << 'EOF'
# 🗂️ ~/.claude/ conventions

## Directory naming

- **User-created dirs:** underscore prefix — e.g. `_docs/`, `_rules/`
- **Claude Code auto-generated dirs:** no prefix — e.g. `backups/`, `memory/`, `sessions/`
EOF

cat > "${HOME}/.claude/_rules/file_standards.md" << 'EOF'
# ✏️ File standards — `_rules/` files

## 📏 Length

- **Limit:** ~100 lines. Up to 110 tolerated; beyond that, split into a parent index
  + child files referenced from the parent.
- **Scope:** one concept per file — don't bundle unrelated rules into a single file.

## 🎨 Style

- **Emojis:** use on all major headings and callout blocks — they aid scannability.
- **Bullets:** prefer over prose for rules and lists.
- **Leading bold keyword + colon:** open each bullet with the key term in bold:
  - `**Why:**` rationale for a decision
  - `**Note:**` a caveat or edge case
  - `**Example:**` a concrete illustration
- **Brevity:** if a sentence can be cut without losing meaning, cut it.

## 🔧 Conventions

- **Filenames:** snake_case, lowercase only.
- **Newline:** files must end with a single newline.
- **Imports:** use `@import` for shared content — never duplicate inline.
EOF

# --- _docs/decisions/ ---
mkdir -p "${HOME}/.claude/_docs/decisions"

cat > "${HOME}/.claude/_docs/decisions/CLAUDE.md" << 'EOF'
# 📋 Decisions — CLAUDE.md

## 🔗 Composition file pattern

- **Why:** Rules evolve independently — separate imported files mean changes can be
  tracked and committed to git without touching CLAUDE.md itself.
- **Note:** CLAUDE.md is a thin orchestration file only. All content belongs in
  imported files; nothing goes inline.

## 📁 `_rules/` directory

- **Why:** Files in `_rules/` are Claude-facing behavioral instructions, categorically
  different from `_docs/` which is human-facing documentation. Separation keeps the
  distinction clear and makes git tracking cleaner.
- **Note:** Underscore prefix marks it as user-created per the `~/.claude/` naming
  convention.

## 📄 `file_standards.md` in `_rules/` not `_docs/`

- **Why:** Authoring standards are a behavioral rule — Claude writes files and must
  follow them. They belong in `_rules/` alongside other behavioral instructions.

## 🧠 `memory/MEMORY.md` imported first

- **Why:** Personal context loads before behavioral rules, so memories and corrections
  are available as the most immediate framing when rules are applied.
EOF

echo ""
echo "Reset complete. ~/.claude/ is now at the v2 minimal baseline."
echo "Archive: ${RELEASE_DIR}"
