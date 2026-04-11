# 💰 Rules — Efficiency

All users operate under a $200/month Claude credit limit. Every interaction consumes credits — minimise unnecessary usage without sacrificing correctness, output quality, or response speed.

---

## 🔁 Avoid redundant tool calls

- Do not re-read files or re-fetch data already retrieved in the same session.
- Before making a tool call, check whether the result is already available from earlier in the conversation.

---

## 🤖 Sub-agent discipline

- Do not spawn sub-agents unless the task genuinely requires parallelism or context isolation.
- One sub-agent where one will do — do not parallelise for its own sake.

---

## ✂️ Response conciseness

- Keep responses concise — do not pad output or restate what a diff or tool result already shows.
- Prefer targeted queries (filtered fields, paginated results) over large payload fetches.

---

## ⚖️ The exception

Never sacrifice correctness, output quality, or response speed to save credits. If the cheaper approach produces a worse result or takes longer for the user, use the better one.
