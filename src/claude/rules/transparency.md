# 🔍 Rules — Execution transparency

Be predictable. Before starting work and during execution, give the user enough information to understand what is happening, how long it will take, and how far along it is.

---

## 📋 Always estimate scope before starting

For any task that is not trivially simple, state the scope and estimated effort before proceeding:

| Task type | Action |
|---|---|
| Single file edit or one tool call | Proceed directly — no scope statement needed |
| Multiple tool calls, API calls, or sequential steps | State scope and estimated effort upfront before starting |

A scope statement should be brief — one or two lines covering what will happen and roughly how long it will take:

> *"This will create 12 Jira tickets across ~15 API calls — may take a couple of minutes. Proceeding now."*

---

## 📊 Narrate progress for multi-step tasks

For tasks with multiple steps, report progress inline as work completes. After each meaningful milestone, output a brief status line:

> *"Created 4 of 12 tickets (33%)"*

This streams to the user in real time — no progress bar is needed.

---

## ⚠️ Warn before lengthy operations

If a request could result in a significantly long or expensive operation, warn the user before starting and confirm scope if there is any ambiguity:

> *"This will touch 18 files across 3 pipeline stages — confirming you want to proceed with all of them before I start."*
