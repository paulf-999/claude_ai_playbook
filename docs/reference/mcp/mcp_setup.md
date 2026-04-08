# 🔌 MCP Server Setup

MCP (Model Context Protocol) servers extend what Claude can access during a session — connecting it to external tools, APIs, and data sources. All servers are installed at user scope and are idempotent — safe to re-run.

---

## 🔗 Key integrations

```bash
make install_mcp_server_github    # prompts for GitHub PAT
make install_mcp_server_atlassian # opens browser for SSO
make install_mcp_server_o365      # prints manual setup instructions
```

| Server | Purpose |
|---|---|
| `github` | 🐙 Private GitHub repo access — see [`github_mcp_setup.md`](github_mcp_setup.md) |
| `atlassian` | 🔗 Jira and Confluence access via SSO — requires an active Atlassian account; opens browser to authenticate |
| `o365` | 🪟 Microsoft 365 (Outlook, Teams, SharePoint, Calendar) — cannot be configured via CLI; see [`o365_mcp_setup.md`](o365_mcp_setup.md) |

---

## ⚙️ Core servers

```bash
make install_core_mcp_servers
```

| Server | Purpose |
|---|---|
| `memory` | 💾 Persistent knowledge graph across sessions |
| `context7` | 📚 Up-to-date library and framework documentation |
| `sequential-thinking` | 🧠 Structured multi-step reasoning |
| `filesystem` | 🗂️ Broader file access beyond the current project (scoped to `$HOME`) |
