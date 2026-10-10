<!-- version: 2.0.1 -->
<!-- created: 2026-05-20 -->
<!-- updated: 2026-10-06 -->
# 📅 Sprint Planning

Sprint IDs, quarter-to-component mapping, parent epic references, and capacity conventions. Your project's board, sprint IDs and component IDs live in the Jira values in `~/.claude/_rules_lazy_load/org.md`.

## 📋 Contents

- [🔢 Sprint IDs](#-sprint-ids)
- [📦 Quarter components](#-quarter-components)
- [🏆 Parent epics](#-parent-epics)
- [⚖️ Capacity conventions](#-capacity-conventions)
- [🔄 Sprint assignment rule](#-sprint-assignment-rule)

---

## 🔢 Sprint IDs

The Sprint field takes Jira's internal sprint ID, not the sprint number shown on the board.

- Look the ID up in the sprint table in `org.md`.
- Sprint IDs usually increment by 1 per sprint, so extrapolate from the last known value for a sprint beyond the table.
- Confirm an extrapolated ID via `searchJiraIssuesUsingJql` before using it.

---

## 📦 Quarter components

If your project tags tickets by quarter, derive the quarter component from the sprint the ticket is assigned to.

- Take the component names and IDs from the components table in `org.md`.
- Combine the quarter component with any year-level component that table lists as required on every ticket.

---

## 🏆 Parent epics

Parent epics are **initiative-specific** — there is no single shared planning epic to default to. Select the parent epic based on the work being done:

- For feature or delivery work: use the relevant initiative or project epic
- For planning prep or admin work: use the assignee's own planning epic — ask the user to provide it, do not assume

Confirm the epic ID via `getJiraIssue` before setting the parent. Do not hardcode or default to a personal planning epic.

---

## ⚖️ Capacity conventions

- **Admin/overhead tasks** (planning prep, ceremonies, BAU): minimum **0.5 story points**
- **Standard feature stories**: size using the team's agreed scale — `1`, `2`, `3`, `5`, `8`, `13`
- Story points must be set before a ticket enters the sprint — `0` is a hygiene failure

---

## 🔄 Sprint assignment rule

Assign a ticket to the sprint in which the **work will be done**.

Exception: planning prep tickets are assigned to the **current sprint** (the sprint running at the time of creation), since the prep occurs before the next sprint begins.
