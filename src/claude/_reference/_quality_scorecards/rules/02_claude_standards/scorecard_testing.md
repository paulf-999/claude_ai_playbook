# Quality Scorecard — testing.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-27

**Overall score:** 7.3/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Swap the ML examples in Test Goals (F1, accuracy, sentiment, sarcasm) for examples from this config's own hooks, scripts and rules, or move the section into `_testing_design_pattern.md`.
- Record the evidence of need: at least one dated incident or issue where code shipped without a test.
- Cut the always-loaded concept count by moving Test Goals, and possibly Test Layers, into lazy children.
- Justify `**/*.sql` in `paths:` with SQL- or dbt-specific guidance, or remove it.
- Put each bullet's emoji before the bold keyword (`🆕 **New features:**`), not inside it.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Clear core:** "if you added code, write a test" and the When Tests Are Required list are easy to act on<br>• ⚠️ **Off-domain goals:** lines 39–43 talk about "accurate sentiment classification", F1/accuracy and sarcasm, which don't fit a config repo of hooks, scripts and rules<br>• ⚠️ **Code vs config:** line 17 says "if you added code", but line 23 also requires tests for "config settings", so the trigger is wider than the rule of thumb says |
| **Complexity** | 5/10 | 2026-10-25 | • 🧮 **Raw complexity 5:** Concepts 2 (5 sections: when, goals, layers, writing, running) + Scope 2 (`_tests/` subfolders plus `_rules_lazy_load/testing_lazy_load/`) + Dependencies 1 (pytest/`CLAUDE_CONFIG_DIR`) + Prerequisites 0<br>• ⚠️ **Two tables:** Test Goals and Test Layers both load every time, and either could live in a lazy child |
| **Evidence of Need** | 6/10 | 2026-10-27 | • ✅ **Established practice:** `test_testing.py` checks that every hook has a test, so the requirement is in active use<br>• ⚠️ **No dated incident:** the only incident in the rule (line 29, 2026-09-21) belongs to `_concurrent_sessions.md`, not to this rule's need |
| **Token Cost Justification** | N/A | 2026-10-25 | • 🎯 **Path-scoped:** loads only for `*.py`, `*.sh`, `*.sql` and `_tests/**` (lines 2–6), so it's left out of the average<br>• ⚠️ **SQL glob:** nothing in the body is SQL- or dbt-specific, so `**/*.sql` loads it where it adds little |
| **Structural Compliance** | 8/10 | 2026-10-27 | • ✅ **Shape:** 89 lines, `paths:` frontmatter, version/created/updated header, emoji H1/H2s, Purpose line, bold-keyword bullets<br>• ⚠️ **Emoji placement:** bullets such as line 23 `**🆕 New features:**` put the emoji inside the bold keyword, not before it<br>• ⚠️ **Not run here:** this review is read-only, so it didn't confirm that `test_rules_structure.py` and the header tests pass |
| **Currency** | 9/10 | 2026-10-27 | • ✅ **All references exist:** every test file in lines 29–68, all 5 lazy children, `_shared_paths.py`, `_tests/README.md` and `_tests/_root_files/` exist at commit 1705887<br>• ✅ **Metadata scans real:** per-type header tests exist for hooks, agents, skills and config metadata |
| **Test Coverage** | 9/10 | 2026-10-27 | • 🧪 **Dedicated test:** `test_testing.py` checks that the children exist, that every named `test_*.py` exists, that relative links resolve and that hooks map to tests<br>• ✅ **No incident to pin:** the rule records no incident of its own, so no content-regression test is needed<br>• ⚠️ **Pass not recorded:** none of the files read shows a recorded test run |
| **Overall** | **7.3/10** | 2026-10-27 | • 💪 **Well-verified:** every file it names exists, and a dedicated test checks that<br>• ⚠️ **Gaps:** ML-flavoured goals, a high concept count and no recorded evidence of need |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/path_scoped_rules/testing.md` — the rule being scored
- `src/claude/_tests/rules/02_claude_standards/test_testing.py` — Test Coverage, Currency
- `src/claude/_tests/rules/test_rules_structure.py` — Structural Compliance, Test Coverage
- `src/claude/_tests/_shared_checks/test_metadata_header_format.py` — Structural Compliance
- `src/claude/_tests/hooks/test_hook_metadata_header.py` — Currency
- `src/claude/_tests/agents/test_agent_metadata_header.py` — Currency
- `src/claude/_tests/skills/_all_skills/test_skill_metadata_header.py` — Currency
- `src/claude/_tests/rules/03_authoring_guidelines/test_claude_config_metadata.py` — Currency
- `src/claude/_tests/rules/02_claude_standards/test_concurrent_sessions.py` — Evidence of Need
- `src/claude/rules/_rules_lazy_load/testing_lazy_load/_testing_design_pattern.md` — Complexity (where Test Goals could move)
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity formula
