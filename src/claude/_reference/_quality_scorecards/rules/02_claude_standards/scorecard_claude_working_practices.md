# Quality Scorecard — claude_working_practices.md

**Date Created:** 2026-10-11
**Date Updated:** 2026-10-25

**Overall score:** 7.9/10

**Recommended improvements:**
- Make the Contents summary on line 16 name all six operational-efficiency topics
- Add a test that the index's three pointers resolve and its Contents matches its headings
- Record why the index layer is needed

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-25 | • 🎯 **Index purpose clear:** `claude_working_practices.md` line 9 names the three practice areas, and lines 21–31 point to each one without any ambiguity<br>• ⚠️ **Summary under-describes:** line 16 sums up operational efficiency as "token awareness, delegation, turn budgets and automation controls", but `claude_operational_efficiency.md` lines 19–21 also cover external system access, task request conventions and MCP toggling<br>• ⚠️ **Loose gate wording:** `claude_plans.md` line 31 ("tightly coupled … stopping breaks workflow") and line 41 ("or similar") leave room for readers to judge differently |
| **Complexity** | 8/10 | 2026-10-25 | • 🧮 **Raw complexity 2:** Concepts 1 (3 topics) + Scope 1 (one folder, `claude_working_practices/`) + Dependencies 0 + Prerequisites 0<br>• ⚠️ **Fans out widely:** each child is itself a parent, with `claude_operational_efficiency.md` lines 45–83 naming 6 more children |
| **Evidence of Need** | 7/10 | 2026-10-25 | • ✅ **Dated incidents in one child:** `portable_paths.md` lines 21–28 record 4 incidents from 2026-09-17/18<br>• ⚠️ **No recorded need for the index itself:** the only record is a test comment, `test_always_on_reachability.py` line 85 ("indexes the plans, efficiency and portable-paths group"), with no incident or usage data<br>• ⚠️ **Two children unbacked:** `claude_plans.md` lines 76–80 give a made-up example rather than a dated incident, and `claude_operational_efficiency.md` records none |
| **Token Cost Justification** | 7/10 | 2026-10-25 | • ⚖️ **`applies_to` set:** `applies_to: *` on line 4 is honest for content about how Claude works, and the file is small at 32 lines<br>• ⚠️ **Pointer-only content:** lines 21–31 only restate that children "load on their own", which Claude Code does anyway, yet the file adds a startup file (`test_always_on_reachability.py` line 85, 42 → 43) |
| **Structural Compliance** | 8/10 | 2026-10-25 | • ✅ **Parent clean:** metadata and usage header on lines 1–6, an emoji H1, a Purpose line, Contents justified by 3 `##` headings, 32 lines and no Related section<br>• ⚠️ **Child style slips:** `claude_plans.md` lines 24–32 and 68–72 have bullets with no bold keyword, plus "Do NOT" negative framing<br>• ⚠️ **Multi-sentence lines:** `portable_paths.md` lines 15, 17 and 38 each hold several sentences |
| **Currency** | 9/10 | 2026-10-25 | • ✅ **Pointers resolve:** all three child paths on lines 23, 27 and 31 exist and were read<br>• 🔍 **Small count drift:** `portable_paths.md` line 23 says "all three shipped" but lines 25–28 list four incidents (the fourth is dated a day later) |
| **Test Coverage** | 8/10 | 2026-10-25 | • ✅ **Group structure tested:** `test_rule_directory_organisation.py` line 47 registers the folder as a grouping folder<br>• ✅ **Efficiency child tested:** `test_rule_cross_references.py` lines 224–247 check its child pointers, orphans and Contents<br>• ✅ **Portable paths enforced:** by `test_portable_paths_python.py` and `test_portable_paths_hooks.py`<br>• ⚠️ **Index pointers untested:** no test found by Grep checks that lines 23, 27 and 31 resolve, or that the Contents entries on lines 15–17 match the headings, as `test_rule_cross_references.py` does for the efficiency child |
| **Overall** | **7.9/10** | 2026-10-25 | • 💪 **Lean, tested index:** a small, well-formed index over children that are tested and partly backed by incidents<br>• ⚠️ **Gaps:** no recorded need for the index layer, a Contents summary that misses three efficiency topics, and no direct test of its own pointers |

## 🔗 Related files

- `src/claude/rules/02_claude_standards/claude_working_practices.md` — the rule being scored
- `src/claude/_tests/rules/01_essentials/test_rule_directory_organisation.py` — Structural Compliance and Test Coverage dimensions
- `src/claude/_tests/rules/02_claude_standards/test_always_on_reachability.py` — Token Cost Justification dimension
