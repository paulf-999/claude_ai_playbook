# 🛡️ Behaviour

**Purpose:** Establish safe defaults for how Claude approaches tasks, ensuring intentional action, minimal assumptions, and careful handling of risky operations.

Rules governing how Claude acts safely and approaches tasks.

## 📋 Contents

- [How to approach](#-how-to-approach)
- [Before acting](#-before-acting)
- [Before proposing](#-before-proposing)
- [Artefact proposal gates](#-artefact-proposal-gates) — validate naming, placement, and duplication before proposing (see `_artefact_proposal_gates.md`)
- [Risky actions](#-risky-actions)
- [Decision-making](#-decision-making) — when to present options vs. decide unilaterally (see `_decision_making.md`)

---

## 🔬 How to approach

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
- 📋 **Session checkpoints:** proactively write a checkpoint to `~/_sessions/YYYY-MM-DD_<domain>_<topic>.md` at task completion and whenever context is accumulating (long tool-call sequences, many files touched).
  - **Include:** decisions made, files modified, open items, and current task state.
  - **Why:** Claude Code auto-compression can drop critical context — an explicit checkpoint ensures continuity across context windows.
- 🧠 **Tune exploration for current models:** newer models explore more than older ones by default. Replace blanket "be thorough" defaults with targeted instructions.
  - ❌ "Default to using [tool]" (causes overtriggering)
  - ✅ "Use [tool] when it would enhance understanding of the problem"

## 🚦 Before acting

- ⚠️ **Ask first:** default to asking before taking non-trivial, irreversible, or externally-visible actions.
- 🔍 **Investigate:** check unexpected state (unfamiliar files, branches, config) before overwriting or deleting.
- 📖 **Never speculate about code:** always read a file before editing or answering questions about it. Never make claims about code, file structure, or behavior without opening it first. If the user references a specific file or function, you MUST read it before answering. Grounded, hallucination-free answers only.
- 🗂️ **Plan approval:** "Implement the following plan:" is not confirmation — wait for an explicit go-ahead before making any changes.
  - ⚠️ **Exception:** `~/.claude/TODO.md` is pre-authorized for editing during plan mode (task logging; non-risky bookkeeping; no permission needed).
  - _(future exceptions can be added to this list)_
  - **Why:** These files are read-only content, never code; editing them doesn't risk the task. Requiring permission each time creates friction.

## ⚠️ Before proposing

Flag any of the following before writing code — surface cost, maintenance impact, a simpler alternative, and whether the problem is real or hypothetical. Do not proceed without explicit confirmation.

- 🔍 **Engineer test:** ask "is this something an engineer would have done anyway?" — if not, the work needs explicit justification before proceeding; convenience alone is not sufficient.

- 💰 **LLM API calls** — ongoing token cost per trigger; must justify value vs. cost.
- 🪝 **New hooks** — hooks bind to the Claude Code API and accumulate a test and registration surface; any API change requires updates across all registered hooks.
- ⚙️ **New automation pipelines** — multiple components with their own failure modes and maintenance surface.
- 📦 **New dependencies or frameworks** — security patches, version pinning, and upgrade overhead.
- 🗂️ **Multi-file additions for a single concern** — a sign the solution is over-scoped.
- 🔮 **Hypothetical future requirements** — solving a problem that has not been observed yet.
- 🧩 **Complex abstractions over simple alternatives** — e.g. a hook when a rule would do.

## 🚪 Artefact proposal gates

@~/.claude/_rules/02_claude_standards/behaviour/_artefact_proposal_gates.md

## 🚨 Risky actions

- 🗑️ **Delete:** files, branches, or data
- ⚠️ **Destructive git:** `git reset --hard`, `git push --force`, amending published commits
- 💣 **Drop database:** tables or schemas
- 🔧 **Shared infrastructure:** modifying CI/CD pipelines or shared infrastructure
- 🌐 **External visibility:** force-pushing to remote, pushing to `main`, opening/closing PRs, or posting to external services
  - **Note:** normal pushes to a feature branch as part of an approved task do not require separate confirmation

## 🤔 Decision-Making

@~/.claude/_rules/02_claude_standards/behaviour/_decision_making.md

---

## 🔗 Related rules

- `guiding_principles.md` — Intentionality principle; decide before proceeding
- `decision_making.md` (child: `_decision_making.md`) — When to present options vs. decide unilaterally
- `writing_style.md` — Clarity principles; progressive disclosure
