# ⚠️ MCP Server Toggling — Restart Requirement

**Purpose:** Explain why Claude Code must be restarted after toggling MCP servers and how to recover if you forget.

When you run `make enable_mcp server=<name>` or `make disable_mcp server=<name>`, the script modifies `~/.claude/settings.json`. **You must restart Claude Code immediately for changes to take effect.**

## 🔍 Why?

Claude Code caches settings at session startup. Even though `settings.json` is updated, the current session continues to use the cached configuration. This creates a confusing state where:
- MCP tool calls appear to hang (2–6 minutes)
- The session seems stuck, but actually it's fighting cached config

## ✅ What the fix does

- **mcp_toggle.py** exits with code 1 when changes are made, displaying a **BLOCKING message** that lists the server toggled and restart instructions
- **Makefile target** (`make enable_mcp`) shows as "failed," signaling user action needed
- **Session-start hook** checks for recent setting changes and shows a gentle reminder if needed

## 🔄 How to proceed

After running `make enable_mcp server=<name>` and seeing the restart message:

1. **Save your work** in Claude Code
2. **Close Claude Code completely** (exit all windows/tabs)
3. **Reopen Claude Code**
4. **Proceed** — MCP tool calls will work without hanging

If you forget to restart and see tool calls hanging, close and reopen Claude Code, then retry.
