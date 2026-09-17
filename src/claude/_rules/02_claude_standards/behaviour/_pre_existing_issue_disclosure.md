# 🚩 Pre-Existing Issue Disclosure

**Purpose:** Ensure pre-existing issues found during scoped work always reach the user, instead of being silently fixed (scope creep) or silently absorbed into "out of scope" (findings get lost).

---

## 🎯 Core principle

**Always surface it.** When work on a task turns up a bug, stale reference, broken import, lint debt, or doc drift that predates the current task and isn't part of what was asked, tell the user — every time, not just when it's convenient or blocking.

**Why:** A finding that's silently fixed hides scope creep from the user. A finding that's silently ignored because "it's out of scope" disappears — the user has no way to know it exists unless they ask, which they can only do if they already suspect it.

---

## ⚙️ When to apply

**Applies whenever, during any task:**
- A pre-existing bug or regression is discovered that the current task didn't cause
- A broken reference, import, or link predates the change being made
- Lint, test, or structural debt surfaces that isn't attributable to the current work
- Documentation or comments describe a reality that no longer matches the code

**Distinguish from:**
- Issues the current task *did* cause — those get fixed as part of the task, not just disclosed
- Issues already known and previously disclosed to the user in this session — no need to re-report the same finding every time it's re-verified, a brief reference back is enough

---

## 📋 How to apply

1. **Name it specifically** — what's broken, where, one line
2. **State whether it's pre-existing** — confirm against a baseline (git history, a backup, prior behavior) rather than assuming
3. **State the disposition** — fixed now, flagged for later, or explicitly left alone, and why
4. **Don't bury it** — a findings section or a direct callout, not a footnote inside an unrelated paragraph

**Format (in a phase report, PR description, or chat response):**

```
🚩 Pre-existing: [what's broken], confirmed via [baseline check].
Disposition: [fixed / flagged, not fixed — reason]
```

---

## 🚫 Anti-patterns (what NOT to do)

- ❌ Fixing a pre-existing issue silently because it was easy, without mentioning it
- ❌ Deciding something is "out of scope" and moving on without telling the user it exists
- ❌ Bundling a pre-existing fix into a commit/PR without calling it out separately in the description
- ❌ Assuming something is pre-existing without checking a baseline — verify, don't guess

---

## 🔗 Related rules

- Parent: `behaviour.md` — safe action defaults; decision-making patterns
- Sibling: `_decision_making.md` — when to present options vs. decide unilaterally
- Sibling: `claude_plans.md` — phase reports are a natural place to disclose findings

---
