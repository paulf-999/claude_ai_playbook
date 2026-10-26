# Quality Scorecard — mermaid.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 6.2/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Widen the `paths:` trigger, or narrow the scope on line 16, so the guide loads with the files it governs
- Remove or add the "reference example" that line 21 says `advanced.md` holds
- Give the children `_` prefixes and Purpose lines, and record evidence of need

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Clear body:** each child section gives a concrete, checkable instruction (two-decision-node threshold, shape table, `classDef` rules)<br>• ⚠️ **Scope vs trigger:** `mermaid.md` line 16 says the rule covers skill `flow.md` files and role READMEs, but lines 2–3 set `paths: "**/*.mmd"`, so a reader can't tell which files it is meant to govern<br>• ⚠️ **Jargon:** "Role READMEs" (`mermaid.md` line 16, `mermaid/fundamentals.md` line 33) is never explained<br>• ⚠️ **Direction wording:** `fundamentals.md` lines 55–59 say "Always use top-down" with `TD`, while `advanced.md` line 70 uses `direction TB` with no note that the two mean the same thing |
| **Complexity** | 6/10 | 2026-10-25 | • 🧮 **Raw complexity 4:** Concepts 3 (eight concepts: when to use, placement, level, direction, shapes, node format, styling, subgraphs) + Scope 1 (parent plus the `mermaid/` folder) + Dependencies 0 + Prerequisites 0 — see `_complexity_scoring.md`<br>• ⚠️ **Many concepts:** the eight concepts across `fundamentals.md` and `advanced.md` hold the score below the ~9 "raw 1" anchor |
| **Evidence of Need** | 4/10 | 2026-10-25 | • ❓ **Speculative:** no incident, issue, PR or usage record appears in `mermaid.md` lines 10–21 or either child<br>• ⚠️ **Hard gate missed:** `_hard_gates_checklist.md` line 26 requires recorded evidence of need, and none of these files has it |
| **Token Cost Justification** | N/A | 2026-10-25 | • N/A — lazy-load rule, so the rubric leaves this out of the average |
| **Structural Compliance** | 6/10 | 2026-10-25 | • ✅ **Parent clean:** frontmatter, three-line metadata header, `miss_cost`/`loading` fields, emoji H1 and Purpose line (`mermaid.md` lines 1–12)<br>• ⚠️ **Child naming:** `mermaid.md` lines 20–21 link `mermaid/fundamentals.md` and `mermaid/advanced.md`, which have no `_` prefix (`_hard_gates_checklist.md` line 16)<br>• ⚠️ **No child Purpose:** `fundamentals.md` lines 4–6 and `advanced.md` line 4 go from the H1 straight into prose or Contents, with no `**Purpose:**` line<br>• ⚠️ **Bullet style:** no bold-keyword lead on `fundamentals.md` lines 21–22, 35, 43–44 or `advanced.md` lines 48–49, 65–66<br>• ⚠️ **Negative framing:** "Do not add" / "Do not embed" / "do not define" (`fundamentals.md` lines 24, 35; `advanced.md` lines 49, 66) |
| **Currency** | 6/10 | 2026-10-25 | • 🍂 **Stale index entry:** `mermaid.md` line 21 says `advanced.md` holds a "reference example", but its Contents (lines 8–11) and headings have no such section<br>• ⚠️ **Trigger drift:** `paths: "**/*.mmd"` (`mermaid.md` line 3) never matches the `flow.md` and README files that line 16 names, so the auto-load misses the files the guide is for<br>• 🔍 **Child dates:** `advanced.md` line 2 was created 2026-06-07, before its parent's 2026-08-28 (`mermaid.md` line 6), which suggests the parent wraps older content |
| **Test Coverage** | 8/10 | 2026-10-25 | • ✅ **Runs:** `_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` line 53 tracks `mermaid.md` for its header, Purpose line, child links, link resolution, Contents and the `Structure` H2<br>• ⚠️ **Children unchecked:** `_rule_texts()` (same file, line 220) reads only the parent, so neither child's header, Purpose or Contents is tested<br>• 🔍 **No regression test needed:** the rule records no incident |
| **Overall** | **6.2/10** | 2026-10-25 | • 💪 **Concrete guidance:** clear thresholds, shape and styling tables, guarded by a dedicated structural test<br>• ⚠️ **Gaps:** no recorded evidence of need, the `paths:` trigger misses the files the guide is for, a stale "reference example" pointer, and children that break the `_` prefix and Purpose conventions |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/utilities/mermaid.md` — the rule being scored
