# 🐙 GitHub MCP Server Setup

Gives Claude read and write access to GitHub repositories (public and private) via the official GitHub MCP server — enabling issue management, PR creation, file browsing, and code search. Works on WSL/Ubuntu and macOS.

---

## ✅ Prerequisites

- Claude Code CLI must be installed and available on `PATH`.
- A GitHub Personal Access Token (PAT) of type **classic** with `repo` scope is required — create one at: https://github.com/settings/tokens/new

---

## 🛠️ Installation

### 🤖 Automated (recommended)

```bash
make claude-mcp SERVER=github
```

You will be prompted to enter your PAT. It is not stored anywhere — it is passed directly to the `claude mcp add-json` command.

### 🔧 Manual

```bash
claude mcp add-json github \
  '{"type":"http","url":"https://api.githubcopilot.com/mcp","headers":{"Authorization":"Bearer YOUR_PAT"}}' \
  --scope user
```

Replace `YOUR_PAT` with your token, or use an environment variable:

```bash
claude mcp add-json github \
  '{"type":"http","url":"https://api.githubcopilot.com/mcp","headers":{"Authorization":"Bearer '"${GITHUB_PAT}"'"}}' \
  --scope user
```

---

## 🔍 Verify

```bash
claude mcp list
```

You should see `github` listed as a registered server.

---

## 📝 Notes

- The `--scope user` flag makes the server available across all projects.
- The npm package `@modelcontextprotocol/server-github` is deprecated as of April 2025 — do not use it.
- If `claude mcp add-json` returns `Invalid input`, use the legacy HTTP transport format:

```bash
claude mcp add --transport http github https://api.githubcopilot.com/mcp \
  -H "Authorization: Bearer YOUR_PAT" --scope user
```
