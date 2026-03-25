# 🧠 Claude AI Playbook

*Source of truth for version-controlled Claude workflows, personas, and session instructions.*

---

## Purpose

Defines the standard approach for using Claude, including:

- **Session startup instructions**
- **Workflows**
- **Personas**
- **Context templates**

These files are installed locally into `~/.claude/`.

---

## How It Works

- **`src/claude/`** → managed Claude files
- **`src/sh/claude/`** → install and update scripts
- **`~/.claude/`** → local runtime location

---

## Quick Start

Clone the repo:

```bash
git clone <repo-url>
cd claude_ai_playbook
````

Install the Claude files locally:

```bash
bash src/sh/claude/install_claude_files.sh
```

This will:

* create `~/.claude/` if needed
* copy managed files into it
* back up conflicting files if required

---

## Updating

Pull latest changes and re-sync:

```bash
git pull
bash src/sh/claude/update_claude_files.sh
```

---

## Repo Structure

```text
src/
  claude/
    commands/
    context/
    personas/
    session/
    workflows/

  sh/claude/
    bootstrap_claude_repo.sh
    install_claude_files.sh
    update_claude_files.sh
```

---

## Principles

* **Plan before execution**
* **Reuse standard workflows**
* **Keep instructions modular**
* **Update in Git, then sync locally**

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for branching, commit, and PR standards.
