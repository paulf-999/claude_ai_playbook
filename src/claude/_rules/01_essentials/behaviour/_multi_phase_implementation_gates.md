# 🚪 Multi-Phase Implementation Gates

**Purpose:** Establish review/approval gates after each phase of multi-phase implementations, preventing wasted effort and enabling course correction.

---

## 🎯 Core principle

**Pause after each phase.** When implementing a multi-phase plan (3+ phases), complete one phase, then stop and request explicit approval before proceeding to the next phase.

**Why:** Early feedback catches misalignments before effort is wasted on subsequent phases. User can correct course, adjust scope, or deprioritize based on results from each phase.

---

## ⚙️ When to apply

**Apply gates when:**
- Implementing a plan with 3+ distinct phases (sequential, not parallel)
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

**Format:**

```
✅ Phase N complete.

**Deliverables:**
- Item 1: what was done
- Item 2: what was done

**Ready for Phase N+1:** [description]

Proceed? (yes/no/adjust)
```

---

## 🚫 Anti-patterns (what NOT to do)

- ❌ Complete all phases silently, then ask "Done?" at the end
- ❌ Ask "Ready to proceed?" while already starting Phase N+1
- ❌ Summarize all phases as one massive wall of text; break by phase
- ❌ Ignore user feedback ("no, adjust this") and barrel forward anyway
- ❌ Apply gates to parallel work where phases run concurrently

---

## 📚 Examples

### ✅ Correct: Multi-phase with gates

```
✅ Phase 1: Exploration — complete

**Deliverables:**
- Identified 12 existing rules in 01_essentials/
- Documented 3 potential consolidation opportunities
- No blockers found

**Ready for Phase 2:** Audit quality across rules + score each dimension

Proceed? (yes/no/adjust)
```

### ❌ Wrong: No gate, silent progress

User plans 3-phase work. Claude completes Phase 1, 2, and 3 without stopping for feedback. User discovers Phase 2 approach was misaligned and wasted effort.

---

## 🔗 Related rules

- Parent: `behaviour.md` — safe action defaults; decision-making patterns
- Sibling: `_decision_making.md` — when to present options vs. decide unilaterally
- Reference: `~/.claude/_rules/03_reference/claude_operational_efficiency.md` — turn budgets, context preservation

---
