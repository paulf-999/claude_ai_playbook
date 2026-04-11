## Memory — Instructions and Persistence

Claude Code uses two mechanisms to retain knowledge across sessions: **CLAUDE.md files** (explicit instructions you write) and **auto memory** (learnings Claude saves automatically). Both are loaded into context at the start of every session.

---

## CLAUDE.md files

CLAUDE.md files are plain markdown files that Claude reads at session start. Use them to define coding standards, workflows, architectural expectations, and any other persistent instructions.

### File locations and hierarchy

Instructions are loaded from most general to most specific — more specific locations take precedence:

| Scope | Path | Purpose |
|---|---|---|
| Managed policy | `/etc/claude-code/CLAUDE.md` (Linux/WSL) | Org-wide standards enforced by IT or DevOps |
| User | `~/.claude/CLAUDE.md` | Personal preferences that apply across all projects |
| Project | `./CLAUDE.md` or `./.claude/CLAUDE.md` | Team-shared, project-specific instructions; committed to source control |

Subdirectory CLAUDE.md files (e.g. `src/claude/CLAUDE.md`) are loaded on demand when Claude processes files in that directory.

### How this repo uses CLAUDE.md

This repo is the source of truth for the team's Claude configuration. `src/claude/` mirrors `~/.claude/` and is installed via `make install`. The user-level `~/.claude/CLAUDE.md` composes the full instruction set using `@import`:

```text
@~/.claude/process/session.md
@~/.claude/rules/git.md
@~/.claude/style_guide_standards/python.md
```

To add or change a rule, edit the relevant file in `src/claude/` and run `make update` to sync to `~/.claude/`.

### @import syntax

Use `@` to import another file's contents inline:

```text
# Relative to the current file's directory
@./rules/testing.md

# Absolute path using the ~/.claude/ alias
@~/.claude/rules/security.md

# Import project files (README, package.json, etc.)
@README
```

Imported files are loaded in full at session start. Use this to compose modular instruction sets rather than maintaining one large CLAUDE.md.

---

## Auto memory

Auto memory lets Claude accumulate knowledge across sessions without explicit input. Claude saves notes on things like build commands, debugging insights, architectural decisions, and workflow habits — and recalls them automatically next session.

Requires Claude Code **v2.1.59 or later** (`claude --version` to check).

### What Claude saves

- Build and test commands discovered during a session
- Debugging approaches that worked
- Corrections you gave Claude (e.g. "don't use mocks in these tests")
- Code style preferences observed in the codebase

Claude decides what is worth saving — it does not write a memory entry after every session.

### Configuration

Auto memory is enabled in the team `settings.json`:

```json
{
  "autoMemoryEnabled": true
}
```

This is installed to `~/.claude/settings.json` by `make install`. To disable for a specific project, add a project-level `.claude/settings.json` with `"autoMemoryEnabled": false`. To disable globally, set the environment variable:

```bash
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
```

---

## Which mechanism to use

| Use case | Mechanism |
|---|---|
| Team-wide coding standards and rules | CLAUDE.md (committed to repo) |
| Personal preferences across all projects | `~/.claude/CLAUDE.md` |
| Project-specific architecture or workflows | Project-level CLAUDE.md |
| Claude learning from corrections and habits | Auto memory (automatic) |
