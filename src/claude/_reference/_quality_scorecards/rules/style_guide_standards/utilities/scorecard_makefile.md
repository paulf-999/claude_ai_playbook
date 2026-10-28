# Quality Scorecard — makefile.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-28

**Overall score:** 6.2/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Bring the repo's own `Makefile` and `src/make/*.mk` into line with the guide, or add a "Known exceptions" section that explains `SHELL = /bin/bash`, the `@echo` colour output and the uppercase colour variables.
- Say which shell `SHELL` must be set to, or state that any explicit value is fine.
- Explain that `$(info)` inside a recipe prints when Make expands the recipe, before any shell line runs, and say when `@echo` is still the right choice.
- Use one word for each strength of rule ("must" or "prefer") and use it consistently across both child pages.
- Add emojis to the child pages' H2 headings so the `#-…` anchors in the Contents list of `_variables_operators_and_commands.md` resolve, or remove the leading `-` from those anchors.
- Reword "do not use `echo`" as a positive instruction, and turn the child pages' prose rules into bold-keyword bullets.
- Record a real incident or usage evidence that justifies the guide, such as a Makefile defect it would have prevented.
- Extend `test_lazy_load_rule_structure.py` so it checks the child pages' metadata headers and that Contents anchors resolve.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 6/10 | 2026-10-25 | • 🔍 **Concrete examples:** every rule comes with a short code example, so it can be acted on.<br>• ⚠️ **SHELL value unclear:** "Every Makefile must define the `SHELL` variable" shows `/bin/sh` but never says whether that value is required.<br>• ⚠️ **`$(info)` timing missing:** the guide says to use `$(info)` instead of `echo`, and its `install:` example puts `$(info)` in a recipe, but it never says this prints at expansion time, before the shell lines run.<br>• ⚠️ **Mixed strength:** "must" (SHELL, naming) and "prefer" (`:=`) appear side by side with no rule for which one applies.<br>• ⚠️ **Variable scope unclear:** "not special to Make or inherited from the environment" leaves project-wide constants such as colour codes open to interpretation. |
| **Complexity** | 6/10 | 2026-10-25 | • 🧮 **Raw complexity 4:** Concepts 3 (7 rules: target naming, variable naming, SHELL, output functions, `:=`, `@`, `$@`) + Scope 1 (parent plus one child folder) + Dependencies 0 + Prerequisites 0.<br>• ⚠️ **Two topics in one child:** `_variables_operators_and_commands.md` bundles five separate rules. |
| **Evidence of Need** | 5/10 | 2026-10-25 | • ❓ **No recorded need:** no file records an incident, issue or usage figure for Makefile style.<br>• ⚠️ **Self-rated low:** the header says `<!-- miss_cost: low — Makefile style drift -->`. |
| **Token Cost Justification** | N/A | 2026-10-25 | • 🎯 **Path-scoped:** `paths:` limits loading to `**/Makefile` and `**/*.mk`, so this is excluded from the average. |
| **Structural Compliance** | 6/10 | 2026-10-25 | • ✅ **Header and split:** the parent has frontmatter, a metadata header, a Purpose line and links to both `_`-prefixed children, and every file is well under 110 lines.<br>• ⚠️ **No heading emojis:** the child pages' H2 headings (`## Targets`, `` ## `SHELL` variable ``, …) have none, against `writing_style.md`.<br>• ⚠️ **Broken anchors:** Contents links such as `#-shell-variable` and `#-simply-expanded-operator` assume emoji headings that don't exist, so they won't resolve.<br>• ⚠️ **Prose and negation:** the rules are written as prose paragraphs rather than bold-keyword bullets, and "do not use `echo`" is a negation. |
| **Currency** | 6/10 | 2026-10-25 | • ✅ **Links resolve:** both child links and the makefiletutorial.com link point at real targets.<br>• 🍂 **Repo drifts from the guide:** the repo's own `Makefile` line 1 is `SHELL = /bin/bash` (`=`, not `:=`).<br>• 🍂 **`echo` everywhere:** `Makefile` and `src/make/mcp.mk` use `@echo` on more than 20 lines.<br>• 🍂 **Uppercase variables:** `src/make/variables.mk` defines `INFO`, `COLOUR_OFF` and similar, against the lowercase-variable rule, and no exception is recorded. |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Parent checked:** `test_lazy_load_rule_structure.py` tracks `makefile.md` (`["Structure"]`) for metadata header, Purpose line, child links, link resolution and Contents-to-heading matches.<br>• 🧪 **Children checked:** the same file checks each child's `_` prefix and Purpose line.<br>• ⚠️ **Gaps:** nothing checks the child pages' metadata headers.<br>• ⚠️ **Anchors untested:** `contents_mismatches` compares entry text only, so the broken `#-…` anchors pass.<br>• 🔍 **No content test needed:** the rule documents no incident, so no content-regression test is warranted. |
| **Overall** | **6.2/10** | 2026-10-25 | • 💪 **Lean and loaded only when needed:** a small, path-scoped guide with clear examples and structural test coverage.<br>• ⚠️ **Not followed at home:** the repo's own Makefiles break three of its rules with no exception recorded, and nothing evidences the need. |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/utilities/makefile.md` — the rule being scored
- `src/claude/_reference/_style_guide_standards/utilities/makefile/_naming_conventions.md` — Clarity, Currency
- `src/claude/_reference/_style_guide_standards/utilities/makefile/_variables_operators_and_commands.md` — Clarity, Structural Compliance
- `Makefile` — Currency (`SHELL = /bin/bash`, `@echo` lines)
- `src/make/mcp.mk` — Currency (`@echo` lines)
- `src/make/variables.mk` — Clarity, Currency (uppercase variables)
- `src/claude/_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` — Test Coverage
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
- `src/claude/rules/01_essentials/claude_usage_standards/writing_style.md` — Structural Compliance
