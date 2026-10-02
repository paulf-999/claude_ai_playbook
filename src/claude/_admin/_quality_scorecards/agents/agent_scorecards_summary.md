# 📊 Agent Scorecards Summary

**Purpose:** One-glance rollup of every agent scorecard, showing where quality is weakest and what to fix first, without opening each file.

---

## 📋 Scores by group

- **Overall:** the mean of every scorecard's Overall score in that group.
- **Strongest and weakest:** the highest- and lowest-scoring file in that group, by Overall score.
- **Date Updated:** the latest `Date Updated` among that group's scorecards.

| Group | Scored | Overall | Date Updated | Strengths and gaps |
|---|---|---|---|---|
| Agents | 1 | 6.0/10 | 2026-10-02 | • 💪 **Strongest:** `technical_writer` is the only agent (6.0/10)<br>• ⚠️ **Gap:** overlaps two skills and has no tool allowlist |

---

## 🚀 Recommended next actions

Ranked by impact, highest first.

| # | Action | Why | Source |
|---|---|---|---|
| 1 | • 🔒 **Tool allowlist:** add `tools:` to `technical_writer` | • 🛡️ **Least privilege:** a writing agent can currently run any tool | `scorecard_technical_writer.md` |
| 2 | • 🧭 **Overlap:** decide how `technical_writer` relates to `git_create_pr` and `confluence_create_page` | • 🔁 **Duplication:** two skills already do its two jobs | `scorecard_technical_writer.md` |

---

## 📄 All scorecards

Sorted by Overall score, highest first.

| Scorecard | Overall | Date Updated | Recommended improvements |
|---|---|---|---|
| `scorecard_technical_writer.md` | 6.0/10 | 2026-10-02 | • Add a `tools:` allowlist.<br>• Resolve the overlap with two skills.<br>• Record usage or downgrade maturity.<br>• Structure the evals.<br>• Drop the GitHub MCP requirement. |

---

## 🔄 Keeping this current

- **Same commit:** update this file whenever a scorecard it covers is created or re-scored.
- **Recompute:** re-average the Overall scores and re-check the strongest and weakest files.
- **Bump dates:** set a group's `Date Updated` to the re-scored scorecard's `Date Updated`.
- **Prune actions:** remove an action once its scorecard no longer lists it.
- **Template:** this file follows `_templates/scorecard_summary.md.template`.
