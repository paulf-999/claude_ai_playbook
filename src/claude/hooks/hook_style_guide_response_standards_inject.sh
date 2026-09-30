#!/bin/bash
# version: 3.0.0
# created: 2026-09-07
# updated: 2026-09-30
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

# SKILL WAIVER CHECK: a prompt that invokes a skill by slash command
# (/<skill_name>) gets no injection when that skill's skill.contract.yaml
# declares waives_response_standards: true — the skill sets its own format.
# Natural-language skill runs and follow-up turns still get the directive.
CLAUDE_ROOT_DIR="$(dirname "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)")"
HOOK_INPUT="$(cat || true)"
SKILL_NAME="$(HOOK_INPUT="$HOOK_INPUT" python3 -c '
import json, os, re
try:
    prompt = json.loads(os.environ["HOOK_INPUT"]).get("prompt", "")
except (ValueError, AttributeError):
    prompt = ""
match = re.match(r"\s*/([a-z0-9_]+)(\s|$)", prompt if isinstance(prompt, str) else "")
print(match.group(1) if match else "")
')"
if [ -n "$SKILL_NAME" ]; then
  for contract in "${CLAUDE_ROOT_DIR}/skills/${SKILL_NAME}/skill.contract.yaml" \
                  "${CLAUDE_ROOT_DIR}"/skills/*/"${SKILL_NAME}"/skill.contract.yaml; do
    if [ -f "$contract" ] && grep -Eq '^waives_response_standards:[[:space:]]*true([[:space:]]|#|$)' "$contract"; then
      exit 0
    fi
  done
fi

read -r -d '' DIRECTIVE <<'EOF' || true
RESPONSE STANDARDS — apply to this response now. These rules apply in ALL modes, including plan mode. Skip only for short, single-fact answers or casual conversational exchanges.

- Open with a bold **Summary** label. Under it, present 3–4 themes. Format each theme as its own heading line — an emoji followed by a bold keyword, with NO leading dash and NO colon (it is a heading, not a bullet). Under each theme heading, put its point(s) as bullets, each starting with an emoji then ≤~15 words. Exactly ONE point per bullet — never merge two points into one bullet with a semicolon or comma; split them into separate bullets. Never repeat a theme. Example: a theme line `⏱️ **Timing**` followed by two bullets `- ✅ Footer humanized to Mmin Ss` and `- 🔁 Change mirrored to the playbook`.
- Next steps: when the answer implies actionable follow-ups, add a "**Next steps:**" block after the Summary — numbered options (1., 2., 3.). Format each numbered line as an emoji + bold keyword only (a heading; add "(recommended)" to the best one), then put its description as a child bullet beneath it (emoji + short concrete text, honour writing_style.md). Omit the block entirely when there are no meaningful next steps. Example: `1. ✅ **Commit now** (recommended)` followed by an indented child bullet `- 📦 Stage and commit the hook, rule, and test`.
- Nothing else may appear between the Summary (or the Next steps block, if present) and the offer line — no stray bullets, no partial lines. Citations, if any, go immediately before the offer line.
- After the Summary/Next steps, on its own line, ask whether to continue: use "⚡ Speed prioritised over verification — More detail, or verify first? (Y/N/V)" if speed was prioritised over full verification, otherwise "More detail? (Y/N)". If a Next steps block is present, append ", or pick a next step (1–N)". Wait for an explicit reply before proceeding.
- Timing (MANDATORY, including in plan mode): this prompt was submitted at PROMPT_SUBMITTED_AT=__START__ (Unix epoch seconds). Immediately before you compose your closing lines, run `date +%s` as your last tool call — it is read-only and permitted in plan mode — then compute elapsed = end value − PROMPT_SUBMITTED_AT. On its own line after the offer line, output "Response time: <D>" where <D> is the elapsed formatted human-readably: under 60 seconds as "Ss" (e.g. "45s"); 60 seconds or more as "Mmin Ss" (e.g. "1min 15s"). This is true wall-clock from prompt submission, so it INCLUDES reasoning time. Never write a placeholder such as "checking..."; if you have not yet run the end timestamp, run it now before finishing. Never fabricate the number.
- Prefer the fastest correct first pass; run independent tool calls in parallel.
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
