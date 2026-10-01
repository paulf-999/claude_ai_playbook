# Quality Scorecard — bash.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-01

**Overall score:** 7.7/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Fix the template path so it reads `05_lazy_load/style_guide_standards/bash/templates/template_bash_script.sh`.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 9/10 | 2026-09-28 | • 📋 **Concrete:** exact safety-flag snippet, named log-level constants, a shellcheck-suppression example with required justification |
| **Complexity** | 7/10 | 2026-09-28 | • 🧮 **Raw complexity 3:** 8 distinct small sections (structure, safety, utilities, tooling, naming, variables, conditionals, general) in a single file, no dependencies |
| **Evidence of Need** | 9/10 | 2026-09-28 | • 🔗 **Actively enforced:** shellcheck is a real CI gate, log-level constants and shell_utils.sh are real shared infrastructure |
| **Token Cost Justification** | N/A | 2026-09-28 | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 9/10 | 2026-09-28 | • ✅ **Compliant:** Purpose statement, Contents section, emoji headers, 81 lines well within limit |
| **Currency** | 3/10 | 2026-09-28 | • 🐛 **Wrong tier:** template path reads `03_lazy_load/...` — the real tier is `05_lazy_load/`<br>• 🐛 **Wrong subdirectory:** path reads `style_guide_standards/unix/templates/...` — the real path is `style_guide_standards/bash/templates/template_bash_script.sh` (confirmed via `find`)<br>• ✅ **One correct reference:** `shell_utils.sh`'s canonical path is accurate |
| **Test Coverage** | 9/10 | 2026-10-01 | • 🧪 **Dedicated test:** `test_lazy_load_rule_structure.py` checks its header, Purpose line, key sections, child links, relative links and Contents<br>• ✅ **Generic checks:** also passes `test_rules_structure.py` |
| **Overall** | **7.7/10** | 2026-10-01 | • 💪 **Strength:** concrete, actively-enforced conventions (shellcheck, log levels)<br>• ⚠️ **Gap:** Currency (3/10) is now the weakest dimension |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/style_guide_standards/bash.md` — the rule being scored
- `src/claude/_rules/05_lazy_load/style_guide_standards/bash/templates/template_bash_script.sh` — Currency dimension (the real location the stale reference should point to)
- `src/claude/_templates/utils/shell_utils.sh` — Currency dimension (the one reference confirmed correct)

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Stale tier + wrong path:** "Template location" reads `~/.claude/_rules/03_lazy_load/style_guide_standards/unix/templates/template_bash_script.sh` — both the tier (`03_lazy_load` vs. the real `05_lazy_load`) and the subdirectory (`unix` vs. the real `bash`) are wrong. Confirmed via `find`.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
