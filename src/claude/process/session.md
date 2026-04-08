# 📋 Session

## 🚀 At the start of every session

IMPORTANT: Call the `EnterPlanMode` tool NOW, before outputting any text or taking any other action. Do not respond to the user until planning mode is active. Then complete the steps below before addressing the user's first message.

**Step 1 — Context**
Read all imported context files. Summarise the current project context in 2-3 sentences so I can confirm you have loaded it correctly.

**Step 2 — Task**
Prompt: "What is the task for this session?" Wait for my response before doing anything.

---

## 🏁 At the end of a session

When I say "wrap up", produce a context update in this format:

**Project:** ...
**What changed:** ...
**Decisions made:** ...
**Open questions:** ...
**Known issues:** ...

I will paste this into `context.md`.
