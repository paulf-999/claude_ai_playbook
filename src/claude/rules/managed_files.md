# 📋 Rules — Managed files

The following files are **managed index files**. Do not edit them — edits will cause them
to drift from the content they index.

| File | Why it is managed |
|---|---|
| `docs/whats_installed.md` | High-level overview of all installed Claude components — manual edits will drift from actual installed content |
| `src/claude/agents/README.md` | Index of agent directories — must stay in sync with the test suite; incremental edits risk table drift |
| `src/claude/skills/README.md` | Index of skill categories — delegates to per-category READMEs which are the source of truth |

## What to do instead

- **To document a new skill** — update the relevant category README (e.g. `src/claude/skills/_git_skills/README.md`), not `src/claude/skills/README.md`
- **To document a new agent** — update the relevant group README (e.g. `src/claude/agents/core/README.md`), not `src/claude/agents/README.md`
- **To document a new playbook component** — raise a PR and ask DPE to update `docs/whats_installed.md`

All three files carry a `DO NOT EDIT` notice at the top as an additional signal.
