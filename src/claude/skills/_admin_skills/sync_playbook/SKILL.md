---
name: sync_playbook
description: Pull latest playbook changes and sync to both WSL and Windows Claude config. Run from WSL terminal. Use when the playbook repo has been updated and you want both environments current.
version: 1.0.0
maturity: tactical
tags:
  criticality: should
  status: active
  tested: false
tools: Bash
---

## Scope gate

This skill is at **tactical** maturity. Claude behaviour is constrained accordingly:

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

You are syncing the Claude playbook. Work through the steps below in order. Stop and report any failure immediately — do not skip ahead.

---

## ⚠️ Pre-check — WSL environment

Confirm this is running in WSL by checking for `powershell.exe`:

```bash
command -v powershell.exe
```

If not found, stop and tell the user:

> "This skill must be run from a WSL terminal. Open your WSL terminal (e.g. Ubuntu in Windows Terminal) and try again."

---

## 🔍 Step 1 — Locate the playbook repo

Resolve the repo path in this order:

1. Use `$CLAUDE_PLAYBOOK_DIR` if set
2. Fall back to `~/git_repos/dmt-scripts-claude_ai_playbook`

Verify the path exists:

```bash
ls "${CLAUDE_PLAYBOOK_DIR:-${HOME}/git_repos/dmt-scripts-claude_ai_playbook}"
```

If not found, stop and tell the user:

> "Playbook repo not found. Set the CLAUDE_PLAYBOOK_DIR environment variable to its path, or clone it to ~/git_repos/dmt-scripts-claude_ai_playbook."

---

## 📥 Step 2 — Pull latest changes

```bash
cd <playbook_repo_path>
git pull
```

Capture the output. If already up to date, tell the user and still proceed with the sync (config may differ from what is installed).

---

## 🔄 Step 3 — Sync to WSL and Windows

```bash
make sync
```

This runs `make update` (WSL `~/.claude`) followed by `make install_windows` (Windows `C:\Users\<user>\.claude`).

Report the output clearly. If either step fails, stop and show the error.

---

## ✅ Step 4 — Report

Tell the user:

- Whether the pull fetched new commits (and how many if available)
- That WSL `~/.claude` has been updated
- That Windows `C:\Users\<username>\.claude` has been updated
- A reminder to restart Claude Code in any open sessions to pick up the changes
