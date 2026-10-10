<!-- version: 1.2.2 -->
<!-- created: 2026-09-18 -->
<!-- updated: 2026-10-02 -->
<!-- miss_cost: low — the enforcement hook changes without its tests -->
<!-- loading: lazy — only matters when changing the response-format hook or its tests -->
# 🔒 Response Standards Enforcement

**Purpose:** Explain the mechanism that keeps response formatting reliable turn-to-turn, and where its implementation lives.

---

## 🔒 Enforcement

This standard is enforced by **per-turn salience injection** (the "crawl" mechanism). A `UserPromptSubmit` hook re-emits a compact, imperative version of this directive as `additionalContext` before every response — placing it at high salience right next to generation, mirroring how the same text enforces reliably in Desktop/Cowork.

**Why injection, not post-response validation:**
- **Root cause:** ⚠️ The always-on rule import is diluted to low-salience background by response time.
- **Same text, opposite outcome:** 📊 Desktop enforces reliably with near-identical wording, purely from salient placement.
- **Cheapest faithful mirror:** 💸 Injection reproduces the Desktop position at zero LLM cost — no model call per turn.

**When the standard is waived (Claude self-applies):**
- ❌ Short answers (<50 words) — single fact, direct reply, casual exchange
- ❌ Skill invocation output — skill determines format, not this standard
- ❌ Code output, command results — raw pass-through, no validation
- ❌ Error messages or debugging output — brief, unstructured content is OK
- ❌ Inline code blocks or raw data — validation applies only to prose responses

**Decision rule:** If a response is substantive AND involves tool calls OR extends beyond a few sentences, the standard applies — unless explicitly waived above.

---

## 🛠️ Implementation

Enforcement is implemented via the injection hook: `~/.claude/hooks/hook_style_guide_response_standards_inject.sh`

- **Event:** `UserPromptSubmit` — fires before Claude responds (the high-salience slot).
- **Behaviour:** Emits the compact directive (Summary format, offer line, timing footer) as `hookSpecificOutput.additionalContext` on stdout.
- **Timing start:** Injects `PROMPT_SUBMITTED_AT=<epoch>` captured at prompt submission (pre-reasoning) so the footer spans reasoning time; the model runs only the end timestamp.
- **Cost:** Zero LLM cost; a small per-turn context injection — salience, not volume, is what makes it work.
- **Skill waiver:** a prompt starting with `/<skill_name>` gets no injection when that skill's `skill.contract.yaml` sets `waives_response_standards: true`; natural-language skill runs and follow-up turns still get it.

**Test coverage:** `_tests/hooks/response_standards/test_style_guide_response_standards_inject.py` — asserts the hook exits 0 and emits valid JSON whose `additionalContext` contains the required markers (`**Summary**`, `More detail? (Y/N)`, `Response time: Xs`) plus a real injected `PROMPT_SUBMITTED_AT` start timestamp.

**Future path (the "walk" escalation) — build only if injection proves insufficient:**
- **Mechanism:** 🚪 A `type:"prompt"` `Stop` hook that runs an LLM to validate each finished response and force correction.
- **Trade-off:** ⚖️ Hard mechanical guarantee, but incurs a model call on every substantive turn (cost + latency).
- **Reserved asset:** 🧪 The post-response validator `hook_style_guide_response_standards.sh` (+ its `_flags` and `_waivers` tests) is retained for this path — it is not wired into `settings.json` today.
- **Kept on purpose:** 🛡️ `test_hook_registry_utils.py` lists it in `RESERVED_HOOKS`, so deleting it, wiring it in, or dropping its RESERVED header note fails the suite until that list is updated too.
