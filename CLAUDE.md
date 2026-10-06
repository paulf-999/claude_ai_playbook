# CLAUDE.md — claude_ai_playbook

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
| Find a rule | `Glob src/claude/{rules,_rules_lazy_load}/**/<rule_name>.md` |
| Find rules referencing another | `Grep "<rule_name>" src/claude/rules/ src/claude/_rules_lazy_load/` |
| Find skills in a group | `Glob src/claude/skills/_<group>_skills/**/SKILL.md` |
| Find a style guide | `Glob src/claude/{rules/04_path_scoped,_rules_lazy_load}/style_guide_standards/**/<name>.md` |

---

## Playbook maintenance

Whenever a new artefact is added to `src/claude/`, the documentation listed below **must be updated in the same PR**. Do not consider a playbook addition complete without these updates.

| Artefact | Required doc updates |
|---|---|
| **Skill** (`skills/`) | `src/claude/skills/README.md` |
| **Rule** (`rules/<tier>/` or `_rules_lazy_load/`) | `src/claude/_rules_lazy_load/_tier_readmes/<tier>.md` for tiers 01–03, or `src/claude/_rules_lazy_load/README.md` for lazy and path-scoped rules — no `@import`, since Claude Code loads `rules/` natively |
| **Agent** (`agents/<group>/<name>/AGENT.md`) | None — the `agents/` folder is the index |
| **Hook** (`hooks/`) | `settings.json` lifecycle event registration |
| **Style guide** (`rules/04_path_scoped/style_guide_standards/` or `_rules_lazy_load/style_guide_standards/`) | None — the folders are the index (path-scoped entry points load on a matching file; children are read on demand) |
| **Skill behavioural test** (`src/claude/_tests/skills/`) | Set `tested: true` in the skill's `SKILL.md` frontmatter · update the group README (`_<group>_skills/README.md`) `Tested` column — no other doc updates required |

`docs/whats_installed.md` only links to each folder's index with a one-line summary, so it needs a new section only when a new kind of artefact (a new top-level folder) is added.

After updating the required files above, scan the rest of `docs/` for pages that may reference the area being changed — `quickstart.md`, `training.md`, and files under `docs/reference/` may also need updating depending on the nature of the addition.

---

## 🧪 Running tests

Tests read the config from `CLAUDE_CONFIG_DIR`, which a local shell may point at the live `~/claude/` install. Point it at the repo explicitly — the same target CI uses:

```bash
CLAUDE_CONFIG_DIR=$PWD/src/claude python3 -m pytest src/claude/_tests
```

- **Why:** a plain `pytest` (or `make test`) checks whatever `CLAUDE_CONFIG_DIR` points at, so it can pass or fail on the live config instead of your changes (found 2026-09-30).
- **Flat live install:** the live `skills/` has no `_<group>_skills/` folders, so skill-folder checks skip there and only run against the repo.

---

## Priority reads

Files most frequently cross-referenced across the playbook, derived from static reference-frequency analysis of `src/claude/_rules_lazy_load/style_guide_standards/`. Consult these before scanning broadly when looking for conventions or standards:

| File | Domain |
|---|---|
| `src/claude/rules/04_path_scoped/style_guide_standards/sql.md` | SQL / SQLFluff |
| `src/claude/rules/04_path_scoped/style_guide_standards/airflow.md` | Airflow DAGs |
| `src/claude/rules/04_path_scoped/style_guide_standards/dbt.md` | dbt models |
| `src/claude/_rules_lazy_load/style_guide_standards/jira.md` | Jira tickets |
| `src/claude/rules/04_path_scoped/style_guide_standards/infra/terraform.md` | Terraform |
| `src/claude/rules/04_path_scoped/style_guide_standards/infra/ansible.md` | Ansible |
| `src/claude/_rules_lazy_load/org.md` | Organisation-specific standards (naming, secrets, estate) |
