# Permission Modes

Permission modes control what Claude can do automatically versus what requires your explicit approval. The team default is `plan` — set in `src/claude/settings.json` and applied automatically on every session.

---

## Modes

| Mode | What Claude can do | When to use |
|---|---|---|
| `default` | Read files and run tools; prompts before each write or shell command | General use when you want visibility into every action |
| `plan` | Read and analyse only; no file writes or shell commands until you approve | **Team default** — safe starting point for any session |
| `acceptEdits` | Auto-approves file edits without prompting; still prompts for shell commands | Rapid iteration where you trust the direction and want less friction |
| `bypassPermissions` | Skips almost all prompts | Automated pipelines in isolated environments (containers, VMs) only |

> **Warning — `bypassPermissions`:** This mode skips most safety prompts. Only use it in fully isolated environments. It is never appropriate for interactive developer sessions.

---

## How it is configured

### Default mode (repo setting)

`src/claude/settings.json` sets the default for all sessions:

```json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

This is installed to `~/.claude/settings.json` by `make install` and updated by `make update`.

### Override for a single session (CLI flag)

```bash
claude --permission-mode acceptEdits
```

Valid values: `default`, `plan`, `acceptEdits`, `bypassPermissions`.

### Escalating mid-session

To move from `plan` to `acceptEdits` during a session, exit plan mode when Claude asks for confirmation — Claude will prompt you to choose a mode at that point.

---

## Recommended usage

- **Start every session in `plan` mode** (the default). Review Claude's proposed approach before approving changes.
- **Switch to `acceptEdits`** only when you are iterating quickly on a well-understood task and the risk of an unreviewed edit is low.
- **Never use `bypassPermissions`** in an interactive session on a shared or production machine.
