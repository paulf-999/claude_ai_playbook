# 🔌 install_mcp_servers.sh

Installs a named MCP server (or all core servers) into Claude at user scope. Takes a single argument identifying the target server.

## 🔄 Flow

```mermaid
flowchart TD
    A[🔤 Argument: server name] --> B{🔀 Route}
    B -- core --> C[🔌 Install all npx servers + filesystem]
    B -- context7 / sequential-thinking / memory --> D[install_npx_server]
    B -- filesystem --> E[install_filesystem_server]
    B -- github --> F[🔑 Prompt for PAT → install via HTTP]
    B -- atlassian --> G[🌐 Install via HTTP — opens browser for SSO]
    B -- o365 --> H[📋 Print manual setup instructions]
    B -- unknown --> I[❌ Error + exit 1]

    D --> J{Already registered?}
    E --> J
    J -- yes --> K[⏭️ Skip]
    J -- no --> L[claude mcp add] --> M[✅ Verify registration]
```

## 🗂️ Servers

| Server | Group | Install method | Prerequisite |
|---|---|---|---|
| `context7` | core | npx | none |
| `sequential-thinking` | core | npx | none |
| `memory` | core | npx | none |
| `filesystem` | core | npx, scoped to `$HOME` | none |
| `github` | optional | HTTP | PAT with `repo` scope |
| `atlassian` | optional | HTTP + SSO | opens browser |
| `o365` | optional | manual only | Claude web UI |

## 🚀 Usage

```bash
# Install all core servers
bash src/sh/claude/install_mcp_servers.sh core

# Install a single server
bash src/sh/claude/install_mcp_servers.sh github
bash src/sh/claude/install_mcp_servers.sh atlassian

# Via make targets
make install_core_mcp_servers
```

## ⚠️ Prerequisites

- Must be run from the repo root.
- Requires `claude` CLI on `PATH` — except for `o365`, which only prints manual setup instructions.
