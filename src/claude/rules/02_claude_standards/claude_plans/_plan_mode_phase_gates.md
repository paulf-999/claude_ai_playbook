<!-- version: 3.0.1 -->
<!-- created: 2026-09-17 -->
<!-- updated: 2026-10-01 -->
# 🗂️ Plan-Mode Phase Gates

**Purpose:** Apply phase gates without exception in plan mode — a plan's whole point is structured, checkpointed progression.

In plan mode, stop after each phase and wait for the user's explicit approval before starting the next.

**Why plans require gates:**
- Plans articulate structured intent; phases represent distinct decision boundaries
- Early feedback (after Phase 1) prevents wasted effort on subsequent phases based on stale assumptions
- Plan mode is *designed* for intentional progression — gates are not optional

**Report format:** use the phase report described in the parent `claude_plans.md` → How to apply, which follows the normal Summary + Next steps format.

Wait for the user's explicit response before starting the next phase, and treat silence as no approval.

## 🗂️ Plan approval

- 🗂️ **Plan approval:** "Implement the following plan:" is not confirmation — wait for an explicit go-ahead before making any changes.
  - ⚠️ **Exception 1:** `~/.claude/TODO.md` is pre-authorized for editing during plan mode (task logging; non-risky bookkeeping; no permission needed). **Why:** Read-only content; editing doesn't risk the task.
  - ⚠️ **Exception 2:** Explicit slash commands (`/skill_name` or `/command_name`) run without a confirmation prompt. **Why:** the slash command is the user's explicit intent.

## 📁 Persist the plan to `_plans/`

Claude Code's plan-mode harness assigns a scratch plan file under `~/.claude/plans/<slug>.md` — auto-generated, no underscore, not date-prefixed. That is the *only* file editable during plan mode, but it is not the durable plan archive.

- 📤 **Copy on exit:** the moment `ExitPlanMode` is approved and before any implementation step begins, copy the finalized plan content into `<config-dir>/_plans/<date>_<topic>.md`, where `<config-dir>` is the absolute path of `$CLAUDE_CONFIG_DIR` (or `~/.claude` when it's unset), date-prefixed per `writing_style.md`'s drafts/errors convention, formatted per `_plan_file_format.md`.
- ⚠️ **Resolve `~` before calling Write, every time:** the Write tool requires an absolute path and does not perform shell tilde-expansion — a literal `~` argument creates a real directory named `~` under whatever the current working directory happens to be, not the home directory. Always substitute the actual absolute config path (e.g. `/Users/<you>/.claude/_plans/...`, or your `$CLAUDE_CONFIG_DIR`'s path) before the call.
  - **Incident (2026-09-19):** exactly this happened — a prior session wrote the persisted plan to a literal `~/claude/_plans/...` path while the cwd was a project repo, creating `<repo>/~/claude/_plans/<slug>.md` inside that repo instead of the real archive. Confirmed via the stray file's content matching the plan actually being implemented in the following session.
- 🗑️ **Scratch file is disposable:** once copied, the harness-assigned `~/.claude/plans/<slug>.md` file is no longer the source of truth — don't reference it in later turns or in the persisted plan's own content.
- ✅ **Why:** the harness's plan-mode file lives in an auto-generated location outside version control and outside `_plans/`'s naming convention — without this step, approved plans never reach the durable, indexed archive.
