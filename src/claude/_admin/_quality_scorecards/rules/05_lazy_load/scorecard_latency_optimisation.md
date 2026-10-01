# Quality Scorecard — latency_optimisation.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 7.5/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Cite a specific incident or observed need for this guidance, rather than general LLM-parameter advice.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-28 | • 📋 **Concrete:** specific temperature values per scenario, a measure-before-optimizing checklist, explicit appropriate/not-appropriate use cases |
| **Complexity** | 9/10 | 2026-09-28 | • 🧮 **Raw complexity 1:** single concept (temperature as a latency lever) with a small "how to apply" appendix, single file, no dependencies |
| **Evidence of Need** | 6/10 | 2026-09-28 | • 🔗 **Plausible but unevidenced:** reads as sound general LLM-API guidance, but no specific incident or recurring problem in this config is cited |
| **Token Cost Justification** | N/A | 2026-09-28 | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 6/10 | 2026-09-28 | • 🚩 **Unusual frontmatter:** opens with `name:`/`description:`/`metadata: type: feedback` YAML — the personal-memory-entry schema, not used by any other `_rules/` file seen this session<br>• ✅ **Otherwise compliant:** emoji H1, Purpose statement, trailing newline, well under the line limit |
| **Currency** | 9/10 | 2026-09-28 | • 🔍 **Check:** no stale references found; temperature guidance matches current model behavior |
| **Test Coverage** | 6/10 | 2026-09-28 | • 🧪 **Moderate:** `test_latency_optimisation.py` — 4 functions, 6 assertions, self-rated 5/10 quality |
| **Overall** | **7.5/10** | 2026-09-28 | • 💪 **Strength:** clear, practical, appropriately scoped guidance<br>• ⚠️ **Gap:** stray memory-schema frontmatter and no cited real-world justification |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/latency_optimisation.md` — the rule being scored
- `src/claude/_tests/rules/05_lazy_load/test_latency_optimisation.py` — Test Coverage dimension

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Anomalous frontmatter:** the file opens with `name: latency_optimisation`, `description: ...`, `metadata: {type: feedback}` — YAML matching this user's personal-memory-entry schema (see the memory system's own file format), not any convention used by other `_rules/` files.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
