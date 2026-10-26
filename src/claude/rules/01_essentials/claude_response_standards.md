<!-- version: 3.1.5 -->
<!-- created: 2026-09-07 -->
<!-- updated: 2026-10-26 -->
<!-- applies_to: * -->
<!-- miss_cost: medium — replies in the wrong shape, which the user asks to redo -->
<!-- loading: always-on — shapes every substantive reply -->
# 📝 Response Standards

**Purpose:** Establish expected response format, delivery approach, and timing measurement for Claude when working on substantive tasks — ensuring clarity, efficiency, and measurable progress tracking.

---

## 📋 Contents

- [Default Behaviour](#-default-behaviour)
- [Response Format & Style](#-response-format--style)
- [Delivery Cadence](#-delivery-cadence)
- [Response Timing](#-response-timing)
- [Enforcement & Implementation](#-enforcement--implementation) — read on demand

---

## 🎯 Default Behaviour

- **Plan mode by default:** For Medium and Complex tasks (tiers in `_before_acting.md`), outline approach, list assumptions, flag risks, and wait for explicit go-ahead before changing anything.
- **Ask before acting:** Never take irreversible or externally visible actions silently, at any tier; confirm first.
- **Investigate unfamiliar state:** Before overwriting or deleting, check what exists (files, config, data) — don't assume.
- **Read before claiming:** Always read a file before editing it or making claims about it — no speculation.
- **Respect scope:** Narrow requests are narrow; don't refactor or expand unless asked.
- **Show complete revisions:** When proposing document/config changes, always show the full revised content (not partial diffs) — reconciling diffs creates friction.

---

## 📤 Response Format & Style

**Summary structure (for substantive responses):**
- **Label:** open with a bold **Summary** label, then present 3–4 themes (no prose).
- **Theme lines:** format each theme as its own heading line — an emoji followed by a bold keyword, no leading dash and no colon (a heading, not a bullet).
- **Bullets:** under each theme heading, put its point(s) as bullets, each starting with an emoji then ≤~15 words (~100 chars).
- **One point each:** split two points into separate bullets rather than joining them with a semicolon or comma.
- **No repeats:** give each theme one heading, and don't repeat a theme.
- **Example:** theme line `⏱️ **Timing**` followed by bullets `- ✅ Footer humanised to Mmin Ss` and `- 🔁 Change mirrored to the playbook`.
- **Skip:** leave this structure out for short answers or casual exchanges.

**Next steps block (when the answer implies actionable follow-ups):**
- **Placement:** add a **Next steps:** block after the Summary — numbered options (1., 2., 3.).
- **Option lines:** format each numbered line as an emoji + bold keyword only (a heading), and add "(recommended)" to the best one.
- **Descriptions:** put each option's description as a child bullet beneath it (emoji + short concrete text, honour writing_style.md).
- **Omit:** leave the block out entirely when there are no meaningful next steps.
- **Example:** `1. ✅ **Commit now** (recommended)` followed by `- 📦 Stage and commit the hook, rule, and test`.

**Progress narration:**
- ✅ **Welcome:** "checking the official docs for current rates" (task-related progress)
- ❌ **Avoid:** "running a timestamp check" (internal bookkeeping unrelated to task)
- **Structure intact:** never break, duplicate, or reorder the Summary structure with narration.

**Handling complex research:**
- **Acknowledge first:** for questions expected to need real digging, open with a one-line acknowledgement (e.g., "This'll take a moment") before diving in.

**Nothing between Summary and offer line:**
- **Only Next steps:** between the Summary and the offer line, include only the Next steps block (if present) — no other bullets, partial lines, or content drift.
- **Sources:** put sources and citations immediately before the offer line, never after.
- **Last lines:** the offer line and Response timing line are the true final content, with nothing after them.

**Follow-up offer:**
- **Offer line:** after the Summary (and Next steps, if present), ask for continuation on its own line:
  - **Speed prioritised:** `⚡ Speed prioritised over verification — More detail, or verify first? (Y/N/V)`
  - **Otherwise:** `More detail? (Y/N)`
- **With Next steps:** append `, or pick a next step (1–N)` to the offer line.
- **Wait:** get an explicit reply before proceeding.
- **On Y:** provide detail with sub-Summary + max 4 headings (3 bullets each, bold-keyword-led).
- **On V:** re-verify Summary claims and report outcome before offering more.
- **Anti-pattern:** avoid dense, slow-to-read responses.

---

## 🚀 Delivery Cadence

- **Ship first, iterate later:** Share a first usable version of deliverables (doc, file, draft, analysis) as soon as it exists — don't wait for perfection.
- **Surface early progress:** On multi-step or longer tasks, show partial results or a quick update early instead of going silent until complete.
- **Fastest correct path:** Default to the fastest path producing a correct, usable first pass; refine and add more after showing it.
- **Minimise digging:** Avoid unnecessary tool calls and over-researching before responding — speed matters more than exhaustiveness.
  - **Exception:** The end timestamp check required by Response timing below is exempt from this rule.
- **Parallelise:** Run independent tool calls concurrently; serialise only when one genuinely depends on another's result.

---

## ⏱️ Response Timing

- **Start is injected:** The `UserPromptSubmit` hook fires before any reasoning and injects the submission time as `PROMPT_SUBMITTED_AT=<epoch>` — this is the timer start, so elapsed includes reasoning.
- **End timestamp:** As the very last action before finalising, run a real `date +%s` and compute elapsed = end − `PROMPT_SUBMITTED_AT`.
  - **Silent:** never mention the check in the visible response.
- **Every mode:** emit the footer on every reply that the skip rule below doesn't cover, including in plan mode, always from a real end timestamp.
- **Real numbers only:** The duration must be real — never fabricate or use a placeholder like "checking...".
- **Human-readable format:** Under 60 seconds show `Ss` (e.g. `45s`); 60 seconds or more show `Mmin Ss` (e.g. `1min 15s`).
- **Format:** On its own line after the offer line:
  ```
  Response time: 1min 15s
  ```
- **Skip for:** Short, single-fact answers or casual exchanges.

---

## 🔒 Enforcement & Implementation

- **Read on demand:** `~/.claude/_rules_lazy_load/claude_config/response_standards_enforcement.md` — when changing how this standard is enforced (the per-turn injection hook and its tests).
