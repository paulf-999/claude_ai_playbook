# 📋 Rules — Managed files

The following files must not be edited directly — edits will cause them to drift from
the content they index or compose.

| File | Why it is managed |
|---|---|
| `src/claude/CLAUDE.md` | Managed composition file — imports all rules, process, and style guides via `@import`; do not add content inline |
| `src/claude/README.md` | Reference overview of the `src/claude/` directory — update only when adding new top-level directories or components |
| `src/claude/REGISTRY.md` | Managed component index — delegates to per-component READMEs which are the source of truth |
| `docs/whats_installed.md` | High-level overview of all installed Claude components — manual edits will drift from actual installed content |
| `src/claude/agents/README.md` | Index of agent directories — must stay in sync with the test suite; incremental edits risk table drift |
| `src/claude/skills/README.md` | Index of skill categories — delegates to per-category READMEs which are the source of truth |

## What to do instead

- **To add a new import to `CLAUDE.md`** — adding a new `@import` line is the one permitted direct edit to `CLAUDE.md`; all other content belongs in the imported file, not inline
- **To document a new skill** — update the relevant category README (e.g. `src/claude/skills/_git_skills/README.md`), not `src/claude/skills/README.md`
- **To document a new agent** — update the relevant group README (e.g. `src/claude/agents/core/README.md`), not `src/claude/agents/README.md`
- **To document a new playbook component** — raise a PR and ask DPE to update `docs/whats_installed.md`

All files carry a `DO NOT EDIT` notice at the top as an additional signal.
