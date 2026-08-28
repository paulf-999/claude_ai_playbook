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

### Decision framework

**Before spawning a sub-agent, answer these in order:**

| Question | Decision | Justification |
|----------|----------|---------------|
| **Is this a single file/tool call?** | → Work directly | Sub-agents are overkill; context overhead not justified |
| **Do I need the output to decide the next step?** | → Work directly | Sequential dependencies require main loop; sub-agent context lag blocks iteration |
| **Is the task bounded and read-only?** | → Consider sub-agent | Tight prompt + Explore agent minimizes output |
| **Will output exceed 5K tokens?** | → Sub-agent justified | Isolation protects main window from content bloat |
| **Do I need context across steps?** | → Work directly | Sub-agent can't carry conversational context forward safely |

### When to spawn a sub-agent

Spawn a sub-agent when:

- **Large output expected:** research, codebase scans, long documentation reads (>5K tokens)
- **Read-only research:** `subagent_type: "Explore"` for bounded file exploration or grep searches
- **Parallelism saves time:** multiple independent lookups or analyses that don't block each other
- **Tight prompt scope:** task is narrow enough that the sub-agent reads only what's necessary
  - **Good:** "Find all usages of `foo()` in src/ via grep, report file paths only"
  - **Bad:** "Explore the entire codebase and figure out what this project does"

### When NOT to spawn a sub-agent

**Avoid sub-agents for:**

- **Single-file edits:** "Read this file and make a fix" — work directly (context carried through)
- **Sequential operations:** Steps where output gates the next action (parsing, validating, then modifying)
- **Conversational context needed:** Building on prior discussion; sub-agent has no context bridge
- **Tool interpretation:** When Claude must inspect tool output before proceeding (parsing test failures, reading git state)
- **Simple tasks:** Use direct tool calls instead of sub-agent overhead

### Sub-agent constraints

When spawning a sub-agent, apply these constraints:

**Tight prompt scoping**
- Narrow the task: specify exactly what to search for, not "explore broadly"
  - ❌ Bad: "Explore the codebase" (unbounded)
  - ✅ Good: "Find all `.tsx` files in src/components/ that import Context" (bounded)
- Expected output: tell the sub-agent how much detail to return and what format (file paths only, summary, bullet list)

**Explore sub-agent type**
- Use for read-only research: `subagent_type: "Explore"` cannot write files — safe for safe zones
- Pair with scoped search: Combine with grep, glob, or find patterns to narrow search space before spawning

**Tool restrictions**
- Custom agents: agents in `.claude/agents/` can declare `allowedTools` list (omit write/bash for read-only work)
- MCP tools: Use read-only MCP tools; avoid mutation operations in sub-agents

**Summary-only returns**
- Main loop receives: Sub-agent summary (~500 tokens), not raw content (10K+ tokens)
- Context protection: Main window stays focused on current task, not buried in intermediate research

### Context cost analysis

**Token cost of sub-agent spawn:**

| Component | Cost |
|---|---|
| Sub-agent setup + prompt transmission | ~200 tokens |
| Sub-agent reasoning overhead | ~300 tokens |
| Summary return + context reintegration | ~200 tokens |
| **Total baseline** | ~700 tokens |

**Breakeven analysis:**
- **If output would be >5K tokens:** sub-agent saves (5K + integration cost) → isolation wins
- **If output would be <2K tokens:** work directly (direct call + context < 700-token sub-agent overhead)
- **Grey zone (2–5K):** decide by: do I need output to proceed (direct), or is output large enough to risk main window bloat (sub-agent)?

---

## 🔗 Related

- Parent: `claude_operational_efficiency.md` — context management principles and constraints
- Sibling: `behaviour/_model_selection_strategy.md` — when to use which Claude model
