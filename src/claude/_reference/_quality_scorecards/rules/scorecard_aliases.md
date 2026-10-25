# Quality Scorecard — aliases.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 7.1/10

**Recommended improvements:**
- Add the standard metadata header and `applies_to` / `miss_cost` fields to `aliases.md`
- Define what the `Ready` and `Testing` statuses mean
- Drop the controls-path repetition in lines 17–25, and use British "optimise" on line 10
- Add a test that checks `aliases.md` has a metadata header

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Clear rows:** each alias has a plain, actionable meaning, such as `plan` → "Enter plan mode" on line 13.<br>• ⚠️ **Undefined status:** `aliases.md` lines 5–13 use the statuses `Ready` and `Testing` but never say what they mean or when a `Testing` alias becomes `Ready`.<br>• ⚠️ **Repeated pointer:** lines 7, 11 and 12 each embed the controls path, and lines 17–25 say it again in prose, so the reader must check that the two agree. |
| **Complexity** | 9/10 | 2026-10-25 | • 🧮 **Raw complexity 1:** Concepts 1 (an alias list plus one pointer to the controls doc) + Scope 0 (one file) + Dependencies 0 + Prerequisites 0, per `_complexity_scoring.md`.<br>• ⚠️ **Second concept:** the "Note on automation controls" section (`aliases.md` lines 17–25) is the one extra concept above raw 0. |
| **Evidence of Need** | 6/10 | 2026-10-25 | • ❓ **No usage record:** `aliases.md` has no usage-evidence section, incident or issue reference showing these shortcuts are used.<br>• ⚠️ **Built-ins listed:** `/batch`, `/goal`, `/loop`, `/fewer-permission-prompts` and `plan` (lines 7, 10–13) appear to be Claude Code's own commands, and no file shows that documenting them fixed a real problem.<br>• ✅ **Custom shorthands:** `bullets` and `draft` (lines 8–9) are this config's own shorthands, which gives some sign they were needed. |
| **Token Cost Justification** | 6/10 | 2026-10-25 | • ⚖️ **Always imported:** `CLAUDE.md`'s `@~/.claude/aliases.md` loads the file every session, and the file is small (25 lines).<br>• ⚠️ **No `applies_to` / `miss_cost`:** `aliases.md` line 1 goes straight to the H1, so nothing in the file justifies loading it always-on.<br>• ⚠️ **Duplicate tokens:** lines 17–25 repeat the controls path that lines 7, 11 and 12 already carry, so every session pays for it twice. |
| **Structural Compliance** | 5/10 | 2026-10-25 | • ❌ **No metadata header:** `aliases.md` line 1 is the H1, with no `version` / `created` / `updated` lines, which fails `_hard_gates_checklist.md` line 19.<br>• ⚠️ **Bullets without bold keywords:** lines 20–23 ("Turn budgets and caps", …) have no bold keyword, against `_hard_gates_checklist.md` line 25.<br>• ⚠️ **Prose paragraphs:** line 19 is a multi-clause paragraph and line 25 is a loose prose sentence, not bullets.<br>• ⚠️ **American spelling:** line 10 uses "optimize", where British English is the house style.<br>• ✅ **Basics met:** emoji H1, a Purpose line (line 3), well under 110 lines, and one concept. |
| **Currency** | 8/10 | 2026-10-25 | • ✅ **Paths checked:** `test_referenced_rule_paths_exist` in `_tests/_root_files/test_aliases.py` (lines 111–116) proves the `_automation_controls.md` path in lines 7, 11 and 12 exists.<br>• ⚠️ **Unchecked commands:** nothing in the inputs shows that `/fewer-permission-prompts` (line 10) or the `Testing` status of `/batch`, `/goal` and `/loop` (lines 7, 11, 12) still match today's Claude Code. |
| **Test Coverage** | 9/10 | 2026-10-25 | • ✅ **Content tests:** `_tests/_root_files/test_aliases.py` has 18 tests: required fields, valid status, unique inputs, input format, paths exist, the note matches the table, core aliases kept, plus negative cases for the parser.<br>• ✅ **Wiring tests:** `test_claude_md_imports_aliases` (`_tests/rules/02_claude_standards/test_always_on_reachability.py` line 68) and `test_aliases_at_claude_root` (`_tests/rules/test_rules_structure_layout.py` line 86) check the import and the file's location.<br>• ⚠️ **No header check:** none of the tests found checks that `aliases.md` has a metadata header, which is how the gap on line 1 went unnoticed. |
| **Overall** | **7.1/10** | 2026-10-25 | • 💪 **Well tested:** a strong set of tests, and simple to follow.<br>• ⚠️ **Structure and justification gaps:** no metadata or usage headers, no recorded evidence of need, and the pointer to the controls doc appears twice. |

## 🔗 Related files

- `src/claude/aliases.md` — the rule being scored
- `src/claude/_tests/_root_files/test_aliases.py` — Test Coverage dimension
- `src/claude/_tests/rules/test_aliases_behavior.py` — Test Coverage dimension
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_automation_controls.md` — Currency dimension
