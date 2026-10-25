# Quality Scorecard — makefile.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 6.2/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Indent the recipe examples with tabs, since space-indented recipes fail with "missing separator"
- Resolve the echo ban (`variables_operators_and_commands.md` line 28) against the `@echo` example on lines 57–58
- Use `:=` in the `SHELL` example on line 21, as lines 40–44 recommend
- Give the children `_` prefixes, Purpose lines and emoji headings

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 6/10 | 2026-10-25 | • ⚠️ **Self-contradiction:** `makefile/variables_operators_and_commands.md` line 28 says "do not use `echo`", but its own example at lines 57–58 uses `@echo`<br>• ⚠️ **Mixed operator:** the `SHELL = /bin/sh` example at line 21 uses `=`, while lines 40–44 say to prefer `:=` and avoid `=`<br>• 🔍 **No scope for the echo ban:** line 28 doesn't say whether the ban covers recipe lines or only Make-level messages, so readers could apply it either way |
| **Complexity** | 6/10 | 2026-10-25 | • 🧮 **Raw complexity 4:** Concepts 3 (7 separate conventions: target naming, variable naming, SHELL, display built-ins, `:=`, `@` and `$@`) + Scope 1 (a parent plus one child folder) + Dependencies 0 + Prerequisites 0, per `_complexity_scoring.md`<br>• 🔍 **Gap:** `makefile.md` lines 17–18 cover more concepts than the ~7 anchor's single job |
| **Evidence of Need** | 5/10 | 2026-10-25 | • ❓ **No evidence on file:** `makefile.md` line 13 states a purpose ("the team's standards") but records no incident, PR or repeated failure<br>• ⚠️ **Unrecorded need:** no file shows Makefile style drift ever happening, which matches the ~5 "speculative" anchor |
| **Token Cost Justification** | N/A | 2026-10-25 | • N/A — lazy-load rule, so the rubric leaves this out of the average |
| **Structural Compliance** | 6/10 | 2026-10-25 | • ✅ **Parent clean:** `makefile.md` has `paths:` frontmatter, the metadata header (lines 6–8), an emoji H1, a Purpose line and 19 lines<br>• ⚠️ **Children lack Purpose:** `makefile/naming_conventions.md` and `makefile/variables_operators_and_commands.md` have no `**Purpose:**` line under their H1 (line 4 in each)<br>• ⚠️ **No emoji on H2s:** child headings such as `## Targets` (naming line 6) and `## \`SHELL\` variable` (variables line 16) have no emoji, while the Contents anchors at variables lines 8–12 (`#-shell-variable`) assume one<br>• ⚠️ **Child prefix:** the child files have no `_` prefix, which `_hard_gates_checklist.md` line 16 requires<br>• ⚠️ **Prose, not bullets:** child guidance is in prose paragraphs (e.g. naming line 8, variables line 40), not bold-keyword bullets |
| **Currency** | 6/10 | 2026-10-25 | • ✅ **Links resolve:** both child links in `makefile.md` lines 17–18 point to files that exist<br>• 🚩 **Broken examples:** the recipe lines in `makefile/naming_conventions.md` line 12 and `makefile/variables_operators_and_commands.md` lines 57–58 and 69 are indented with spaces, and a Grep for leading tabs found none, so copying them gives GNU Make's "missing separator" error<br>• 🔍 **Narrow globs:** `makefile.md` lines 3–4 match `Makefile` and `*.mk` but not `makefile` or `GNUmakefile` |
| **Test Coverage** | 8/10 | 2026-10-25 | • ✅ **Structural test runs:** `_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` line 58 tracks `makefile.md`, checking its header, Purpose line, child links, relative links and the `Structure` H2<br>• ⚠️ **Children unchecked:** that test reads only the parent's text (lines 218–220), so it misses the children's missing Purpose lines and the space-indented recipes<br>• 🔍 **No incident:** no incident is recorded, so no content-regression test is needed |
| **Overall** | **6.2/10** | 2026-10-25 | • 💪 **Lean, wired parent:** a 19-line path-scoped entry with a valid header, guarded by a structural test that runs<br>• ⚠️ **Child quality:** the children contradict themselves (echo ban, `=` vs `:=`), break when copied (space-indented recipes) and skip house structure (no Purpose, emoji or `_` prefix), and no evidence of need is recorded |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/utilities/makefile.md` — the rule being scored

---

## 🚩 Pre-existing issue disclosed, not fixed

- 🐛 **Broken reference:** "Templates are available in `~/.claude/templates/makefile/`" — confirmed via `find` that no such directory exists anywhere in this repo, under either `templates/` or `_templates/`.
- 📋 **Disposition:** out of scope for this scorecard — flagged here per this config's pre-existing-issue disclosure rule, not silently fixed.
