# Quality Scorecard — _claude_config_metadata.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 8.4/10

**Recommended improvements:**
- Re-score Evidence of Need after one audit cycle has used the backfilled `updated` dates.
- Decide whether shared authoring standards should stay always-on or move behind a reachability exemption, to recover the ~400 tokens/session.

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 📋 **Exact formats:** two tables give the fields and the per-artefact placement verbatim<br>• ⚠️ **Judgement call:** MAJOR vs MINOR ("reversed or removed" vs "added") still needs the author's judgement on mixed edits |
| **Complexity** | 9/10 | • 🧮 **Raw complexity 1:** single file, ~3 concepts (fields, version bumps, placement), no dependencies or prerequisites |
| **Evidence of Need** | 7/10 | • 🔗 **Real gap:** the live `~/claude/` copy carries no git history, so audits and 6-month resets had no created/updated signal<br>• ⚠️ **Unproven yet:** no audit has used the fields, since the backfill hasn't happened |
| **Token Cost Justification** | 6/10 | • 🎯 **Always-on:** imported from `authoring_rules.md` so `test_always_on_reachability.py` can reach it<br>• ⚠️ **Narrow use:** only relevant while authoring or editing artefacts, yet costs ~400 tokens every session |
| **Structural Compliance** | 9/10 | • ✅ **Compliant:** three-line metadata header, emoji H1, Purpose statement, Related section, 57 lines, trailing newline |
| **Currency** | 10/10 | • 🔍 **New:** written 2026-09-28, all references resolve |
| **Test Coverage** | 9/10 | • 🧪 **Dedicated test:** `test_claude_config_metadata.py`, 13 functions covering placement, format and value errors<br>• ✅ **Required:** every rule file must carry a header, since the backfill added them to all 147 rules |
| **Overall** | **8.4/10** | • 💪 **Strength:** one lean, testable standard shared across rules, skills, agents and hooks<br>• ⚠️ **Gap:** always-on token cost for guidance used only while authoring |

## 🔗 Related files

- `src/claude/_rules/03_authoring_guidelines/_claude_config_metadata.md` — the rule being scored
- `src/claude/_rules/03_authoring_guidelines/authoring_rules.md` — imports this file (Token Cost Justification)
- `src/claude/_tests/rules/03_authoring_guidelines/test_claude_config_metadata.py` — Test Coverage dimension
- `src/claude/_tests/rules/02_claude_standards/test_always_on_reachability.py` — why the always-on import is required
