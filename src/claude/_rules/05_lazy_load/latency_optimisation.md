<!-- version: 2.0.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-01 -->
# ⚡ Latency Optimisation

**Purpose:** Establish when and how to make Claude API responses faster or cheaper for interactive, high-volume or cost-sensitive work, without giving up the quality the task needs.

---

## 🎯 When latency matters

Latency optimisation is **only justified when actual latency is blocking the task**. Premature optimisation wastes context and ruins response quality. Ask first: "Is latency actually a problem here?"

**Appropriate cases:**
- **Interactive tools:** CLI commands or chat where users wait for output.
- **High-volume routes:** classification, extraction or routing calls where output tokens drive the bill.
- **Loops:** polling or real-time monitoring where each second compounds.

**Not appropriate:**
- **Batch work:** offline processing, which the Batch API runs at half price anyway.
- **Research:** one-off analysis where thinking time adds value.
- **Hard problems:** tasks where quality > speed (design decisions, security reviews, complex debugging).

---

## 🎛️ Effort is the main lever

**`output_config.effort` sets how much Claude thinks and writes.** Lower effort means less thinking, fewer and more consolidated tool calls, less preamble and terser answers.

| Effort | Use for |
|---|---|
| `low` | Chat, classification, extraction and other high-volume or latency-sensitive routes |
| `medium` | The step down when `high` is slower than needed and quality still holds |
| `high` | Intelligence-sensitive work, and the default on most current models |
| `xhigh` / `max` | Coding, long agentic runs, or work where correctness matters more than cost |

- **Defaults differ:** `high` is the default on most current models, but Claude Opus 5.5 defaults to `medium`, so set effort explicitly.
- **Lower effort, don't disable thinking:** Claude Opus 5.5 and Fable 5/5.1 can't switch thinking off, and on other models lower effort is the safer saving.
- **Tune per route:** set effort for each kind of request rather than once for everything.

**Temperature is not a lever on current models.** Claude Opus 5.5, Opus 5, Opus 4.8, Opus 4.7, Fable 5/5.1 and Sonnet 5 return a 400 error for any `temperature`, and Sonnet 5.5 rejects non-default values.
- **Older models:** Opus 4.6, Sonnet 4.6 and Haiku 4.5 still accept `temperature` from 0 to 1, but lowering it changes randomness, not speed.

---

## 🛠️ How to apply

### When requesting a response
- **Ask for brevity:** say what shape you want, for example "answer in three bullets, no preamble".

### When using the Claude API directly
- **Set effort:** `output_config={"effort": "low"}` for fast, structural tasks such as extraction, formatting and classification.
- **Keep effort up for hard work:** use `high` or above for design, debugging and architecture.
- **Pick the model last:** before switching to a smaller model, check whether the current model at lower effort already meets the bar.

### Related parameters
- **max_tokens:** set it high enough for a full answer, because a low cap cuts the reply off mid-thought rather than making it shorter.
- **streaming:** shows output sooner and avoids timeouts on long replies, but doesn't make the full reply finish faster.
- **Prompt caching:** reusing a cached prefix cuts both cost and time-to-first-token on repeated context.

---

## 📏 Constraint: measure before optimising

Before applying latency tuning:

1. **Baseline:** run the task at the default effort and measure actual latency
2. **Justify:** "This is X seconds, and I need it under Y because Z"
3. **Test:** lower the effort and verify output quality doesn't degrade on real requests
4. **Revert if needed:** if quality suffers, accept the latency or find a different bottleneck

Judge cost per completed task, not per request, since a cheaper request that needs retries isn't cheaper.

---
