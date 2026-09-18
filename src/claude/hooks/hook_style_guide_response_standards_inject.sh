#!/bin/bash
# hook_style_guide_response_standards_inject.sh
#
# Per-turn salience injection for Response Standards.
# Fires on UserPromptSubmit (before Claude responds) and emits a compact,
# imperative version of the response-standards directive as additionalContext.
#
# This mirrors the Desktop/Cowork experience: the same directive text enforces
# reliably there because it sits at high salience right next to generation. In
# Claude Code the always-on rule import is diluted to low-salience background by
# response time, so we re-inject the directive each turn at the high-salience slot.
#
# Timing: the hook fires at prompt-submission time (before any reasoning), so it
# captures the TRUE start timestamp and injects it as PROMPT_SUBMITTED_AT. The
# model then only needs a single end timestamp — elapsed spans reasoning too.
#
# Lifecycle event: UserPromptSubmit
# Output: JSON on stdout with hookSpecificOutput.additionalContext

set -euo pipefail

# True start of the turn — the moment the prompt was submitted (pre-reasoning).
START=$(date +%s)

# SKILL WAIVER CHECK: If a skill declares it waives response standards,
# skip injection entirely. Skills set SKILL_WAIVES_RESPONSE_STANDARDS=true
# to enable custom output formats (e.g. interactive multi-phase workflows).
# This check allows skills like confluence_create_page to produce free-form
# interactive prompts instead of Summary + Next steps format.
if [ "${SKILL_WAIVES_RESPONSE_STANDARDS:-false}" == "true" ]; then
  # Waiver is active — exit cleanly without injecting response standards
  exit 0
fi

read -r -d '' DIRECTIVE <<'EOF' || true
RESPONSE STANDARDS — apply to this response now. These rules apply in ALL modes, including plan mode. Skip only for short, single-fact answers or casual conversational exchanges.

- Open with a bold **Summary** label. Under it, present 3–4 themes. Format each theme as its own heading line — an emoji followed by a bold keyword, with NO leading dash and NO colon (it is a heading, not a bullet). Under each theme heading, put its point(s) as bullets, each starting with an emoji then ≤~15 words. Exactly ONE point per bullet — never merge two points into one bullet with a semicolon or comma; split them into separate bullets. Never repeat a theme. Example: a theme line `⏱️ **Timing**` followed by two bullets `- ✅ Footer humanized to Mmin Ss` and `- 🔁 Change mirrored to the playbook`.
- Next steps: when the answer implies actionable follow-ups, add a "**Next steps:**" block after the Summary — numbered options (1., 2., 3.). Format each numbered line as an emoji + bold keyword only (a heading; add "(recommended)" to the best one), then put its description as a child bullet beneath it (emoji + short concrete text, honour writing_style.md). Omit the block entirely when there are no meaningful next steps. Example: `1. ✅ **Commit now** (recommended)` followed by an indented child bullet `- 📦 Stage and commit the hook, rule, and test`.
- Nothing else may appear between the Summary (or the Next steps block, if present) and the offer line — no stray bullets, no partial lines. Citations, if any, go immediately before the offer line.
- After the Summary/Next steps, on its own line, ask whether to continue: use "⚡ Speed prioritised over verification — More detail, or verify first? (Y/N/V)" if speed was prioritised over full verification, otherwise "More detail? (Y/N)". If a Next steps block is present, append ", or pick a next step (1–N)". Wait for an explicit reply before proceeding.
- Timing (MANDATORY, including in plan mode): this prompt was submitted at PROMPT_SUBMITTED_AT=__START__ (Unix epoch seconds). Immediately before you compose your closing lines, run `date +%s` as your last tool call — it is read-only and permitted in plan mode — then compute elapsed = end value − PROMPT_SUBMITTED_AT. On its own line after the offer line, output "Response time: <D>" where <D> is the elapsed formatted human-readably: under 60 seconds as "Ss" (e.g. "45s"); 60 seconds or more as "Mmin Ss" (e.g. "1min 15s"). This is true wall-clock from prompt submission, so it INCLUDES reasoning time. Never write a placeholder such as "checking..."; if you have not yet run the end timestamp, run it now before finishing. Never fabricate the number.
- Match reasoning depth to complexity; prefer the fastest correct first pass; run independent tool calls in parallel.
EOF

# Substitute the real submission timestamp into the directive.
DIRECTIVE="${DIRECTIVE/__START__/$START}"

# Emit JSON safely (directive contains asterisks, quotes, em dashes, newlines).
DIRECTIVE="$DIRECTIVE" python3 - <<'PY'
import json, os
context = os.environ["DIRECTIVE"]
print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": context,
    }
}))
PY

exit 0
