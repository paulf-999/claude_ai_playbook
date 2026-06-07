# 🔌 MCP Server Setup

MCP (Model Context Protocol) servers extend what Claude can access during a session — connecting it to external tools, APIs, and data sources. All servers are installed at user scope and are idempotent — safe to re-run.

---

## 🔒 Enable / disable integration servers

Integration servers (GitHub, Atlassian) are **disabled by default** via `deniedMcpServers` in `settings.json`. Enable only what the current task requires; disable when finished.

```bash
# Enable for a session
make enable_mcp server=github
make enable_mcp server=atlassian
make enable_mcp server=dev      # group: github
make enable_mcp server=docs     # group: atlassian
make enable_mcp server=all      # all integration servers

# Disable when done
make disable_mcp server=github
make disable_mcp server=all
```

Restart Claude Code after toggling. `make update` resets to the default disabled state.

Core servers (context7, memory, sequential-thinking, filesystem) are always active — they are utility servers with no external API calls.

---

## 🔗 Key integrations

```bash
make install_mcp_server_github    # prompts for GitHub PAT
make install_mcp_server_omni      # opens browser for OAuth
make install_mcp_server_atlassian # opens browser for SSO
make install_mcp_server_o365      # prints manual setup instructions
```

| Server | Purpose |
|---|---|
| `github` | 🐙 Private GitHub repo access — see [`github_mcp_setup.md`](github_mcp_setup.md) |
| `omni` | 📊 Omni Analytics — natural language queries against governed data models — see [`omni_mcp_setup.md`](omni_mcp_setup.md) |
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

---

## 🧪 Evaluating a new MCP server

Before adopting a new MCP server, work through this checklist:

| Question | Notes |
|---|---|
| **What problem does it solve?** | Is this genuinely not covered by existing servers or Claude's built-in tools? |
| **Who maintains it?** | Official (Anthropic or the vendor) vs. community-maintained — prefer official where available |
| **Transport and auth** | HTTP (OAuth/SSO) or stdio (npx/local process)? What credentials does it require and where are they stored? |
| **Security** | Does it need access to sensitive data (prod credentials, PII)? Apply least-privilege — scope to read-only where possible |
| **Stability** | Is it versioned and actively maintained? Check for open issues and last release date |
| **Install complexity** | Can it be added to `install_mcp_servers.sh` and made idempotent? |

Only proceed if there is a clear, justified use case. Log the decision (what it solves, why adopted, any security considerations) in a new setup doc under `docs/reference/claude_config/mcp/`.

---

## 🔭 Candidates for future evaluation

MCP servers relevant to the team's stack that are worth investigating when the need arises:

| Tool | What to look for |
|---|---|
| Snowflake | Natural language queries against Snowflake — check for an official Snowflake or Anthropic-supported server; evaluate read-only scoping carefully given prod data access |
