# 🪝 Enforcement hooks — decisions

## 🎯 Why hooks instead of rules alone

- **Why:** rules are guidance — Claude can rationalize ignoring them. Hooks fire automatically and inject the rule content at the point of violation, making it harder to bypass silently.
- **Note:** hooks don't guarantee compliance; they raise the cost of ignoring a rule by surfacing the constraint exactly when it's relevant.

## ⚡ Soft inject vs. hard block

- **Soft inject (`hookSpecificOutput.additionalContext`):** used when the action is valid but context is missing — `mkdir` under `~/.claude/`, unscoped reads, multi-step prompts. The hook adds the relevant rule; the action proceeds.
- **Hard block (`decision: block`):** used only when the action should not proceed without review — new file creation under `~/.claude/` where naming hasn't been confirmed.
- **Rule:** default to soft inject; only hard block when the action is irreversible or when proceeding without review causes lasting harm.

## 🔄 Lifecycle event choices

| Hook | Event | Reason |
|---|---|---|
| `hook_enforcement_naming_convention.sh` | PreToolUse (Write) | Block before the file is created — naming can't be fixed after the fact without a rename. Denies only names with an error under `test_file_structure_compliance.py`, which it calls for that one path |
| `hook_enforcement_writing_style.sh` | PostToolUse (Edit/Write) | Inject style reminder after an edit — the edit is valid, but style compliance should follow |
| `hook_style_guide_response_standards_inject.sh` | UserPromptSubmit | Only place to act before Claude starts reasoning — adds the response-format reminder to every prompt |

- **Removed 2026-08-07:** `enforcement_subagent_reads.sh` and `enforcement_task_tracking.sh` were dropped with the rest of the hooks section — see the audit trail in `settings_json_readme.md`.

## 🧪 Test suite

- **Why:** hooks are shell scripts consuming JSON from stdin and outputting JSON to stdout — behaviour can be verified deterministically with pytest + subprocess.
- **Location:** `_tests/hooks/<type>/test_<type>_<domain>.py` — mirrors the hook naming convention (e.g. `enforcement/test_enforcement_naming_convention.py`).
- **Pattern:** tests use the shared `run_hook(hook, payload)` helper in `_tests/hooks/hook_test_utils.py`, which pipes JSON to the hook via stdin, then assert on stdout/returncode.
- **Note:** tests must pass before a hook is registered in `settings.json`.
