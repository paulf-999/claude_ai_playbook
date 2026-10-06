---
name: claude_review_config
description: Audit your global Claude config across six quality dimensions. Receive scorecard with A–F grade, gap analysis, and actionable recommendations
maturity: tactical
tags:
  criticality: should
  status: active
  tested: true
  test_coverage_level: comprehensive
---
<!-- version: 1.1.0 -->
<!-- created: 2026-09-07 -->
<!-- updated: 2026-10-06 -->

## 🤖 Instructions for Claude

- **Pre-check:** resolve the config folder from `$CLAUDE_CONFIG_DIR` (or `~/.claude` when unset), and stop if it has no `CLAUDE.md`.
- **Read first:** read `reference/_implementation.md` for the four phases, then `reference/_scoring_guide.md` before scoring.
- **Always:** write the report to `~/claude/_drafts/general/YYYY_MM_DD_claude_config_review.md`, with `~` expanded to the absolute home path.
- **Never:** apply a fix the user hasn't approved individually.
- **Never:** commit changes, and instead list the files changed so the user can commit them.

## 🎯 Purpose

Audits your global Claude config across six quality dimensions:
- **Objective scoring** — rule quality, complexity, testing, security, documentation and standards, each out of 10.
- **Overall grade** — an A–F grade from the six scores.
- **Gap analysis** — a MoSCoW table of what's missing.
- **Recommendations** — severity-rated fixes, applied only when you approve them.

## 💡 Example Usage

```
$ /claude_review_config

Auditing the config folder...

| Dimension | Score | Reasoning |
|---|---|---|
| Rule Quality | 8 | Clear, actionable rules; minor duplication |
| Config Complexity | 7 | Shallow imports; 2 files over 100 lines |
| Testing | 8 | Good hook and rule coverage |

**Overall Grade: B+ (7.7/10)**

| Priority | Item | Category |
|---|---|---|
| Must | Reduce 2 files over 100 lines | Standards |
| Should | Update stale memory entries | Documentation |

✅ Report saved to ~/claude/_drafts/general/2026_10_06_claude_config_review.md
Apply fixes? [y/n] → n
```

## ✨ Best For

Monthly or quarterly config health checks, and justifying clean-up priorities. Currently at the **tactical** stage — main paths and error cases are covered, but not adversarial or edge-case inputs yet.

**Caveats:** scoring is heuristic, and each audit stands alone with no history. It reviews the installed config, not individual skills, which have their own scorecards in `_admin/_quality_scorecards/skills/`. The contract sets `waives_response_standards: true`, so the audit keeps its own format.

## 📚 References

- `reference/_implementation.md` — four phases: read and score, gaps, report, optional fixes
- `reference/_scoring_guide.md` — scoring dimensions and criteria
- `tests/evals.yaml` — 11 test scenarios covering all phases and edge cases
- `_admin/_quality_scorecards/skills/scorecard_claude_review_config.md` — quality scorecard
