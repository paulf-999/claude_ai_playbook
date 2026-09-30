# Quality Scorecard — bash.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-09-28

**Overall score:** 6.5/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Add a dedicated structural test for this file.

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | 9/10 | • 📋 **Concrete:** exact safety-flag snippet, named log-level constants, a shellcheck-suppression example with required justification |
| **Complexity** | 7/10 | • 🧮 **Raw complexity 3:** 8 distinct small sections (structure, safety, utilities, tooling, naming, variables, conditionals, general) in a single file, no dependencies |
| **Evidence of Need** | 9/10 | • 🔗 **Actively enforced:** shellcheck is a real CI gate, log-level constants and shell_utils.sh are real shared infrastructure |
| **Token Cost Justification** | N/A | • N/A — lazy-loaded, not always-on |
| **Structural Compliance** | 9/10 | • ✅ **Compliant:** Purpose statement, Contents section, emoji headers, 81 lines well within limit |
| **Currency** | 3/10 | • 🐛 **Wrong tier:** template path reads `03_lazy_load/...` — the real tier is `05_lazy_load/`<br>• 🐛 **Wrong subdirectory:** path reads `style_guide_standards/unix/templates/...` — the real path is `style_guide_standards/bash/templates/template_bash_script.sh` (confirmed via `find`)<br>• ✅ **One correct reference:** `shell_utils.sh`'s canonical path is accurate |
| **Test Coverage** | 2/10 | • 🧪 **Gap:** confirmed via `find` — no test file references `bash` style guide content by name |
| **Overall** | **6.5/10** | • 💪 **Strength:** concrete, actively-enforced conventions (shellcheck, log levels)<br>• ⚠️ **Gap:** the one file-path reference readers actually need to follow is wrong in two ways |

## 🔗 Related files

- `src/claude/_rules/05_lazy_load/style_guide_standards/bash.md` — the rule being scored
- `src/claude/_rules/05_lazy_load/style_guide_standards/bash/templates/template_bash_script.sh` — Currency dimension (the real location the stale reference should point to)
- `src/claude/_templates/utils/shell_utils.sh` — Currency dimension (the one reference confirmed correct)

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Stale tier + wrong path:** "Template location" reads `~/.claude/_rules/03_lazy_load/style_guide_standards/unix/templates/template_bash_script.sh` — both the tier (`03_lazy_load` vs. the real `05_lazy_load`) and the subdirectory (`unix` vs. the real `bash`) are wrong. Confirmed via `find`.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
