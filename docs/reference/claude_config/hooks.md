# Claude Code Hooks

Hooks are shell commands or prompts that Claude Code runs automatically in response to events during a session. They let you enforce team standards without relying on Claude to remember — the hook runs regardless of what Claude does.

---

## How hooks work

Hooks are configured in `~/.claude/settings.json` under the relevant event key. Each hook has a `matcher` (a regex against the tool name) and one or more `hooks` entries of type `command` or `prompt`.

```json
{
  "PostToolUse": [
    {
      "matcher": "Edit|Write",
      "hooks": [
        {
          "type": "command",
          "command": "bash ~/.claude/hooks/lint_on_edit.sh"
        }
      ]
    }
  ]
}
```

**Exit behaviour for `command` hooks:**
- Exit `0` — stdout is shown in the Claude transcript
- Exit `2` — stderr is fed back to Claude as an error (Claude will attempt to fix it)

---

## Event types

| Event | When it fires |
|---|---|
| `PreToolUse` | Before a tool executes — can approve or deny the action |
| `PostToolUse` | After a tool completes — ideal for linting, formatting, logging |
| `Stop` | When Claude considers stopping — can verify task completion before allowing it |
| `SessionStart` | At the start of a session — useful for loading context or state |

---

## Team-relevant examples

### 1. Lint Python files after edit

Runs `ruff` whenever Claude edits or writes a Python file. Claude will see any lint errors and attempt to fix them.

`~/.claude/hooks/lint_python_on_edit.sh`:
```bash
#!/bin/bash
# Passed the edited file path via CLAUDE_TOOL_INPUT_FILE_PATH
FILE="${CLAUDE_TOOL_INPUT_FILE_PATH:-}"
[[ "$FILE" == *.py ]] || exit 0
ruff check "$FILE" 1>&2
```

`~/.claude/settings.json`:
```json
{
  "PostToolUse": [
    {
      "matcher": "Edit|Write",
      "hooks": [
        {
          "type": "command",
          "command": "bash ~/.claude/hooks/lint_python_on_edit.sh"
        }
      ]
    }
  ]
}
```

---

### 2. Run shellcheck after editing shell scripts

`~/.claude/hooks/shellcheck_on_edit.sh`:
```bash
#!/bin/bash
FILE="${CLAUDE_TOOL_INPUT_FILE_PATH:-}"
[[ "$FILE" == *.sh ]] || exit 0
shellcheck "$FILE" 1>&2
```

Add to `PostToolUse` alongside the Python hook:
```json
{
  "matcher": "Edit|Write",
  "hooks": [
    {
      "type": "command",
      "command": "bash ~/.claude/hooks/shellcheck_on_edit.sh"
    }
  ]
}
```

---

### 3. Verify task completion before Claude stops

Prompts Claude to confirm tests were run and the task is fully complete before it stops responding.

```json
{
  "Stop": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "prompt",
          "prompt": "Before stopping, verify: were tests run after any code changes? Were all parts of the task addressed? If anything is incomplete, continue working rather than stopping."
        }
      ]
    }
  ]
}
```

---

## When to use hooks vs. CLAUDE.md rules

| Use a hook | Use a CLAUDE.md rule |
|---|---|
| You want something enforced automatically, regardless of Claude's behaviour | You want to guide Claude's decisions and planning |
| The check can be expressed as a shell command or exit code | The guidance requires judgement or context |
| You want Claude to see and fix the output (exit 2) | You want Claude to avoid the problem in the first place |

In practice: CLAUDE.md rules shape intent; hooks enforce outcomes.

---

## Setup

Hooks are configured manually in `~/.claude/settings.json`. This file also stores your MCP server configuration, so edit it carefully — do not overwrite existing content.

If `settings.json` does not exist yet, create it:

```bash
touch ~/.claude/settings.json
```

Then add the relevant hook configuration from the examples above.
