# Claude AI Playbook — Conventions

Standards for authoring and naming files within the Claude AI playbook (`src/claude/` / `~/.claude/`).

---

## General naming rule

All Claude components — agents, skills, rules, process files, hooks, commands, memory files, and style guides — use **snake_case** (underscores, not hyphens). This applies to both filenames and the `name:` field in frontmatter.

- `new_user`, not `new-user`
- `code_reviewer`, not `code-reviewer`
- `technical_writer`, not `technical-writer`

**Why:** Consistency across the playbook. Hyphens are ambiguous in shell contexts and in some tool identifiers; underscores are unambiguous and consistent with Python, SQL, and the rest of the team's naming conventions.

---

## Skills

### Naming

- Use **action-object** (verb_noun) naming: `plan_sprint`, `create_confluence_page`, `draft_comms`
- snake_case, lowercase only — no hyphens
- Name should reflect what the skill *does*, not what it *produces*

**Why:** Adopted in sprint 61 after reviewing the existing skill names and observing they all followed an action-object pattern organically. Codified to ensure new skills (e.g. `plan_sprint`, future `plan_roadmap`) remain consistent and distinguishable from one another. Action-object names also read naturally as invocations: `/plan_sprint`, `/draft_comms`.

### `SKILL.md` frontmatter

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

---

## Commands

### Naming

- Single **imperative verb**, lowercase: `debug`, `review`, `commit`
- No underscores or hyphens — commands are brief and action-focused
- Name should be the verb a user would naturally say: "let's `/review`", "run `/debug`"

**Why:** Commands are mid-session prompts — they interrupt flow and need to be typed quickly. All existing commands (`debug`, `review`, `commit`) follow this pattern. A single verb is also semantically distinct from skills (action-object), making it immediately clear whether you are invoking a short prompt or a multi-step workflow.

---

## Agents

### Directory structure

Agents are grouped under `agents/` by role:

| Directory | Purpose |
|---|---|
| `core/` | Full-session personas (e.g. `architect`, `project_manager`) |
| `utility/` | Read-only review and diagnostics (e.g. `code_reviewer`, `debugger`) |
| `ops/` | Claude setup and maintenance (e.g. `new_user`, `claude_reviewer`) |
| `tools/` | Technology-specific, one per style guide (e.g. `python`, `dbt`) |

**Why:** The four-directory structure was introduced during the agent refactor (sprint 60) to replace a flat layout that made it hard to distinguish full-session personas from narrow-scope tools. Grouping by role makes it clear which agent to reach for and prevents the directory from becoming an unsorted list as new agents are added.

### Naming

- Lowercase descriptive noun or noun phrase: `architect`, `code_reviewer`, `technical_writer`
- snake_case for multi-word names

**Why:** Consistent with the rest of the playbook's file naming (snake_case, lowercase). Noun phrases describe *what the agent is* rather than what it does, which is appropriate since agents represent persistent personas rather than one-off actions.

---

## Rules

### Naming

- Lowercase noun or noun phrase: `git.md`, `security.md`, `file_standards.md`
- Name the file after the domain it governs, not the actions it prescribes

**Why:** Rule files have existed from the start of the playbook and have always used domain-based noun names. Naming by domain (not action) keeps them stable — a file called `git.md` covers everything git-related regardless of which specific rules are added over time.

---

## Memory files

### Naming

- Pattern: `{type}_{topic}.md` — e.g. `feedback_pr_template.md`, `project_sprint61.md`
- `type` must be one of: `user`, `feedback`, `project`, `reference`
- `topic` should be a short, specific descriptor (2–3 words max)

**Why:** The four memory types (`user`, `feedback`, `project`, `reference`) are defined by the auto-memory system built into this playbook. Prefixing the filename with the type makes it immediately clear what kind of memory it is when scanning the directory, and enables future tooling to filter by type. Adopted from sprint 61 onwards.

---

## Skill development

When creating or improving a skill, use the `/skill-creator` skill (from the `skill-creator` plugin). It covers the full cycle:

1. **Create** — draft the skill from a description of what it should do
2. **Eval** — run test prompts and review results qualitatively and quantitatively
3. **Improve** — rewrite the skill based on eval feedback
4. **Benchmark** — measure performance with variance analysis

Invoke with `/skill-creator` and describe the skill you want to create or improve.

**Why:** Building skills without evals leads to skills that trigger inconsistently or produce variable output. The Skill Creator enforces a test-driven loop for skill development, which is especially important in this repo where skills are used by the whole team.

---

## Instruction file authoring

- Keep files under ~100 lines. Beyond that, split into a parent index + child files.
- Use `@import` for modular content rather than duplicating it inline.
- Prefer one concept per file over monolithic files that cover many areas.
- All files must end with a single newline (enforced by pre-commit).

**Why:** This convention mirrors the Anthropic recommendation for CLAUDE.md files and is reflected in the team's own `rules/workflows.md` documentation guideline ("break up long documents"). Short, focused files load faster, are easier to reason about in context, and degrade more gracefully when context is compressed. The `@import` pattern was introduced to allow the global CLAUDE.md to remain a thin orchestration file rather than a monolith.
