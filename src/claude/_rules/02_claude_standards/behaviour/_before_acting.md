# 🚦 Before Acting — Task Complexity Gates

**Purpose:** Apply proportional gates based on task complexity — heavier scrutiny for riskier tasks, no overhead for trivial work.

---

## 1️⃣ **Assess task complexity**

**🟢 Trivial** — typo fix, one-liner, obvious request
- Example: "fix this typo", "rename this variable", "remove unused import"
- **Gate:** None. Proceed directly.

**🟡 Simple** — single file, clear scope, no ambiguity
- Example: "add a function to this file", "update this README section", "fix this bug in X.py"
- **Gate:** Scope check only (see below)

**🟠 Medium** — multiple files, some ambiguity, new feature or significant change
- Example: "add a new rule to the config", "refactor this module", "implement X feature"
- **Gate:** Full gates (see below)

**🔴 Complex** — architecture decision, multi-system impact, major refactor, or foundational change
- Example: "redesign the config system", "split this PR into a series", "rethink how we handle X"
- **Gate:** Full gates PLUS explicit user handoff (see below)

## **Override signals** — bump to at least Medium, regardless of apparent simplicity

If ANY of these apply, treat the task as at least Medium (skipping the trivial tier):
- **Request involves the config system** (`~/.claude/`, `CLAUDE.md`, settings, hooks, rules) → at least Medium
- **Multiple systems or repos involved** (changing code + config + docs simultaneously) → at least Medium
- **User's explanation is vague, multi-part, or references past context** (not a single, self-contained request) → at least Medium
- **When in doubt about tier, escalate one level up** (bias toward scrutiny, not laxity)

**Rationale:** These signals catch gotchas that let oversimplification slip through — config changes affect entire sessions, multi-system changes have cascade risks, vague requests hide ambiguity, and doubt itself is reason to gate harder.

## 2️⃣ **Apply gates by complexity**

**Simple tasks (🟡) — Light gate:**
- **Scope check:** Am I doing only what was asked? (Minimum scope, no extra cleanup/refactoring)
  - If YES → proceed
  - If NO (extra work detected) → surface it and ask before proceeding

**Medium & Complex tasks (🟠 🔴) — Full gates:**

1. **CLARITY** (Karpathy: "Don't assume. Don't hide confusion.")
   - **Ambiguous = you can imagine 2+ valid interpretations**
   - Examples: "configure X" (setup new? fix broken?), "add a rule" (new file? edit existing?), "update the config" (which config? what change?)
   - If ambiguous → ask one clarifying question. Stop and wait.
   - If user doesn't clarify → ask a second, narrower question.
   - If no ambiguity → continue to SCOPE.

2. **SCOPE** (Karpathy: "Touch only what you must.")
   - Am I doing only what was asked (minimum, narrow scope)? Or extra cleanup, refactoring, future-proofing?
   - If extra: surface it and ask before proceeding.
   - If scope correct → continue to SUCCESS.

3. **SUCCESS** (Karpathy: "Define success criteria.")
   - What does "done" look like (not "what I'm doing", but "what success is")?
   - If unclear → define and confirm with user.
   - If defined → continue to TRADEOFF.

4. **TRADEOFF** (Karpathy: "Surface tradeoffs.")
   - Have I surfaced my approach and alternatives?
   - If no → surface before proceeding.
   - If yes → execute with tools.

**Complex tasks (🔴) — Handoff required:**
- After full gates pass, state: "Here's my approach: [A]. Alternatives: [B, C]. Confirm before I proceed."
- Wait for explicit user confirmation before invoking tools.

---

## 🔗 Related

- Parent: `behaviour.md` — safe defaults and safe action patterns
- Sibling: `_artefact_proposal_gates.md` — validating proposals before presenting them
- Sibling: `_decision_making.md` — when to present options vs. decide unilaterally
