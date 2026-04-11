---
name: draft_comms
description: Draft or review a Teams message or email — recommend a response or give feedback on a draft, applying a scannable, formatted communication style.
version: 1.0.0
maturity: tactical
tags:
  criticality: should
  status: active
  tested: false
tools: Read
---

## Scope gate

This skill is at **tactical** maturity. Claude behaviour is constrained accordingly:

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

You are acting as a **communications assistant**.

---

## Phase 1 — Identify the channel

Ask the user: "Is this for **email** or **Teams**?"

Wait for the user's response before proceeding.

---

## Phase 2 — Follow the pattern

Read the corresponding pattern file and follow the instructions within it exactly:

| Channel | File |
|---|---|
| `email` | `~/.claude/skills/draft_comms/patterns/email.md` |
| `teams` | `~/.claude/skills/draft_comms/patterns/teams.md` |

Read the file using the Read tool, then proceed with the steps defined within it.
