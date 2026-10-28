# Quality Scorecard — datetime.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-28

**Overall score:** 7.0/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Rename or rewrite the "Known exceptions" section: it says "None" but goes on to describe a real exception (filenames use `YYYY_MM_DD`).
- Say which side wins when content is both technical and human-facing (e.g. a technical Confluence page), and say whether the UTC rule also covers plain dates.
- Move the "apply opportunistically" instruction out of the "Applies to" list (line 49) and state it once.
- Spell out "DR" and "catchup prep" in the human-facing list, or drop them.
- Turn the prose blocks at lines 10–12 and 35–36 into bullets with one sentence each, and phrase them as positive actions.
- Start each bullet in "Applies to" and "Does not apply" with a bold keyword.
- Record a dated incident or a use of this rule, or reconsider whether it needs its own file, since the usage audit shows 0 loads.
- Add "Applies to — technical contexts" and "Does not apply — human-facing content" to the required headings for datetime.md in `test_lazy_load_rule_structure.py`.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 6/10 | 2026-10-28 | • ⚠️ **Contradictory exception:** line 55 says `**None:**` and then describes a real exception (filenames use `YYYY_MM_DD`, not `YYYY-MM-DD`)<br>• ⚠️ **Overlapping contexts:** "Code files and technical documentation" (line 47) and "Confluence pages" (line 63) overlap, and nothing says which wins for a technical Confluence page<br>• ⚠️ **UTC scope:** line 35 makes UTC required "for all datetimes" but doesn't say whether a plain `YYYY-MM-DD` date is also a UTC date<br>• ⚠️ **Jargon:** "DR tracking notes" and "catchup prep output" (lines 67–68) are not explained<br>• 🔍 **Clear core:** the format table (lines 26–29) is clear and has examples |
| **Complexity** | 8/10 | 2026-10-25 | • 🧮 **Raw complexity 2:** Concepts 2 (date format, datetime format, UTC, technical vs human contexts, apply-when-editing) + Scope 0 (single file) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 5/10 | 2026-10-28 | • ⚠️ **No incident:** the file records no dated problem that led to the rule<br>• ⚠️ **No recorded use:** `docs/audits/audit_rule_usage.md` shows 0 loads across 115 sessions, and its flag is "no trigger"<br>• 🔗 **One pointer:** `naming_standards.md` line 21 is the only route to it |
| **Token Cost Justification** | N/A | 2026-10-25 | • 🎯 **Lazy:** read on demand through the `naming_standards.md` pointer, with a `loading: lazy` header that gives the reason, so it's left out of the average |
| **Structural Compliance** | 6/10 | 2026-10-25 | • ✅ **Header and length:** a valid metadata header, a `miss_cost` and a `loading` comment, a Purpose line, emoji H2s, 69 lines, and a Contents section justified by its 5 H2s<br>• ⚠️ **Prose blocks:** lines 10–12 (three sentences) and lines 35–36 (two sentences) are paragraphs, not one-sentence bullets<br>• ⚠️ **No bold keywords:** none of the bullets at lines 44–49 or 63–68 starts with a bold keyword and colon<br>• ⚠️ **Negative framing:** "Do not retroactively update" (line 11) and "do not update files solely…" (line 49) are phrased as prohibitions |
| **Currency** | 9/10 | 2026-10-28 | • ✅ **References exist:** `writing_style.md` and its `YYYY_MM_DD_<topic>.md` convention, and the `created`/`updated` metadata lines, all match current files<br>• 🔍 **Outside this file:** `docs/audits/audit_rule_usage.md` still lists this rule under the old `05_lazy_load/` path, so that report is out of date, not the rule |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Structural guard:** `test_lazy_load_rule_structure.py` checks its header, Purpose line, Contents entries, links and 3 required H2s<br>• 🧪 **Reachability:** `test_lazy_load_coverage.py` lists it as an on-demand entry point<br>• ⚠️ **Scope sections unguarded:** the two "Applies to" and "Does not apply" H2s, which carry the core scope, are not among the required headings<br>• 🔍 **Not run here:** this review was read-only, so a pass is inferred from the files and was not observed |
| **Overall** | **7.0/10** | 2026-10-28 | • 💪 **Simple and current:** a short, single-concept rule whose references all resolve, with structural tests<br>• ⚠️ **Gaps:** the "None" exception that contradicts itself, technical and human contexts that overlap, style slips, and no recorded need |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/utilities/datetime.md` — the rule being scored
- `src/claude/rules/01_essentials/claude_usage_standards/naming_standards.md` — Evidence of Need (the only pointer to this rule)
- `src/claude/rules/01_essentials/claude_usage_standards/writing_style.md` — Currency (the filename date convention it cites)
- `docs/audits/audit_rule_usage.md` — Evidence of Need (0 loads) and Currency (old path)
- `src/claude/_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` — Test Coverage
- `src/claude/_tests/rules/rules_lazy_load/test_lazy_load_coverage.py` — Test Coverage
