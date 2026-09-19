# 🗂️ Plan-Mode Phase Gates (MANDATORY)

**Purpose:** Make phase gates non-negotiable specifically in plan mode — a plan's whole point is structured, checkpointed progression.

**Phase gates are MANDATORY in plan mode.** When a user creates or enters a multi-phase plan, explicit approval between phases is non-negotiable. Do NOT proceed to the next phase without explicit user confirmation.

**Why plans require gates:**
- Plans articulate structured intent; phases represent distinct decision boundaries
- Early feedback (after Phase 1) prevents wasted effort on subsequent phases based on stale assumptions
- Plan mode is *designed* for intentional progression — gates are not optional

**Plan-mode execution format (same structure, absolute requirement):**

```
✅ Phase N: [Phase Name] — complete

**Deliverables:**
- [Item 1]: specific output or discovery
- [Item 2]: specific output or discovery

**Ready for Phase N+1:** [brief description of next phase]

Proceed? (yes/no/adjust)
```

**CRITICAL:** Wait for explicit user response. Do NOT proceed automatically.

**Example: Audit plan with mandatory gates**

```
✅ Phase 1: Scan — complete

**Deliverables:**
- Scanned 47 files in src/claude/
- Identified 12 deviations from standard

**Ready for Phase 2:** Analyze root causes + score by severity

Proceed? (yes/no/adjust)
```

**Example: Feature plan with mandatory gates**

```
✅ Phase 1: Design — complete

**Deliverables:**
- Designed component structure with 3 integration points
- Identified 2 dependencies to resolve first

**Ready for Phase 2:** Implement component + wire dependencies

Proceed? (yes/no/adjust)
```

**Example: Infrastructure plan with mandatory gates**

```
✅ Phase 1: Explore — complete

**Deliverables:**
- Gathered requirements from 4 stakeholders
- Mapped existing infrastructure constraints

**Ready for Phase 2:** Provision test environment

Proceed? (yes/no/adjust)
```

**Key rule:** Phase gates in plan mode are **BLOCKING**. User approval is always required; never skip or assume approval.

## 🗂️ Plan approval

- 🗂️ **Plan approval:** "Implement the following plan:" is not confirmation — wait for an explicit go-ahead before making any changes.
  - ⚠️ **Exception 1:** `~/.claude/TODO.md` is pre-authorized for editing during plan mode (task logging; non-risky bookkeeping; no permission needed). **Why:** Read-only content; editing doesn't risk the task.
  - ⚠️ **Exception 2:** Explicit slash commands (`/skill_name` or `/command_name`) bypass plan-mode gates entirely — NEVER ask permission, execute immediately. **Why:** Slash command IS user's explicit intent; asking for confirmation defeats the entire purpose of direct invocation. Do NOT show any confirmation prompts or options.

## 📁 Persist the plan to `_plans/`

Claude Code's plan-mode harness assigns a scratch plan file under `~/.claude/plans/<slug>.md` — auto-generated, no underscore, not date-prefixed. That is the *only* file editable during plan mode, but it is not the durable plan archive.

- 📤 **Copy on exit:** the moment `ExitPlanMode` is approved and before any implementation step begins, copy the finalized plan content into `~/.claude/_plans/<date>_<topic>.md`, date-prefixed per `writing_style.md`'s drafts/errors convention, formatted per `_plan_file_format.md`.
- 🗑️ **Scratch file is disposable:** once copied, the harness-assigned `~/.claude/plans/<slug>.md` file is no longer the source of truth — don't reference it in later turns or in the persisted plan's own content.
- ✅ **Why:** the harness's plan-mode file lives in an auto-generated location outside version control and outside `_plans/`'s naming convention — without this step, approved plans never reach the durable, indexed archive.

## 🔗 Related

- Parent: `claude_plans.md` — general phase-gate principle and chat-response format
- Sibling: `_plan_file_format.md` — how to format the persisted plan document itself
