---
name: populate_jira_business_value
description: >
  Populate the Business Value Statement (customfield_10650) and CALC score
  (customfield_16845) on a Jira ticket hierarchy. Accepts a root ticket key
  and an optional exclusion list. Skips tickets that already have a valid,
  complete Business Value statement (contains Impact Rating block, no TODO
  placeholders, no legacy "AI GENERATED" format). Triggered by requests to
  "populate business value", "fill in BV statements", or similar Jira BV work.
version: 0.1.0
maturity: draft
tags:
  criticality: should
  status: active
  tested: true
tools:
  - mcp__claude_ai_Atlassian__getJiraIssue
  - mcp__claude_ai_Atlassian__searchJiraIssuesUsingJql
  - mcp__claude_ai_Atlassian__editJiraIssue
---

## Scope gate

This skill is at **draft** maturity — happy path only. Log unexpected states as notes; do not try to handle them inline.

---

## Required MCP server

This skill requires the **Atlassian** MCP server. If `mcp__claude_ai_Atlassian__*` tools are not visible, stop and tell the user:

> "The Atlassian MCP server is not active. Run `make enable_mcp server=atlassian` then restart Claude Code."

---

## Field reference

| Field | Jira ID | Type | Notes |
|---|---|---|---|
| Business Value Statement | `customfield_10650` | ADF document | Requires `contentFormat: "adf"` on every edit call |
| CALC score | `customfield_16845` | Number | Decimal — e.g. `0.75`, `1.50` |

**cloudId:** `payroc.atlassian.net`

---

## Phase 1 — Gather inputs

Ask in a single message:

> **1. Root ticket key**
> Which Jira ticket is the root of the hierarchy to process? (e.g. `DM-39006`)
>
> **2. Exclusions** *(optional)*
> Any ticket keys to exclude, along with all their descendants? (e.g. `DM-37182`)
>
> **3. Force overwrite?** *(optional, default: no)*
> Should tickets with an existing valid BV statement be overwritten? Default is to skip them.

---

## Phase 2 — Fetch the ticket hierarchy

Fetch the hierarchy top-down using JQL. Start from the root, then recurse through children:

```
parent = <KEY> ORDER BY created ASC
```

Repeat for each child level until no further children are found. Use `maxResults=50` per query.

Collect all ticket keys and summaries. Apply exclusions: remove any excluded key and all of its descendants from the working set.

State the scope before proceeding:

> "Found N tickets. Excluded M (DM-XXXXX and descendants). Processing N-M tickets."

---

## Phase 3 — Classify each ticket

Fetch `customfield_10650` and `customfield_16845` for each ticket (batch reads where possible — fetch fields per issue).

Classify each ticket as one of:

| Status | Criteria | Action |
|---|---|---|
| **Skip** | BV is populated, contains "Calculated Score", and contains no "TODO", "< TODO >", or "AI GENERATED" markers | Skip unless force overwrite is on |
| **Stale** | BV is populated but contains TODO placeholders or "AI GENERATED" header | Overwrite |
| **Missing** | BV field is empty or null | Populate |

Announce the tally:

> "N tickets to populate (M missing, K stale). P tickets already valid — skipping."

If all tickets are already valid and force is off, stop here and report done.

---

## Phase 4 — Score each ticket

For each ticket to populate, assess its nature and assign scoring.

### Framework selection

**Use the 7-category framework** when the ticket is primarily about platform reliability or operational continuity:
- Infrastructure or container work
- Dependency upgrades before deprecation / EOL
- Platform stability and BAU
- Preventing production outages or SLA breaches
- Airbyte / Airflow / environment provisioning

**Use the 6-category framework** for all other work:
- Feature delivery
- Planning prep and sprint ceremonies
- Process and engineering practice adoption
- Team admin and BAU coordination
- Analytics and reporting work

### 6-category framework (standard)

| Driver | Weight |
|---|---|
| Compliance & Risk | 25% |
| Transaction Integrity | 20% |
| Ops Efficiency | 15% |
| M&A Synergy | 15% |
| Exit Readiness | 15% |
| Customer Value | 10% |

**Scoring rubric:**
- [5] Critical / Immediate — regulatory fine imminent, transaction bug dropping >1% of volume, Due Diligence failure risk
- [3] Strategic / Important — schema mapping, automating 10+ hrs/week of manual work, new merchant data insight
- [1] Maintenance / Low Impact — minor tweaks, nice-to-have metadata, R&D with no clear ROI path

**Common patterns:**
- Planning prep / sprint ceremonies: Ops Efficiency 3 + M&A Synergy 1 → CALC = (3 × 0.15) + (1 × 0.15) = **0.60**
- Process / engineering adoption: Ops Efficiency 3 + M&A Synergy 1 → CALC = **0.60**

### 7-category framework (platform reliability)

| Driver | Weight |
|---|---|
| Compliance & Risk | 25% |
| Transaction Integrity | 20% |
| Platform Reliability & Technical Risk | 15% |
| Ops Efficiency | 15% |
| M&A Synergy | 10% |
| Exit Readiness | 10% |
| Customer Value | 5% |

**Scoring rubric for Platform Reliability & Technical Risk:**
- [5] Imminent production outage or SLA breach if not addressed
- [3] Critical dependency reaching end-of-life within the quarter
- [1] Technical debt reduction with no near-term operational risk

**Common patterns:**
- Platform stability / BAU: Platform Reliability 3 + Ops Efficiency 2 → CALC = (3 × 0.15) + (2 × 0.15) = **0.75**
- EOL dependency upgrade (e.g. Airflow 2.x): Platform Reliability 5 + Transaction Integrity 3 → CALC = (5 × 0.15) + (3 × 0.20) = **1.50**
- Airbyte / environment provisioning: Ops Efficiency 3 + Platform Reliability 2 → CALC = (3 × 0.15) + (2 × 0.15) = **0.75**

### CALC formula

Only the top 2 drivers are scored:

```
CALC = (primary score × primary weight) + (secondary score × secondary weight)
```

Round to 2 decimal places.

---

## Phase 5 — Confirm plan

Present a concise table for user approval before making any API calls:

```
Ticket    | Summary                          | Framework | Primary Driver         | Sec Driver        | CALC
DM-39006  | H&A Initiative H2                | 7-cat     | Platform Reliability 3 | Ops Efficiency 2  | 0.75
DM-38531  | Sprint 66 planning prep          | 6-cat     | Ops Efficiency 3       | M&A Synergy 1     | 0.60
...
```

Ask: "Does this scoring look correct? Confirm to proceed, or tell me what to adjust."

Do not proceed until the user confirms.

---

## Phase 6 — Batch update

Fire all `editJiraIssue` calls in a **single parallel batch** — do not serialise them.

Each call must include:
- `customfield_10650` — ADF document (see template below)
- `customfield_16845` — numeric CALC score
- `contentFormat: "adf"`

Do **not** include any other fields in the edit call — do not set Team, Sprint, or any other field.

### ADF document template

```json
{
  "version": 1,
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [{"type": "text", "text": "<1-sentence intro for a non-technical business audience>"}]
    },
    {
      "type": "bulletList",
      "content": [
        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "<bullet 1 — risk, context, or scope>"}]}]},
        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "<bullet 2>"}]}]},
        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "<bullet 3>"}]}]}
      ]
    },
    {
      "type": "paragraph",
      "content": [{"type": "text", "text": "Impact Rating (per Data Team Prioritization Framework):"}]
    },
    {
      "type": "bulletList",
      "content": [
        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "a. Prioritization Matrix: https://payroc.atlassian.net/wiki/x/k4DcRQE"}]}]},
        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "b. Priority Value Driver: <Driver> – Score: N"}]}]},
        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "c. Secondary Value Driver: <Driver> – Score: N"}]}]},
        {"type": "listItem", "content": [{"type": "paragraph", "content": [{"type": "text", "text": "d. Calculated Score: X.XX"}]}]}
      ]
    }
  ]
}
```

### Content rules

**Intro sentence:**
- Written for a non-technical business audience
- One sentence — what this ticket does and why it matters to the business
- No internal tool names (not: Airflow, dbt, Docker, PAT, GHCR). Describe by function instead (e.g. "automated data pipelines", "the software that orchestrates data processing", "containerised runtime environment")
- Named company-wide systems are acceptable (e.g. "GitHub Enterprise migration", "Salesforce")

**Three bullets:**
- Cover risk, context, and scope
- Concrete and specific to the ticket — not generic filler

**Impact Rating block:**
- Always present; always the last section
- Scores filled in from Phase 4 — no TODO placeholders

---

## Phase 7 — Report results

After all calls complete, output a summary:

```
Updated:  N tickets
Skipped:  N tickets (already valid)
Excluded: N tickets (DM-XXXXX and descendants)
Failed:   N tickets (list any that errored)
```

If any calls failed, list the ticket keys and suggest re-running for those individually.
