# Session

## At the start of every session

**Step 1 — Sub-agent**

Read `~/.claude/process/session_input.md`. If the `## Sub-agent` section contains a non-comment value, use it and state which agent was selected. Otherwise, default to `architect` and inform the user:

> "No sub-agent specified — defaulting to **architect** (senior analytics architect; full data stack, hands-on + design).
>
> **Custom sub-agents — core:**
> - `architect` *(default)* — end-to-end analytics architecture, hands-on across the full stack
> - `project_manager` — planning, stakeholder comms, sprint/backlog work
> - `technical_writer` — docs, READMEs, runbooks, ADRs, Confluence pages
>
> **Custom sub-agents — utility:**
> - `utility/code_reviewer` — holistic code review across all files (standards, security, test coverage)
> - `utility/debugger` — systematic root-cause debugging
>
> **Custom sub-agents — ops:**
> - `ops/new_user` — simulates a first-time user; use for onboarding validation
> - `ops/claude_reviewer` — reviews Claude configuration artefacts against best practices
> - `ops/mac_user` — reviews shell scripts for macOS compatibility (bash 3.2, BSD coreutils)
>
> **Custom sub-agents — tools** (focused work or automated code review per technology):
> - `tools/python`, `tools/sql`, `tools/unix`, `tools/makefile`, `tools/dbt`, `tools/docker`, `tools/cicd`, `tools/ansible`, `tools/airflow`, `tools/terraform`
>
> **Built-in Claude Code agents:**
> - `general-purpose` — research, multi-step tasks, code search
> - `explore` — fast read-only codebase exploration
>
> To switch, specify one in `~/.claude/process/session_input.md` before the next session, or tell me now."

**Step 2 — Context**
Read all imported context files. Summarise the current project context in 2-3 sentences so I can confirm you have loaded it correctly.

**Step 3 — Task**
Read `~/.claude/process/session_input.md`. If the `## Task` section contains a non-comment value, read it and confirm back to me: "I'll be working on: ..." Wait for my confirmation before proceeding. Otherwise, prompt: "What is the task for this session?" and wait for my response before doing anything.

**Step 4 — MCP servers**
Integration MCP servers (GitHub, Atlassian, Microsoft_365, omni) are disabled by default. Based on the confirmed task, state which integrations are needed and prompt:

> "This task will need: [list]. Run `make enable_mcp server=<name>` for each, then restart Claude Code. Core servers (context7, memory, filesystem, sequential-thinking) are always active."

Skip this step if the task requires no external integrations.

**Step 5 — Reviewer session (optional)**
Once the task is confirmed, ask: "Would you like to set up a writer/reviewer session? I'll act as the writer. You can open a second Claude session and paste the reviewer prompt below to have it independently critique my output."

If the user says yes, output the following prompt — replacing `[task]` with the confirmed task description:

---
*Reviewer prompt (paste into a second Claude session):*

```
You are a reviewer. The writer session is working on: [task]

Your role is to independently critique the writer's output. Do not produce new output yourself.

Review for:
- Correctness — logic errors, incorrect assumptions, broken references
- Standards compliance — style guides, naming conventions, security rules
- Completeness — anything missing or not addressed by the task
- Clarity — anything ambiguous or likely to cause confusion

Group findings by severity:
- Blocking — must be fixed before the work is accepted
- Recommended — should be fixed but not a blocker
- Optional — minor suggestions

Be specific: quote the relevant output and explain the issue. Where possible, suggest the fix.
```
---

If the user says no, proceed without a reviewer session.

---

## After making changes

Once changes have been made, before moving on to the next task, prompt the user to verify:

- **Code changes** — "Please run `make test` (or the relevant test command) and review the diff before we continue."
- **SQL / dbt changes** — "Please spot-check the output: row counts, nulls, and grain look as expected?"
- **Config or process file changes** — "Does this match your intent? Worth a quick read before we move on."

Do not consider a task complete until the user has confirmed the output is correct.

---

## At the end of a session

When I say "wrap up", first run `/revise-claude-md` to capture any session learnings into CLAUDE.md. Then prompt:

> "Disable any MCPs enabled for this session? Run `make disable_mcp server=<name>` for each, then restart Claude Code."

Then produce a context update in this format:

**Project:** ...
**What changed:** ...
**Decisions made:** ...
**Open questions:** ...
**Known issues:** ...
**Pruning candidates:** Rules in CLAUDE.md that appeared redundant, were never relevant this session, or duplicate what a tool already enforces. Leave blank if none.

I will paste this into `context.md`.
