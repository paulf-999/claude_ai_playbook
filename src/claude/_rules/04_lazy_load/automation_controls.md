# ⚙️ Automation Controls

**Purpose:** Establish guardrails for experimental automation features (`/loop`, `/batch`, `/goal`) to prevent runaway sessions, excessive token usage, and unintended side effects.

Automation features are powerful but risky — these rules protect against costly mistakes.

## 📋 Contents

- [🚀 `/loop` — Repeat on schedule](#-loop-repeat-on-schedule)
- [🎯 `/goal` — Work until condition met](#-goal-work-until-condition-met)
- [🔀 `/batch` — Parallel subagents](#-batch-parallel-subagents)
- [🛑 Kill-switch procedures](#-kill-switch-procedures)
- [🔍 Permission gates](#-permission-gates)

---

## 🚀 `/loop` — Repeat on schedule

Run a prompt or command repeatedly at a fixed interval (e.g., poll for deploy status every 5 minutes).

- **Minimum interval:** 5 minutes (prevent hammering endpoints)
- **Default interval:** 10 minutes (conservative baseline)
- **Max runtime:** 2 hours before manual re-approval required
- **Termination:** use `TaskStop` or `/stop_loop` to kill
  - **Note:** always confirm the task is actually complete before stopping; don't interrupt mid-work

| Use for | Example | Don't use for |
|---------|---------|---------------|
| **Polling** | Check the deploy every 5 minutes | One-off tasks (single command is faster) |
| **Monitoring** | Keep running tests until they pass | Tasks needing human judgment each iteration |
| **Watching** | Alert me when X completes | Unbounded exploration (use `/goal` instead) |

---

## 🎯 `/goal` — Work until condition met

Work in a loop until a verifiable condition is satisfied. The condition gates all iterations.

- **Define success upfront:** explicit, measurable condition required before starting
  - **Example:** "Run tests until all pass" or "Code coverage reaches 90%"
- **Turn budget:** capped at 20 turns by default; higher requires explicit approval
- **Fallback condition:** stop and report if no progress after 3 consecutive iterations
- **Timeout:** stop and hand off if total runtime exceeds 30 minutes

| Use for | Example | Don't use for |
|---------|---------|---------------|
| **Verifiable goals** | Implement feature until QA sign-off | Exploration ("let's see what happens") |
| **Measurable targets** | Refactor until code coverage reaches 90% | Open-ended improvement ("make it better") |
| **Test-driven work** | Run tests until all pass | External dependencies (use `/loop` instead) |

---

## 🔀 `/batch` — Parallel subagents

Decompose a large change into isolated parallel subagents, each opening a PR.

- **Item limit:** max 12 items per batch (prevent overwhelming the agent queue)
- **Scope:** each item is a complete, independent unit (one concern per PR)
- **PR limit:** each subagent opens exactly one PR (no multi-PR agents)
- **Approval:** user must confirm the batch specification before agents start
- **Monitoring:** show progress as agents complete

| Use for | Example | Don't use for |
|---------|---------|---------------|
| **Large refactoring** | Migrate 10 microservices to new config format | Changes <5 items (single agent faster) |
| **Bulk creation** | Create tickets for 8 unrelated bugs | Interdependent work (items aren't independent) |
| **Parallel exploration** | Try 3 different implementations, let them race | Tasks requiring human judgment per item |

---

## 🛑 Kill-switch procedures

If a looping automation is consuming tokens too quickly or behaving unexpectedly:

1. **Stop immediately:** `TaskStop` or close Claude Code
2. **Don't restart** without investigating
3. **Check the transcript:** what was the agent doing? Where did it diverge?
4. **Narrow the scope:** reduce the batch size, tighten the goal condition, or extend the `/loop` interval
5. **Verify before restarting:** confirm the new spec won't repeat the same issue

---

## 🔍 Permission gates

- **Explicit invocation required:** all three features (`/loop`, `/batch`, `/goal`) require explicit invocation — no auto-triggering
- **Complete specification upfront:** each invocation must include the full specification (interval, condition, item list)
- **No ambiguous specs:** "work until satisfied" is not allowed — surface and clarify before proceeding

---

## 📊 Common Failure Scenarios & Recovery

### `/loop` runaway

**Symptom:** Loop fires every 5m for 2+ hours, accumulating tokens

**Recovery:**
1. Stop immediately: `TaskStop`
2. Extend interval: was 5m → try 15m
3. Clarify condition: is the endpoint responding? Is the logic sound?
4. Restart: approve new interval explicitly

### `/goal` never converges

**Symptom:** 20+ turns, condition never met, tokens wasted

**Recovery:**
1. Check transcript: is the agent actually making progress?
2. Verify condition: is it achievable? Is it measurable?
3. Fallback to `/loop`: if the goal is unbounded, use `/loop` instead with a timeout
4. Narrow scope: smaller changes converge faster

### `/batch` conflicts

**Symptom:** Subagents clash on shared files, PRs conflict

**Recovery:**
1. Stop batch: kill remaining agents
2. Split items: ensure each PR touches disjoint files
3. Sequence manually: do 3 items in sequence instead of 12 parallel
4. Review PR merging order: must merge in dependency order

---

## 🎯 Decision Tree: Which Automation?

```
Need something done repeatedly on a schedule?
├─ YES → Use /loop (e.g., "check deploy every 5m")
│
Need something done once, but iteratively until a condition?
├─ YES → Use /goal (e.g., "implement until tests pass")
│
Need to do the same change 10+ times in parallel?
├─ YES → Use /batch (e.g., "migrate 12 microservices")
│
Otherwise → Manual invocation (faster, clearer)
```

---

## 📚 Related Rules

- **claude_efficiency.md** — When NOT to spawn subagents; when /batch is overkill
- **behaviour.md** — Ask-first gates for risky operations
- **testing.md** — How to verify automation-generated code

---

## ✅ Verification Checklist

Before invoking any automation feature:

- [ ] Condition/goal/interval is explicit and measurable
- [ ] Success criteria are defined upfront
- [ ] Kill-switch procedure is clear
- [ ] Side effects are understood and acceptable
- [ ] Token budget is estimated and acceptable
- [ ] Manual alternative was considered and rejected
