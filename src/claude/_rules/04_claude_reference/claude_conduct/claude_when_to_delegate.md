# 🤝 Claude When to Delegate

**Purpose:** Establish decision criteria for when Claude should handle a task directly vs. delegate to the user or spawn a sub-agent, reducing turns and context bloat while preserving reasoning capability.

---

## 🎯 Core principle

**Delegation preserves context.** Each action (Bash tool call, sub-agent spawn) consumes turns and grows context. Before acting, assess: Can the user do this? Can a sub-agent handle this independently? If so, delegate instead of handling directly.

---

## 📋 Contents

- [Delegating to user](#-delegating-to-user) — bash execution decisions
- [Delegating to sub-agent](#-delegating-to-sub-agent) — sub-agent spawning decisions

---

## 👤 Delegating to User

### Decision framework

**Before running Bash commands, check in order:**

| Criterion | If YES | If NO |
|---|---|---|
| **Output gates the next step?** | Run in Claude (need to parse) | → Offer user self-execution |
| **Command is copy-paste safe?** | → Offer user option | Run in Claude (complex setup) |
| **Non-branching workflow?** | → Offer user option | Run in Claude (dependencies) |
| **User can safely retry?** | → Offer user option | Run in Claude (risky to retry) |

### When to offer user self-execution

Condition: command is copy-paste runnable AND Claude doesn't need to inspect output

**Present the full command block and ask:**
```
Want to run this yourself?

[command block]

Or I can run it and continue.
```

**Examples:**
- ✅ Installing dependencies: `npm install` or `pip install -r requirements.txt`
- ✅ Running tests locally: `pytest` or `npm test`
- ✅ Building: `make build` or `cargo build`
- ✅ Cleanup: `rm -rf dist/` or `git clean -fd`
- ✅ Formatting: `black .` or `prettier --write .`

**Why:** These tasks are self-contained; output doesn't gate the next step; user can watch and retry if needed.

### When to run in Claude

Condition: Claude must interpret output to proceed

**Examples:**
- ❌ Parsing test failures to decide what to fix next
- ❌ Reading file content to inform the next edit
- ❌ Checking git state before the next step (`git status`, `git diff`)
- ❌ Inspecting environment variables to determine next action
- ❌ Checking if a process is running before proceeding

**Why:** Output gates decision-making; sub-turn delay would block iteration.

### Rules for user self-execution

**Before offering:**
1. Present the command in a code block — copy-paste ready, not prose
2. Explain what it does — one sentence, plain language
3. Wait for confirmation — get explicit yes/no before proceeding
4. Provide fallback: "Or I can run it and continue" if they want Claude to execute

**After user completes:**
1. Don't run verification tools preemptively — wait for user to confirm "done" or report output
2. Respect user's experience — they may have learned something or want to explore further
3. Ask if needed: "Ready to proceed?" or "Everything OK?" — give them space to surface issues

### Retry and recovery

**If user runs command and hits an error:**
1. Ask for the error output (they copy-paste it to you)
2. Diagnose the issue
3. Offer either: a fix they can apply and retry, or running the corrected command in Claude

**If user doesn't respond within a reasonable time:**
- Don't preemptively run the command
- Ask: "Should I go ahead and run this?"

---

## 🤖 Delegating to Sub-Agent

@~/.claude/_rules/04_claude_reference/claude_conduct/claude_when_to_delegate/_delegating_to_subagent.md

---

## 🔗 Related

- Reference: `claude_operational_efficiency.md` — token efficiency and default behaviours (this file's parent import)
- Sibling: `behaviour/_model_selection_strategy.md` — when to use which Claude model
