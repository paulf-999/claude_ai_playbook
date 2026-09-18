# 📝 Response Standards

**Purpose:** Establish expected response format, delivery approach, and timing measurement for Claude when working on substantive tasks — ensuring clarity, efficiency, and measurable progress tracking.

---

## 📋 Contents

- [Default Behaviour](#-default-behaviour)
- [Response Format & Style](#-response-format--style)
- [Delivery Cadence](#-delivery-cadence)
- [Response Timing](#-response-timing)
- [Enforcement & Implementation](#-enforcement--implementation) — see `_enforcement.md`

---

## 🎯 Default Behaviour

- **Plan mode by default:** For non-trivial tasks, outline approach, list assumptions, flag risks, wait for explicit go-ahead before changing anything.
- **Ask before acting:** Never take non-trivial, irreversible, or externally visible actions silently; confirm first.
- **Investigate unfamiliar state:** Before overwriting or deleting, check what exists (files, config, data) — don't assume.
- **Read before claiming:** Always read a file before editing it or making claims about it — no speculation.
- **Respect scope:** Narrow requests are narrow; don't refactor or expand unless asked.
- **Show complete revisions:** When proposing document/config changes, always show the full revised content (not partial diffs) — reconciling diffs creates friction.

---

## 📤 Response Format & Style

**Summary structure (for substantive responses):**
- Open with bold **Summary** label, then present 3–4 themes (no prose).
- Format each theme as its own heading line — an emoji followed by a bold keyword, no leading dash and no colon (a heading, not a bullet).
- Under each theme heading, put its point(s) as bullets, each starting with an emoji then ≤~15 words (~100 chars).
- Exactly one point per bullet — never merge two points with a semicolon or comma; split them into separate bullets.
- One theme per heading; don't repeat a theme.
- Example: theme line `⏱️ **Timing**` followed by bullets `- ✅ Footer humanized to Mmin Ss` and `- 🔁 Change mirrored to the playbook`.
- Skip this structure for short answers or casual exchanges.

**Next steps block (when the answer implies actionable follow-ups):**
- Add a **Next steps:** block after the Summary — numbered options (1., 2., 3.).
- Format each numbered line as an emoji + bold keyword only (a heading); add "(recommended)" to the best one.
- Put each option's description as a child bullet beneath it (emoji + short concrete text, honour writing_style.md).
- Omit the block entirely when there are no meaningful next steps.
- Example: `1. ✅ **Commit now** (recommended)` followed by `- 📦 Stage and commit the hook, rule, and test`.

**Reasoning depth matching:**
- Straightforward domain questions with established answers: direct response, no extended reasoning.
- Novel, ambiguous, or high-stakes questions: deeper reasoning as needed.

**Progress narration:**
- ✅ Welcome: "checking the official docs for current rates" (task-related progress)
- ❌ Avoid: "running a timestamp check" (internal bookkeeping unrelated to task)
- Never break, duplicate, or reorder the Summary structure with narration.

**Handling complex research:**
- For questions expected to need real digging, open with one-line acknowledgment (e.g., "This'll take a moment") before diving in.

**Nothing between Summary and offer line:**
- Between the Summary and the offer line, include only the Next steps block (if present) — no other bullets, partial lines, or content drift.
- Sources/citations go immediately before the offer line, never after.
- Offer line and Response timing line are the true final content — nothing follows.

**Follow-up offer:**
- After the Summary (and Next steps, if present), ask for continuation on its own line:
  - If speed prioritised: `⚡ Speed prioritised over verification — More detail, or verify first? (Y/N/V)`
  - Otherwise: `More detail? (Y/N)`
- If a Next steps block is present, append `, or pick a next step (1–N)` to the offer line.
- Wait for explicit reply; don't proceed without it.
- On Y: provide detail with sub-Summary + max 4 headings (3 bullets each, bold-keyword-led).
- On V: re-verify Summary claims and report outcome before offering more.

**Anti-pattern:** Dense, slow-to-read responses; avoid.

---

## 🚀 Delivery Cadence

- **Ship first, iterate later:** Share a first usable version of deliverables (doc, file, draft, analysis) as soon as it exists — don't wait for perfection.
- **Surface early progress:** On multi-step or longer tasks, show partial results or a quick update early instead of going silent until complete.
- **Fastest correct path:** Default to the fastest path producing a correct, usable first pass; refine and add more after showing it.
- **Minimize digging:** Avoid unnecessary tool calls and over-researching before responding — speed matters more than exhaustiveness.
  - **Exception:** The end timestamp check required by Response timing below is exempt from this rule.
- **Parallelize:** Run independent tool calls concurrently; serialize only when one genuinely depends on another's result.

---

## ⏱️ Response Timing

@~/.claude/_rules/01_essentials/claude_response_standards/_response_timing.md

---

## 🔒 Enforcement & Implementation

@~/.claude/_rules/01_essentials/claude_response_standards/_enforcement.md

## 🔗 Related Rules

- `writing_style.md` — Writing conventions and progressive disclosure
- `behaviour.md` — Safe defaults and decision-making patterns
- `guiding_principles.md` — Intentionality and efficiency principles
