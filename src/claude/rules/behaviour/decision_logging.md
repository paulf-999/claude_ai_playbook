# 🗂️ Rules — Decision Logging

A `decision` memory type for capturing non-obvious choices that future sessions should know about. Claude logs these **proactively** — no explicit invocation required.

---

## Grain test — both must be true to log

1. A meaningful choice was made between two or more viable alternatives
2. The rationale wouldn't be recoverable from reading the resulting code, config, or commit message

A useful self-check: *"Would a future session Claude, without this memory, likely make a different (worse) call?"* If yes, log it. If the code or context makes the answer obvious, don't.

**Examples:**

| Log? | Decision | Why |
|---|---|---|
| ✓ | Chose MCP memory over file-based storage for the todos skill | File-based loses cross-session portability — not obvious from the implementation |
| ✓ | Decided not to use `make install` to sync playbook changes | `make install` overwrites personal `~/.claude/` content — a non-obvious footgun |
| ✗ | Used `for_each` over `count` for Terraform resources | Already the house standard — explained by the style guide |
| ✗ | Added `set -e` to a new Bash script | Required by the Bash standards — obvious from the rules |

---

## When NOT to log

- The choice was the obvious default — no real alternative existed
- Code, comments, or the commit message already explain the why
- It's a behavioural correction to Claude → belongs in `feedback`
- It's project state (sprint, tickets, open work) → belongs in `project`
- The decision is ephemeral and won't influence future work
- The user documented it themselves (plan, ADR, Confluence page)

---

## Memory format

```markdown
---
name: <title>
description: <one-line summary>
type: decision
date: YYYY-MM-DD
project: <project name or "global">
status: active
---

<The decision in one sentence.>

**Why:** <1–2 sentences — what made this the right call>
**Scope:** <where this applies — specific project, or globally>
```

---

## Memory filing

| Decision scope | Path |
|---|---|
| Specific to one project | `~/.claude/projects/<project>/memory/decision_*.md` |
| Cross-project convention | `~/.claude/memory/decision_*.md` |

Always add a pointer entry to the relevant `MEMORY.md` index.

---

## Publishing to the repo

Project-level decisions that are relevant to contributors are also written to the repo as a lightweight decision file. Personal workflow preferences and cross-project Claude conventions stay in `~/.claude/memory/` only.

**Publish to the repo when** the decision:
- Establishes a lasting convention that contributors need to follow
- Records why a significant architecture, tooling, or approach choice was made
- Would be useful for a new contributor to understand the project's current state

**Do not publish to the repo when** the decision:
- Is a personal workflow preference (how the user works with Claude)
- Is a cross-project Claude convention (global memory only)
- Is already captured in a PR description, plan, ADR, or Confluence page

### Repo location

```
docs/decisions/<theme>/YYYY-MM-DD_<keyword>.md
```

Theme aligns to the area of the stack the decision concerns:

| Theme | Covers |
|---|---|
| `dbt` | Models, macros, testing, snapshots |
| `cicd` | Pipelines, deployment, PR gates |
| `airflow` | DAGs, operators, scheduling |
| `infrastructure` | Terraform, Ansible, Docker, VMs |
| `data_platform` | Architecture, source systems, ingestion |
| `skills` | Claude skill authoring, playbook conventions |
| `process` | Team workflows, session conventions |
| `tooling` | CLI tools, dependencies, package management |
| `general` | Cross-cutting concerns, repo structure, contributor conventions — use when no other theme fits |

If a decision spans two themes, use the one it primarily concerns.

### Repo file format

```markdown
# <title>
**Date:** YYYY-MM-DD
**Status:** active

<Decision in 1–2 sentences.>

**Rationale:** <2–3 sentences — why this was the right call>
```

No alternatives table, no consequences section. Rationale must be substantive enough to explain the why — a decision with no rationale restates git history without adding value.

### Commit behaviour

Claude creates the file and stages it automatically. It is committed alongside the changes that prompted the decision — not as a standalone commit.

---

## Superseding a decision

When a decision is overturned:

**Memory file:** `status: active` → `status: superseded`. Add `**Superseded by:** <new decision title>`. Annotate the `MEMORY.md` pointer as superseded. Do not delete the file.

**Repo file:** Update `**Status:** active` → `**Status:** superseded`. Add `**Superseded by:** <new decision title>`. Commit the update alongside the change that prompted it.
