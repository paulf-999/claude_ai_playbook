# Microsoft 365 MCP Connector Setup

Gives Claude access to Microsoft 365 — including Outlook email, Teams chat, SharePoint, and calendar — via Anthropic's first-party cloud connector. Unlike other MCP servers, this connector is not registered via the CLI; it is configured through the Claude web UI and authenticated via OAuth.

---

## Prerequisites

- An active Microsoft 365 account (Payroc work account).
- Access to [claude.ai](https://claude.ai) — the connector is configured in the web UI, but once enabled it is also available in Claude Code CLI sessions.

---

## Setup

This connector cannot be scripted. Complete the following steps manually:

1. Open [https://claude.ai](https://claude.ai) and sign in.
2. Go to **Settings → Connectors**.
3. Find **Microsoft 365** and click **Connect**.
4. Follow the OAuth prompts to authenticate with your Microsoft work account.

Reference: [Anthropic support article](https://support.claude.ai/en/articles/12542951)

---

## Verify

Once connected, start a Claude Code session and check that the Microsoft 365 tools are available:

```bash
claude mcp list
```

Microsoft 365 will not appear in this list — it is a cloud connector, not a registered MCP server. Instead, confirm availability by checking that `mcp__claude_ai_Microsoft_365__*` tools appear in your session (visible in the available tools list at session start).

---

## What it provides

| Tool category | Examples |
|---|---|
| Outlook email | Search, read, and draft emails |
| Teams chat | Search messages, read threads |
| Calendar | Search events, check availability |
| SharePoint | Search files and pages |

---

## Notes

- The connector authenticates against your personal Microsoft account — it cannot be pre-configured for another user.
- Re-authentication may be required periodically when the OAuth token expires.
- The connector is scoped to your own Microsoft 365 data — it does not provide access to other users' mailboxes or calendars unless delegated.
