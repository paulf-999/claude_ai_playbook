# notify_pr — Setup Overview

Covers the `teams_config.json` schema, webhook setup steps, and the reviewer cache format. Each repo that uses `notify_pr` needs its own `teams_config.json` in the corresponding Claude project memory directory.

---

## teams_config.json schema

| Field | Required | Description |
|-------|----------|-------------|
| `webhook_url` | Yes | Power Automate incoming webhook URL for the Teams channel |
| `channel_display_name` | Yes | Human-readable channel name (used in error messages) |
| `go_to_reviewers` | Yes | Fallback reviewer pools when no reviewers are auto-assigned |
| `layers` | Yes | File prefix → label mappings for DWH layer detection. Set to `[]` to omit the DWH layers line from messages |

### go_to_reviewers structure

```json
"go_to_reviewers": {
  "uk_ireland": {
    "window": {"start": "06:00", "end": "16:00"},
    "handles": ["handle1_pyrc", "handle2_pyrc"]
  },
  "north_america": {
    "window": {"start": "13:00", "end": "22:00"},
    "handles": ["handle3_pyrc", "handle4_pyrc"]
  }
}
```

Windows are evaluated in UTC. When both windows overlap, both pools are merged.

### layers structure

```json
"layers": [
  {"prefix": "path/to/layer/", "label": "label"}
]
```

Set `"layers": []` to suppress the DWH layers line entirely from all messages posted to that channel.

---

## Webhook setup

1. In Teams, navigate to the target channel.
2. Channel settings → **Manage channel** → **Connectors** → **Incoming Webhook** → Configure.
3. Give the webhook a name matching the channel (e.g. `dmt-lib-airflow_dags`).
4. Copy the generated webhook URL.
5. Create or update `teams_config.json` in the repo's Claude memory directory with the URL.

Memory directory path: `~/.claude/projects/<cwd-with-slashes-replaced-by-dashes>/teams_config.json`

---

## github_teams_mapping.json cache

Stores resolved GitHub handle → Teams identity mappings to avoid repeated MCP lookups.

```json
{
  "alice-example_pyrc": {
    "display_name": "Alice Example",
    "aad_id": "00000000-0000-0000-0000-000000000000"
  }
}
```

- The cache file lives in the same directory as `teams_config.json`.
- `aad_id` equal to `"00000000-0000-0000-0000-000000000000"` is a placeholder — the skill will re-resolve it automatically via the Microsoft 365 MCP.
- `aad_id: null` means auto-resolve failed; the message will use a plain text `@DisplayName` instead of a clickable @mention.

---

## Per-repo config examples

- [airflow_dags.md](./airflow_dags.md) — `dmt-lib-airflow_dags` channel
- [claude_playbook.md](./claude_playbook.md) — `dmt-scripts-claude_ai_playbook` channel
