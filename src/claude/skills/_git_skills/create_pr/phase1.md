## 🔍 Phase 1 — Gather information (read-only, no prompting)

Run the following silently to understand the current state:

1. `git status` — identify changed/untracked files and current branch
2. `git diff` — review unstaged changes
3. Run `git rev-parse --show-toplevel` to get the repo root, then read `<repo_root>/.github/pull_request_template.md` using that absolute path. **This file must be read and used as the PR body structure — no exceptions.** If it does not exist, stop and tell the user:

   > "No `.github/pull_request_template.md` found in this repo. Please create one before raising a PR, or confirm you want to proceed without it."

   Do not invent a PR body structure or fall back to a minimal body.

If the working tree is clean (nothing to commit), stop and tell the user.

Using what you have gathered:

- **Branch**: If already on a `feature/` or `hotfix/` branch, use it. Otherwise, derive a branch name from $ARGUMENTS (if provided) or propose one based on the changes. `$ARGUMENTS` is the text passed after the skill invocation — e.g. `/create_pr fix login redirect` → use `fix login redirect` as the branch hint. Branch naming pattern: `^(feature|hotfix)/[a-z0-9_]+$`
- **Files to stage**: List all changed/untracked files. Default to staging all of them unless context suggests otherwise.
- **Commit message**: Draft a Conventional Commits message:
  - Format: `type(scope): imperative description`
  - `type`: one of `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `ci`
  - `scope`: chosen based on breadth of change:
    - **Single file** → filename in backticks (e.g. `` `git.md` ``, `` `settings.json` ``)
    - **Multiple files under `src/claude/wip/skills/<skill_name>/`** → skill name in backticks (e.g. `` `ideas` ``, `` `release` ``)
    - **Multiple files in one skill** → skill name in backticks (e.g. `` `create_pr` ``, `` `review_pr` ``)
    - **Multiple files in one area (non-skill)** → area descriptor without backticks (e.g. `staging`, `rules`, `dependencies`)
    - **Multiple files across unrelated areas** → omit scope entirely
  - Description: lowercase, imperative mood, no trailing period
- **PR title**: Derived separately from the commit message — do NOT reuse the commit message as the PR title.
  - Format: `type(scope): plain English description` — same type and scope as the commit message
  - The description must be plain English for a mixed audience: describes what changed, not how
  - No filenames, code references, path separators, or backticks in the description
  - Lowercase after the colon, no trailing period
  - Good: ``chore(`settings.local.json`): remove personal configuration file from version control``
  - Bad: ``chore(`settings.local.json`): untrack .claude/settings.local.json`` (description contains a filename)
- **PR body**: Use the `Agent` tool with `subagent_type: technical-writer` to draft the PR body. Pass the agent the full diff, the commit message, and the contents of `.github/pull_request_template.md`. Instruct the agent to follow these rules:
  - **Template structure is mandatory**: reproduce every section from the template exactly — do not invent sections, remove headers, or reorder them. Populate only the designated placeholder fields.
  - **PR Summary**: 1 punchy plain-English sentence. 2 sentences absolute maximum — only if a single sentence would lose critical context. No jargon, no implementation detail, no code references. State what changed and why it matters.
  - **(Optional) Additional Details**: omit this section entirely if not needed. If used: one line if there is a single point; bullet-point every point (max 3) if there are multiple. Never mix prose and bullets in the same section.
  - Leave all checkboxes intact and tick only the one that applies.
  - **Jira links**: If the template has a "Related Jira Issue(s)" section and the context contains a Jira ticket ID (e.g. `DM-39010`), format it as a hyperlink: `[DM-39010](https://payroc.atlassian.net/browse/DM-39010)`. If no Jira ticket is known, leave the placeholder text from the template unchanged.
  - **Team name links**: When the PR body mentions a GitHub team by name, hyperlink it to its team page. Examples: `[den](https://github.com/orgs/dmt-ghe-engineering/teams/den)`, `[DPE](https://github.com/orgs/dmt-ghe-engineering/teams/dpe)`. Apply consistently across all sections.
- **Labels**: Inspect the changed file paths, branch name, and commit message to map to GitHub labels. Apply all matching labels using `--label "<label>"` in the `gh pr create` command (multiple `--label` flags are allowed). Mapping rules:

  *File path rules (apply for any matching changed file):*
  - Any file under `src/claude/skills/` → `claude-skill`
  - Any file under `src/claude/rules/` → `claude-rule`
  - Any file under `src/claude/agents/` → `claude-agent`
  - Any file under `src/claude/hooks/` → `claude-hook`
  - Any file under `src/claude/process/` → `claude-process`
  - Any file under `src/claude/commands/` → `claude-command`
  - Any file under `src/claude/style_guide_standards/` → `style-guide-and-standards`
  - Any file under `src/sh/` → `build scripts`
  - Any file under `src/cicd/` or under `.github/workflows/`, or named `.pre-commit-config.yaml` → `CI/CD`
  - Any file named `CODEOWNERS` → `Git codeowners`
  - Any file under `.github/ISSUE_TEMPLATE/` or named `pull_request_template.md` → `governance`
  - Any file named `requirements.txt`, `packages.yml`, `pyproject.toml`, or `package.json` → `dependencies`
  - Any file named `settings.json`, `ansible.cfg`, `dbt_project.yml`, `.sqlfluff`, or `.yamllint` → `config`
  - All changed files are under `docs/` → `documentation` (do not apply if any file outside `docs/` is also changed)

  *Branch name rules:*
  - Branch prefix `hotfix/` → `hotfix`

  *Commit message rules:*
  - Commit type `refactor` (message starts with `refactor(`) → `refactor`
  - Commit message scope contains `security` (e.g. `fix(security):`) → `security`
  - Commit message contains `!` after the type (e.g. `feat!:`, `fix!:`) or a `BREAKING CHANGE:` footer → `breaking-change`

  - If no mapping from the table above applies, do not apply a label. Raise the PR without one. Never create a new label without the user's explicit instruction.
