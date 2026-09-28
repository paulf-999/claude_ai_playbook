# Quality Scorecard — authoring_rules.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 7.1/10

**Recommended improvements:**
- Extend `test_authoring_rules.py` to check the checklist's tier names against the actual directory structure, so this kind of drift is caught mechanically.

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 7/10 | • 📋 **Generally clear:** 5-question checklist plus a 5-step creation process<br>• 🚩 **Actively misleading in one spot:** step 5 of the checklist lists directory names that no longer exist (see Currency) |
| **Complexity** | 8/10 | • 🧮 **Raw complexity 2:** single file, no children, ~4 concepts (checklist, creation steps, quality gates, references) |
| **Evidence of Need** | 9/10 | • 🔗 **Heavily used this session:** its 5-step process and quality-gate checklist were followed repeatedly while building the scorecard convention itself |
| **Token Cost Justification** | 9/10 | • 🎯 **Scope:** Tier 3, always-on — directly governs how every future rule (including these scorecards) gets created |
| **Structural Compliance** | 7/10 | • ✅ **Compliant:** emoji header, Purpose statement, trailing newline, Related Rules section present<br>• 🚩 **Correctness issue bleeds into structure:** the guidance itself is factually wrong in one place (see Currency) |
| **Currency** | 4/10 | • 🐛 **Stale tier names:** step 5 of the Pre-Creation Checklist lists `02_claude_internal/` and `03_lazy_load/` — the actual current tiers are `02_claude_standards/` and `05_lazy_load/`<br>• 🚫 **Actively wrong, not cosmetic:** a reader following this checklist today would place a new rule in a directory that doesn't exist |
| **Test Coverage** | 6/10 | • 🧪 **Direct test exists:** `test_authoring_rules.py`, 5 functions<br>• ⚠️ **Doesn't catch this drift:** purely structural (checks sections/patterns exist), so it passed despite the stale tier names |
| **Overall** | **7.1/10** | • 💪 **Strength:** actively followed, well-structured process<br>• ⚠️ **Gap:** its own directory-naming guidance has drifted from the real 5-tier structure |

## 🔗 Related files

- `src/claude/_rules/03_authoring_guidelines/authoring_rules.md` — the rule being scored
- `src/claude/_tests/rules/03_authoring_guidelines/test_authoring_rules.py` — Test Coverage dimension

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Stale tier names:** the Pre-Creation Checklist's step 5 (line 32–33) reads `02_claude_internal/` and `03_lazy_load/` — neither directory exists in the current config, which uses `02_claude_standards/` and `05_lazy_load/`.
- 🚫 **Impact:** this is the file that tells authors where to place a new rule — the exact guidance it gives for two of three tiers is currently wrong.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
