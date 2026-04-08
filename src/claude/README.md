# 🤖 Claude Config

Files installed into `~/.claude/` by `make install`. Everything here shapes how Claude behaves across all sessions and projects.

| File / Directory | Purpose |
|------------------|---------|
| [`CLAUDE.md`](CLAUDE.md) | 🔗 Root config — imports all rules, process, and style guides via `@` directives |
| [`context.md`](context.md) | 📝 Session context — updated at the end of each session via `/wrap_up` |
| [`settings.json`](settings.json) | ⚙️ Claude Code settings — team baseline configuration |
| [`agents/`](agents) | 🤖 Sub-agent personas for core and DMT-specific roles |
| [`commands/`](commands/README.md) | ⚡ Slash commands available during a Claude Code session |
| [`process/`](process/README.md) | 🔄 Session structure — startup checklist, planning, and wrap-up |
| [`rules/`](rules/README.md) | 📏 Hard rules Claude must follow across all sessions |
| [`skills/`](skills/README.md) | 🛠️ Reusable multi-step workflows invoked via `/skill-name` |
| [`style_guide_standards/`](style_guide_standards/README.md) | 🎨 Language-specific style guides (Python, SQL, Bash) |
