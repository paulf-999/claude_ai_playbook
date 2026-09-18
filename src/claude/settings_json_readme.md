# ⚙️ settings.json Reference

This file documents the Claude Code settings configuration. Each setting is justified by a guiding principle or observed workflow need.

See `~/.claude/_rules/guiding_principles.md` for the decision framework applied to all settings.

---

## Core Settings

### `permissions.defaultMode: "plan"`

**What it does:** Every Claude Code session starts in plan mode, requiring explicit user approval before any code execution.

**Why:** Prevents accidental code changes on non-trivial tasks. Aligns with the principle "ask first" in `_rules/behaviour.md`.

**When set:** 2026-08-07 (fixed from top-level placement to correct `permissions` nesting)

**Guiding principle:** Explicit over implicit — visible choice beats silent execution.

---

### `permissions.allow` (22 safe commands)

**What it does:** Pre-approved commands that don't require a permission prompt on every invocation. Reduces friction on routine dev operations.

**Why:**
- Git operations are safe (read-only reads, staged commits, pushes to feature branches)
- `gh` CLI for GitHub is read-only with our restrictions
- `find` and `grep` are text-only, non-destructive
- All patterns use wildcards or specific flags to prevent mutations

**When set:** Incrementally; see commit history for per-command additions

**Guiding principle:** Intentionality gates everything — each pattern earned its place via observed usage (transcript audit).

**Current patterns:**

| Pattern | Justification | Usage |
|---------|--------------|-------|
| `Bash(find:*)` | File discovery (non-destructive) | Common codebase search |
| `Bash(gh api:*)` | GitHub API reads (GET requests safe via flags) | Issue/PR inspection |
| `Bash(gh issue:*)` | Read GitHub issues | Common workflow |
| `Bash(gh pr:*)` | Read GitHub PRs | Very common |
| `Bash(gh repo view:*)` | Inspect repository metadata | Occasional |
| `Bash(gh run:*)` | View CI/CD runs | Occasional |
| `Bash(git -C:*)` | Run git commands in other directories | Very common (25 uses/session) |
| `Bash(git add:*)` | Stage files (safe: isolated to current branch) | Common |
| `Bash(git branch:*)` | List/read branches | Common (8 uses/session) |
| `Bash(git checkout:*)` | Switch branches (intentional via `--`) | Common |
| `Bash(git commit:*)` | Create commits (with message) | Common |
| `Bash(git diff:*)` | View uncommitted changes | Very common (4+ uses/session) |
| `Bash(git fetch:*)` | Download remote updates (no merge) | Common |
| `Bash(git log:*)` | View commit history | Very common |
| `Bash(git merge:*)` | Merge branches (requires explicit intent) | Intentional |
| `Bash(git pull:*)` | Fetch + merge (requires intent) | Intentional |
| `Bash(git push:*)` | Push to remote (requires intent, only to feature branches per rules) | Intentional |
| `Bash(git rebase:*)` | Rebase (dangerous but intentional) | Intentional |
| `Bash(git show:*)` | Display git object info (read-only) | 4 uses/session |
| `Bash(git status:*)` | Show repo status | Very common (7 uses/session) |
| `Bash(grep *)` | Text search | Very common (48 uses/session) |
| `Bash(mkdir:*)` | Create directories under `~/.claude/` | Occasional config work |

**Rationale for breadth:** Git and gh operations are controlled via `CLAUDE.md` rules (no force-push to main, no skipping hooks, stage by name). The allowlist just removes friction; the rules prevent misuse.

---

### `permissions.deny` (secrets + destructive-op firewall)

**What it does:** Hard blocklist — Claude cannot read/run these patterns regardless of permission mode. Backs the advisory rules in `_rules/security.md` with a mechanical guard.

**When set:** 2026-08-07 (adopted from `_reference/settings_json_recommendations.md` item 1)

**Why:** `security.md` says "never read/commit secrets" and "no destructive ops" — but until now that was guidance only. This gives it teeth at zero per-session context cost, fully reversible.

**Guiding principle:** Explicit over implicit — a mechanical firewall beats trusting every future session to honour an advisory rule.

**Current patterns:**

| Pattern | Blocks | Reliability |
|---------|--------|-------------|
| `Read(./.env)` | Reading the project `.env` | ✅ Reliable — exact path match |
| `Read(./.env.*)` | Reading `.env.local`, `.env.prod`, etc. | ✅ Reliable — docs' own example pattern |
| `Read(~/.ssh/**)` | Reading SSH private keys | ✅ Reliable — recursive path glob |
| `Read(~/.aws/**)` | Reading AWS credentials | ✅ Reliable — recursive path glob |
| `Read(**/secrets/**)` | Reading any `secrets/` directory | ✅ Reliable — recursive path glob |
| `Bash(rm -rf:*)` | Recursive force-delete (`-rf` order) | ⚠️ Defense-in-depth — prefix match |
| `Bash(rm -fr:*)` | Recursive force-delete (`-fr` order) | ⚠️ Defense-in-depth — prefix match |
| `Bash(rm -r -f:*)` | Recursive force-delete (split flags) | ⚠️ Defense-in-depth — prefix match |
| `Bash(rm -f -r:*)` | Recursive force-delete (split flags, reversed) | ⚠️ Defense-in-depth — prefix match |
| `Bash(sudo:*)` | Privilege escalation | ⚠️ Defense-in-depth — prefix match |

**Honesty note:** the `Bash(...)` denies now cover the four common orderings of `rm -rf`, but Bash-text denial is **inherently incomplete** — it cannot catch long-form flags (`rm --recursive --force`), flags placed after the path (`rm foo -rf`), or aliases/variables. They raise the bar substantially for the common case; they are not an airtight seal. The `Read(...)` denies on secret files *are* reliable and remain the load-bearing part of this firewall.

---

### `enabledPlugins`

**What it does:** Activates optional Claude Code plugins for specific workflows.

**When set:** 2026-08-07 (pruned from 6 to 2 after context bloat audit)

**Guiding principle:** Context efficiency is non-negotiable — removed plugins with zero observed value.

**Current plugins (2):**

| Plugin | Purpose | Enabled | Reason |
|--------|---------|---------|--------|
| `skill-creator` | Create/edit custom skills | ✅ Yes | Active use: custom skill creation (`/skill-creator`) |
| `tokensave` | Token optimization (internal) | ✅ Yes | **Load-bearing** for token-aware workflows; governed by `_rules/claude_internal/claude_efficiency.md` |
| `ralph-loop` | Loop automation (`/loop`, `/goal`) | ❌ Disabled | Not actively used; moved to `_wip/disabled_plugins.md` |
| `security-guidance` | Security review prompts | ❌ Disabled | Ad-hoc tool only; moved to `_wip/disabled_plugins.md` |
| `pyright-lsp` | Python LSP hints | ❌ Disabled | Convenience only; repos have own linting; moved to `_wip/disabled_plugins.md` |
| `claude-md-management` | CLAUDE.md audits (`/claude-md-improver`) | ❌ Disabled | Manual editing works fine; moved to `_wip/disabled_plugins.md` |

**To re-enable a plugin:** Edit `settings.json` and set the value to `true`, then run `claude --version` to reload config.

---

### `extraKnownMarketplaces`

**What it does:** Registers custom plugin registries so Claude Code can discover and install plugins from your internal sources.

**When set:** 2026-08-07 (preserved during plugin audit)

**Why:** Enables `tokensave@pyrc-agentic-context` plugin installation/updates. If removed, tokensave plugin updates will fail.

**Guiding principle:** Reversible by design — trivial to add/remove; no downstream dependencies.

**Registries:**

| Registry | Repo | Purpose |
|----------|------|---------|
| `claude-plugins-official` | `anthropics/claude-plugins-official` | Official plugins (skill-creator, etc.) |
| `pyrc-agentic-context` | `pyrc-ghe-engineering/pyrc-lib-agentic_context` | Payroc-internal plugins (tokensave) |

---

### `autoMemoryEnabled: true`

**What it does:** Automatically saves session context to `~/.claude/memory/MEMORY.md` across sessions.

**When set:** 2026-08-07 (preserved; core feature)

**Why:** Enables cross-session learning. Your memories persist even after `/compact` or `/clear` commands.

**Guiding principle:** Lazy-load by default — memory is loaded on-demand per session only if it exists.

---

### `showClearContextOnPlanAccept: true`

**What it does:** When exiting plan mode, shows the context window size before implementation begins.

**When set:** 2026-08-07 (preserved; minor UX)

**Why:** Keeps you aware of context capacity before making changes. Useful since you default to plan mode.

**Guiding principle:** Explicit over implicit — visibility into system state.

---

### `model: "claude-haiku-4-5-20251001"`

**What it does:** Sets the default model to Claude Haiku 4.5 (fast, cost-efficient).

**When set:** 2026-08-07 (preserved; strategic choice)

**Why:**
- Haiku is fast and cheap for most tasks (summarizing, formatting, Q&A, simple code changes)
- `_rules/claude_internal/claude_efficiency.md` flags when to escalate to Sonnet/Opus
- You can override per-session with `/model claude-sonnet-5`

**Guiding principle:** Context efficiency — smaller models preserve reasoning capacity for harder tasks.

---

### `cleanupPeriodDays: 30`

**What it does:** Sets session-transcript retention to 30 days. Transcripts older than this are cleaned up automatically.

**When set:** 2026-08-07 (adopted from `_reference/settings_json_recommendations.md` item 2)

**Why:** 30 is also the documented default — this makes the retention window an explicit, auditable choice rather than an implicit one. Near-zero cost.

**Guiding principle:** Explicit over implicit — a documented default beats a silent one; if the default ever changes upstream, this pins the behaviour.

---

## Audit Trail

| Date | Setting | Change | Reason |
|------|---------|--------|--------|
| 2026-08-07 | `permissions.defaultMode` | Fixed placement (top-level → under `permissions`) | Claude Code expects it nested; was blocking plan mode activation |
| 2026-08-07 | `hooks` | Removed entire section | 5 hooks (task_tracking, naming_convention, dir_structure, subagent_reads, style_guide_dispatch) were injecting 5000+ tokens/session with zero observed value |
| 2026-08-07 | `enabledPlugins` | Removed 4 plugins | Context bloat audit: removed ralph-loop, security-guidance, pyright-lsp, claude-md-management; kept skill-creator + tokensave |
| 2026-08-07 | `permissions.allow` | Added `git show *`, `grep *` | Transcript analysis: 4 and 48 uses/session respectively; both read-only, safe |
| 2026-08-07 | `permissions.deny` | Added 7-pattern secrets + destructive-op firewall | Backs advisory `security.md` rules with a mechanical guard; zero context cost. Adopted from `_reference/settings_json_recommendations.md` |
| 2026-08-07 | `cleanupPeriodDays` | Set to `30` (explicit form of documented default) | Makes transcript retention an auditable choice. Adopted from `_reference/settings_json_recommendations.md` |
| 2026-08-07 | `permissions.deny` | Added `rm -fr` / `rm -r -f` / `rm -f -r` flag-reordering variants | Widen destructive-op coverage; still defense-in-depth (Bash-text denial can't be airtight) |
| 2026-08-07 | `model` + key order | Reconciled live `~/.claude/settings.json` with repo source (added missing `model`, aligned key order) | `src/claude/` must mirror `~/.claude/`; the two had drifted |

---

## Related Files

- **`~/.claude/_rules/guiding_principles.md`** — Decision framework (lazy-load, explicit, context-efficient, intentional, reversible)
- **`~/.claude/_rules/behaviour.md`** — Operational rules (ask first, simplest approach, friction reduction)
- **`~/.claude/_rules/claude_internal/claude_efficiency.md`** — Model selection, sub-agent constraints, token awareness
- **`~/.claude/_wip/disabled_plugins.md`** — Disabled plugins; conditions for re-enabling
- **`~/.claude/_wip/hooks/`** — Disabled hook files; restorable if needed
- **`~/.claude/memory/MEMORY.md`** — Cross-session memories

---

## Design Philosophy

This configuration prioritizes:

1. **Context efficiency** — Every setting justified by usage or principle; bloat removed aggressively
2. **Intentionality** — Settings exist because of observed need, not speculation
3. **Reversibility** — Disabled features (plugins, hooks) remain in `_wip/` for easy restoration
4. **Transparency** — This README documents the why, not just the what

When in doubt, the guiding principles apply: lazy-load by default, prefer explicit choice, measure token cost, only add what's needed, and design for easy removal.
