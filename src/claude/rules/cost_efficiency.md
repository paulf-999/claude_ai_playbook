# 💰 Rules — Efficiency

All users operate under a $200/month Claude credit limit. Every interaction consumes credits — minimise unnecessary usage without sacrificing correctness, output quality, or response speed.

---

## 🔁 Avoid redundant tool calls

- Do not re-read files or re-fetch data already retrieved in the same session.
- Before making a tool call, check whether the result is already available from earlier in the conversation.

---

## 🤖 Sub-agent discipline

- Before orchestrating: ask whether a single, well-prompted call would answer this. If yes, stop — every added pattern is an added failure mode.
- Do not spawn sub-agents unless the task genuinely requires parallelism or context isolation.
- One sub-agent where one will do — do not parallelise for its own sake.
- When spawning a sub-agent, brief it fully — goal, surrounding context, what has already been tried, and the expected output shape. It has no memory of the current conversation; references like "based on our conversation" will produce irrelevant work.
- When a task involves reading more than 3 files, editing across more than one directory, or a search → edit cycle, automatically use the task brief pattern — do not wait to be asked. Write `/tmp/task_brief_<slug>.md`, pass the path to the appropriate sub-agent (see `process/task_brief.md` for sub-agent selection), then read only `/tmp/task_output_<slug>.md` on return. Do not re-read files the sub-agent already processed.

---

## 🎯 Model routing

Match model capability to task complexity — do not default every sub-agent call to the same model:

- Use `haiku` for lightweight sub-agents: exploration, lookups, file reads, and classification tasks.
- Use `sonnet` (default) for standard work — code generation, multi-step reasoning, and editing tasks.
- Reserve `opus` for the most complex architectural or analytical work where quality is paramount.

Set the `model` parameter on the Agent tool: `"haiku"`, `"sonnet"`, or `"opus"`.

---

## 💾 Prompt caching

When building Claude API integrations, apply `cache_control` markers to repeated context —
system prompts, large reference documents, and tool definitions. A well-placed cache breakpoint
reduces token cost by up to 80% on subsequent calls that share the same context prefix.

Use the `claude-api` skill (`/claude-api`) for any Claude API / Anthropic SDK work — it
enforces prompt caching by default.

---

## ✂️ Response conciseness

- Keep responses concise — do not pad output or restate what a diff or tool result already shows.
- Prefer targeted queries (filtered fields, paginated results) over large payload fetches.

---

## ⚖️ The exception

Never sacrifice correctness, output quality, or response speed to save credits. If the cheaper approach produces a worse result or takes longer for the user, use the better one.
