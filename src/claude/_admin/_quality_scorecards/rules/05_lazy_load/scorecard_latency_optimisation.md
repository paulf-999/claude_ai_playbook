# Quality Scorecard — latency_optimisation.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-01

**Overall score:** 9.2/10 (6-dimension average, Token Cost N/A)

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-28 | • 📋 **Concrete:** an effort table by use, explicit appropriate and not-appropriate cases, and a measure-first checklist |
| **Complexity** | 9/10 | 2026-09-28 | • 🧮 **Raw complexity 1:** single concept (making responses faster or cheaper), single file, no dependencies |
| **Evidence of Need** | 8/10 | 2026-10-01 | • 🔗 **Incident:** the rule recommended temperatures of 1.5–2.0, which the API never accepts, and temperature on models that reject it, so it needed correcting against the API reference |
| **Token Cost Justification** | N/A | 2026-09-28 | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 9/10 | 2026-10-01 | • ✅ **Header:** 3-line metadata header, emoji H1 and headings, Purpose statement and British spelling<br>• ✅ **Fixed:** the stray memory-schema frontmatter is gone |
| **Currency** | 10/10 | 2026-10-01 | • 🔍 **Check:** effort levels, the Opus 5.5 `medium` default and which models reject `temperature` match the API reference as of 2026-10-01 |
| **Test Coverage** | 10/10 | 2026-10-01 | • 🧪 **Strong:** `test_latency_optimisation.py` — 13 functions, 18 assertions, 9/10, and it fails on any temperature above 1 |
| **Overall** | **9.2/10** | 2026-10-01 | • 💪 **Strength:** current, practical guidance with a test that stops the temperature error coming back<br>• ⚠️ **Gap:** model-specific details will date, so re-check them at each model release |

## 🔗 Related files

- `src/claude/_rules_lazy_load/latency_optimisation.md` — the rule being scored
- `src/claude/_tests/rules/05_lazy_load/test_latency_optimisation.py` — Test Coverage dimension
