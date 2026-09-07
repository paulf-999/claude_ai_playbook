---
name: claude_review_config
description: Audit your global Claude config across six quality dimensions. Receive scorecard with A–F grade, gap analysis, and actionable recommendations
version: 0.1.0
maturity: draft
tags:
  criticality: should
  status: active
  tested: true
  test_coverage_level: comprehensive
---

## 🎯 Purpose

Audit your global Claude config (`~/.claude/`) across six quality dimensions:
- **Objective assessment** — Score rule quality, config complexity, testing coverage, security posture, documentation, and standards adherence
- **Comprehensive scorecard** — Per-dimension scores (1–10) with reasoning + overall A–F grade
- **Gap analysis** — MoSCoW table identifying missing elements (Must/Should/Could)
- **Actionable recommendations** — Severity-rated improvements with rationale + optional fixes

## 💡 Example Usage

```
$ /claude_review_config

Auditing ~/.claude/ config...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 SCORECARD (per dimension, 1–10 scale)

| Dimension | Score | Reasoning |
|---|---|---|
| Rule Quality | 8 | Clear, specific rules with good actionability; minor duplication |
| Config Complexity | 7 | Mostly shallow import chains; 2 files >100 lines |
| Testing | 8 | 34 tests covering all phases; good hook coverage |
| Security Posture | 8 | Clear separation; explicit injection defence; safe secrets |
| Documentation | 7 | READMEs present; curated memory; good rationale |
| Standards Adherence | 8 | Consistent naming; most files <100 lines; uniform style |

**Overall Grade: B+ (7.7/10)**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 GAP ANALYSIS (MoSCoW priority)

| Priority | Item | Category |
|---|---|---|
| Must | Add README to _tests/hooks/ | Documentation |
| Must | Reduce 2 files >100 lines | Standards |
| Should | Update stale memory entries | Documentation |
| Should | Add rationale to lazy_load rules | Documentation |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Full report saved to: ~/.claude_config_review.md

Apply fixes? [y/n] → n
```

## ✨ Best For

Periodic config health checks (monthly/quarterly) to maintain quality standards and identify gaps. Use to justify config cleanup priorities.

**Caveats:** Scoring is subjective (heuristic-based). Doesn't audit playbook repo structure (use `/audit_skills` instead). No historical tracking (each audit is standalone).

**Special Note — Response Standards Waiver:**
- This skill uses custom interactive output format (multi-phase audit workflow)
- Free-form prompts are incompatible with standard Claude response formatting requirements
- The response standards rule makes an exception for this skill to preserve interactive capability

## 📚 References

**Workflow & Implementation:**
- `reference/_implementation.md` — 4-phase workflow (read → score → analyze → fix)
- `reference/_scoring_guide.md` — Detailed scoring dimensions and criteria
- `evals.yaml` — 34 test scenarios covering all phases and edge cases

**Quality & Design:**
- `reference/_quality_scorecard.md` — Quality assessment and Draft maturity justification
