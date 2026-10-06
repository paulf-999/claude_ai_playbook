<!-- version: 2.0.0 -->
<!-- created: 2026-05-20 -->
<!-- updated: 2026-10-06 -->
# 📋 Field Standards

Required fields, default values, custom fields, component conventions, label rules, and the business value field format. Your project's field IDs, components and label live in the Jira values in `~/.claude/_rules/05_lazy_load/org.md`.

## 📋 Contents

- [✅ Required fields](#-required-fields)
- [🔧 Custom fields](#-custom-fields)
- [🏷️ Labels](#-labels)
- [📦 Components](#-components)
- [💼 Business value field](#-business-value-field)

---

## ✅ Required fields

Every ticket must have the following fields set before it enters a sprint:

| Field | Required | Default | Notes |
|---|---|---|---|
| Summary | Yes | — | See naming convention in `ticket_conventions.md` |
| Description | Yes | — | Two-section format: intro bullets + acceptance criteria |
| Priority | Yes | **Medium** | Deviate only with explicit justification |
| Story points | Yes | — | Must be > 0 |
| Sprint | Yes | — | Integer sprint ID — see `sprint_planning.md` |
| Assignee | Yes | — | Must be set before sprint entry |
| Components | Yes | — | The components `org.md` lists as required |
| Parent epic | Yes | — | Set to the relevant planning or initiative epic |
| Status | Yes | **Backlog** | Triage is a hygiene failure — transition to Backlog immediately |
| Business Value | Yes | — | Must follow format and scoring convention — see [`business_value.md`](business_value.md) |

---

## 🔧 Custom fields

Story points, Sprint and Business value are custom fields, and their `customfield_<n>` IDs differ between Jira sites.

| Field | Type | Notes |
|---|---|---|
| Story points | Number | Decimal allowed (e.g. `0.5`) |
| Sprint | Integer | Sprint ID, not the sprint number — see `sprint_planning.md` |
| Business value | ADF document | See format below |

- **IDs:** take each field's ID from `org.md`.
- **Unknown ID:** if the table there is still a placeholder, look the field up with `getJiraIssueTypeMetaWithFields` rather than guessing.

---

## 🏷️ Labels

- The Claude-created label named in `org.md` — **required** on all tickets created by Claude; enables hygiene check filtering and auditability
- Additional labels may be added where useful; no other standard labels are currently defined

---

## 📦 Components

- **Which ones:** apply the components `org.md` lists as required on every ticket.
- **Quarter component:** where your project uses one, derive it from the ticket's sprint — see `sprint_planning.md`.

---

## 💼 Business value field

See [`business_value.md`](business_value.md) for the full format, audience guidance, scoring framework, and worked example.
