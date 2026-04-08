# 🚀 Claude AI Playbook — Quick Start

This guide walks you through setting up the team's Claude configuration and starting your first session.

---

## ⚙️ Step 1: Install

Run the install target:

```bash
make install
```

---

## 📂 Step 2: Open a project in Claude Code

Navigate to your project directory and run:

```bash
claude
```

---

## 🧭 Step 3: Session startup

At the start of every session, type:

```
enter plan mode
```

This triggers the session startup protocol. Claude will work through three steps in order:

1. 🤖 **Sub-agent** — Claude asks which specialist persona to use for the session. See [reference/sub_agents.md](reference/sub_agents.md) for the available options and when to use each.
2. 📋 **Context** — Claude reads all imported context files, summarises the current project state, and asks you to confirm the summary is correct.
3. 💬 **Task** — Claude asks what the task is for the session. Describe the work you want to do.

Claude operates as an **architect** by default — a planner-first persona that outlines its approach and waits for your go-ahead before making changes. See [reference/sub_agents.md](reference/sub_agents.md) for available specialist personas.

---

## 💡 Step 4: During the session

Claude will outline its approach and list assumptions before making any non-trivial change. Review and confirm before it proceeds.

Before considering a task complete, Claude should run the relevant tests and confirm they pass. If no tests cover the changed area, Claude will flag the gap and agree on what to add before proceeding — do not accept changes that arrive without test coverage.

---

## 🏁 Step 5: End of session

When you are done, say **"wrap up"**. Claude will produce a context summary in this format:

```
Project: ...
What changed: ...
Decisions made: ...
Open questions: ...
Known issues: ...
```

Paste this into `~/.claude/context.md`.

---

## ➕ Extras: MCP server configuration

MCP servers extend what Claude can access during a session. See [`docs/reference/mcp/mcp_setup.md`](reference/mcp/mcp_setup.md) for the full setup guide.
