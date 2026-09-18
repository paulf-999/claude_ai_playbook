# ⏱️ Response Timing

**Purpose:** Define the mandatory timing-footer mechanics — how the elapsed time is measured and formatted at the end of every substantive response.

---

- **Start is injected:** The `UserPromptSubmit` hook fires before any reasoning and injects the submission time as `PROMPT_SUBMITTED_AT=<epoch>` — this is the timer start, so elapsed includes reasoning.
- **End timestamp:** As the very last action before finalizing, run a real `date +%s` and compute elapsed = end − `PROMPT_SUBMITTED_AT`. Never mention the check in the visible response.
- **Mandatory in all modes:** Always emit the footer, including in plan mode — never skip it and never fabricate the number; always run the real end timestamp.
- **Real numbers only:** The duration must be real — never fabricate or use a placeholder like "checking...".
- **Human-readable format:** Under 60 seconds show `Ss` (e.g. `45s`); 60 seconds or more show `Mmin Ss` (e.g. `1min 15s`).
- **Format:** On its own line after the offer line:
  ```
  Response time: 1min 15s
  ```
- **Skip for:** Short, single-fact answers or casual exchanges.

---

## 🔗 Related

- Parent: `claude_response_standards.md` — response format, delivery cadence
- Sibling: `_enforcement.md` — how this standard is enforced turn-to-turn
