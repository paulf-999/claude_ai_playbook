# Quality Scorecard — git.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-11

**Overall score:** 8.7/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-28 | • 📋 **Concrete:** branch-naming regex, PR file-count limit, and Conventional Commits format are all unambiguous |
| **Complexity** | 7/10 | 2026-09-28 | • 🧮 **Raw complexity 3:** ~4 concepts (complex-ops, protected branches, branch naming, PRs) plus 3 children |
| **Evidence of Need** | 9/10 | 2026-09-28 | • 🔗 **Followed exactly, repeatedly:** every commit and PR created this session matched this rule's format and branch-naming pattern |
| **Token Cost Justification** | 9/10 | 2026-09-28 | • 🎯 **Scope:** Tier 2, always-on — governs every git operation, used constantly |
| **Structural Compliance** | 9/10 | 2026-09-28 | • ✅ **Compliant:** Contents matches headings, emoji headers, trailing newline, well organized |
| **Currency** | 8/10 | 2026-09-28 | • 🔍 **Rule content itself:** accurate, no stale references in git.md |
| **Test Coverage** | 10/10 | 2026-10-11 | • 🧪 **Rubric met:** parent and children pass `test_rules_structure.py`, and git.md itself records no incident<br>• 🔗 **Cross-file:** `test_rule_cross_references.py` checks its child pointers and runs its branch pattern against its own examples<br>• 🧷 **Incident child:** `_concurrent_sessions.md` keeps its own content test for the 2026-09-21 incident |
| **Overall** | **8.7/10** | 2026-10-11 | • 💪 **Strength:** heavily used and correctly followed all session<br>• ⚠️ **Gap:** Complexity (7/10) is now the weakest dimension |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/git.md` — the rule being scored
- `src/claude/_tests/rules/test_rule_cross_references.py` — Test Coverage dimension
