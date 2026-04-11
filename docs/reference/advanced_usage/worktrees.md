# 🌿 Git Worktrees for Parallel Claude Sessions

Git worktrees let you run multiple Claude sessions simultaneously, each in its own isolated working directory and branch. Changes in one session cannot interfere with another.

---

## When to use worktrees

Use a worktree when you want to work on two or more tasks in parallel — for example, developing a feature while fixing a bug, or running a long Claude task in the background while starting another.

Without worktrees, two sessions on the same directory would conflict: file edits, branch state, and uncommitted changes would collide.

---

## Starting a session in a worktree

Use the `--worktree` flag when launching Claude:

```bash
# Start a session in a worktree named "feature-auth"
# Creates .claude/worktrees/feature-auth/ on branch worktree-feature-auth
claude --worktree feature-auth

# Start a second parallel session in a separate worktree
claude --worktree bugfix-123
```

If you omit the name, Claude generates a random one:

```bash
claude --worktree
# Creates something like .claude/worktrees/bright-running-fox/
```

Worktrees branch from `origin/HEAD` (the remote's default branch). If the default branch has changed since you cloned, re-sync it first:

```bash
git remote set-head origin -a
```

---

## Cleanup behaviour

When you exit a worktree session, Claude handles cleanup based on whether changes were made:

| Outcome | What happens |
|---|---|
| No changes made | Worktree and branch are removed automatically |
| Changes or commits exist | Claude prompts: keep (preserves directory and branch) or remove (discards all changes) |

---

## Copying gitignored files into worktrees

Worktrees are fresh checkouts and do not include untracked files like `.env`. To automatically copy these files when a worktree is created, add a `.worktreeinclude` file to the repo root.

This repo includes a `.worktreeinclude` that copies `.env`:

```text
.env
```

The file uses `.gitignore` syntax. Only files that match a pattern **and** are gitignored get copied — tracked files are never duplicated.

---

## Subagent worktrees

The `architect` and `technical_writer` agents are configured with `isolation: worktree` in their frontmatter. This means when either agent runs as a subagent, it automatically gets its own isolated worktree — preventing branch conflicts when Claude is delegating work in parallel.

For other agents, you can request worktree isolation on demand:

```
Use worktrees for your agents.
```

See [`src/claude/agents/core/architect.md`](../../src/claude/agents/core/architect.md) for the frontmatter reference.

---

## Manual worktree management

For full control over branch and location, use Git directly:

```bash
# Create a worktree on a new branch
git worktree add ../project-feature-a -b feature-a

# Create a worktree on an existing branch
git worktree add ../project-bugfix bugfix-123

# Start Claude in the worktree
cd ../project-feature-a && claude

# List active worktrees
git worktree list

# Remove a worktree when done
git worktree remove ../project-feature-a
```

Manual worktrees are placed outside the repo directory by convention (using `../`), unlike `--worktree` which places them inside `.claude/worktrees/`.
