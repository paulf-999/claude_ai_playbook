# 📊 Omni MCP Server Setup

Gives Claude access to the Omni Analytics semantic layer — enabling natural language queries against governed data models directly from Claude Code.

---

## ✅ Prerequisites

- Claude Code CLI must be installed and available on `PATH`.
- An **Organisation Admin** must enable two settings in the Omni instance:
  - **MCP Server AI setting** — Settings > AI > General
  - **Personal Access Tokens (PATs)** — Settings > API Keys > Personal tokens

---

## 🛠️ Installation

### 🤖 Automated (recommended)

```bash
make install_mcp_server_omni
```

This opens a browser tab to complete OAuth authorisation. Omni creates a Personal Access Token linked to your account automatically.

### 🔧 Manual

```bash
claude mcp add --transport http omni https://callbacks.omniapp.co/callback/mcp --scope user
```

After running the command, start a session with `claude`, run `/mcp`, select Omni, and press Enter to authenticate via browser.

---

## 🔍 Verify

```bash
claude mcp list
```

You should see `omni` listed as a registered server.

---

## 🛠️ Available tools

| Tool | What it does |
|---|---|
| `pickModel` | Lists available Omni models — use to select which model to query |
| `pickTopic` | Lists topics within the selected model — use to scope the query |
| `getData` | Executes a natural language query against the selected model and returns results |
| `searchOmniDocs` | Searches Omni's product documentation |

---

## 📝 Notes

- If Claude Code returns a permission denied error in "don't ask" mode, start the session with:
  ```bash
  claude --allowed-tools 'mcp__omni__*'
  ```
  Or add `mcp__omni__*` to the `allow` list in `.claude/settings.json`.
- The server uses OAuth — no API key needs to be stored locally.

---

## 🔗 Reference

[Omni MCP — Claude Code setup guide](https://docs.omni.co/ai/mcp/claude-code)
