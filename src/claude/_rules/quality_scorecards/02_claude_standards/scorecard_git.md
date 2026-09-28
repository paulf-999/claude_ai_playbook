# Quality Scorecard — git.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 8.1/10

**Recommended improvements:**
- Fix the stale `_rules/claude_internal/git.md` reference in `test_git.py`'s module docstring to `_rules/02_claude_standards/git.md`.

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 📋 **Concrete:** branch-naming regex, PR file-count limit, and Conventional Commits format are all unambiguous |
| **Complexity** | 7/10 | • 🧮 **Raw complexity 3:** ~4 concepts (complex-ops, protected branches, branch naming, PRs) plus 3 children |
| **Evidence of Need** | 9/10 | • 🔗 **Followed exactly, repeatedly:** every commit and PR created this session matched this rule's format and branch-naming pattern |
| **Token Cost Justification** | 9/10 | • 🎯 **Scope:** Tier 2, always-on — governs every git operation, used constantly |
| **Structural Compliance** | 9/10 | • ✅ **Compliant:** Contents matches headings, emoji headers, trailing newline, well organized |
| **Currency** | 8/10 | • 🔍 **Rule content itself:** accurate, no stale references in git.md |
| **Test Coverage** | 7/10 | • 🧪 **Direct test exists:** `test_git.py`, 5 functions, checks sections/patterns/line-limit<br>• 🚩 **Drift signal:** its own docstring says "Structural tests for `_rules/claude_internal/git.md`" — a stale pre-reorg path (actual constant on line 18 correctly uses `02_claude_standards/git.md`) |
| **Overall** | **8.1/10** | • 💪 **Strength:** heavily used and correctly followed all session<br>• ⚠️ **Gap:** its own test's docstring has drifted from the real path |

## 🔗 Related files

- `src/claude/_rules/02_claude_standards/git.md` — the rule being scored
- `src/claude/_tests/rules/02_claude_standards/test_git.py` — Test Coverage dimension (the disclosed stale docstring)

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Stale reference:** `test_git.py`'s module docstring (line 9) reads "Structural tests for `_rules/claude_internal/git.md`" — `claude_internal/` is a pre-reorg directory name that no longer exists.
- ✅ **Functionally fine:** the actual path constant on line 18 correctly uses `_rules/02_claude_standards/git.md` — only the docstring drifted, not the test logic.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
