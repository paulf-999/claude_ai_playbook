# notify_pr — Setup: dmt-scripts-claude_ai_playbook

Configuration for posting PR notifications to the **dmt-scripts-claude_ai_playbook** Teams channel.

---

## Memory directory

`~/.claude/projects/-home-paul-git-repos-core-dmt-scripts-claude_ai_playbook/`

---

## teams_config.json

```json
{
  "webhook_url": "<paste Power Automate webhook URL here>",
  "channel_display_name": "dmt-scripts-claude_ai_playbook",
  "go_to_reviewers": {
    "uk_ireland": {
      "window": {"start": "06:00", "end": "16:00"},
      "handles": ["paul-fry_pyrc", "imelda-godswill_pyrc", "shane-orourke_pyrc"]
    },
    "north_america": {
      "window": {"start": "13:00", "end": "22:00"},
      "handles": ["nivedita-baliga_pyrc", "rajesh-rao_pyrc"]
    }
  },
  "layers": []
}
```

`layers` is set to `[]` — the DWH layers line is omitted from all messages in this channel.

---

## Webhook setup

1. In Teams, open the **dmt-scripts-claude_ai_playbook** channel.
2. Channel settings → **Manage channel** → **Connectors** → **Incoming Webhook** → Configure.
3. Name the webhook `dmt-scripts-claude_ai_playbook`.
4. Copy the URL and set it as `webhook_url` in the config above.
