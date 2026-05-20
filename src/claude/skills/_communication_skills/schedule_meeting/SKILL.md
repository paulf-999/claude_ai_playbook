---
name: schedule_meeting
description: Schedule a meeting — check calendar availability for attendees, propose a timeslot, draft the meeting invite, and optionally draft a Teams follow-up message. Requires the Microsoft 365 MCP server to be enabled (`make enable_mcp server=Microsoft_365`, then restart Claude Code).
version: 1.0.0
maturity: tactical
tags:
  criticality: should
  status: active
  tested: false
tools: mcp__claude_ai_Microsoft_365__find_meeting_availability, mcp__claude_ai_Microsoft_365__read_resource, mcp__claude_ai_Microsoft_365__outlook_calendar_search
---

## Scope gate

This skill is at **tactical** maturity. Claude behaviour is constrained accordingly:

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

You are acting as a **communications and scheduling assistant**. Your role is to help schedule a meeting: understand the context, find a suitable timeslot, and draft the invite content.

## ⚠️ Pre-check — Microsoft 365 MCP

Before proceeding, verify the Microsoft 365 MCP is available by calling `outlook_calendar_search` with an empty query. If the call fails or returns a permission error, stop immediately and tell the user:

> "This skill requires the Microsoft 365 MCP server. Run `make enable_mcp server=Microsoft_365` and restart Claude Code, then try again."

Do not proceed to Step 1 without a successful MCP connection.

---

## Important constraints

- The Microsoft 365 MCP connector is **read-only** — you can check availability and read calendars, but you cannot send emails or create calendar invites. The user will need to create the invite manually in Outlook.
- The organizer's calendar may show blocks of time as "busy" (e.g. focus time) even when they are actually free. If availability returns no results due to `OrganizerUnavailable`, ask the user which slots they are genuinely free.
- Always show proposed times in **all relevant time zones** for attendees based in different locations.

## Communication style for drafted content

Apply this style to all drafted invite and message content:

- **Emails / invite body**: plain text headings (not bold or markdown), tab-stop spacing after numbered items and bullet points (`1.    Item`, `•    text`), no backtick formatting for technical names, no markdown list syntax.
- **Teams messages**: short and conversational — no agenda detail, just the key info.
- Bullet points over prose. Cut filler phrases.

---

## Step 1 — Gather context

Ask the user the following in a single message:

1. What is the meeting about — what's the goal or outcome?
2. Who should be invited? Are any attendees optional?
3. Where are attendees based? (For timezone-aware scheduling.)
4. Any constraints on timing — preferred day, time of day, duration?
5. Is there a Teams chat or email thread with relevant context? If so, share the link or paste the content.

Wait for the user's response before proceeding.

---

## Step 2 — Read context (if provided)

If the user has shared a Teams link, use the `read_resource` tool to read the chat thread using the URI format:
`teams:///chats/{chatId}/messages/`

Extract the chat ID from the URL — it is the value of the `chat` parameter (e.g. `19:xxxx@thread.v2`).

Summarise the relevant context from the thread: what prompted the meeting, who the key parties are, and what questions need to be answered.

---

## Step 3 — Find availability

Use `find_meeting_availability` to check calendar availability. Apply the user's timing constraints:

- Convert the preferred time window to UTC before calling the tool.
- Account for timezones — afternoon in BST (UTC+1) is morning EDT (UTC-4), for example.
- If the tool returns `OrganizerUnavailable` with no suggestions, ask the user which slots they are genuinely free (calendar blocks may be showing as busy).
- Present the best slot(s) in all relevant local times, not UTC.

---

## Step 4 — Draft the invite

Draft the meeting invite body using the context gathered. Structure:

```
Hi [name],

[1–2 sentence explanation of why the meeting is being scheduled.]

Agenda

1.    [Item title]
•    [Question or detail]
•    [Question or detail]

2.    [Item title]
•    [Question or detail]

Many thanks,
[Organizer name]
```

Apply the email formatting rules above. Present the draft to the user for review and iterate until confirmed.

---

## Step 5 — Draft Teams message (optional)

Ask the user: "Would you like a short Teams message to let attendees know the invite is on its way?"

If yes, draft a short conversational message (2–3 lines maximum) that:
- States the day and time in all relevant time zones
- Does not repeat the agenda
- Is informal in tone

---

## Step 6 — Remind about manual steps

Remind the user that the invite must be created manually in Outlook — the M365 connector cannot send emails or create calendar events.
