# 📊 Quality Scorecards

**Purpose:** One home for the quality scorecards that review this config's artefacts — kept apart from rules and skills, since they're review records Claude never reads while working.

---

## 📁 Where each scorecard lives

| Folder | Scores | File pattern |
|---|---|---|
| `agents/` | Agents in `agents/`, one flat folder | `agents/scorecard_<agent_name>.md` |
| `hooks/` | Hooks in `hooks/`, one flat folder | `hooks/scorecard_<hook_name>.md` |
| `rules/` | Rules in `_rules/`, mirroring the tier path | `rules/<tier>/scorecard_<rule_name>.md` |
| `skills/` | Skills in `skills/`, one flat folder | `skills/scorecard_<skill_name>.md` |
| `tests/` | Tests in `_tests/`, mirroring the `_tests/` path | `tests/<subpath>/scorecard_<test_file_stem>.md` |

- **Summaries:** each folder has a `<type>_scorecards_summary.md` rollup (e.g. `skills/skill_scorecards_summary.md`) — update it in the same commit as any scorecard change.
  - **Top-level rollup:** `quality_scorecards_summary.md` compares all five types and ranks the next actions.
  - **Template:** all six summaries follow `_templates/scorecard_summary.md.template`.
- **Templates:** rules use the template in `rules/README.md`, and skills use `_templates/skills/_quality_scorecard_template.md`.
- **Never `@import`:** these files are for review and audit only, so they cost no session tokens.
- **Audits:** cross-cutting audits of whole areas live in `_admin/_audits/`, not here.

---

## 🚀 Top 5 recommended actions

The five lowest-scoring artefacts, each with the first recommended improvement from its scorecard.

| # | Artefact | Score | Action | Scorecard |
|---|---|---|---|---|
| 1 | `makefile.md` | 6.8 | Fix or remove the broken `~/.claude/templates/makefile/` templates reference | [scorecard_makefile.md](rules/05_lazy_load/style_guide_standards/utilities/scorecard_makefile.md) |
| 2 | `claude_operational_efficiency.md` | 7.1 | Add structural tests for the parent and its imported children | [scorecard_claude_operational_efficiency.md](rules/04_claude_reference/scorecard_claude_operational_efficiency.md) |
| 3 | `claude_kaizen` | 7.1 | Add a `reference/_implementation.md` covering the audit and promotion logic | [scorecard_claude_kaizen.md](skills/scorecard_claude_kaizen.md) |
| 4 | `automation_controls.md` | 7.5 | Split the 162-line file into a parent and child files | [scorecard_automation_controls.md](rules/05_lazy_load/scorecard_automation_controls.md) |
| 5 | `claude_plans.md` | 7.6 | Add a "Right" example alongside the existing "Wrong" one | [scorecard_claude_plans.md](rules/02_claude_standards/scorecard_claude_plans.md) |

- **Tie:** `claude_plans.md` and `jira_create` both score 7.6, and the always-on rule ranks first because it loads every session.
- **Upkeep:** refresh this list whenever a scorecard is re-scored.
- **Full ranking:** see `quality_scorecards_summary.md`.
