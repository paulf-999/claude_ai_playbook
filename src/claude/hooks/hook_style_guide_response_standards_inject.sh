#!/bin/bash
# version: 4.0.0
# created: 2026-09-07
# updated: 2026-10-02
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
# Output: JSON on stdout with hookSpecificOutput.additionalContext, or the plain
# directive when jq is missing (Claude Code adds plain stdout to the context too).
# The directive is a short reminder: the full rules live in claude_response_standards.md,
# which is always loaded, and every injection stays in the transcript, so size adds up.

set -euo pipefail

# True start of the turn — the moment the prompt was submitted (pre-reasoning).
START=$(date +%s)

# SKILL WAIVER CHECK: a prompt that invokes a skill by slash command
# (/<skill_name>) gets no injection when that skill's skill.contract.yaml
# declares waives_response_standards: true — the skill sets its own format.
# Natural-language skill runs and follow-up turns still get the directive.
CLAUDE_ROOT_DIR="$(dirname "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)")"
HOOK_INPUT="$(cat || true)"

# Bad JSON, a non-object payload or a non-string prompt all read as an empty prompt.
PROMPT="$(jq -r 'if type == "object" and (.prompt | type) == "string" then .prompt else "" end' \
  <<<"$HOOK_INPUT" 2>/dev/null || true)"
SKILL_PATTERN='^[[:space:]]*/([a-z0-9_]+)([[:space:]]|$)'
if [[ "$PROMPT" =~ $SKILL_PATTERN ]]; then
  SKILL_NAME="${BASH_REMATCH[1]}"
  for contract in "${CLAUDE_ROOT_DIR}/skills/${SKILL_NAME}/skill.contract.yaml" \
                  "${CLAUDE_ROOT_DIR}"/skills/*/"${SKILL_NAME}"/skill.contract.yaml; do
    if [ -f "$contract" ] && grep -Eq '^waives_response_standards:[[:space:]]*true([[:space:]]|#|$)' "$contract"; then
      exit 0
    fi
  done
fi

read -r -d '' DIRECTIVE <<'EOF' || true
RESPONSE STANDARDS (full rules in claude_response_standards.md) — apply now, including plan mode. Skip only short, single-fact or casual replies.
- Open with a bold **Summary** label, then 3–4 themes. Each theme is a heading line (emoji + bold keyword, no dash or colon) followed by bullets: emoji + ≤~15 words, exactly one point each.
- When there are follow-ups, add a **Next steps:** block of numbered emoji + bold-keyword headings, marking the best "(recommended)", each with one child bullet.
- Then the offer line on its own: "More detail? (Y/N)" (or the ⚡ speed-prioritised variant), adding ", or pick a next step (1–N)" when Next steps is present. Nothing between the Summary block and the offer line.
- Timing: PROMPT_SUBMITTED_AT=__START__. Run `date +%s` as your last tool call, then put "Response time: <D>" on its own line after the offer line, as "45s" under a minute or "1min 15s" above. Never a placeholder or a guessed number.
EOF

# Substitute the real submission timestamp into the directive.
DIRECTIVE="${DIRECTIVE/__START__/$START}"

# Emit JSON when jq is available, otherwise the plain text, which Claude Code also adds as context.
if command -v jq >/dev/null 2>&1; then
  jq -n --arg context "$DIRECTIVE" \
    '{"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": $context}}'
else
  printf '%s\n' "$DIRECTIVE"
fi

exit 0
