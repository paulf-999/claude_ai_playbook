# Quality Scorecard — python.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-28

**Overall score:** 7.0/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Move "Meaningful names" and "No history in names" (lines 35–36) out from under "Constants" so they read as rules for every name.
- Rename the "Absolute imports" bullet (line 41) to "No wildcard imports", or add a sentence that actually covers absolute versus relative imports.
- Add the cleanup-handler exception that `python/logging/_error_handling.md` line 95 already uses to the "never `except Exception:`" rule (line 50), or change that child's example.
- Fix the docstring example on lines 58–59, which mentions a "body" the function has no parameter for.
- Split the multi-clause bullets on lines 35, 51 and 91, and reword line 46 as a positive instruction.
- Record a dated style-drift incident, or real loads of this guide, as evidence beyond the "applied" rows.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Clear core:** PEP 8 baseline with a single stated override (line 14), and each section gives concrete do/don't rules.<br>• ⚠️ **Misplaced scope:** "Meaningful names" and "No history in names" (lines 35–36) are nested under "Constants", so they read as applying only to constants.<br>• ⚠️ **Keyword mismatch:** "**Absolute imports:** no wildcard imports" (line 41) labels one rule and states a different one, and absolute versus relative imports are never covered.<br>• ⚠️ **Contradicted absolute:** "never bare `except:` or `except Exception:`" (line 50), yet the child `python/logging/_error_handling.md` line 95 shows `except Exception as e:` as a good cleanup pattern.<br>• ⚠️ **Example slip:** the docstring on line 59 says "from a shebang, header and body", but `build_hook` has no body parameter. |
| **Complexity** | 5/10 | 2026-10-25 | • 🧮 **Raw complexity 5:** Concepts 3 (10 topic sections plus 6 child pages) + Scope 1 (one guide tree, `python.md` plus `python/`) + Dependencies 1 (`ruff`, line 14) + Prerequisites 0.<br>• ⚠️ **Breadth:** this many topics is normal for a style guide, but it sits at the raw-5 anchor. |
| **Evidence of Need** | 7/10 | 2026-10-28 | • 📈 **Recurring applicability:** `docs/audits/rule_usage_sessions.csv` has 30 rows for this guide marked applied, from 2026-08-31 to 2026-09-30.<br>• ⚠️ **One recorded load:** only 1 of those 30 rows has `loaded=1`, and those rows use the old `rules/04_path_scoped/` path, from before `paths:` scoping.<br>• ⚠️ **No incident:** no file records style drift that this guide prevented, and its own header says `miss_cost: low` (line 8). |
| **Token Cost Justification** | N/A | 2026-10-25 | • 🎯 **Path-scoped:** `paths: "**/*.py"` (lines 1–4) loads it only when a Python file is open, so the rubric marks this N/A and leaves it out of the average. |
| **Structural Compliance** | 7/10 | 2026-10-28 | • ✅ **Header and Purpose:** frontmatter, then the version/created/updated header, an emoji H1, a Purpose line and emoji H2s.<br>• ⚠️ **At the limit:** 110 lines, the top of the tolerated range.<br>• ⚠️ **Bullet slips:** semicolon-joined clauses on lines 35, 51 and 91, and a negation ("do not use", line 46) where `writing_style.md` asks for positive framing.<br>• ⚠️ **Prose paragraph:** line 95 packs three instructions into one sentence instead of bullets. |
| **Currency** | 8/10 | 2026-10-25 | • ✅ **Paths exist:** all 6 linked children are on disk under `python/`.<br>• ✅ **Line length current:** the 120 limit (line 14) matches `.pre-commit-config.yaml` line 86 (`ruff --line-length=120`).<br>• ⚠️ **Drift from children:** the `except Exception` ban (line 50) disagrees with `python/logging/_error_handling.md` line 95 and `python/examples/logging_patterns.py` line 33.<br>• ⚠️ **Drift from practice:** `src/claude/_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` was updated 2026-10-27 and still uses `:type:`/`:rtype:`, which line 76 bans, while its header says "Python style compliant: Yes". |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Structural tests:** `test_lazy_load_rule_structure.py` line 51 pins this guide's H2s, and its tests check the header, the Purpose line, child links and link resolution.<br>• 🧪 **Loading pinned:** `test_lazy_load_triggers.py` line 257 requires the `paths:` trigger.<br>• ✅ **Mechanically enforced:** ruff selects N, I, UP031/UP032, BLE, PTH, B006 and D10x (`.pre-commit-config.yaml` line 87), which covers naming, imports, f-strings, broad excepts, pathlib, mutable defaults and docstring presence.<br>• ⚠️ **Not run here:** the reviewer can only read files, so it didn't run the tests.<br>• ⚠️ **Gap:** nothing checks that the guide agrees with its own children, which is how the `except Exception` contradiction got through. |
| **Overall** | **7.0/10** | 2026-10-28 | • 💪 **Well-enforced:** path-scoped, structurally tested, and most rules are backed by ruff in pre-commit.<br>• ⚠️ **Clarity and drift:** misplaced bullets, a mislabelled imports rule, and an absolute `except` ban that its own child contradicts. |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/python.md` — the rule being scored
- `src/claude/_reference/_style_guide_standards/python/logging/_error_handling.md` — Clarity and Currency (`except Exception` in the line 95 good example)
- `src/claude/_reference/_style_guide_standards/python/examples/logging_patterns.py` — Currency (`except Exception` on line 33)
- `docs/audits/rule_usage_sessions.csv` — Evidence of Need (30 applied rows, 1 load)
- `.pre-commit-config.yaml` — Currency and Test Coverage (ruff line length and selected rules, lines 82–93)
- `src/claude/_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` — Test Coverage (structural tests), and Currency (`:type:`/`:rtype:` drift)
- `src/claude/_tests/rules/rules_lazy_load/test_lazy_load_triggers.py` — Test Coverage (`paths:` trigger pinned)
