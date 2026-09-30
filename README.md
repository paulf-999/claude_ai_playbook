# 📖 Claude AI Playbook

This repo provides a starting point for every session across every project: how Claude should behave, what role it plays, what standards it follows, and how sessions should start and end.

---

## 🚀 Setup

### Getting started

Set the folder the config installs into, then run the install from your own terminal:

```bash
export CLAUDE_CONFIG_DIR="$HOME/claude"
make install
```

- **Preview first:** it shows the source, target and backup paths and the five install steps before changing anything.
- **Typed confirm:** type `install` to go ahead — any other answer cancels and nothing changes.
- **Your terminal only:** it refuses to run without a real terminal, so Claude can't run it for you.
- **Backup:** your existing config folder is moved to `~/.claude_backup_<timestamp>` before the new files are copied in.

> **First-time install:** open a new terminal after `make install` before running `claude`.

See [docs/quickstart.md](docs/quickstart.md) for the full walkthrough.

### Keeping up to date

When the playbook is updated, pull and re-run the install:

```bash
git pull
make install
```

- **Local edits:** any changes you made in `$CLAUDE_CONFIG_DIR` end up in the backup folder, so copy back anything you want to keep.

### What's installed

See [docs/whats_installed.md](docs/whats_installed.md) for a description of every category of file deployed into `~/.claude/` — rules, process, agents, commands, skills, and style guides.

---

## 💡 Using Claude well

### Best practices

This playbook operationalises the patterns from the [Claude Code best practices guide](https://docs.anthropic.com/en/docs/claude-code/best-practices).

### Training resources

See [docs/training.md](docs/training.md) for free training resources from Anthropic.

---

## 🤝 Contributing

### Testing

See [docs/testing.md](docs/testing.md) for what is tested and how to run tests locally.

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for branching, commit, and PR conventions.
