# 🤖 Delegating to Sub-Agent

**Purpose:** Decision framework, constraints, and cost analysis for when to spawn a sub-agent vs. work directly.

---

## Decision framework

**Before spawning a sub-agent, answer these in order:**

| Question | Decision | Justification |
|----------|----------|---------------|
| **Is this a single file/tool call?** | → Work directly | Sub-agents are overkill; context overhead not justified |
| **Do I need the output to decide the next step?** | → Work directly | Sequential dependencies require main loop; sub-agent context lag blocks iteration |
| **Is the task bounded and read-only?** | → Consider sub-agent | Tight prompt + Explore agent minimizes output |
| **Will output exceed 5K tokens?** | → Sub-agent justified | Isolation protects main window from content bloat |
| **Do I need context across steps?** | → Work directly | Sub-agent can't carry conversational context forward safely |

## When to spawn a sub-agent

Spawn a sub-agent when:

- **Large output expected:** research, codebase scans, long documentation reads (>5K tokens)
- **Read-only research:** `subagent_type: "Explore"` for bounded file exploration or grep searches
- **Parallelism saves time:** multiple independent lookups or analyses that don't block each other
- **Tight prompt scope:** task is narrow enough that the sub-agent reads only what's necessary
  - **Good:** "Find all usages of `foo()` in src/ via grep, report file paths only"
  - **Bad:** "Explore the entire codebase and figure out what this project does"

## When NOT to spawn a sub-agent

**Avoid sub-agents for:**

- **Single-file edits:** "Read this file and make a fix" — work directly (context carried through)
- **Sequential operations:** Steps where output gates the next action (parsing, validating, then modifying)
- **Conversational context needed:** Building on prior discussion; sub-agent has no context bridge
- **Tool interpretation:** When Claude must inspect tool output before proceeding (parsing test failures, reading git state)
- **Simple tasks:** Use direct tool calls instead of sub-agent overhead

## Sub-agent constraints

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

## Context cost analysis

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

- Parent: `claude_when_to_delegate.md` — delegating to user vs. sub-agent overview
