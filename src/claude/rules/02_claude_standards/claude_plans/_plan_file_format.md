<!-- version: 1.5.0 -->
<!-- created: 2026-09-17 -->
<!-- updated: 2026-10-11 -->
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

## 🏷️ Plan status

Put one `**Plan status:**` line straight under the plan's H1, giving the whole plan's state — separate from the per-phase Status column.

| Plan status | Meaning | Set by |
|---|---|---|
| 📝 **Draft** | Written in plan mode and not yet approved, in `plans/` | Claude, when it first writes the plan |
| 🟢 **Active** | Approved and being worked on, possibly across sessions | Claude, when it saves the plan to `_plans/` |
| ⏸️ **Parked** | Kept for later, with no work happening now | Claude, only when the user says so |
| ✅ **Done** | Every phase is Done | Claude, in the same edit that marks the last phase Done |
| 🗑️ **Dropped** | Abandoned, and kept only as a record | Claude, only when the user says so |

- **Format:** `**Plan status:** 🟢 Active · updated 2026-10-11` — the emoji is optional, and the word must be one of the five above.
- **Updated date:** set it to today whenever a phase's Status cell or the plan status changes.
  - **Why:** the file's modified time resets on any edit or copy, so only this date says when work last moved.
- **Why:** phase cells alone can't tell a finished plan from an abandoned one, so plans still being acted on get lost among the rest.
- **Find them:** `make list_plans` groups plans by status and flags Active plans whose updated date is 14 or more days old, to park or drop.
- **Status folders:** `make clean_plans` files each saved plan into `_plans/<status>/` (`active/`, `parked/`, `done/`, `dropped/`), and each draft into `plans/draft/`, or `plans/archive/` after 14 days unchanged.
  - **Line wins:** the folder follows the status line, so change the line and the next run moves the file.
  - **Why archive drafts:** an approved draft was already copied into `_plans/`, so an old draft is almost always abandoned.

**Not a replacement:** the "How to apply" format in the parent rule is the live chat progress report during execution — this table is the plan document's own record. `writing_style.md` still governs all other plan-file prose.
