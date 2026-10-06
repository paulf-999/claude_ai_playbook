# Quality Scorecard — portable_paths.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-01

**Overall score:** 9.4/10

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 10/10 | 2026-09-28 | • 📋 **Unambiguous:** concrete do/don't guidance for both Python and shell, with exact code patterns to use instead |
| **Complexity** | 8/10 | 2026-09-28 | • 🧮 **Raw complexity 2:** single file, no children, 2 concepts (Python resolution + shell resolution) |
| **Evidence of Need** | 10/10 | 2026-09-28 | • 🔗 **Gold-standard evidence:** documents four real, dated incidents (2026-09-17/18) with exact files and exact bugs — the strongest Evidence-of-Need case in this survey |
| **Token Cost Justification** | 9/10 | 2026-09-28 | • 🎯 **Scope:** Tier 2, always-on — prevents silent cross-machine breakage, directly justified by the documented incidents |
| **Structural Compliance** | 10/10 | 2026-09-28 | • ✅ **Compliant:** no children, clean sections, 46 lines, emoji headers, Related Rules section present |
| **Currency** | 9/10 | 2026-09-28 | • 🔍 **Check:** correctly documents both `~/.claude/` and `~/claude/` deployment conventions in use today |
| **Test Coverage** | 10/10 | 2026-09-28 | • 🧪 **Best-in-class:** `test_portable_paths_hooks.py` and `test_portable_paths_python.py` each score 9/10, with 11 and 12 test functions, and together regression-test every one of the four documented incidents |
| **Overall** | **9.4/10** | 2026-09-28 | • 💪 **Strength:** the strongest-scored rule in this survey — focused, evidenced, tested<br>• ⚠️ **Gap:** none found |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/portable_paths.md` — the rule being scored
- `src/claude/_tests/rules/02_claude_standards/test_portable_paths_hooks.py` — Test Coverage dimension (hooks)
- `src/claude/_tests/rules/02_claude_standards/test_portable_paths_python.py` — Test Coverage dimension (Python)
