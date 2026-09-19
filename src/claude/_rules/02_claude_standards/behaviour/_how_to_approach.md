# 🔬 How to Approach

**Purpose:** Establish habits for approaching a task well — diagnosing root causes, scoping narrowly, and preserving context across long sessions.

---

- 🎯 **Simplest approach:** try the simplest solution first — diagnose root causes, don't brute-force past blockers.
  - **Note:** if a search fails twice, stop and ask; a clarifying question is cheaper than five failed tool calls.
- 🎯 **Colleague test:** before finalizing a prompt, show it to someone with minimal context on the task and ask them to follow it. If they'd be confused, Claude will be too.
- 🔬 **Narrow scope:** treat a narrow request as narrow — don't refactor or restructure unless explicitly asked.
  - **Note:** when asked to modify specific files or a PR, state the exact files and target branch before editing; don't touch anything outside that scope.
- 📄 **Offload to files:** proactively write a checkpoint to `TODO.md` in the project root at task completion and whenever context is accumulating — never write session state to `CLAUDE.md`.
  - **Include:** active decisions, file paths, build commands, constraints, and open items.
  - **Why:** Claude reads the file on demand — the conversation doesn't need to carry it.
- ✅ **No best-effort:** only propose solutions with a guaranteed, verifiable outcome — if no such solution exists, say so and ask how to proceed rather than proposing a workaround that relies on convention, trust, or hope.
- 📐 **Same quality bar:** apply the same standards to agent-generated code as to human-written code — same linting, same test coverage, same review rigour; speed of generation is not a reason to lower the bar.
  <!-- Source: Boris Cherny — Steps of AI Adoption https://claude.ai/code/artifact/bfdfaef9-bc62-4dfe-ba9e-c58a26c9accf -->
- 🧪 **Rules require tests:** adding or modifying an **enforcement rule** in `_rules/` is not complete until a corresponding test exists in `_tests/rules/` or `_tests/hooks/` — propose the test alongside the rule, not as a follow-up.
  - **Note:** instructional guidance (rules Claude reads and follows, with no mechanical trigger) does not require a test — structural tests in `test_rules_structure.py` already cover file quality for all `_rules/` files.
- 📋 **Session checkpoints:** proactively write a checkpoint to `~/_sessions/YYYY_MM_DD_<domain>_<topic>.md` at task completion and whenever context is accumulating (long tool-call sequences, many files touched).
  - **Include:** decisions made, files modified, open items, and current task state.
  - **Why:** Claude Code auto-compression can drop critical context — an explicit checkpoint ensures continuity across context windows.
- 🧠 **Tune exploration for current models:** newer models explore more than older ones by default. Replace blanket "be thorough" defaults with targeted instructions.
  - ❌ "Default to using [tool]" (causes overtriggering)
  - ✅ "Use [tool] when it would enhance understanding of the problem"

## 🔗 Related

- Parent: `behaviour.md` — safe action defaults; decision-making patterns
