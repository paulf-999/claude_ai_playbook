# Quality Scorecard — datetime.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 6.7/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Change line 44's "Frontmatter fields" to the HTML-comment metadata header
- Fix the Contents anchors on lines 18 and 20 so they match the em-dash headings
- Record evidence of need, and give the bullets on lines 44–49 and 63–68 bold keywords

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Clear core:** the two-row format table (lines 26–29) and the UTC-with-`Z` rule (lines 35–36) are unambiguous.<br>• ⚠️ **Mixed list:** `datetime.md` line 49 puts a timing condition ("Existing files being actively modified for another reason") into a list of technical contexts, which repeats lines 11–12 and muddles what the list means.<br>• ⚠️ **Undefined term:** `datetime.md` line 68 says "DR tracking notes" without explaining "DR". |
| **Complexity** | 8/10 | 2026-10-25 | • 🧮 **Raw complexity 2:** Concepts 2 (formats, timezone, technical scope, exceptions, human-facing scope) + Scope 0 (one file) + Dependencies 0 + Prerequisites 0, per `_complexity_scoring.md`.<br>• ⚠️ **Five concepts:** `datetime.md` lines 24–68 cover five separate aspects, which keeps it at the Concepts 2 band. |
| **Evidence of Need** | 4/10 | 2026-10-25 | • ❓ **None recorded:** `datetime.md` has no incident, PR or usage record anywhere in lines 1–68.<br>• ⚠️ **Gate unmet:** `_hard_gates_checklist.md` line 26 requires evidence of need to be recorded, and the only rationale given is the general sort-and-compare claim on line 8. |
| **Token Cost Justification** | N/A | 2026-10-25 | • N/A — lazy-load rule, so the rubric leaves this out of the average |
| **Structural Compliance** | 6/10 | 2026-10-25 | • ✅ **Basics met:** it has the metadata header plus `miss_cost` and `loading` (lines 1–5), an emoji H1, a Purpose line, 69 lines and a Contents section that its 5 headings justify.<br>• ⚠️ **Prose paragraphs:** `datetime.md` lines 10–12 and 35–36 are multi-sentence prose where the style calls for bullets with one sentence each.<br>• ⚠️ **No bold keywords:** the bullets on `datetime.md` lines 44–49 and 63–68 don't open with a bold keyword, against `_hard_gates_checklist.md` line 25.<br>• ⚠️ **Anchor slugs:** `datetime.md` lines 18 and 20 use `#-applies-to-technical-contexts` and `#-does-not-apply-human-facing-content`, but em-dash headings usually slug to a double hyphen (`-applies-to--technical-contexts`), so these links probably don't resolve. |
| **Currency** | 7/10 | 2026-10-25 | • ⚠️ **Header drift:** `datetime.md` line 44 calls `created` and `updated` "Frontmatter fields", but the metadata header is the HTML-comment lines 1–3 (its own lines 1–3, and `_hard_gates_checklist.md` line 19), not frontmatter.<br>• ⚠️ **Unverified field:** nothing in the allowed inputs shows the `last-reviewed` field on `datetime.md` line 44 still exists.<br>• ⚠️ **Empty section:** `datetime.md` line 55 keeps a "Known exceptions" heading only to say "None", which reads like a leftover from an exception that was removed. |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Structural guard:** `_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` line 47 tracks this file, checking its header, Purpose line, required H2s, links and Contents text.<br>• 🧪 **Reachability:** `_tests/rules/rules_lazy_load/test_lazy_load_coverage.py` line 151 lists it as an on-demand entry point.<br>• ⚠️ **Gaps:** `contents_mismatches` (`test_lazy_load_rule_structure.py` lines 188–198) compares Contents text only, not anchor slugs, so it can't catch the line 18/20 problem, and no test checks bold-keyword bullets. No incident is recorded, so no content-regression test is owed. |
| **Overall** | **6.7/10** | 2026-10-25 | • 💪 **Strength:** short, single-file and clearly bounded between technical and human-facing dates, with structural tests that run.<br>• ⚠️ **Gap:** no recorded evidence of need, style slips in its prose and bullets, and the "Frontmatter fields" wording no longer matches the HTML-comment header. |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/utilities/datetime.md` — the rule being scored
