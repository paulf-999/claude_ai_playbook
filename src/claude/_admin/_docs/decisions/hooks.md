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
| `enforcement_naming_convention.sh` | PreToolUse (Write) | Block before the file is created — naming can't be fixed after the fact without a rename |
| `enforcement_writing_style.sh` | PostToolUse (Edit/Write) | Inject style reminder after an edit — the edit is valid, but style compliance should follow |
| `enforcement_dir_structure.sh` | PreToolUse (Bash) | Soft inject before `mkdir` — structure decisions should be intentional |
| `enforcement_subagent_reads.sh` | PreToolUse (Read) | Nudge before a large read — the most effective point to redirect to a sub-agent |
| `enforcement_task_tracking.sh` | UserPromptSubmit | Only place to intercept the prompt — detects multi-step intent before any action starts |

## 🧪 Test suite

- **Why:** hooks are shell scripts consuming JSON from stdin and outputting JSON to stdout — behaviour can be verified deterministically with pytest + subprocess.
- **Location:** `_tests/hooks/test_enforcement_<name>.py` — mirrors the hook naming convention.
- **Pattern:** each test file provides a `run_hook(payload)` helper that pipes JSON to the hook via stdin, then asserts on stdout/returncode.
- **Note:** tests must pass before a hook is registered in `settings.json`.
