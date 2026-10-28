<!-- version: 2.3.0 -->
<!-- created: 2026-09-17 -->
<!-- updated: 2026-10-28 -->
<!-- applies_to: * -->
<!-- miss_cost: medium — phases run without approval, so wrong turns need rework -->
<!-- loading: always-on — any task can grow into multi-phase work that needs approval gates -->
# 🗂️ Claude Plans

**Purpose:** Establish review/approval gates for multi-phase work — plans and any other 3+ phase implementation — preventing wasted effort and enabling course correction.

---

## 🎯 Core principle

**Pause after each phase.** When implementing multi-phase work (3+ phases), complete one phase, then stop and request explicit approval before proceeding to the next phase.

**Why:** Early feedback catches misalignments before effort is wasted on subsequent phases. User can correct course, adjust scope, or deprioritise based on results from each phase.

---

## ⚙️ When to apply

**Apply gates when:**
- **3+ phases:** the work has 3+ distinct phases (sequential, not parallel)
- **Concrete output:** each phase produces concrete deliverables or changes
- **Feedback matters:** feedback from one phase could affect the next phase's approach
- **No waiver:** the user hasn't explicitly waived gates

**Skip gates when:**
- **User waiver:** the user explicitly says "proceed without interruption" or "no gates"
- **Tightly coupled:** phases are tightly coupled (output of phase N is required input for phase N+1; stopping breaks workflow) — outside plan mode only, since a plan keeps its gates unless the user waives them
- **Single phase:** single-phase work needs no gates

---

## 📋 How to apply

**After completing each phase:**

1. **Summarise what was delivered:** one sentence per deliverable (what changed, what's done)
2. **Request explicit approval:** "Ready to proceed to Phase X?" or similar
3. **Wait for response:** proceed only once the user confirms (yes/no)
4. **On "yes":** proceed to next phase
5. **On "no" or feedback:** adjust approach, ask clarifying questions, or halt

**Format:** use the normal response format from `claude_response_standards.md` (Summary, then Next steps). The phase report must contain:

- **Phase theme:** a heading for the finished phase, with one bullet per deliverable
- **Gate theme:** a heading that names the next phase and says work has stopped
- **Next steps:** "Start Phase N+1" as the recommended option, plus an "Adjust first" option

---

## 🗂️ Plan-Mode Phase Gates

- **Loads on its own from:** `rules/02_claude_standards/claude_working_practices/plan_mode_phase_gates.md`

---

## 📊 Plan file format

- **Loads with plan files from:** `rules/02_claude_standards/path_scoped_rules/plan_file_format.md` — through `paths:`, whenever a plan file is open
- **Read on demand:** `~/.claude/rules/02_claude_standards/path_scoped_rules/plan_file_format.md` — before writing a brand-new plan file, which opens no matching file first

---

## 🚫 Anti-patterns (what NOT to do)

- ❌ **Silent run:** complete all phases silently, then ask "Done?" at the end
- ❌ **Asking while acting:** ask "Ready to proceed?" while already starting Phase N+1
- ❌ **Wall of text:** summarise all phases as one massive wall of text instead of breaking by phase
- ❌ **Ignoring feedback:** ignore user feedback ("no, adjust this") and barrel forward anyway
- ❌ **Gating parallel work:** apply gates to parallel work where phases run concurrently

---

## 📚 Example

### ❌ Wrong: No gate, silent progress

User plans 3-phase work. Claude completes Phase 1, 2, and 3 without stopping for feedback. User discovers Phase 2 approach was misaligned and wasted effort.
