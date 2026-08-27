# 📅 Sprint Planning

Sprint ID mapping, quarter-to-component mapping, parent epic references, and capacity conventions for the DM project (board 217).

---

## 🔢 Sprint ID mapping (board 217)

| Sprint | ID | Sprint | ID |
|---|---|---|---|
| 61 | 15560 | 67 | 15566 |
| 62 | 15561 | 68 | 15567 |
| 63 | 15562 | 69 | 15568 |
| 64 | 15563 | 70 | 15569 |
| 65 | 15564 | 71 | 15570 |
| 66 | 15565 | | |

Sprint IDs increment by 1 per sprint. For sprints beyond the table, extrapolate from the last known value or confirm via `searchJiraIssuesUsingJql`.

---

## 📦 Quarter component mapping (2026)

| Quarter | Component name | Component ID | Sprints |
|---|---|---|---|
| Q2 | `Data Platform Initiatives 2026 Q2` | `13444` | 63–65 |
| Q3 | `Data Platform Initiatives 2026 Q3` | `13445` | 66–69 |
| Q4 | `Data Platform Initiatives 2026 Q4` | `13446` | 70–73 |

Always combine the quarter component with the year-level component `Data Platform Initiatives 2026` (ID `13377`). Every ticket requires both.

---

## 🏆 Parent epics (2026)

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
