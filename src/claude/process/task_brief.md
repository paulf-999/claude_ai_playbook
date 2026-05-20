# 📋 Task Brief Convention

Defines the file format for handing work off from the orchestrator (main session) to a sub-agent, and for receiving structured output back. Using this pattern keeps the main session context lean — the sub-agent does the heavy lifting in an isolated context that terminates when done.

---

## When to use

Apply the task brief pattern automatically — without waiting to be asked — when the task involves any of:
- Reading more than 3 files
- Editing files across more than one directory
- A search → edit cycle

These thresholds reflect the point at which sub-agent context isolation outweighs spawn overhead — below them, delegating costs more than it saves.

Do not use for: single-file edits, quick lookups, or anything trivially short.

---

## Sub-agent selection

Map the task domain to the appropriate sub-agent:

| Domain | Sub-agent |
|---|---|
| dbt / SQL | `tools/dbt` or `tools/sql` |
| Python | `tools/python` |
| Airflow / DAGs | `tools/airflow` |
| Terraform | `tools/terraform` |
| Docker | `tools/docker` |
| CI/CD | `tools/cicd` |
| Shell / Make | `tools/unix` or `tools/makefile` |
| Multi-domain or unclear | `general-purpose` |

---

## Task brief template

**Location:** `/tmp/task_brief_<slug>.md` (slug = 2–3 word description, e.g. `dbt_model_review`)

```markdown
## Objective
<One sentence: what must be accomplished.>

## Inputs
<File paths only — not content. The sub-agent will read them.>
- path/to/file1
- path/to/file2

## Constraints
<Scope limits, style guides to apply, things to avoid.>
- Apply style guide: ~/.claude/style_guide_standards/<name>.md
- Do not modify files outside the listed paths

## Output spec
Write results to: /tmp/task_output_<slug>.md
Follow the output summary format below exactly.

## Done when
<Observable completion criteria — how the sub-agent knows it is finished.>
- All listed files reviewed
- Output summary written to the specified path
```

---

## Output summary template

**Location:** `/tmp/task_output_<slug>.md`

```markdown
## Status
completed | partial | failed

## Summary
- <bullet: what was done>
- <bullet: key finding or change>
- <bullet: any notable decision made>

## Artefacts
<Paths of files created or modified. Empty if none.>
- path/to/modified/file

## Errors
<Anything the orchestrator needs to act on. Empty if none.>
```

---

## Orchestrator behaviour

1. Write the task brief to `/tmp/task_brief_<slug>.md`
2. Spawn the sub-agent via the `Agent` tool — pass the brief path in the prompt, not the file contents
3. When the sub-agent returns, read `/tmp/task_output_<slug>.md` — **one Read call only**
4. Do not re-read any file the sub-agent already processed
5. Surface the summary to the user; ask for next steps if needed
