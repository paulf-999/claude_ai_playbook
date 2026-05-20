# 🔐 Permission Model

Guidance on which Claude Code permission prompts to suppress, which to keep, and why. Applies when configuring `permissions.allow` in `~/.claude/settings.json`.

---

## The core principle

**Read-only operations** — no state is modified, no side effects. Safe to suppress.

**Write, mutate, or external-facing operations** — modify files, git state, or systems visible to others. Keep the prompt.

---

## What's safe to suppress

**Read-only bash commands** — inspect state without changing anything:
- `find`, `grep`, `cat`, `head`, `tail`, `ls`
- `git status`, `git diff`, `git log`, `git branch`

**MCP read tools** — fetch or inspect data, do not modify anything:
- `mcp__filesystem__read_*`, `mcp__filesystem__list_*`, `mcp__filesystem__directory_tree`
- `mcp__memory__read_graph`, `mcp__memory__search_nodes`, `mcp__memory__open_nodes`
- `mcp__context7__*`, `mcp__sequential-thinking__*`

**Standard git workflow** — already in the allow list; safe to run without prompting in normal development flow.

---

## What should always prompt — and why

### `settings.json` edits

**Risk:** Privilege escalation via prompt injection.

`settings.json` controls what tools are auto-approved and what hooks execute. If edits to this file were auto-approved, a prompt injection attack via external content Claude is asked to process (a document, web page, or third-party file) could silently:

- Add `Bash(*:*)` to `permissions.allow`, granting unrestricted shell access
- Insert a hook that executes an arbitrary shell command on every tool use
- Enable a rogue MCP server

The prompt on `settings.json` is the last line of defence against this escalation path. Do not suppress it.

---

### MCP filesystem write operations

**Risk:** Silent file modification from injected instructions.

`mcp__filesystem__write_file`, `mcp__filesystem__edit_file`, `mcp__filesystem__create_directory`, and `mcp__filesystem__move_file` can modify the filesystem without leaving a Bash trace. If auto-approved, external content processed by Claude could embed instructions that silently create, overwrite, or rearrange files.

Keep these out of `permissions.allow`. The built-in `Write` and `Edit` tools are covered by the permission model directly — MCP filesystem writes should be treated the same way.

---

### `cd && git` compound commands

**Risk:** Git hook execution from untrusted repositories.

When `cd /some/repo && git <command>` runs, git executes hooks from that directory's `.git/hooks/`. If Claude were directed (via prompt injection) to `cd` into a malicious repository and run a git command, those hooks would execute silently.

**Mitigation:** Use `git -C /path/to/repo <command>` instead. This runs the git command in the specified directory without changing the shell's working directory, eliminating the hook-execution risk. `Bash(git -C:*)` is in the allow list for this reason.

**Scope note:** `Bash(git -C:*)` is a prefix entry, not a subcommand entry — it covers all subcommands used via `-C`, including destructive ones (`reset --hard`, `push --force`). These remain governed by `rules/behaviour/risky_actions.md`, which requires confirmation regardless of the allow list. Do not remove or weaken that rule.

---

### Destructive git operations

**Risk:** Irreversible state loss.

`git reset --hard`, `git push --force`, and `git checkout -- .` discard work permanently. These are covered by `rules/behaviour/risky_actions.md` and must always prompt regardless of the allow list.

---

### External-facing actions

**Risk:** Visible to others and cannot be quietly undone.

Creating PRs, posting Jira comments, pushing to remote, or sending messages affect shared systems and are visible to other people. Always confirm before executing.

---

## The `Bash(*:*)` anti-pattern

Adding `"Bash(*:*)"` to `permissions.allow` suppresses every bash prompt — including destructive commands (`rm -rf`), privilege escalation (`sudo`), and arbitrary script execution. Even in a personal single-user context, it eliminates the permission layer that prompt injection depends on finding intact.

Prefer specific entries (`Bash(find:*)`, `Bash(make:*)`) over a catch-all. When a command keeps prompting and the pattern is safe, add the specific prefix — do not open the floodgates.

---

## Where to store allow entries

Not all entries belong in the same file. Choose based on scope and lifecycle:

| Entry type | File | Reason |
|---|---|---|
| Team baseline — safe for all users, all projects | `~/.claude/settings.json` | Synced from the repo via `make install`; applies globally |
| Personal workflow exceptions — specific to your setup | `.claude/settings.local.json` | Gitignored; not overwritten by `make install`; project-scoped |

**Personal exceptions** are entries that are legitimate for your workflow but not appropriate to impose on all users — for example, allowing writes to `~/.claude/skills/` as part of the playbook install flow, or scoped `cd && git` patterns for a specific known-safe repo path.

If an entry would raise a security concern in a team review, it belongs in `.claude/settings.local.json`, not the shared baseline.

---

## How to add a new allow entry

Before adding a new entry to `permissions.allow`, apply this checklist:

1. **Is it read-only?** If yes, safe to add.
2. **Does it modify the filesystem, git state, or external systems?** If yes, keep the prompt. *Exception: `Bash(git -C:*)` — a prefix entry covering all git subcommands run via `-C`. Destructive subcommands (`reset --hard`, `push --force`) remain governed by `rules/behaviour/risky_actions.md`, which requires confirmation regardless of the allow list. See the `cd && git` section above for full rationale.*
3. **Could a prompt injection via external content exploit this permission?** If yes, do not add it.
4. **Is the prefix specific enough?** Use the narrowest prefix that covers the use case — avoid wildcards that would cover unintended commands.

**Format:** `"Bash(prefix:*)"` matches any command whose full string starts with `prefix`. For example, `"Bash(find:*)"` matches `find . -name "*.py"`.
