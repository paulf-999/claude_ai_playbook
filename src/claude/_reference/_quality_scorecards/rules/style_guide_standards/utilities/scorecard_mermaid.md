# Quality Scorecard — mermaid.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-28

**Overall score:** 6.5/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Rewrite the Placement table in `_fundamentals.md` around where diagrams actually live (`_install/docs/` under `## 🔄 Flow`, `docs/reference/`), and either drop the skill `flow.md` row or add `flow.md` to the allowed skill layout in `authoring_skills.md`
- Bring the 5 existing diagrams into line with the node-format, terminal-shape and `classDef milestone` rules, or relax those rules to match how diagrams are really written
- Widen the `paths:` scope, or say plainly that it never fires: no `.mmd` file exists, and every real diagram is embedded in `.md`
- Rewrite the child-page bullets as bold keyword + colon, framed as what to do
- Make the direction wording match (`TD` in `_fundamentals.md`, `TB` in the `_advanced.md` subgraph example), and either explain "some Mermaid versions" or remove it

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Clear thresholds:** "two decision nodes" or "one conditional stop path" (`_fundamentals.md` lines 23–24) gives a testable rule for when to add a diagram<br>• ⚠️ **Undefined term:** "Role READMEs" (`_fundamentals.md` line 35) names nothing in this repo<br>• ⚠️ **Wording mismatch:** "Always use top-down layout: `flowchart TD`" vs `direction TB` in the `_advanced.md` subgraph example (line 72)<br>• ⚠️ **Vague caveat:** "affects rendering in some Mermaid versions" (`_advanced.md` line 41) doesn't say which versions |
| **Complexity** | 6/10 | 2026-10-25 | • 🧮 **Raw complexity 4:** Concepts 3 (8 topics: when, placement, level, direction, shapes, content, styling, subgraphs) + Scope 1 (parent plus `mermaid/` folder) + Dependencies 0 + Prerequisites 0, per `_complexity_scoring.md`<br>• ✅ **One job:** it all serves diagram style, split cleanly into two children |
| **Evidence of Need** | 6/10 | 2026-10-28 | • ✅ **Real use:** 5 Mermaid diagrams exist (4 in `src/claude/_install/docs/`, plus `docs/reference/claude_config/orchestration.md`)<br>• ⚠️ **No recorded need:** no dated incident, issue or usage record in the parent or children, and `miss_cost: low` (line 8)<br>• ⚠️ **Not applied:** none of the 5 diagrams uses the two-line node format, `classDef milestone`, hexagon milestones or rounded terminals, so nothing shows the guide changing practice |
| **Token Cost Justification** | N/A | 2026-10-25 | • 🎯 **Path-scoped:** loads only on `**/*.mmd` (lines 1–4), so it costs no tokens per session<br>• ⚠️ **Never fires:** no `.mmd` file exists in the repo, so in practice it is read only when someone remembers to (line 16) |
| **Structural Compliance** | 7/10 | 2026-10-28 | • ✅ **Clean shell:** metadata header after frontmatter, Purpose lines, emoji H2s, all 3 files well under 110 lines, Contents entries match the headings<br>• ⚠️ **Bullet style:** child bullets don't open with a bold keyword + colon (e.g. `_fundamentals.md` lines 23–24, 37, 45–46; `_advanced.md` lines 50–51, 67–68)<br>• ⚠️ **Negative framing:** "Do **not** add a diagram…" (`_fundamentals.md` line 26), "Do not embed…" (line 37), "Do not use for single-step phases" (`_advanced.md` line 68) go against `writing_style.md`'s positive-action rule |
| **Currency** | 5/10 | 2026-10-28 | • 🍂 **Phantom pattern:** the Placement table's skill `flow.md` row (`_fundamentals.md` line 34) matches no file, and `authoring_skills.md`'s File Organisation allows nothing at skill root beyond `SKILL.md`, the contract, `reference/` and `tests/`<br>• 🍂 **Missing heading:** `## Install sequence` (line 35) appears nowhere, since the real diagrams sit under `## 🔄 Flow` in `_install/docs/*.md`<br>• ⚠️ **Drifted from practice:** for example, `src/claude/_install/docs/install_claude_files.md` lines 8–25 use single-line emoji nodes with no step numbers and no `classDef`, against `_advanced.md` lines 30–51 |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Structural guard:** `test_lazy_load_rule_structure.py` line 54 tracks the parent (header, Purpose, `Structure` heading, children linked, links resolve), and its style-guide checks cover both children's `_` prefix and Purpose line<br>• ✅ **No incident:** it records no incident, so it needs no content-regression test<br>• ⚠️ **Scope unchecked:** no test shows that `**/*.mmd` matches any real file, which is how the dead trigger went unnoticed |
| **Overall** | **6.5/10** | 2026-10-28 | • 💪 **Compact and testable:** short, well split, and structurally guarded, with concrete thresholds and syntax examples<br>• ⚠️ **Out of step with reality:** the placement guidance names things that don't exist, the repo's own diagrams ignore the styling rules, and the path scope never fires |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/utilities/mermaid.md` — the rule being scored
- `src/claude/_reference/_style_guide_standards/utilities/mermaid/_fundamentals.md` — Clarity, Structural Compliance, Currency
- `src/claude/_reference/_style_guide_standards/utilities/mermaid/_advanced.md` — Clarity, Structural Compliance, Currency
- `src/claude/_install/docs/install_claude_files.md` — Evidence of Need, Currency (drift from the guide)
- `src/claude/_install/docs/install_claude_cli.md` — Evidence of Need
- `src/claude/_install/docs/install_mcp_servers.md` — Evidence of Need
- `src/claude/_install/docs/update_claude_files.md` — Evidence of Need
- `docs/reference/claude_config/orchestration.md` — Evidence of Need
- `src/claude/rules/03_authoring_guidelines/authoring_skills.md` — Currency (skill layout has no `flow.md`)
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
- `src/claude/rules/01_essentials/claude_usage_standards/writing_style.md` — Structural Compliance
- `src/claude/_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` — Test Coverage
