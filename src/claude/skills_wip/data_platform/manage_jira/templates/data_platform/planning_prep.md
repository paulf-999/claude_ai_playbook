# Template: planning_prep

Sprint planning prep ticket for the Data Platform team. Modelled on DM-37980.

---

## Fixed fields

| Field | Value |
|---|---|
| Project | `DM` |
| Issue type | `Story` |
| Assignee | `638fb4828fd2d2d5f13226cf` (Paul Fry) |
| Story points (`customfield_10028`) | `0.5` |
| Priority | `Medium` |
| Labels | `["dm-claude-created"]` |

---

## Variable fields (per ticket)

| Field | Value |
|---|---|
| Title | `Data Platform — Sprint N planning prep` |
| Sprint (`customfield_10020`) | Sprint N-1 ID (plain integer — see sprint ID reference below) |
| Components | Derived from sprint number — see quarter mapping below |
| Parent epic | Derived from sprint number — see quarter mapping below |

---

## Quarter mapping

Map the sprint number (N) to the correct component IDs and parent epic:

| Sprints | Components | Parent epic |
|---|---|---|
| 63–65 (H1) | `13377`, `13444` | `444372` |
| 66–69 (H2 Q3) | `13377`, `13445` | `495840` |
| 70–73 (H2 Q4) | `13377`, `13446` | `495840` |

> ⚠️ Component IDs and epic IDs are year-specific. Verify before use — these reflect 2026 H1/H2 values.

---

## Sprint ID reference

Sprint IDs for board 217 (DM board) follow a sequential pattern. Known IDs:

| Sprint | ID |
|---|---|
| 61 | 15560 |
| 62 | 15561 |
| 63 | 15562 |
| 64 | 15563 |
| 65 | 15564 |
| 66 | 15565 |
| 67 | 15566 |
| 68 | 15567 |
| 69 | 15568 |
| 70 | 15569 |
| 71 | 15570 |

To assign a ticket to sprint N-1, use the ID from this table. If the target sprint is not listed, look it up via JQL: `project = DM AND sprint = "DM Sprint <number>"` and read `customfield_10020[0].id` from any matching ticket.

---

## Description structure

Intro paragraph + 4 bullet points + Acceptance criteria heading + 2 AC bullets. Substitute sprint number N and N-1:

> Sprint planning prep for Sprint N.
>
> * Review roadmap priorities
> * Assess what's complete, in-flight, and outstanding from Sprint N-1
> * Confirm availability/capacity for myself and Imelda
> * Identify and size Sprint N candidates for myself and Imelda
>
> ### Acceptance criteria
>
> * Availability/capacity confirmed for myself and Imelda for Sprint N
> * Sprint N backlog finalised and tickets moved into sprint in Jira

---

## Business value field (`customfield_10650`)

One-sentence business value statement followed by an Impact Rating block:

> Ensures Sprint N is well-prepared, with capacity confirmed, priorities aligned, and the backlog ready to execute.
>
> **Impact Rating** (per Data Team Prioritization Framework):
> a. Prioritization Matrix: [https://payroc.atlassian.net/wiki/x/k4DcRQE]
> b. Priority Value Driver: Operational Efficiency – Score: < TODO >
> c. Secondary Value Driver: Customer Value – Score: < TODO >
> d. Calculated Score: < TODO >

Leave `< TODO >` placeholders in place — these are completed manually after the scoring session.
