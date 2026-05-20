# Template: planning_prep

Sprint planning prep ticket for the team.

---

## Fixed fields

| Field | Value |
|---|---|
| Project | `<PROJECT_KEY>` |
| Issue type | `Story` |
| Assignee | `<ASSIGNEE_ACCOUNT_ID>` |
| Story points (`customfield_10028`) | `0.5` |
| Priority | `Medium` |
| Labels | `["<TEAM_LABEL>"]` |

---

## Variable fields (per ticket)

| Field | Value |
|---|---|
| Title | `Team — Sprint N planning prep` |
| Sprint (`customfield_10020`) | Sprint N-1 ID (plain integer — see sprint ID reference below) |
| Components | Derived from sprint number — see quarter mapping below |
| Parent epic | Derived from sprint number — see quarter mapping below |

---

## Quarter mapping

Map the sprint number (N) to the correct component IDs and parent epic. Component IDs and epic IDs are year-specific — verify before use.

| Sprints | Components | Parent epic |
|---|---|---|
| `<SPRINT_RANGE_1>` | `<COMPONENT_ID_1>`, `<COMPONENT_ID_2>` | `<EPIC_ID_1>` |
| `<SPRINT_RANGE_2>` | `<COMPONENT_ID_1>`, `<COMPONENT_ID_3>` | `<EPIC_ID_2>` |

---

## Sprint ID reference

Sprint IDs for board `<BOARD_ID>` follow a sequential pattern. Look up the sprint ID via JQL:

```
project = <PROJECT_KEY> AND sprint = "<SPRINT_NAME>"
```

Read `customfield_10020[0].id` from any matching ticket. After resolving the ID, record the new sprint → ID mapping so future runs do not need to re-query Jira.

---

## Description structure

Intro paragraph + bullet points + Acceptance criteria heading + AC bullets. Substitute sprint number N and N-1:

> Sprint planning prep for Sprint N.
>
> * Review roadmap priorities
> * Assess what's complete, in-flight, and outstanding from Sprint N-1
> * Confirm availability/capacity for the team
> * Identify and size Sprint N candidates for the team
>
> ### Acceptance criteria
>
> * Availability/capacity confirmed for the team for Sprint N
> * Sprint N backlog finalised and tickets moved into sprint in Jira

---

## Business value field (`customfield_10650`)

One-sentence business value statement followed by an Impact Rating block:

> Ensures Sprint N is well-prepared, with capacity confirmed, priorities aligned, and the backlog ready to execute.
>
> **Impact Rating** (per team prioritisation framework):
> a. Prioritization Matrix: `<LINK_TO_MATRIX>`
> b. Priority Value Driver: Operational Efficiency – Score: < TODO >
> c. Secondary Value Driver: Customer Value – Score: < TODO >
> d. Calculated Score: < TODO >

Leave `< TODO >` placeholders in place — these are completed manually after the scoring session.
