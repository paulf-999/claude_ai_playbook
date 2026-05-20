# Skills — Work in Progress

Skills in this directory are in active development. They **are** installed by `make install` — each subdirectory is merged into `~/.claude/skills/` and is invokable via `/skill-name`.

The distinction from `skills/` is maturity, not availability: WIP skills are iterated on freely and may change behaviour between sessions.

| Skill | Status |
|---|---|
| `/ideas` | draft v0.1.0 — capture and browse Claude-related ideas via MCP memory server |
| `/release` | draft v0.1.0 — cut a GitHub Release for a completed phase; changelog from merged PRs |
| `/todos` | draft v0.1.1 — lightweight todo tracker backed by MCP memory server |
| `/plan_sprint` | WIP — Jira integration needs further testing; Confluence page creation now publishes to correct parent with full section structure (Executive Summary, Must, Should, Stretch Goals, Blocked, Not Picked Up) |

Archived skills (no longer in active development) are in `archive/` and are not installed.
