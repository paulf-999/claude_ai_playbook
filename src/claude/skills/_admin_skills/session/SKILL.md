---
name: session
description: "Save the current session under a short name for later resumption, or resume a previously saved session. Usage: /session to save, /session <name> to resume."
version: 0.1.0
maturity: draft
tags:
  criticality: should
  status: active
  tested: false
tools: Read, Write, Bash
---

## Scope gate

This skill is at **draft** maturity. Claude behaviour is constrained accordingly:

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

Determine the mode from the argument passed:

- **No argument** (`/session`) → save mode
- **Name provided** (`/session <name>`) → resume mode

---

## Save mode

### Step 1 — Propose name options

Generate 5 short session name options based on what has happened in this session. Rules:
- Kebab-case (`word-word`)
- 2–3 words maximum
- Easy and quick to type — no long words
- Descriptive enough to recognise weeks later

Present as a numbered list and wait for the user to pick:

```
1. <option>
2. <option>
3. <option>
4. <option>
5. <option>
```

### Step 2 — Save the session

Create `~/.claude/sessions/<chosen-name>.md` with:

```markdown
---
name: <chosen-name>
date: <YYYY-MM-DD>
project: <current working directory>
---

## Context

<2–4 sentence summary of what this session covered and current status>

## State

<bullet points of key decisions, blockers, or next steps>
```

### Step 3 — Confirm

Output exactly:

> "Saved as **`<name>`**. To resume: start a new Claude session and run `/session <name>`"

---

## Resume mode

### Step 1 — Read the session file

Read `~/.claude/sessions/<name>.md`. If the file does not exist, tell the user:

> "No session found named `<name>`. Run `ls ~/.claude/sessions/` to see what's available."

Stop here if missing.

### Step 2 — Brief the user

Output:

> **Resuming `<name>`** — saved <date>, project: <project>
>
> <Context summary from the file>
>
> **State:**
> <bullet points from the file>

Then ask:

> "Ready to continue. What would you like to do next?"
