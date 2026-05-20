# 📋 Field Standards

Required fields, default values, custom field IDs, component conventions, label rules, and the business value field format.

---

## ✅ Required fields

Every ticket must have the following fields set before it enters a sprint:

| Field | Required | Default | Notes |
|---|---|---|---|
| Summary | Yes | — | See naming convention in `ticket_conventions.md` |
| Description | Yes | — | Two-section format: intro bullets + acceptance criteria |
| Priority | Yes | **Medium** | Deviate only with explicit justification |
| Story points | Yes | — | Must be > 0; field `customfield_10028` |
| Sprint | Yes | — | Integer sprint ID; field `customfield_10020` |
| Assignee | Yes | — | Must be set before sprint entry |
| Components | Yes | — | Always exactly 2 — see component conventions below |
| Parent epic | Yes | — | Set to the relevant H1/H2 planning epic |
| Status | Yes | **Backlog** | Triage is a hygiene failure — transition to Backlog immediately |
| Business Value | Yes | — | Must follow format and scoring convention — see [`business_value.md`](business_value.md) |

---

## 🔧 Custom field IDs

| Field | Jira ID | Type | Notes |
|---|---|---|---|
| Story points | `customfield_10028` | Number | Decimal allowed (e.g. `0.5`) |
| Sprint | `customfield_10020` | Integer | Sprint ID from board 217 — see `sprint_planning.md` |
| Business value | `customfield_10650` | ADF document | See format below |

---

## 🏷️ Labels

- `dm-claude-created` — **required** on all tickets created by Claude; enables hygiene check filtering and auditability
- Additional labels may be added where useful; no other standard labels are currently defined

---

## 📦 Components

Every ticket must have exactly two components:

| Component | ID | When to use |
|---|---|---|
| `Data Platform Initiatives 2026` | `13377` | Always — applied to every ticket |
| `Data Platform Initiatives 2026 Q{N}` | See `sprint_planning.md` | Current quarter — derived from the sprint the ticket is assigned to |

The quarter component changes each quarter. See `sprint_planning.md` for the sprint-to-quarter-to-component-ID mapping.

---

## 💼 Business value field (`customfield_10650`)

See [`business_value.md`](business_value.md) for the full format, audience guidance, scoring framework, and worked example.
