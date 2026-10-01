# Quality Scorecard — docker.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 6.5/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Add a `**Purpose:**` statement at the top — this file opens with plain prose instead.
- Add some inline content (principles, examples, or a "when to load" column) — at 15 lines it's a bare 2-item routing list with nothing else, the thinnest parent file in this survey.
- Add a dedicated structural test for this file and its 2 children.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 6/10 | 2026-09-28 | • 📋 **Bare routing only:** two one-line links to children with no inline principles, examples, or "when to load" guidance |
| **Complexity** | 10/10 | 2026-09-28 | • 🧮 **Raw complexity 0:** a pure 2-item router, single file, no dependencies, no fixtures — about as simple as a rule file gets |
| **Evidence of Need** | 6/10 | 2026-09-28 | • 🔗 **Plausible but unevidenced:** Docker standards are a reasonable thing to document, but nothing here demonstrates real, specific usage |
| **Token Cost Justification** | N/A | 2026-09-28 | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 6/10 | 2026-09-28 | • 🚩 **Missing Purpose statement:** opens with plain prose, unlike this config's convention<br>• ✅ **Otherwise compliant:** emoji header, Contents section, trailing newline |
| **Currency** | 9/10 | 2026-09-28 | • 🔍 **Check:** nothing stale found, no orphaned duplicate |
| **Test Coverage** | 2/10 | 2026-09-28 | • 🧪 **Gap:** confirmed via `find` — no test file references this rule by name |
| **Overall** | **6.5/10** | 2026-09-28 | • 💪 **Strength:** simple, no orphaned duplicate, nothing stale<br>• ⚠️ **Gap:** the thinnest content in this survey — a bare router with no substance of its own |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/style_guide_standards/infra/docker.md` — the rule being scored
