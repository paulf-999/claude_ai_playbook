# 🚀 Claude AI Playbook — Quick Start

## ⚙️ Step 1: Install

Run this from your own terminal — the install refuses to run anywhere else, including from Claude:

```bash
make install
```

It previews the target, backup path and six install steps, then asks you to type `install` — any other answer cancels with nothing changed.

> **First-time install:** open a new terminal after `make install` before running `claude`.

> **Custom folder:** the config installs into Claude Code's default folder, `~/.claude`. To use another one, such as `~/claude`, add `export CLAUDE_CONFIG_DIR="$HOME/claude"` to your shell profile (e.g. `~/.zshrc`) and open a new terminal before running `make install` — Claude Code reads the same variable to find it.

---

## 📂 Step 2: Open a project in Claude Code

```bash
claude
```

> **First run:** you will be prompted to log in with your Claude account before the session starts.

---

## 🧭 Step 3: Session startup

Claude starts in [plan mode](reference/advanced_usage/permission_modes.md) automatically *(read-only — won't make changes without your approval)* and runs through the session startup protocol:

1. 🤖 **Sub-agent** — Claude defaults to `architect` (general dev work) — name a different one for specialised tasks or press enter to continue ([full list](reference/claude_config/sub_agents.md)).

   > **💡 Tip:** To skip this prompt, pre-populate `~/.claude/process/session_input.md` before launching — Claude reads it automatically at the start of every session.

2. 📋 **Context** — Claude reads your configuration and any saved project context, summarises the current state, and asks you to confirm.
3. 💬 **Task** — Claude asks what the task is for the session. Describe the work you want to do.

---

## 💡 Step 4: During the session

- 📋 Claude outlines its approach before any non-trivial change — review and confirm before it proceeds.
- ✅ Tests must pass before a task is complete — Claude flags any coverage gaps before proceeding.

---

## ➕ Extras: Keeping up to date

After any `git pull`, re-run the install from your own terminal:

```bash
make install
```

Your current config folder is copied to `~/.claude_backup_<timestamp>` first, so copy back any local edits you want to keep.

---

## ➕ Further reading

| Topic | Guide |
|---|---|
| MCP server configuration | [Connect Claude to GitHub, Atlassian, Microsoft 365, etc.](reference/claude_config/mcp/mcp_setup.md) |
| Permission modes | [Control what Claude can do automatically vs. with approval](reference/advanced_usage/permission_modes.md) |
| Memory and persistent instructions | [CLAUDE.md files, auto memory, and the `@import` syntax](reference/advanced_usage/memory.md) |
| Parallel sessions with worktrees | [Run multiple Claude sessions simultaneously on separate branches](reference/advanced_usage/worktrees.md) |
| Resuming sessions | [Resume interrupted sessions, pick up from a PR, or fork a session](reference/advanced_usage/sessions.md) |
| Training resources | [Free training from Anthropic](training.md) |
