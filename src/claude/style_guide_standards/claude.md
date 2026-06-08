# Claude AI Playbook — Conventions

Standards for authoring and naming files within the Claude AI playbook (`src/claude/` / `~/.claude/`).

---

## 🔤 General naming rule

All Claude components — agents, skills, rules, process files, hooks, memory files, and style guides — use **snake_case** (underscores, not hyphens). This applies to both filenames and the `name:` field in frontmatter.

- `new_user`, not `new-user`
- `code_reviewer`, not `code-reviewer`
- `technical_writer`, not `technical-writer`

**Why:** Consistency across the playbook. Hyphens are ambiguous in shell contexts and in some tool identifiers; underscores are unambiguous and consistent with Python, SQL, and the rest of the team's naming conventions.

---

## 🎯 Skills

### 📛 Naming

- Use **descriptive snake_case** naming — the name should clearly convey what the skill does or is for
- Prefer action-object (verb_noun) where it reads naturally: `draft_comms`, `schedule_meeting`, `confluence_create_page`
- Use noun phrases where they are clearer: `sprint_planning_dpe_team`, `warehouse_design`, `weekly_one_to_one_prep`
- snake_case, lowercase only — no hyphens
- Where three or more skills share a domain, prefix each with that domain name — e.g. `confluence_`, `jira_`, `git_`. Do not prefix a standalone skill.

**Why (descriptive naming):** Originally codified as strict action-object (sprint 61) after observing the first cohort of skills followed that pattern organically. Relaxed after noun-phrase names like `sprint_planning_dpe_team` and `warehouse_design` proved equally clear as invocations. The constraint is descriptiveness and consistency — not word order.

**Why (domain prefix):** Skills are installed into `~/.claude/skills/`, a flat directory — subdirectories are not supported. Domain prefixes are the only way to visually cluster related skills once a family forms. Apply only when the family exists (three or more skills sharing a domain) — do not prefix a standalone skill like `ansible_playbook_creation` just because an `ansible_` domain could theoretically exist. This prefix applies to the skill's invocation name (the filename and `/skill-name` command), not to the source directory (`_<domain>_skills/` in the repo, which is for housekeeping only).

| Domain | Prefix | Examples |
|---|---|---|
| Confluence | `confluence_` | `confluence_create_page`, `confluence_review_page` |
| Jira | `jira_` | `jira_create`, `jira_update`, `jira_hygiene` |
| Git / GitHub | `git_` | `git_create_pr`, `git_review_pr`, `git_notify_pr` |

> **Note:** Examples show target names — currently installed skills retain their existing names until next edited. The table is not exhaustive — apply the same pattern for any domain with multiple related skills.

Do not prefix a standalone skill. Rename existing skills to add a prefix opportunistically once the family reaches three.

### 📋 `SKILL.md` frontmatter

Every skill must have a frontmatter block with exactly these two fields:

```markdown
---
name: skill_name
description: One sentence — what the skill does and when to use it.
---
```

- `name` must match the directory name
- `description` must fit on a single line; it appears verbatim in the skills README

**Why:** The frontmatter mirrors the pattern used by Claude Code's built-in skill discovery. A consistent, machine-readable name and description allows the skills README to be kept in sync and makes it easier to surface the right skill at invocation time.

### ✂️ Scope

A skill should do one thing. If a skill requires the user to choose between multiple unrelated
operations, it is likely too broad and should be split.

**Signs a skill is too broad:** the skill presents a menu of multiple unrelated options; the
skill name contains "manage", "handle", or another generic verb; different operations
would have different natural language triggers.

**Preferred approach:** one skill per distinct user intent; use pattern classification as
the dispatcher — not a Phase 1 menu inside the skill; group related skills in the same
`_<domain>_skills/` directory.

**Acceptable exceptions:**
- Two operations that are always invoked together or share a single logical outcome.
- Operations that are genuinely inseparable — the user would never want one without the other.

---

## 🤖 Agents

### 🗂️ Directory structure

Agents are grouped under `agents/` by role:

| Directory | Purpose |
|---|---|
| `core/` | Full-session personas (e.g. `architect`, `project_manager`) |
| `utility/` | Read-only review and diagnostics (e.g. `code_reviewer`, `debugger`) |
| `ops/` | Claude setup and maintenance (e.g. `new_user`, `claude_reviewer`) |
| `tools/` | Technology-specific, one per style guide (e.g. `python`, `dbt`) |

**Why:** The four-directory structure was introduced during the agent refactor (sprint 60) to replace a flat layout that made it hard to distinguish full-session personas from narrow-scope tools. Grouping by role makes it clear which agent to reach for and prevents the directory from becoming an unsorted list as new agents are added.

### 📛 Naming

- Lowercase descriptive noun or noun phrase: `architect`, `code_reviewer`, `technical_writer`
- snake_case for multi-word names

**Why:** Consistent with the rest of the playbook's file naming (snake_case, lowercase). Noun phrases describe *what the agent is* rather than what it does, which is appropriate since agents represent persistent personas rather than one-off actions.

---

## 📏 Rules

### 📛 Naming

- Lowercase noun or noun phrase: `git.md`, `security.md`, `file_standards.md`
- Name the file after the domain it governs, not the actions it prescribes

**Why:** Rule files have existed from the start of the playbook and have always used domain-based noun names. Naming by domain (not action) keeps them stable — a file called `git.md` covers everything git-related regardless of which specific rules are added over time.

---

## 🧠 Memory files

### 📛 Naming

- Pattern: `{type}_{topic}.md` — e.g. `feedback_pr_template.md`, `project_sprint61.md`
- `type` must be one of: `user`, `feedback`, `project`, `reference`
- `topic` should be a short, specific descriptor (2–3 words max)

**Why:** The four memory types (`user`, `feedback`, `project`, `reference`) are defined by the auto-memory system built into this playbook. Prefixing the filename with the type makes it immediately clear what kind of memory it is when scanning the directory, and enables future tooling to filter by type. Adopted from sprint 61 onwards.

---

## 🔧 Skill development

When creating or improving a skill, use the `/skill-creator` skill (from the `skill-creator` plugin). It covers the full cycle:

1. **Create** — draft the skill from a description of what it should do
2. **Eval** — run test prompts and review results qualitatively and quantitatively
3. **Improve** — rewrite the skill based on eval feedback
4. **Benchmark** — measure performance with variance analysis

Invoke with `/skill-creator` and describe the skill you want to create or improve.

**Why:** Building skills without evals leads to skills that trigger inconsistently or produce variable output. The Skill Creator enforces a test-driven loop for skill development, which is especially important in this repo where skills are used by the whole team.

---

## ✏️ Instruction file authoring

- Keep files under ~100 lines. Beyond that, split into a parent index + child files.
- Use `@import` for modular content rather than duplicating it inline.
- Prefer one concept per file over monolithic files that cover many areas.
- All files must end with a single newline (enforced by pre-commit).

**Why:** This convention mirrors the Anthropic recommendation for CLAUDE.md files and is reflected in the team's own `rules/workflows.md` documentation guideline ("break up long documents"). Short, focused files load faster, are easier to reason about in context, and degrade more gracefully when context is compressed. The `@import` pattern was introduced to allow the global CLAUDE.md to remain a thin orchestration file rather than a monolith.
