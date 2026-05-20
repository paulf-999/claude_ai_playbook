---
name: audit_agents
description: Audit all Claude Code agents in ~/.claude/agents/ and produce a prioritised gap report. Use this skill whenever someone wants to check agent health, find missing guidance, surface tool mismatches, or identify quality issues across the agent ecosystem. Triggers on phrases like "audit my agents", "check agent quality", "what's wrong with my agents", "/audit_agents", "run the agent auditor", or "agent health check".
version: 0.2.0
maturity: draft
tags:
  criticality: should
  status: active
  tested: false
tools: Agent, Bash, Read, Edit, Glob
triggers:
  explicit:
    - /audit_agents
    - "audit my agents"
    - "check agent quality"
    - "run the agent auditor"
    - "agent health check"
  contextual:
    - user wants to surface quality issues or missing guidance across the Claude agent ecosystem
not_for:
  - reviewing a single agent (read the file directly instead)
  - making agent fixes without first seeing the gap report
output:
  type: conversational
  confirmation_required: false
---

## Scope gate

This skill is at **draft** maturity — happy path only. See [known_gaps.md](known_gaps.md) for open TODOs.

---

## Playbook repo path

The installed agents at `~/.claude/agents/` are copies managed by the playbook repo. The source of truth is:

```
~/github_repository/dmt-scripts-claude_ai_playbook/src/claude/agents/
```

Any fix applied only to `~/.claude/agents/` will be **overwritten** the next time `make install` runs. All fixes must be applied to both the installed copy and the corresponding repo source file.

### Path mapping

| Installed path | Repo source path |
|---|---|
| `~/.claude/agents/core/<name>.md` | `src/claude/agents/core/<name>.md` |
| `~/.claude/agents/utility/<name>.md` | `src/claude/agents/utility/<name>.md` |
| `~/.claude/agents/ops/<name>.md` | `src/claude/agents/ops/<name>.md` |
| `~/.claude/agents/tools/<name>.md` | `src/claude/agents/tools/<name>.md` |

If a repo source file does not exist for an installed agent, flag this to the user — fixes should still be applied to the installed copy but the agent should ideally be added to the repo.

---

## Phase 1 — Run the audit

Dispatch the `agent-auditor` agent via the Agent tool:

> "Audit all agent files in ~/.claude/agents/. Follow all agent-auditor instructions. Read every agent file in full before reporting. Produce the full structured gap report."

---

## Phase 2 — Present findings

After the agent returns its report, print it to the user in full.

Then summarise in one sentence: total agents audited, total findings, and the single highest-priority fix.

---

## Phase 3 — Offer to fix

Ask the user:

> "Would you like me to work through the High and Medium findings and apply fixes? I'll tackle them one at a time and confirm each change with you before applying. Each fix will be applied to both the installed agent and the playbook repo source file."

- If **no**: stop. The report is available above for manual action.
- If **yes**: see [fix_workflow.md](fix_workflow.md) for the step-by-step fix and commit sequence.
