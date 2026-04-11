# CLAUDE.md — claude_ai_playbook

This file provides repo-specific instructions for Claude Code when working in the playbook repo.

---

## Playbook maintenance

Whenever a new artefact is added to `src/claude/`, the documentation listed below **must be updated in the same PR**. Do not consider a playbook addition complete without these updates.

| Artefact | Required doc updates |
|---|---|
| **Skill** (`skills/`) | `src/claude/skills/README.md` · `docs/whats_installed.md` skills section |
| **Skill WIP** (`skills_wip/`) | `src/claude/skills_wip/README.md` only — WIP skills are not listed in `whats_installed.md` |
| **Rule** (`rules/`) | `src/claude/rules/README.md` · `src/claude/CLAUDE.md` (add `@import`) · `docs/whats_installed.md` rules description |
| **Rule (behaviour)** (`rules/behaviour/`) | `src/claude/rules/behaviour/README.md` · `src/claude/CLAUDE.md` (add `@import`) · `docs/whats_installed.md` rules description |
| **Process file** (`process/`) | `src/claude/process/README.md` · `src/claude/CLAUDE.md` (add `@import`) · `docs/whats_installed.md` process section |
| **Agent** (`agents/<group>/`) | Group README (e.g. `agents/core/README.md`) · `src/claude/process/session.md` agent list · `src/claude/CLAUDE.md` sub-agent table |
| **Hook** (`hooks/`) | `docs/whats_installed.md` hooks table · `settings.json` lifecycle event registration |
| **Style guide** (`style_guide_standards/`) | `src/claude/style_guide_standards/README.md` · `src/claude/CLAUDE.md` (add `@import`) · `docs/whats_installed.md` style guides table · create matching tool agent in `src/claude/agents/tools/` and update `agents/tools/README.md` |
| **Command** (`commands/`) | `src/claude/commands/README.md` · `docs/whats_installed.md` commands section |

After updating the required files above, scan the rest of `docs/` for pages that may reference the area being changed — `quickstart.md`, `training.md`, `best_practices_generic.md`, and files under `docs/reference/` may also need updating depending on the nature of the addition.
