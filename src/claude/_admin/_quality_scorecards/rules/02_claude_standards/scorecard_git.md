# Quality Scorecard — git.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-01

**Overall score:** 8.6/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-28 | • 📋 **Concrete:** branch-naming regex, PR file-count limit, and Conventional Commits format are all unambiguous |
| **Complexity** | 7/10 | 2026-09-28 | • 🧮 **Raw complexity 3:** ~4 concepts (complex-ops, protected branches, branch naming, PRs) plus 3 children |
| **Evidence of Need** | 9/10 | 2026-09-28 | • 🔗 **Followed exactly, repeatedly:** every commit and PR created this session matched this rule's format and branch-naming pattern |
| **Token Cost Justification** | 9/10 | 2026-09-28 | • 🎯 **Scope:** Tier 2, always-on — governs every git operation, used constantly |
| **Structural Compliance** | 9/10 | 2026-09-28 | • ✅ **Compliant:** Contents matches headings, emoji headers, trailing newline, well organized |
| **Currency** | 8/10 | 2026-09-28 | • 🔍 **Rule content itself:** accurate, no stale references in git.md |
| **Test Coverage** | 9/10 | 2026-10-01 | • 🧪 **Direct test exists:** `test_git.py`, 12 functions — one per rule clause, plus the branch-name pattern run against the file's own examples<br>• ✅ **Fixed:** its stale `claude_internal/` docstring is gone |
| **Overall** | **8.6/10** | 2026-10-01 | • 💪 **Strength:** heavily used and correctly followed all session<br>• ⚠️ **Gap:** Complexity (7/10) is now the weakest dimension |

## 🔗 Related files

- `src/claude/_rules/02_claude_standards/git.md` — the rule being scored
- `src/claude/_tests/rules/02_claude_standards/test_git.py` — Test Coverage dimension (the disclosed stale docstring)

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Stale reference:** `test_git.py`'s module docstring (line 9) reads "Structural tests for `_rules/claude_internal/git.md`" — `claude_internal/` is a pre-reorg directory name that no longer exists.
- ✅ **Functionally fine:** the actual path constant on line 18 correctly uses `_rules/02_claude_standards/git.md` — only the docstring drifted, not the test logic.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
