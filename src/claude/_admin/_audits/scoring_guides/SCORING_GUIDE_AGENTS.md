# 📊 Scoring Guide — Agents

Scoring rubric for specialized subagents. Scores range 1–10 across six quality dimensions.

---

## 🎯 The 6 Dimensions

| # | Dimension | What it measures | Higher score = |
|---|---|---|---|
| **1️⃣** | **Purpose Clarity** | Is the agent's purpose and scope clearly defined? | Clear, focused purpose |
| **2️⃣** | **Capability** | Can it do what's intended? Breadth of tasks? | Capable and versatile |
| **3️⃣** | **Reliability** | Does it produce consistent, correct results? | Dependable and accurate |
| **4️⃣** | **Integration** | Works well with main loop and other agents? | Seamless integration |
| **5️⃣** | **Documentation** | Clear instructions, examples, edge cases, failure modes? | Well-documented |
| **6️⃣** | **Efficiency** | Appropriate tool selection, reasoning depth, token cost? | Efficient operation |

**Weighting:** Reliability 20%, Documentation 20%, Capability 15%, Integration 15%, Purpose Clarity 15%, Efficiency 15%

---

## 1️⃣ Purpose Clarity (1–10)

**Principle:** Agent's purpose should be obvious from name and description.

Measures clarity of intent, scope, and appropriate use cases.

| Score | Purpose | Scope | Judgment |
|---|---|---|---|
| **9–10/10** | ✅ Crystal clear | Precise, single-purpose | Purpose obvious from name; use cases explicit; no ambiguity |
| **7–8/10** | ✅ Clear | Focused on 2–3 related tasks | Purpose is clear with brief description; scope defined |
| **5–6/10** | ⚠️ Moderate | 3–4 related tasks | Purpose stated but could be sharper; scope somewhat broad |
| **3–4/10** | ⚠️ Unclear | 4–5 tasks; loosely related | Purpose requires explanation; scope unclear |
| **1–2/10** | ❌ Vague | 5+ unrelated tasks | Purpose ambiguous; could be multiple agents |

---

## 2️⃣ Capability (1–10)

**Principle:** Agent should be able to do what it's intended for.

Measures feature completeness and breadth of tasks it can handle.

| Score | Scope | Feature Completeness | Judgment |
|---|---|---|---|
| 1–4 | Very narrow or incomplete | <50% of intended tasks | Missing critical features; can't do core job |
| 5–6 | Narrow; some gaps | 60–70% of intended tasks | Does main task but with gaps or limitations |
| 7–8 | Appropriately scoped | 80–90% of intended tasks | Handles most tasks well; minor gaps acceptable |
| 9–10 | Well-scoped, comprehensive | 95%+ of intended tasks | Comprehensive; handles edge cases and variations |

**How to assess:**
- Can it accomplish its stated purpose?
- Does it handle common variations?
- What tasks are missing or impossible?

---

## 3️⃣ Reliability (1–10)

**Principle:** Agent output should be trustworthy and consistent.

Measures accuracy, consistency, and failure handling.

| Score | Correctness | Consistency | Error Handling | Judgment |
|---|---|---|---|---|
| 1–4 | Frequently wrong or hallucinating | Unreliable; same input → different output | No error handling; crashes | Untrustworthy |
| 5–6 | Mostly correct; occasional errors | Usually consistent; edge cases unreliable | Basic error handling | Generally usable but needs supervision |
| 7–8 | Correct for main cases; edge cases spotty | Consistent for typical inputs | Good error recovery; explains failures | Reliable for normal use |
| 9–10 | Highly accurate across all cases | Fully consistent and reproducible | Comprehensive error handling | Production-grade reliability |

---

## 4️⃣ Integration (1–10)

**Principle:** Agent should work smoothly with main loop and other agents.

Measures whether it composes well with existing system.

| Score | Integration | Tool Compatibility | State Management | Composition |
|---|---|---|---|---|
| 1–4 | Doesn't work with main loop | Conflicts with other agents | Loses context; side effects | Standalone only; can't combine |
| 5–6 | Works but with friction | Minor tool conflicts | Some state issues | Works with workarounds |
| 7–8 | Works smoothly; minor friction | No conflicts; tool reuse | Preserves context well | Composes naturally |
| 9–10 | Seamless integration | Enhances tool ecosystem | Perfect state management | Improves when combined |

---

## 5️⃣ Documentation (1–10)

**Principle:** Agent usage, edge cases, and failure modes should be documented.

Measures completeness of supporting material.

| Score | Instructions | Examples | Edge Cases | Failure Modes |
|---|---|---|---|---|
| 1–4 | Minimal or missing | None or wrong | Not documented | Not documented |
| 5–6 | Basic instructions | One basic example | Some noted | Brief mention |
| 7–8 | Clear instructions | Multiple examples | Documented | Documented with recovery |
| 9–10 | Comprehensive guide | Rich examples + anti-patterns | Thoroughly covered | Complete failure map + solutions |

**Documentation checklist:**
- **What:** What does this agent do?
- **When:** When should you use it?
- **How:** What input/output does it expect?
- **Edge cases:** What breaks it?
- **Failures:** What error messages mean what?
- **Related:** What other agents work with it?

---

## 6️⃣ Efficiency (1–10)

**Principle:** Agent should use resources appropriately for its task.

Measures tool selection, reasoning depth, and token economy.

| Score | Tool Selection | Reasoning Depth | Token Cost | Judgment |
|---|---|---|---|---|
| 1–4 | Wrong tools or too many | Over-reasoning simple tasks | Expensive; could be 1/5 cost | Wasteful |
| 5–6 | Mostly appropriate tools | Reasonable reasoning | Acceptable cost with room to improve | Could be optimized |
| 7–8 | Good tool selection | Appropriate reasoning | Efficient; no wasted tokens | Well-tuned |
| 9–10 | Perfect tool match | Minimal reasoning needed | Minimal token cost for task | Highly optimized |

**How to assess:**
- Is it using the right tools for the job?
- Is it over-reasoning simple tasks?
- What's the token cost vs. output quality?

---

## Overall Score Calculation

**Formula:** Weighted average across six dimensions

```
Overall = (
  Purpose Clarity    × 0.15 +
  Capability         × 0.15 +
  Reliability        × 0.20 +
  Integration        × 0.15 +
  Documentation      × 0.20 +
  Efficiency         × 0.15
)
```

---

## How to Use This Guide

**During assessment:**
1. Use the agent for its stated purpose
2. For each dimension, identify the band that best describes it
3. Score should be defensible — cite specific examples
4. When unsure, err toward middle bands (5–6)

**Scoring expectations:**
- Well-designed agents score 7–8 overall
- New agents can score 5–6 even if functional (limited maturity)
- Established agents score 8–9 (well-integrated, battle-tested)

**Maintaining scores:**
- Re-score when agent behavior changes
- Update when other agents are added/removed
- Document rationale for scores near extremes (1–2, 9–10)

---

## Related Guidance

- Agent design: `~/.claude/_rules/agent_design.md` (if exists)
- Integration: `~/.claude/agents/README.md`
- Efficiency: `~/.claude/_rules/claude_efficiency.md`
