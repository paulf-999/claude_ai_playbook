# 🧠 Rules — Memory scoping

Claude has two memory scopes. Choose the right one based on whether the memory is relevant beyond the current project.

## Scopes

| Scope | Path | Load behaviour |
|---|---|---|
| **Global** | `~/.claude/memory/` | Loaded in every session via `CLAUDE.md` import — applies across all projects |
| **Project** | `~/.claude/projects/<project>/memory/` | Loaded only when working directory matches — project-specific context only |

## When to use global memory

Save to `~/.claude/memory/` when the memory is:

- A user preference or working style that applies everywhere
- Feedback about Claude's behaviour that should carry across all sessions (e.g. "don't do X", "always prefer Y")
- A workflow convention that is not tied to a specific repo
- A correction the user would expect to apply regardless of which project is open

## When to use project memory

Save to the project-scoped path when the memory is:

- Specific to a single repo or codebase (sprint state, open decisions, project-specific context)
- Ephemeral — only relevant for a short period
- Context that would be noise in unrelated sessions

## How to save a global memory

1. Write the memory file to `~/.claude/memory/<filename>.md` using the standard frontmatter format
2. Add a pointer entry to `~/.claude/memory/MEMORY.md`

The system auto-assigns a project-scoped path for each session — override it by writing to `~/.claude/memory/` when the content is cross-project.

## Sync safety

`~/.claude/memory/MEMORY.md` is personal content and must **never** be overwritten when syncing `src/claude/` → `~/.claude/`. It is not sourced from the repo — it grows over time with personal memories. Only copy `src/claude/memory/MEMORY.md` to `~/.claude/memory/MEMORY.md` if the file does not yet exist (first-time setup).
