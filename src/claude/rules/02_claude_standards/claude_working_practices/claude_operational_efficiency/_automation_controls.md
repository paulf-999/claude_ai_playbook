<!-- version: 1.2.2 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-26 -->
# ⚙️ Automation Controls

**Purpose:** Establish guardrails for experimental automation features (`/loop`, `/batch`, `/goal`) to prevent runaway sessions, excessive token usage, and unintended side effects.

- **Why:** automation features are powerful but risky, so these rules protect against costly mistakes.
- **Turn caps for other non-interactive runs:** see [_turn_budgets.md](_turn_budgets.md).

## 📋 Contents

- [🚀 `/loop` — Repeat on schedule](#-loop-repeat-on-schedule)
- [🎯 `/goal` — Work until condition met](#-goal-work-until-condition-met)
- [🔀 `/batch` — Parallel subagents](#-batch-parallel-subagents)
- [🛑 Kill-switch procedures](#-kill-switch-procedures)
- [🔍 Permission gates](#-permission-gates)
- [🩺 Troubleshooting](#-troubleshooting)

---

## 🚀 `/loop` — Repeat on schedule

Run a prompt or command repeatedly at a fixed interval (e.g., poll for deploy status every 5 minutes).

- **Minimum interval:** 5 minutes, with nothing shorter allowed
  - **Why:** shorter intervals hammer endpoints and waste tokens on overhead
- **Default interval:** 10 minutes (conservative baseline)
- **Turn budget:** stop after 10 turns per iteration by default; higher requires explicit approval
- **Max runtime:** 2 hours before manual re-approval required
- **Termination:** use `TaskStop` to kill
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
- **Turn budget:** stop after 20 turns by default if the condition isn't met; higher requires explicit approval
- **Pair with auto mode:** run `/goal` under auto mode so it doesn't stop for clarifying questions mid-iteration
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
2. **Investigate first:** don't restart until you know what went wrong
3. **Check the transcript:** what was the agent doing? Where did it diverge?
4. **Narrow the scope:** reduce the batch size, tighten the goal condition, or extend the `/loop` interval
5. **Verify before restarting:** confirm the new spec won't repeat the same issue

---

## 🔍 Permission gates

- **Explicit invocation required:** all three features (`/loop`, `/batch`, `/goal`) require explicit invocation — no auto-triggering
- **Complete specification upfront:** each invocation must include the full specification (interval, condition, item list)
- **No ambiguous specs:** "work until satisfied" is not allowed — surface and clarify before proceeding

---

## 🩺 Troubleshooting

- **Read on demand:** `~/.claude/_rules_lazy_load/claude_config/automation_troubleshooting.md` — when a run misbehaves, or before choosing between `/loop`, `/goal` and `/batch`, for recovery steps, a decision tree and a pre-flight checklist.
