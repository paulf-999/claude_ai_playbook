---
name: weekly_one_to_one_prep
description: >
  Prepare for a 1-to-1 or weekly catch-up meeting with a manager. Use this skill
  whenever the user mentions an upcoming check-in, 1-to-1, weekly sync, or catch-up
  with their manager — even if they say "I have my weekly" or "I have a meeting with
  my manager". This skill guides the user through gathering topics, determining the
  core message, filtering what belongs in the meeting vs. async, prioritising items,
  time-boxing the agenda, and sense-checking it. Always trigger this skill proactively
  when the user mentions a manager meeting, even if they haven't explicitly asked for
  help preparing.
version: 1.1.0
maturity: tactical
tags:
  criticality: should
  status: active
  tested: false
---

## Scope gate

This skill is at **tactical** maturity. Claude behaviour is constrained accordingly:

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

# 📋 Catch-up / 1-to-1 Meeting Prep

Help the user walk into their meeting with:
- A clear core message (the one thing they want their manager to take away)
- A tightly prioritised, time-boxed agenda
- A plan for what to handle async instead
- Confidence in how each item will land

Follow the steps below in order. Ask one question at a time — do not present multiple prompts as a wall of text.

---

## 🔍 Step 1 — Get meeting context

### Quick-start (standing meetings)

If a standing meeting default is known from memory or prior session context, offer
it before asking for context:

> "Is this your usual weekly 1-to-1 with your manager (30 mins)?
> Confirm to skip setup, or give me different details."

If confirmed, load those defaults and skip straight to Step 2.
If not confirmed, fall back to the standard context questions below.

### Standard context questions

Ask for (or infer from context):
- Who is the meeting with (manager name/role if known)
- How long is the meeting
- Is there anything the user already knows they want to raise

If the user gives a list of topics upfront, skip straight to Step 3.

### Previous output

Check `~/_drafts/meetings/` for a previous catchup file (e.g. `YYYY-MMM-DD.md`). If one exists, surface the most recent one — it provides continuity context (open items, blockers carried forward, tone that landed well).

---

## 🧠 Step 2 — Gather topics

### Proactive git scan

Before asking the user, check active git repos for commits since the last meeting (typically the past 7 days). Surface a grouped summary of activity by theme — this prompts the user's memory and saves them having to reconstruct their week manually. Present it as candidate topics, not a final list.

### Brain-dump prompt

Then ask the user to add anything the git scan missed, across these categories:

- **Wins / progress** — what have they delivered or moved forward recently?
- **Blockers** — anything they need help with or want to flag?
- **Team updates** — any direct report progress worth mentioning?
- **Roles / time split** — how did they spend their time this week? Were they wearing multiple hats (e.g. planner, mentor, engineer)? Was the split intentional or forced? This is often worth surfacing explicitly to the manager.
- **Planning / strategic admin** — any roadmap revision, re-prioritisation work, ticket hygiene (e.g. business value tabs), or stakeholder alignment done this week? These activities are invisible unless explicitly named; surface them.
- **Strategic decisions** — any scope changes, de-prioritisations, or pivots?
- **Ongoing workstreams** — anything in flight worth keeping the manager informed on?

Encourage free-form input — you will filter and prioritise next.

---

## 🎯 Step 3 — Reframe through a business lens, then identify the core message

Before picking the core message, reframe the raw topic list through a business priority lens:
- What is the business impact of each item?
- Which items close a loop the manager is already tracking?
- Which signal strategic judgment or proactive management?
- Which are purely operational and better handled async?

Present the reframed topic list to the user for confirmation before proceeding.

Then ask: "What's the ONE thing you want your manager to walk away thinking?"

Offer these options or invite the user to write their own:
- "Train is back on the tracks — and I'm keeping it there"
- "I'm being deliberate about where I spend my time across multiple roles"
- "My team is progressing well despite obstacles"
- "I have good momentum on key initiatives"
- "I'm managing platform dependencies proactively"

Everything in the agenda should reinforce this message.

---

## 🔄 Step 4 — Filter: meeting vs. async

Review the full topic list with the user. Ask which items could be sent as a quick Slack or email update instead of taking up meeting time.

**Good async candidates:**
- Pure status updates with no decision needed
- Items that don't require discussion
- Things the manager just needs to be aware of

**Keep in the meeting:**
- Items needing input, approval, or alignment
- Wins worth saying out loud
- Strategic decisions or context shifts

---

## ⏱️ Step 5 — Prioritise and time-box

Map each item to one of the four output categories:

| Category | What goes here |
|---|---|
| **WINS / PROGRESS** | Deliveries, unblocks, cross-team collaboration, momentum |
| **TEAM** | Direct report progress, coaching notes, capacity flags |
| **BLOCKERS / ESCALATIONS** | Items in someone else's court, risks, dependencies |
| **MANAGER'S ITEMS** | Always last; always 2 mins |

Order within each category to reinforce the core message:
- Lead with the strongest win — sets the tone immediately
- Strategic decisions and escalations near the top of their section
- Informational updates toward the end
- Always leave 2 mins for the manager's items

**Bullet discipline:** Aim for no more than 3 bullets per agenda item. If you have more, combine related points or move the lowest-value detail to async. The goal is a doc shared with the manager — every bullet must earn its place.

---

## 🔬 Step 6 — Sense-check framing

Review each item's framing:
- Does it reinforce the core message?
- Is it framed as something achieved or decided, not something not yet done?
- Is there any context that reframes a "gap" as an adaptation?
- Is the language confident without being defensive?

Suggest reframes where needed.

---

## 🤝 Step 7 — Handle "manager goes first"

Remind the user that their manager may lead. Advise:
- Let them — don't wrestle the agenda back early
- Find the natural "anything from you?" moment
- If time gets tight, know the priority order to drop items gracefully

---

## 📝 Step 8 — Output the final agenda

Use the template at `~/.claude/skills/_meetings_skills/weekly_one_to_one_prep/catchup_template.md` as the output format.
If the file exists, read it and follow the structure exactly. Key points:

- Open with `# [Meeting title] — [Date]`
- Follow immediately with `**Core message:**` — one sentence, the thing [manager name confirmed in Step 1] walks away thinking
- Section order: ✅ WINS / PROGRESS → 👥 TEAM → 🚧 BLOCKERS / ESCALATIONS → MANAGER'S ITEMS
- Use emoji on section headings (✅, 👥, 🚧) — no emoji on MANAGER'S ITEMS
- Number each item. **No timings in headings.**
- **No editorial framing notes under headings.** Do not add lines like `— Lead with this; closes the loop from last week`. The heading and bullets carry the framing.
- **Scannability:** keep bullets tight and punchy — the agenda is shared as a doc and must be readable cold. Avoid wordy multi-sentence bullets; prefer bold keyword prefix + short phrase.
- **Bullet format:** every bullet uses a bold keyword prefix — `- **Keyword:** text`. This applies at every level. Sub-bullets follow the same pattern. Example: `- **Status:** Not blocking — pipeline working today`
- Use sub-bullets for nested detail (e.g. ownership chains, named contributors). Flat bullets should not exceed 3 per item; combine or drop if more accumulate.
- **Blocker heading format:** `[TICKET-REF](link) — topic description`. The blocking/not-blocking signal belongs in a `- **Status:**` bullet, not the heading.
- Always reserve the last 2 mins for manager's items
- Do **not** add an `IF TIME IS SHORT` section or a `SEND ASYNC BEFORE THE MEETING` section

### Save the output

After producing the agenda:
1. Save it to `~/_drafts/meetings/YYYY-MMM-DD.md`
2. Add a row to the past outputs table in `~/.claude/skills/_meetings_skills/weekly_one_to_one_prep/catchup_template.md`:

| Date | File |
|---|---|
| `YYYY-MMM-DD` | `YYYY-MMM-DD.md` |

---

## 💡 Tips

- **Framing beats content.** How an item lands matters as much as what it is.
- **One message, not seven.** Every item should feel like evidence for the same conclusion.
- **Async is a feature.** Sending updates before the meeting means the meeting can be strategic.
- **Returning from leave?** Lead with a human moment, then immediately follow with the strongest win.
