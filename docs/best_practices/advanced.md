# 🏆 Advanced

Practices for users running Claude regularly who want sessions to start fast, finish clean, and scale across workstreams.

| Practice | Source | Description | Example |
|---|---|---|---|
| 🔀 Run sessions in parallel | Anthropic | Writer + reviewer pattern for independent critique, or parallel workstreams on isolated branches. | [reviewer prompt + worktree commands](#parallel-sessions) |
| 🔄 Session continuity via `context.md` | Team | Manual handoff between sessions — deliberate, structured, distinct from auto-memory. | [`/wrap_up`](../../src/claude/commands/wrap_up.md) → [`context.md`](../../src/claude/context.md) — [how it works](#context-md-handoff) |
| 🚀 Structured session startup | Team | Remove the dependency on ad-hoc prompts — capture the sub-agent, task, and integration needs in a session input file before launching so the session starts correctly every time. | [`session_input.md`](../../src/claude/process/session_input.md) — [template](#startup-protocol) |

---

## 💻 Code examples

### 🔀 Parallel sessions

**Writer + Reviewer** — paste into a second Claude session once the writer has produced output:

```
You are a reviewer. The writer session is working on: [task description]

Review for:
- Correctness — logic errors, incorrect assumptions, broken dbt ref() calls
- Standards compliance — SQLFluff, naming conventions, DA_* audit fields present
- Completeness — anything missing from what was asked (e.g. missing dbt tests, missing limit_rows())

Group findings by severity: Blocking / Recommended / Optional.
Quote the relevant output and suggest the fix — don't just name the problem.
```

**Parallel workstreams with worktrees** — useful when developing two independent dbt features simultaneously without branch conflicts:

```bash
git worktree add ../dbtanalytics-feature-a feature/add_salesforce_mart
git worktree add ../dbtanalytics-feature-b feature/refactor_access_one_staging
# Open Claude in each worktree directory separately
```

---

### 🔄 `context.md` handoff

Auto-memory records what Claude learns about the codebase. [`context.md`](../../src/claude/context.md) records what *you* want the next session to know — decisions made, open questions, known issues.

At the end of a session, run [`/wrap_up`](../../src/claude/commands/wrap_up.md). Claude produces:

```
Project: dbt analytics — Salesforce mart model
What changed: Added mart_salesforce_opportunity_revenue; staging model updated to expose opportunity_stage
Decisions made: Materialised as table (not incremental) — row count is small enough
Open questions: Should closed_lost opportunities be excluded from the mart? Check with analytics team.
Known issues: DA_FILE_YEARMONTH not yet populated in staging_salesforce_opportunity — Airbyte doesn't provide it
```

Paste into `~/.claude/context.md`. The file is `@import`ed into every session via [`CLAUDE.md`](../../src/claude/CLAUDE.md) — the next session starts with the full picture of where things were left.

The paste is manual so you can edit or trim the summary before it becomes permanent context.

---

### 🔧 Startup protocol

Without a session input file, the sub-agent, task scope, and integrations are set through ad-hoc prompts — easy to forget, inconsistent across sessions. Pre-populating [`session_input.md`](../../src/claude/process/session_input.md) before launching captures all of this upfront. For example, to review a dbt PR with a focused tool agent:

```markdown
## Sub-agent
tools/dbt

## Task
Review the PR for the new staging models in prod_analytics/models/staging/salesforce/.
Check for: surrogate key on KEY, limit_rows() on all final SELECTs, DA_* audit fields, not_null + unique tests on KEY.
```

Claude runs this 5-step sequence automatically on launch:

| Step | What happens |
|---|---|
| 1. Sub-agent selection | Reads [`session_input.md`](../../src/claude/process/session_input.md) — loads the specified agent, or defaults to [`architect`](../../src/claude/agents/core/architect.md) |
| 2. Context load | Reads all imported context files and summarises project state for confirmation |
| 3. Task confirmation | Reads `## Task` from [`session_input.md`](../../src/claude/process/session_input.md) and confirms back — or asks if not specified |
| 4. MCP activation | Identifies which integration servers the task needs and explains how to update `deniedMcpServers` in `~/.claude/settings.json` |
| 5. Reviewer offer | Asks if you want a writer/reviewer session — outputs a ready-to-paste reviewer prompt if yes |

Without the protocol, sessions drift: wrong agent loaded, integrations forgotten, prior context lost. The protocol eliminates that overhead — the session is productive from the first message.
