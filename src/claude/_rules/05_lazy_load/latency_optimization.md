---
name: latency_optimization
description: Temperature tuning and API-level latency strategies for faster, more focused responses
metadata:
  type: feedback
---

# ⚡ Latency Optimization

**Purpose:** Establish when and how to optimize API-level latency to reduce response time for cost-sensitive or interactive workflows.

---

## When latency matters

Latency optimization is **only justified when actual latency is blocking the task**. Premature optimization wastes context and ruins response quality. Ask first: "Is latency actually a problem here?"

**Appropriate cases:**
- Interactive tools or CLI commands where users wait for output
- Cost-sensitive tasks where response time directly impacts billing
- Polling or real-time monitoring loops where each second compounds

**Not appropriate:**
- Offline batch processing
- One-off research or analysis where thinking time adds value
- Tasks where quality > speed (design decisions, security reviews, complex debugging)

---

## Temperature as a conciseness lever

**Temperature controls randomness — lower = more focused and concise.**

| Scenario | Temperature | Why |
|----------|---|---|
| **Speed priority** | 0.2 | Deterministic, focused, shorter output; reduced thinking overhead; best for structural tasks (formatting, extraction, refactoring) |
| **Default balance** | 0.7–1.0 | Creative reasoning + clarity; natural for explanations, design, and problem-solving |
| **Exploration** | 1.5–2.0 | Diversity of ideas; useful for brainstorming or when multiple approaches are needed |

**Important:** Temperature is a hack for latency. Setting T=0.2 does not guarantee speed — it just removes randomness, making outputs shorter and more predictable. Use only when the task naturally benefits from conciseness (extraction, formatting, simple refactoring).

---

## How to apply

### When requesting a response:
```
@brief:
output as concise bullet points, not prose
use temperature=0.2 for focused extraction
```

### When using the Claude API directly:
- Set `temperature=0.2` for fast, structural tasks (code extraction, formatting, chunking)
- Omit or use default (0.7–1.0) for reasoning-intensive work (design, debugging, architecture)
- Never use `temperature > 1.0` in production tools unless exploring alternatives is the actual goal

### Related parameters (brief references):
- **max_tokens:** cap output token budget to force conciseness — useful with lower temperature
- **streaming:** doesn't reduce latency; reduces time-to-first-token but increases total time — use only for UX (progressive display)

---

## Constraint: measure before optimizing

Before applying latency tuning:

1. **Baseline:** run the task at default temperature and measure actual latency
2. **Justify:** "This is X seconds, and I need it under Y because Z"
3. **Test:** apply temperature change and verify output quality doesn't degrade
4. **Revert if needed:** if quality suffers, accept the latency or find a different bottleneck

Temperature is an approximate tool — verify it actually solves the problem, not just theoretically.

---
