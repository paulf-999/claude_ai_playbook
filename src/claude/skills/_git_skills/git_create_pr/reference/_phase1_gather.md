# Phase 1 — Gather information (read-only)

Run the following silently to understand current state:

1. `git status` — identify changed/untracked files and current branch
2. `git diff` — review unstaged changes
3. Read `.github/pull_request_template.md` from repo root. **This file is mandatory** — stop if not found and ask the user to create one.

If working tree is clean (nothing to commit), stop.

## Derivations

**Branch:** If already on `feature/` or `hotfix/` branch, use it. Otherwise, derive from `$ARGUMENTS` (text after `/git_create_pr`). Pattern: `^(feature|hotfix)/[a-z0-9_]+$`

**Files to stage:** All changed/untracked files unless context suggests otherwise.

**Commit message:** Conventional Commits format `type(scope): description`
- `type`: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`
- `scope`: 
  - Single file → filename in backticks (`` `git.md` ``)
  - Multiple files in one skill → skill name in backticks (`` `create_pr` ``)
  - Area descriptor or omit entirely for cross-area changes
- Description: lowercase, imperative, no period

**PR title:** Derived separately from commit message
- Format: `type(scope): plain English description`
- Plain English for mixed audience (what changed, why it matters)
- No filenames, code refs, path separators, or backticks
- Lowercase after colon
- Max 70 characters
- Examples:
  - ✅ `chore(settings): remove personal configuration from version control`
  - ❌ `chore(settings.local.json): untrack .claude/settings.local.json` (contains filename)

**PR body:** Use Agent tool (`subagent_type: technical-writer`) to draft following template structure exactly:
- **Summary:** 1 punchy sentence max. 2 sentences only if critical context would be lost. No jargon, no code refs. State what + why.
- **Additional Details:** Omit if not needed. 1 line for single point; bullets (max 3) for multiple. Never mix prose and bullets.
- **Checkboxes:** Tick only applicable one
- **Jira links:** Format as `[DM-12345](https://payroc.atlassian.net/browse/DM-12345)` if ticket known
- **Team links:** Format as `[team-name](https://github.com/orgs/dmt-ghe-engineering/teams/team-name)`

**Labels:** Map using file paths, branch name, commit message:
- `src/claude/skills/` → `claude-skill`
- `src/claude/rules/` → `claude-rule`
- `src/claude/agents/` → `claude-agent`
- `src/claude/hooks/` → `claude-hook`
- `src/claude/process/` → `claude-process`
- `src/claude/style_guide_standards/` → `style-guide-and-standards`
- `src/sh/`, `src/cicd/`, `.github/workflows/`, `.pre-commit-config.yaml` → `CI/CD`
- `.github/ISSUE_TEMPLATE/`, `pull_request_template.md` → `governance`
- `requirements.txt`, `packages.yml`, `pyproject.toml`, `package.json` → `dependencies`
- `settings.json`, `ansible.cfg`, `dbt_project.yml`, `.sqlfluff`, `.yamllint` → `config`
- Branch `hotfix/` → `hotfix`
- Type `refactor` → `refactor`
- Scope/message contains `security` → `security`
- Breaking change (`!` or `BREAKING CHANGE:`) → `breaking-change`
- All `docs/` only → `documentation`
