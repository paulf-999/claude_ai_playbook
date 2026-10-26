# Quality Scorecard — bash.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 6.8/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Say whether `local` variables are uppercase too (lines 72 and 78)
- Reconcile the relative `shell_utils.sh` path on line 47 with the absolute-path rule on line 87
- Replace the literal `~/.claude/` paths on lines 30 and 50, and say what "strict mode" means on line 8

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Mostly actionable:** the 8 short sections each give a concrete do-this rule.<br>• ⚠️ **Naming clash:** `bash.md` line 72 says variables are `UPPER_SNAKE_CASE`, but line 78 asks for `local` function variables, and it doesn't say whether locals are uppercase too.<br>• ⚠️ **Path clash:** line 47 sources the relative `src/sh/shell_utils.sh`, while line 87 says to use absolute paths where the working directory may vary.<br>• ⚠️ **Strict mode unclear:** line 8 names "strict mode", but lines 38–39 require only `set -e`, with no `-u` or `pipefail`. |
| **Complexity** | 4/10 | 2026-10-25 | • 🧮 **Raw complexity 6:** Concepts 3 (8 separate sections, lines 26–89) + Scope 1 (points into `_templates/utils/`) + Dependencies 1 (`shellcheck`, line 62) + Prerequisites 1 (copy `shell_utils.sh` into each project, line 50).<br>• ⚠️ **Many concepts:** one style guide covers structure, flags, utilities, linting, naming, variables and conditionals, which is what pushes the raw sum past the ~5 anchor. |
| **Evidence of Need** | 7/10 | 2026-10-25 | • 🔗 **Dated usage signal:** `_tests/rules/rules_lazy_load/test_lazy_load_triggers.py` lines 252–258 list `bash.md` among "the rules that missed most often", with its `paths:` trigger added on 2026-10-01.<br>• ⚠️ **Not in the rule:** `bash.md` records no incident or usage evidence itself, only the `miss_cost` reason on line 8. |
| **Token Cost Justification** | N/A | 2026-10-25 | • N/A — lazy-load rule, so the rubric leaves this out of the average |
| **Structural Compliance** | 7/10 | 2026-10-25 | • ✅ **Header and shape:** `paths:` frontmatter, a 3-line metadata header (lines 5–7), an emoji H1, a Purpose line, Contents for 8 headings and 89 lines.<br>• ⚠️ **Bullets without keywords:** the log-level bullets on lines 53–58 have no bold keyword.<br>• ⚠️ **Hardcoded paths:** lines 30 and 50 write a literal `~/.claude/...`, against the hard-gates item "No hardcoded paths or usernames, per `portable_paths.md`".<br>• ⚠️ **Two-clause bullet:** line 89 joins two instructions with a dash. |
| **Currency** | 8/10 | 2026-10-25 | • ✅ **Paths exist:** `_templates/utils/template_bash_script.sh` and `_templates/utils/shell_utils.sh` are both in the repo today.<br>• ⚠️ **Install-dependent:** the literal `~/.claude/` prefix on lines 30 and 50 resolves only where the config sits at the default location.<br>• ⚠️ **Helper list not checked:** line 51's list of helpers (`log_message`, `handle_interruption` and the rest) was not checked against `shell_utils.sh`. |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Structural guard:** `_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` line 55 checks the header, Purpose, links, Contents and the "Safety flags" and "Naming conventions" headings.<br>• 🧪 **Trigger guard:** `test_lazy_load_triggers.py` line 258 checks that the `paths:` trigger stays.<br>• ⚠️ **Gaps:** I didn't run the tests, and nothing checks the backtick template paths on lines 30 and 50, which the link check doesn't parse.<br>• ✅ **No incident:** the rule records none, so it needs no content-regression test. |
| **Overall** | **6.8/10** | 2026-10-25 | • 💪 **Compact and tested:** a short, path-scoped guide with a working structure test and trigger test.<br>• ⚠️ **Held back by:** a raw complexity of 6, the variable and path contradictions (lines 72/78 and 47/87), and the hardcoded `~/.claude/` paths (lines 30 and 50). |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/bash.md` — the rule being scored
- `src/claude/_templates/template_bash_script.sh` — Currency dimension (the real location the stale reference should point to)
- `src/claude/_templates/utils/shell_utils.sh` — Currency dimension (the one reference confirmed correct)

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Stale tier + wrong path:** "Template location" reads `~/.claude/_rules/03_lazy_load/style_guide_standards/unix/templates/template_bash_script.sh` — both the tier (`03_lazy_load` vs. the real `05_lazy_load`) and the subdirectory (`unix` vs. the real `bash`) are wrong. Confirmed via `find`.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
