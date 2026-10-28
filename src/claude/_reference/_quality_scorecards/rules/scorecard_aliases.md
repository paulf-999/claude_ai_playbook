# Quality Scorecard — aliases.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-27

**Overall score:** 7.7/10

**Recommended improvements:**
- Add a dated usage record, or an incident, for at least the `bullets`, `draft` and `plan` aliases (for example, rows in a usage CSV).
- Say in one line how an alias triggers: only when the whole message is the alias, or anywhere in a message.
- Define the `Ready` and `Testing` statuses in the file.
- Name the controls file once, in the note, and drop the copy from the three automation rows.
- Split the `/fewer-permission-prompts` meaning, which is two clauses joined by a semicolon, into one clause.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Clear table:** the table plus line 9's Purpose make each shortcut easy to read<br>• ⚠️ **Trigger unstated:** nothing says whether `plan` (line 19) or `draft` (line 15) fires only as a whole message or anywhere in a sentence<br>• ⚠️ **Status undefined:** the `Ready` / `Testing` values are used but never explained in the file |
| **Complexity** | 8/10 | 2026-10-27 | • 🧮 **Raw complexity 2:** one concept in one file, with one dependency (`_automation_controls.md`) and no prerequisites |
| **Evidence of Need** | 5/10 | 2026-10-27 | • ❓ **No record:** no file records a use of any alias or an incident behind one<br>• ⚠️ **Illustration only:** the `/fewer-permission-prompts` line in `usage_evidence.md` (line 20) is a template example, not a recorded use |
| **Token Cost Justification** | 8/10 | 2026-10-27 | • 🎯 **Justified placement:** `applies_to: *` is set and CLAUDE.md line 32 imports the file, because shortcuts have to work in every session<br>• ⚠️ **Repeated path:** the long controls path appears four times (lines 13, 17, 18 and 25), which costs tokens every session for little gain<br>• ⚠️ **Low miss cost:** the header itself says `miss_cost: low` (line 5) |
| **Structural Compliance** | 8/10 | 2026-10-27 | • ✅ **Clean shape:** metadata header, emoji H1, Purpose line, 28 lines, bold-keyword bullets in the note<br>• ⚠️ **Style slip:** the line 16 meaning joins two clauses with a semicolon ("Audit transcripts…; optimise…")<br>• ⚠️ **Duplication:** the rows repeat the controls pointer that line 25's note already gives |
| **Currency** | 9/10 | 2026-10-27 | • ✅ **Paths exist:** `_automation_controls.md` exists at the named path, and `test_referenced_rule_paths_exist` keeps it checked<br>• 🔍 **Built-ins not verifiable:** `/batch`, `/goal`, `/loop` and `/fewer-permission-prompts` are Claude Code commands that no repo file can confirm |
| **Test Coverage** | 9/10 | 2026-10-25 | • 🧪 **Dedicated suite:** `test_aliases.py` has 18 tests covering parsing, required fields, status values, input format, rule paths existing, note-to-table match, core aliases and the metadata header<br>• 🧪 **Layout check:** `test_rules_structure_layout.py::test_aliases_at_claude_root` checks where the file lives<br>• 🔍 **No incident to regress:** the rule records no incident, so no content-regression test is needed |
| **Overall** | **7.7/10** | 2026-10-27 | • 💪 **Well tested:** a strong mechanical suite guards a small, current file<br>• ⚠️ **No usage evidence:** nothing on file shows the aliases are used, which holds the score back most |

## 🔗 Related files

- `src/claude/aliases.md` — the rule being scored
- `src/claude/CLAUDE.md` — line 32 import (Token Cost Justification)
- `src/claude/rules/02_claude_standards/claude_working_practices/claude_operational_efficiency/_automation_controls.md` — the controls file it names (Currency, Token Cost, Structural)
- `src/claude/rules/_rules_lazy_load/claude_config/usage_evidence.md` — illustrative alias examples only (Evidence of Need)
- `src/claude/_tests/_root_files/test_aliases.py` — dedicated test suite (Test Coverage, Currency)
- `src/claude/_tests/rules/test_rules_structure_layout.py` — root-location check (Test Coverage)
