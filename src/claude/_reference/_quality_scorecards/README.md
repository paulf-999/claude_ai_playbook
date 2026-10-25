# 📊 Quality Scorecards

**Purpose:** One home for the quality scorecards that review this config's artefacts — kept apart from rules and skills, since they're review records Claude never reads while working.

---

## 📁 Where each scorecard lives

| Folder | Scores | File pattern |
|---|---|---|
| `agents/` | Agents in `agents/`, one flat folder | `agents/scorecard_<agent_name>.md` |
| `hooks/` | Hooks in `hooks/`, one flat folder | `hooks/scorecard_<hook_name>.md` |
| `rules/` | Rules in `rules/` and `_rules_lazy_load/`, mirroring the rule's current tier, with `rules_lazy_load/` for on-demand rules and `style_guide_standards/` for style guides | `rules/<tier>/scorecard_<rule_name>.md` |
| `skills/` | Skills in `skills/`, one flat folder | `skills/scorecard_<skill_name>.md` |
| `tests/` | Tests in `_tests/`, mirroring the `_tests/` path | `tests/<subpath>/scorecard_<test_file_stem>.md` |

- **Summaries:** each folder has a `<type>_scorecards_summary.md` rollup (e.g. `skills/skill_scorecards_summary.md`) — update it in the same commit as any scorecard change.
  - **Top-level rollup:** `quality_scorecards_summary.md` compares all five types and ranks the next actions.
  - **Template:** all six summaries follow `_templates/scorecard/scorecard_summary.md.template`.
- **Templates:** rules use the template in `rules/README.md`, and skills use `_templates/skills/_quality_scorecard_template.md`.
- **Never `@import`:** these files are for review and audit only, so they cost no session tokens.
- **Audits:** cross-cutting audits of whole areas live in the playbook repo under `docs/audits/`, not here.

---

## 🔍 Independent review

Skills, rules and agents are scored by a reviewer that didn't write them, so the author never marks their own work.

1. **Deterministic checks:** `make lint` and `CLAUDE_CONFIG_DIR=$PWD/src/claude python3 -m pytest` pass before any scoring.
2. **Evals:** the artefact's evals exist at the count its maturity needs.
   - **Agents:** run `python3 src/claude/scripts/_audit_scripts/audit_agent_evals.py <agent>` and give the reviewer its pass rate, which costs one Claude call per runnable eval.
3. **Fresh-context review:** call the Agent tool with `subagent_type: quality_scorecard_reviewer`, passing only the artefact's path and its type.
   - **Its inputs:** the artefact, its contract, its evals, the type's rubric and `scoring_anchors.md`.
   - **Never pass:** the authoring conversation or the current scorecard's scores, since either would anchor the result.
4. **History row:** append the row it returns to `score_history.csv` as the next attempt, then copy the scores into the scorecard and its summaries.
   - **Enforced by:** `test_score_history.py`, which fails when attempts skip or the latest row doesn't match the scorecard.
5. **Human review:** a CODEOWNERS reviewer approves the scorecard change in the PR.

- **Anchors:** `scoring_anchors.md` shows what a 5, a 7 and a 9 look like for each type.
- **Seed rows:** attempt 1 for every scorecard that existed before this flow says `reviewer=author`, since those scores were self-assessed.
- **Not yet covered:** hooks and tests keep author scoring for now.

---

## 🚀 Top 5 recommended actions

The five lowest-scoring artefacts, each with the first recommended improvement from its scorecard.

| # | Artefact | Score | Action | Scorecard |
|---|---|---|---|---|
| 1 | `makefile.md` | 6.8 | Fix or remove the broken `~/.claude/templates/makefile/` templates reference | [scorecard_makefile.md](rules/style_guide_standards/utilities/scorecard_makefile.md) |
| 2 | `claude_operational_efficiency.md` | 7.1 | Add structural tests for the parent and its imported children | [scorecard_claude_operational_efficiency.md](rules/02_claude_standards/scorecard_claude_operational_efficiency.md) |
| 3 | `claude_kaizen` | 7.1 | Add a `reference/_implementation.md` covering the audit and promotion logic | [scorecard_claude_kaizen.md](skills/scorecard_claude_kaizen.md) |
| 4 | `automation_controls.md` | 7.5 | Split the 162-line file into a parent and child files | [scorecard_automation_controls.md](rules/02_claude_standards/scorecard_automation_controls.md) |
| 5 | `claude_plans.md` | 7.6 | Add a "Right" example alongside the existing "Wrong" one | [scorecard_claude_plans.md](rules/02_claude_standards/scorecard_claude_plans.md) |

- **Tie:** `claude_plans.md` and `jira_create` both score 7.6, and the always-on rule ranks first because it loads every session.
- **Upkeep:** refresh this list whenever a scorecard is re-scored.
- **Full ranking:** see `quality_scorecards_summary.md`.
