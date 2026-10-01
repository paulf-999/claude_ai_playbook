# Quality Scorecard — docker.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-01

**Overall score:** 8.2/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Add some inline content (principles, examples, or a "when to load" column) — at 15 lines it's a bare 2-item routing list with nothing else, the thinnest parent file in this survey.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 6/10 | 2026-09-28 | • 📋 **Bare routing only:** two one-line links to children with no inline principles, examples, or "when to load" guidance |
| **Complexity** | 10/10 | 2026-09-28 | • 🧮 **Raw complexity 0:** a pure 2-item router, single file, no dependencies, no fixtures — about as simple as a rule file gets |
| **Evidence of Need** | 6/10 | 2026-09-28 | • 🔗 **Plausible but unevidenced:** Docker standards are a reasonable thing to document, but nothing here demonstrates real, specific usage |
| **Token Cost Justification** | N/A | 2026-09-28 | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 9/10 | 2026-10-01 | • ✅ **Fixed:** `**Purpose:**` line added under the H1 (PR #200)<br>• ✅ **Otherwise compliant:** emoji header, Contents section, trailing newline |
| **Currency** | 9/10 | 2026-09-28 | • 🔍 **Check:** nothing stale found, no orphaned duplicate |
| **Test Coverage** | 9/10 | 2026-10-01 | • 🧪 **Dedicated test:** `test_lazy_load_rule_structure.py` checks its header, Purpose line, key sections, child links, relative links and Contents<br>• ✅ **Generic checks:** also passes `test_rules_structure.py` |
| **Overall** | **8.2/10** | 2026-10-01 | • 💪 **Strength:** simple, no orphaned duplicate, nothing stale<br>• ⚠️ **Gap:** Clarity (6/10) is now the weakest dimension |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/style_guide_standards/infra/docker.md` — the rule being scored
