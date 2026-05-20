# 🗂️ Rules — Playbook management

Rules for maintaining and syncing the Claude AI playbook repo (`dmt-scripts-claude_ai_playbook`).

## Syncing src/claude/ to ~/.claude/

- 🚫 Never use `make install` to sync changes from `src/claude/` to `~/.claude/`. It overwrites the entire directory, including personal memory files, plans, and session-specific content that live alongside the synced config.
- ✅ Copy only the specific files that changed using `cp`. Create missing parent directories with `mkdir -p` where needed.
- 📌 `src/claude/` is the source of truth — when syncing, overwrite existing files in `~/.claude/` with the repo versions.
- 🚫 **Never copy `memory/MEMORY.md`** during a sync. It is personal content that grows over time and must not be overwritten. Only copy it if `~/.claude/memory/MEMORY.md` does not yet exist (first-time setup).
