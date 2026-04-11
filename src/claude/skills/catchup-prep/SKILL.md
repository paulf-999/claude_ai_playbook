---
name: catchup-prep
description: >
  Prepare for a 1-to-1 or weekly catch-up meeting with a manager. Use this skill
  whenever the user mentions an upcoming check-in, 1-to-1, weekly sync, or catch-up
  with their manager — even if they say "I have my weekly" or "I have a meeting with
  my manager". This skill guides the user through gathering topics, determining the
  core message, filtering what belongs in the meeting vs. async, prioritising items,
  time-boxing the agenda, and sense-checking it. Always trigger this skill proactively
  when the user mentions a manager meeting, even if they haven't explicitly asked for
  help preparing.
version: 0.1.0
maturity: draft
tags:
  criticality: should
  status: active
  tested: false
---

## Scope gate

This skill is at **draft** maturity. Claude behaviour is constrained accordingly:

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

Ask for (or infer from context):
- Who is the meeting with (manager name/role if known)
- How long is the meeting
- Is there anything the user already knows they want to raise

If the user gives a list of topics upfront, skip straight to Step 3.

---

## 🧠 Step 2 — Gather topics

Prompt the user for a brain-dump across these categories:

- **Wins / progress** — what have they delivered or moved forward recently?
- **Blockers** — anything they need help with or want to flag?
- **Team updates** — any direct report progress worth mentioning?
- **Strategic decisions** — any scope changes, de-prioritisations, or pivots?
- **Ongoing workstreams** — anything in flight worth keeping the manager informed on?

Encourage free-form input — you will filter and prioritise next.

---

## 🎯 Step 3 — Identify the core message

Ask: "What's the ONE thing you want your manager to walk away thinking?"

Offer these options or invite the user to write their own:
- "I'm back, on top of things, and moving forward"
- "I'm being strategic with my time and effort"
- "My team is progressing well despite obstacles"
- "I have good momentum on key initiatives"

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

Order the remaining items to reinforce the core message. Apply these principles:
- Lead with the strongest win — sets the tone immediately
- Strategic decisions near the top — show judgment and awareness
- Informational updates toward the end — important but not the headline
- Always leave 2 mins for the manager's items

Divide the meeting time across items. Flag which to drop first if time runs short.

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

Produce a clean, formatted agenda:

```
Meeting: [Title] — [Date] ([Duration])

YOUR ITEMS
1. [Item] (X mins) — [one-line framing note]
2. [Item] (X mins) — [one-line framing note]

SEND ASYNC BEFORE THE MEETING
- [Item] — [brief note]

IF TIME IS SHORT, DROP IN ORDER: [item] → [item] → [item]
```

---

## 💡 Tips

- **Framing beats content.** How an item lands matters as much as what it is.
- **One message, not seven.** Every item should feel like evidence for the same conclusion.
- **Async is a feature.** Sending updates before the meeting means the meeting can be strategic.
- **Returning from leave?** Lead with a human moment, then immediately follow with the strongest win.
