# 📊 Quality Scorecards Summary

**Purpose:** One-glance rollup across every artefact type, showing where quality is weakest and what to fix first, without opening the five per-type summaries.

---

## 📋 Scores by type

- **Overall:** the mean of every scorecard's Overall score for that type.
- **Strongest and weakest:** the mean of each dimension across that type's scorecards, since the per-type summaries don't carry dimension scores.

| Type | Scored | Overall | Strengths and gaps |
|---|---|---|---|
| Tests | 46 | 8.4/10 | • 💪 **Strongest:** Currency (9.0/10)<br>• ⚠️ **Weakest:** Complexity (7.2/10) |
| Skills | 7 | 8.4/10 | • 💪 **Strongest:** Standards Compliance (9.1/10)<br>• ⚠️ **Weakest:** Code Quality (7.7/10) |
| Rules | 33 | 7.4/10 | • 💪 **Strongest:** Token Cost Justification (8.7/10, scored on 16 of 33)<br>• ⚠️ **Weakest:** Test Coverage (4.9/10) |
| Hooks | 0 | — | • ⚠️ **Gap:** no hooks are scored yet |
| Agents | 0 | — | • ⚠️ **Gap:** no agents are scored yet |

---

## 🚀 Recommended next actions

Ranked by impact, highest first.

| # | Action | Why | Source summary |
|---|---|---|---|
| 1 | • 🧪 **Rule test coverage:** add dedicated structural tests for the 15 `05_lazy_load` rules that have none | • 📉 **Lowest dimension:** rule Test Coverage averages 4.9/10, the lowest anywhere | `rules/rule_scorecards_summary.md` |
| 2 | • 📝 **Missing Purpose statements:** add a `**Purpose:**` line to datetime, ohmyzsh_setup, ansible, terraform, mermaid, docker, jira and makefile | • 🧱 **Structure:** each of these 8 rules loses Structural Compliance points for it | `rules/rule_scorecards_summary.md` |
| 3 | • 🆕 **Unscored hooks and agents:** write the first scorecards for hooks and agents | • 🙈 **Blind spot:** two of the five types have no quality signal at all | `hooks/hook_scorecards_summary.md`<br>`agents/agent_scorecards_summary.md` |
| 4 | • 🔧 **Lowest single scores:** fix `makefile` (5.2/10) and replace `claude_kaizen`'s placeholder eval runner (6.1/10) | • 🔻 **Bottom of the table:** these are the lowest-scoring rule and skill | `rules/rule_scorecards_summary.md`<br>`skills/skill_scorecards_summary.md` |
| 5 | • ✂️ **Test complexity:** split the 11 tests whose complexity score is below 7 (raw complexity above 3) | • 📉 **Weakest test dimension:** 11 of 46 tests sit below the ≥7 complexity floor set for new tests | `tests/test_scorecards_summary.md` |
| 6 | • 💬 **Failure messages:** add assertion failure messages to the Confluence and Jira handler tests | • 🔍 **Clarity:** only 0–1% of their assertions say how to fix a failure today | `tests/test_scorecards_summary.md` |

---

## 🔄 Keeping this current

- **Same commit:** update this file whenever any per-type summary changes.
- **Recompute means:** re-average the dimension scores from the individual `scorecard_*.md` files whenever a scorecard is re-scored.
- **Prune actions:** remove an action once its source summary no longer lists it.
