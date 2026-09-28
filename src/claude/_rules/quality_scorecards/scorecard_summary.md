# 📊 Scorecard Summary

**Purpose:** One-glance rollup of every rule scorecard's Overall score and whether it has Recommended improvements — see which rules need attention without opening each file individually.

---

## 📋 Current scores

| File | Overall | Recommended improvements |
|---|---|---|
| `scorecard_portable_paths.md` | 9.4/10 | No (≥8.5) |
| `scorecard_claude_usage_standards.md` | 8.9/10 | No (≥8.5) |
| `scorecard_aliases.md` | 8.6/10 | No (≥8.5) |
| `scorecard_authoring_skills.md` | 8.6/10 | No (≥8.5) |
| `scorecard_guiding_principles.md` | 8.4/10 | Yes — 1 bullet |
| `scorecard_git.md` | 8.1/10 | Yes — 1 bullet |
| `scorecard_claude_response_standards.md` | 7.9/10 | Yes — 2 bullets |
| `scorecard_behaviour.md` | 7.7/10 | Yes — 2 bullets |
| `scorecard_security.md` | 7.6/10 | Yes — 2 bullets |
| `scorecard_testing.md` | 7.6/10 | Yes — 2 bullets |
| `scorecard_claude_plans.md` | 7.6/10 | Yes — 3 bullets |
| `scorecard_claude_operational_efficiency.md` | 7.1/10 | Yes — 2 bullets |
| `scorecard_authoring_rules.md` | 7.1/10 | Yes — 1 bullet |
| `scorecard_authoring_agents.md` | 6.9/10 | Yes — 1 bullet |
| `scorecard_claude_rule_loading_strategy.md` | 6.4/10 | Yes — 1 bullet |

---

## 🔄 Keeping this current

- **Update on every scorecard change** — when a scorecard is created or re-scored (per `README.md`'s "When to score" cadence), update this file's row in the same commit. A summary that drifts from the underlying scorecards is worse than no summary — per `guiding_principles.md`'s own "False truth rots silently."
- **Sort order:** descending by Overall score — the rules needing the most attention are at the bottom.
- **Full recommendation text** lives in each file's own `**Recommended improvements:**` section — this table intentionally shows only the count, not the bullets themselves, to stay scannable.

---

## 🔗 Related

- `README.md` — the scorecard convention, template, and per-dimension criteria this file summarizes
- Individual `scorecard_*.md` files — full detail behind each row above
