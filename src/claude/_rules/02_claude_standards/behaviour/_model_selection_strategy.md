# 🎛️ Model Selection Strategy

**Purpose:** Establish when to use which Claude model (Haiku vs. Sonnet/Opus), reducing unnecessary API cost while matching task complexity to capability.

---

## 🎯 Core principle

Default to Haiku — fast and cheap for most tasks. Escalate only when task complexity warrants it. Flag at task start before turns are wasted on the wrong model.

---

## 📋 Model selection framework

**Haiku (default):** Fast, cheap, suitable for most work

| Task type | When to use Haiku |
|---|---|
| Summarising | ✅ Always |
| Formatting | ✅ Always |
| Drafting routine emails | ✅ Always |
| Quick Q&A | ✅ Always |
| Simple mechanical edits | ✅ Usually |
| Reading and summarising docs | ✅ Usually |

**Sonnet/Opus (escalate when):** Multi-step reasoning, nuanced analysis, complex code

| Task type | Escalate to Sonnet/Opus |
|---|---|
| Multi-step reasoning | ✅ Yes |
| Nuanced analysis | ✅ Yes |
| Long-form writing | ✅ Yes |
| Complex code generation | ✅ Yes |
| Code review or refactoring | ✅ Yes |
| Adversarial thinking or debate | ✅ Yes |

---

## 📍 When to flag

### At task start

**Signal:** Task description suggests complexity (reasoning, analysis, code)

```
This looks complex. Consider switching with `/model claude-sonnet-5` before we begin.
```

**Why:** Haiku can start the task, but will likely need rethinking. Flag early to avoid wasted turns.

### Mid-session escalation

**Signal:** A simple task unexpectedly expands (quick fix becomes refactoring, summary becomes analysis)

```
This has grown complex — consider switching with `/model claude-sonnet-5`.
```

**Why:** Original model choice was correct for the initial scope. New complexity warrants re-evaluation.

---

## 💰 Cost-benefit thinking

Escalating adds cost but prevents:
- Repeated rework due to insufficient reasoning depth
- Wasted turns on incremental improvements
- Incomplete solutions requiring multiple fix rounds

**Rough heuristic:**
- Task under 5 minutes of reasoning → Haiku
- Task 5–15 minutes of reasoning → Sonnet
- Task >15 minutes of complex thinking → Opus

---

## 🔗 Related

- Parent: `behaviour.md` — safe defaults and decision-making patterns
- Reference: `context_management.md` — context management principles (related but separate concern)
