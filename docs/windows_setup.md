# Windows Setup Guide — Claude CLI with Playbook

This guide sets up Claude Code on a Windows machine so it uses the team playbook. The playbook repo lives in WSL2 — there is no second clone to manage.

---

## Prerequisites

- Windows 10/11 with WSL2 installed
- The playbook repo cloned into WSL2 at `~/git_repos/claude_ai_playbook`
- `winget` available (built into Windows 10 1809+ and Windows 11)

---

## One-time setup

### Step 1 — Install Node.js on Windows

Open **Windows Terminal** (PowerShell or CMD — not WSL):

```powershell
winget install OpenJS.NodeJS.LTS
```

Close and reopen Windows Terminal after installation completes.

### Step 2 — Install Claude CLI on Windows

In a new **Windows Terminal** (PowerShell or CMD):

```powershell
npm install -g @anthropic-ai/claude-code
```

Verify:

```powershell
claude --version
```

### Step 3 — Sync the playbook to Windows

Open your **WSL2 terminal** and run:

```bash
cd ~/git_repos/claude_ai_playbook
make install_windows
```

This copies all playbook files from the WSL repo into `C:\Users\<your-username>\.claude\`. It preserves any existing Windows `.claude` state (sessions, settings, plugins).

### Step 4 — Open Claude in VS Code (Windows)

Open VS Code on Windows and open a terminal. Run:

```
claude
```

Claude Code will start using the playbook automatically — it reads from `C:\Users\<your-username>\.claude\CLAUDE.md`.

---

## Keeping the playbook up to date

Whenever the playbook repo is updated, pull and re-run both installs from your own WSL terminal:

```bash
cd ~/git_repos/claude_ai_playbook
git pull
make install          # WSL — previews, then asks you to type 'install'
make install_windows  # Windows C:\Users\<username>\.claude
```

Both install into Claude Code's default `.claude` folder — to use another folder, see the "Custom folder" note in the [quickstart](quickstart.md).

Restart any open Claude Code sessions after syncing to pick up the changes.

---

## Reference

| Command | What it does |
|---|---|
| `make install` | Full install for WSL (Claude CLI + MCP servers + plugins + config files) — also how you update |
| `make install_windows` | Sync playbook config files to Windows `.claude` (run from WSL) |
| `make update_windows` | Alias for `install_windows` |

---

## Troubleshooting

**`make install_windows` fails with "powershell.exe not found"**
You are not running from WSL2. Open a WSL terminal and retry.

**`make install_windows` fails with "Could not detect Windows username"**
WSL2 cannot reach the Windows environment. Check that WSL interop is enabled:
```bash
cat /proc/sys/fs/binfmt_misc/WSLInterop
```
The output should be `enabled`. If not, run `wsl.exe --shutdown` from Windows and restart.

**Claude on Windows does not show playbook behaviour**
Verify the files were copied:
```powershell
ls $env:USERPROFILE\.claude\CLAUDE.md
```
If missing, re-run `make install_windows` from WSL. If present, restart Claude Code.
