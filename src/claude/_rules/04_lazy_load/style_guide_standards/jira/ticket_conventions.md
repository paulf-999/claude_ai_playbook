# 🎫 Ticket Conventions

Standards for summary naming, description structure, acceptance criteria format, and issue type usage across the DM Jira project.

## 📋 Contents

- [🏷️ Summary (title) naming](#-summary-title-naming)
- [📋 Description structure](#-description-structure)
- [🏗️ Issue types](#-issue-types)

---

## 🏷️ Summary (title) naming

- Format: `<Area> — <action or topic>` using an em-dash (—) separator
- Area: the team or domain the ticket belongs to (e.g. `Data Platform`)
- Action/topic: imperative or noun phrase describing the work — concise enough to parse at a glance in a backlog view

Examples:
- `Data Platform — Sprint 63 planning prep`
- `Data Platform — Claude AI playbook Jira style guide`

---

## 📋 Description structure

Every ticket body follows a **two-section structure**:

```
<1-sentence context line>

* <bullet>
* <bullet>
* <bullet>

### Acceptance criteria

* <outcome bullet>
* <outcome bullet>
```

**Rules:**
- Open with one sentence providing context — what this ticket is for and why
- Follow immediately with bullet points listing scope, tasks, or actions — no prose paragraphs
- Use a `### Acceptance criteria` H3 heading to separate the two sections
- Acceptance criteria are observable outcomes — specific, testable, written so it is clear when done
- No prose walls — every description must be scannable in under 10 seconds

**Canonical example (DM-38528):**

*Description:*

```
Sprint planning prep for Sprint 63.

* Review roadmap priorities
* Assess what's complete, in-flight, and outstanding from Sprint 62
* Confirm availability/capacity for myself and Imelda
* Identify and size Sprint 63 candidates for myself and Imelda
```

*Acceptance criteria:*

```
* Availability/capacity confirmed for myself and Imelda for Sprint 63
* Sprint 63 backlog finalised and tickets moved into sprint in Jira
```

---

## 🏗️ Issue types

| Type | When to use |
|---|---|
| **Story** | Any deliverable unit of work — a feature, task, or piece of analysis |
| **Epic** | A theme, programme, or multi-sprint initiative grouping related stories |

Use Stories for all day-to-day tickets. Reserve Epics for grouping related work across sprints. Every Story must have a parent Epic set.
