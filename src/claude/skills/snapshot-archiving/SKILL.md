---
name: snapshot-archiving
description: Archive ~/.claude_<timestamp> snapshot directories based on age. Use when the user asks to archive, clean up, or tidy Claude snapshot directories.
version: 0.1.0
maturity: draft
tags:
  criticality: should
  status: active
  tested: false
---

## Scope gate

This skill is at **draft** maturity. Claude behaviour is constrained accordingly:

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

# 🗂️ Snapshot Archiving

Archive `~/.claude_<timestamp>` snapshot directories into a two-tier structure based on age.

## 📐 Logic

| Source | Age threshold | Destination |
|---|---|---|
| `~/.claude_<timestamp>` (home root) | > 30 days | `~/.claude_archived/` |
| `~/.claude_archived/<name>` | > 90 days | `~/.claude_deep_archived/` |

Both operations use `mv` — no deletion. Directories are retained, only relocated.

## 🔄 Workflow

### Step 1 — Detect eligible directories

Run both detection commands and report what will be moved before taking any action:

```bash
# Tier 1: root snapshot dirs older than 30 days
find ~ -maxdepth 1 -name ".claude_*" -type d -mtime +30 2>/dev/null

# Tier 2: archived entries older than 90 days (only if ~/.claude_archived exists)
find ~/.claude_archived -maxdepth 1 -mindepth 1 -type d -mtime +90 2>/dev/null
```

If neither command returns any results, report "No directories eligible for archiving." and stop.

### Step 2 — Confirm with user

List the directories that will be moved and the destination for each. Wait for explicit confirmation before proceeding.

### Step 3 — Ensure destination directories exist

```bash
mkdir -p ~/.claude_archived
mkdir -p ~/.claude_deep_archived
```

### Step 4 — Move directories

For each eligible directory, run:

```bash
mv "<source>" "<destination>/"
```

Report each move as it completes:

```
Moved: ~/.claude_20250101_120000 → ~/.claude_archived/
```

### Step 5 — Summary

Report:
- Count of directories moved to `~/.claude_archived/`
- Count of directories moved to `~/.claude_deep_archived/`

> TODO (tactical): handle name collisions if a matching directory already exists in the destination.
> TODO (tactical): add dry-run flag support so the user can preview moves without executing.
