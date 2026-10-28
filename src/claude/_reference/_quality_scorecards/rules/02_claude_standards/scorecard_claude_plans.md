# Quality Scorecard — claude_plans.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-28

**Overall score:** 7.3/10

**Recommended improvements:**
- Replace the "Ready to proceed to Phase X?" step in `claude_plans.md` with the Next steps format the same section already requires, so the gate prompt has one form.
- Add a "✅ Right" example next to the "❌ Wrong" one in `claude_plans.md`'s Example section.
- Merge the two "wait for explicit approval" sentences in `plan_mode_phase_gates.md` (lines 8 and 17) into one.
- Change "the parent `claude_plans.md`" in `plan_mode_phase_gates.md` and "the parent rule" in `plan_file_format.md` to name the sibling or caller file, since neither is a child of `claude_plans.md` any more.
- Give `plan_mode_phase_gates.md` its own `applies_to`, `miss_cost` and `loading` header lines, or move it under `paths:` / a pointer so it loads only when plan mode is in use.
- Turn the bold-label paragraphs in `plan_file_format.md` (lines 15–29) and the prose lines in `plan_mode_phase_gates.md` (lines 8, 17, 29) into one-sentence, bold-keyword bullets.
- Split `plan_mode_phase_gates.md`'s "Copy on exit" bullet (line 34) into child bullets: destination, naming and status line.
- Extend `test_rule_headers.py`'s entry-point scan to rule files inside tier subfolders, so a header-less file like `plan_mode_phase_gates.md` is caught.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-28 | • 🔍 **Conflict resolved:** the "tightly coupled" skip now says it applies outside plan mode only, matching `plan_mode_phase_gates.md`<br>• ⚠️ **Two gate prompts:** step 2 asks "Ready to proceed to Phase X?" while the Format block asks for a Next steps block, so the prompt's form is open to reading<br>• ⚠️ **Wrong-only example:** the Example section shows only "❌ Wrong: No gate, silent progress", with no correct case |
| **Complexity** | 4/10 | 2026-10-28 | • 🧮 **Raw complexity 6:** Concepts 3 (gates, report format, plan approval, persistence, tilde resolution, table format, plan status) + Scope 2 (two rule folders plus `_plans/`, `plans/` and the Makefile) + Dependencies 1 (`make list_plans` / `make clean_plans` and `plansDirectory`) + Prerequisites 0 — see `_complexity_scoring.md` |
| **Evidence of Need** | 8/10 | 2026-10-28 | • 🔗 **Dated incident:** `plan_mode_phase_gates.md` records the 2026-09-19 literal-`~` plan write<br>• 🔗 **Repeat fixes:** `settings_json_readme.md` logs two dated `plansDirectory` changes (2026-10-01, 2026-10-11) about where plans live<br>• ⚠️ **Core gate unbacked:** the pause-after-each-phase rule itself cites no recorded incident or usage |
| **Token Cost Justification** | 7/10 | 2026-10-25 | • 🎯 **Parent justified:** `claude_plans.md` is always-on with `applies_to: *` and `miss_cost: medium`, and any task can grow into phased work<br>• ✅ **Format scoped:** `plan_file_format.md` loads through `paths:` on `**/_plans/**` and `**/plans/**`, with a pointer for brand-new plans<br>• ⚠️ **Plan-mode child always-on:** `plan_mode_phase_gates.md` (~40 lines) loads every session with no `applies_to`, though only plan-mode sessions need it |
| **Structural Compliance** | 7/10 | 2026-10-28 | • ✅ **Within length:** 82, 41 and 64 lines, each with an emoji H1, Purpose line and metadata header<br>• ⚠️ **Prose, not bullets:** `plan_file_format.md` lines 15–29 are bold-label paragraphs, and `plan_mode_phase_gates.md` lines 8, 17 and 29 are bare prose (line 29 holds two sentences)<br>• ⚠️ **Long bullet:** `plan_mode_phase_gates.md` line 34 ("Copy on exit") packs destination, naming, format and status into one bullet<br>• ⚠️ **Header gap:** `plan_mode_phase_gates.md` has no `applies_to` / `miss_cost` / `loading` lines, and `test_rule_headers.py` only scans top-level tier files, so it isn't caught |
| **Currency** | 8/10 | 2026-10-25 | • ✅ **References exist:** `make list_plans`, `make clean_plans`, `make install`, `plansDirectory` in `settings.json`, `src/claude/TODO.md`, `claude_response_standards.md` and `writing_style.md` all exist<br>• ⚠️ **Stale "parent":** `plan_mode_phase_gates.md` line 15 and `plan_file_format.md` line 61 call `claude_plans.md` the parent, but both now sit outside a `claude_plans/` child folder |
| **Test Coverage** | 9/10 | 2026-10-25 | • 🧪 **Incident pinned:** `test_plan_mode_phase_gates.py` keeps the persistence section and the 2026-09-19 note, tagged `# wording-check: incident record`<br>• 🧪 **Scripts tested:** `test_audit_plans.py` and `test_clean_plans.py` cover the plan-status line and status folders `plan_file_format.md` describes<br>• ⚠️ **Not run here:** I read the structural and header tests but didn't run them, and `plan_mode_phase_gates.md` is outside `test_rule_headers.py`'s scan |
| **Overall** | **7.3/10** | 2026-10-28 | • 💪 **Well split:** gates stay always-on, the file format loads only with plan files, and the one incident is pinned by a test<br>• ⚠️ **Polish gaps:** the gate prompt has two forms, the "parent" wording is stale, the plan-mode file lacks usage headers and the bullet style is mixed |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/claude_working_practices/claude_plans.md` — the rule being scored
- `src/claude/rules/02_claude_standards/claude_working_practices/plan_mode_phase_gates.md` — scored with the rule; Clarity, Evidence, Token Cost, Structural, Currency
- `src/claude/rules/02_claude_standards/path_scoped_rules/plan_file_format.md` — scored with the rule; Token Cost, Structural, Currency
- `src/claude/_tests/rules/02_claude_standards/test_plan_mode_phase_gates.py` — Test Coverage
- `src/claude/_tests/rules/03_authoring_guidelines/test_rule_headers.py` — Structural Compliance, Test Coverage
- `src/claude/_tests/scripts/test_audit_plans.py` — Test Coverage
- `src/claude/_tests/scripts/test_clean_plans.py` — Test Coverage
- `src/claude/settings_json_readme.md` — Evidence of Need
- `src/claude/settings.json` — Currency
- `src/claude/TODO.md` — Currency
- `Makefile` — Currency
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
