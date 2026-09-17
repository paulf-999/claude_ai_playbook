# 📊 Plan File Format

**Purpose:** Define how the persisted plan document (not the chat response) presents its phase breakdown, so every plan is scannable at a glance.

**When writing or updating a plan file** (the persisted `.md` document in `_plans/`, not the chat response), present the phase breakdown as a single table, not repeated headings with bullet lists.

**Columns:** Phase | Action | Test | Effort | Risk | Status — one row per phase.

**Bullet the Action and Test cells:** each is a bullet list, one sentence per bullet — never a single run-on sentence or a comma-spliced list. Use `•` bullets joined with `<br>` (standard markdown lists don't render inside table cells; this is the working pattern, already used elsewhere in `writing_style.md`).

**Each bullet:** emoji + leading bold keyword + colon, same as any other bullet under `writing_style.md` — e.g. `• 💾 **Backup:** create a full timestamped copy before touching anything`.

**Effort:** T-shirt size — XS, S, M, L, XL.

**Risk:** Low, Med, or High — how bad it is if this phase goes wrong (irreversibility, blast radius), independent of effort. A Small-effort phase can still be High-risk.

**Status:** Pending, In Progress, Done, or Blocked — this column replaces a separate prose "Progress log" section; update it as phases complete instead of maintaining both.

**Example:**

| Phase | Action | Test | Effort | Risk | Status |
|---|---|---|---|---|---|
| 0 | • 💾 **Backup:** timestamped copy before touching anything<br>• 🔒 **Why:** no VCS, only rollback path | • 🔢 **Count:** file count matches source<br>• 🔍 **Spot-check:** content byte-for-byte | S | Low | ⏳ Pending |
| 2 | • ✅ **Apply:** changes only to the "clean" set<br>• ⏭️ **Skip:** diverged or live-only files | • 🔀 **Diff:** against target — must be zero<br>• 🔎 **Grep:** re-run the stale-reference check | M | High | ⏳ Pending |

**Why:** a table keeps the whole phase sequence scannable in one glance — what, how verified, how big, how dangerous, and where it stands — without a separate log to keep in sync. Bulleted, one-sentence cells follow `writing_style.md`'s "one sentence per bullet" rule, which already covers plans.

**Not a replacement:** the "How to apply" format in the parent rule is the live chat progress report during execution — this table is the plan document's own record. `writing_style.md` still governs all other plan-file prose.

## 🔗 Related

- Parent: `_multi_phase_implementation_gates.md` — general phase-gate principle and chat-response format
- Sibling: `_plan_mode_phase_gates.md` — mandatory gating specifically in plan mode
