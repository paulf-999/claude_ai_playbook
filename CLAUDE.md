# CLAUDE.md — dmt-scripts-claude_ai_playbook

This file provides repo-specific instructions for Claude Code when working in the playbook repo.

---

## 🔍 Codebase exploration — Graphify

[Graphify](https://github.com/lucasrosati/claude-code-memory-setup) generates a local AST-based knowledge graph so structural questions (where a rule is defined, what imports it, which skills live in a group) can be answered from a single file rather than reading the tree. The graph covers `src/claude/`.

### ✅ When Graphify is set up

The knowledge graph is at: `graphify-out/graph.json`

Use the `/graphify` skill to query it — ask structural questions (e.g. "Which rules import `guiding_principles`?", "What skills are in `_git_skills`?") and the skill will query the graph directly rather than reading files.

**Before exploring the codebase manually**, check the graph first. Only open individual files when you need the content itself — not for structural orientation.

Rebuild after significant changes (run from repo root):
```bash
graphify update .
```

### ⚠️ When Graphify is not set up

Use targeted Grep and Glob rather than reading files broadly:

| Goal | Tool |
|---|---|
| Find a rule | `Glob src/claude/_rules/**/<rule_name>.md` |
| Find rules importing another | `Grep "<import_name>" src/claude/_rules/` |
| Find skills in a group | `Glob src/claude/skills/_<group>_skills/**/SKILL.md` |
| Find a style guide | `Glob src/claude/_rules/05_lazy_load/style_guide_standards/<name>.md` |

---

## Playbook maintenance

Whenever a new artefact is added to `src/claude/`, the documentation listed below **must be updated in the same PR**. Do not consider a playbook addition complete without these updates.

| Artefact | Required doc updates |
|---|---|
| **Skill** (`skills/`) | `src/claude/skills/README.md` · `docs/whats_installed.md` skills section |
| **Rule** (`_rules/<tier>/`) | `src/claude/_rules/<tier>/README.md` · `src/claude/CLAUDE.md` (add `@import` for tiers 01–04 only; `05_lazy_load/` is never imported) · `docs/whats_installed.md` rules description |
| **Agent** (`agents/<group>/<name>/AGENT.md`) | `docs/whats_installed.md` agents section |
| **Hook** (`hooks/`) | `docs/whats_installed.md` hooks table · `settings.json` lifecycle event registration |
| **Style guide** (`_rules/05_lazy_load/style_guide_standards/`) | `docs/whats_installed.md` style guides table (never `@import`ed — read on demand) |
| **Skill behavioural test** (`src/claude/_tests/skills/`) | Set `tested: true` in the skill's `SKILL.md` frontmatter · update the group README (`_<group>_skills/README.md`) `Tested` column — no other doc updates required |

After updating the required files above, scan the rest of `docs/` for pages that may reference the area being changed — `quickstart.md`, `training.md`, and files under `docs/reference/` may also need updating depending on the nature of the addition.

---

## Priority reads

Files most frequently cross-referenced across the playbook, derived from static reference-frequency analysis of `src/claude/_rules/05_lazy_load/style_guide_standards/`. Consult these before scanning broadly when looking for conventions or standards:

| File | Domain |
|---|---|
| `src/claude/_rules/05_lazy_load/style_guide_standards/sql.md` | SQL / SQLFluff |
| `src/claude/_rules/05_lazy_load/style_guide_standards/airflow.md` | Airflow DAGs |
| `src/claude/_rules/05_lazy_load/style_guide_standards/dbt.md` | dbt models |
| `src/claude/_rules/05_lazy_load/style_guide_standards/jira.md` | Jira tickets |
| `src/claude/_rules/05_lazy_load/style_guide_standards/infra/terraform.md` | Terraform |
| `src/claude/_rules/05_lazy_load/style_guide_standards/infra/ansible.md` | Ansible |
| `src/claude/_rules/05_lazy_load/style_guide_standards/payroc_engineering_naming_standards.md` | Naming standards |
