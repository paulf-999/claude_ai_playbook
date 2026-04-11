# Always-On Optimisation

A global rule active in all Claude sessions. Instructs Claude toward efficient patterns
by default and intervenes when inefficiency is detected mid-session.

---

## Default behaviours

- **Parallel tool calls** — execute independent operations concurrently; serialise only where there is a genuine dependency
- **No redundant reads** — do not re-read files or re-fetch data already in the current session's context
- **Reuse before creating** — check for existing hooks, utilities, and patterns before proposing new ones
- **No context restating** — do not summarise content already visible in the conversation window

---

## Intervention mode

When inefficiency is detected, flag it but do not block execution:

> "Flagging: this read duplicates one already in context — skipping."

Intervene only where the waste is clear and material — e.g. re-reading a file just read,
spawning a sub-agent for a single tool call, re-summarising context already in the window.

---

## Balancing with token awareness

Parallelism should be balanced against token cost. Prefer targeted, scoped operations over
broad sweeps where the output would be equivalent. Do not parallelise for its own sake —
only where it reduces real wait time or produces meaningfully better results.
