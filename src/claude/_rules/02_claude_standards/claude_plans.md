<!-- version: 2.0.2 -->
<!-- created: 2026-09-17 -->
<!-- updated: 2026-10-01 -->
<!-- applies_to: * -->
<!-- miss_cost: medium — phases run without approval, so wrong turns need rework -->
# 🗂️ Claude Plans

**Purpose:** Establish review/approval gates for multi-phase work — plans and any other 3+ phase implementation — preventing wasted effort and enabling course correction.

---

## 🎯 Core principle

**Pause after each phase.** When implementing multi-phase work (3+ phases), complete one phase, then stop and request explicit approval before proceeding to the next phase.

**Why:** Early feedback catches misalignments before effort is wasted on subsequent phases. User can correct course, adjust scope, or deprioritize based on results from each phase.

---

## ⚙️ When to apply

**Apply gates when:**
- Implementing work with 3+ distinct phases (sequential, not parallel)
- Each phase produces concrete deliverables or changes
- Feedback from one phase could affect the next phase's approach
- User hasn't explicitly waived gates

**Do NOT apply gates when:**
- User explicitly says "proceed without interruption" or "no gates"
- Phases are tightly coupled (output of phase N is required input for phase N+1; stopping breaks workflow)
- Single-phase work (no gates needed)

---

## 📋 How to apply

**After completing each phase:**

1. **Summarize what was delivered** — one sentence per deliverable (what changed, what's done)
2. **Request explicit approval** — "Ready to proceed to Phase X?" or similar
3. **Wait for response** — do not proceed until user confirms (yes/no)
4. **On "yes"** — proceed to next phase
5. **On "no" or feedback** — adjust approach, ask clarifying questions, or halt

**Format:** use the normal response format from `claude_response_standards.md` (Summary, then Next steps). The phase report must contain:

- **Phase theme:** a heading for the finished phase, with one bullet per deliverable
- **Gate theme:** a heading that names the next phase and says work has stopped
- **Next steps:** "Start Phase N+1" as the recommended option, plus an "Adjust first" option

---

## 🗂️ Plan-Mode Phase Gates

@~/.claude/_rules/02_claude_standards/claude_plans/_plan_mode_phase_gates.md

---

## 📊 Plan file format

@~/.claude/_rules/02_claude_standards/claude_plans/_plan_file_format.md

---

## 🚫 Anti-patterns (what NOT to do)

- ❌ Complete all phases silently, then ask "Done?" at the end
- ❌ Ask "Ready to proceed?" while already starting Phase N+1
- ❌ Summarize all phases as one massive wall of text; break by phase
- ❌ Ignore user feedback ("no, adjust this") and barrel forward anyway
- ❌ Apply gates to parallel work where phases run concurrently

---

## 📚 Example

### ❌ Wrong: No gate, silent progress

User plans 3-phase work. Claude completes Phase 1, 2, and 3 without stopping for feedback. User discovers Phase 2 approach was misaligned and wasted effort.
