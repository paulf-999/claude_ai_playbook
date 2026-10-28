# Quality Scorecard — docker.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-28

**Overall score:** 6.5/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Add Compose guidance to the guide, or drop the `docker-compose*` globs from `paths:`, so the guide doesn't load where it has nothing to say
- Add `compose.yaml` / `compose.yml` to `paths:` if Compose guidance is kept, since that's the current Compose file name
- Make the multi-stage example follow the mandated section order, putting `WORKDIR` before `COPY`
- Add a `USER` step to the Fundamentals structure template, so it matches the non-root rule in Advanced
- Rewrite the child-page bullets as bold-keyword bullets with one sentence each, phrased as positive actions
- Record the evidence of need, such as a dated review finding or a project that uses the guide
- Add a check that every `paths:` glob has matching content, or note in the scorecard why the structural test is enough

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • ✅ **Actionable:** most points come with a Good/Bad Dockerfile example (`_fundamentals.md` lines 22–28, `_advanced.md` lines 23–47)<br>• ⚠️ **Compose gap:** `paths:` loads the guide for `docker-compose*.yml`/`.yaml`, but no page says anything about Compose<br>• ⚠️ **Self-contradiction:** `_fundamentals.md` line 34 says "Follow this section order" with `WORKDIR` second, but the `_advanced.md` multi-stage example (lines 102–105) puts `COPY` before `WORKDIR`<br>• ⚠️ **Missing step:** the structure template (`_fundamentals.md` lines 36–60) has no `USER` step, although `_advanced.md` line 53 requires non-root |
| **Complexity** | 6/10 | 2026-10-25 | • 🧮 **Raw complexity 4:** Concepts 3 (7 areas: base images, structure, naming, layers, security, .dockerignore, multi-stage) + Scope 1 (a parent plus one child folder) + Dependencies 0 + Prerequisites 0 |
| **Evidence of Need** | 4/10 | 2026-10-25 | • ❓ **No incident:** no file records a Docker review failure or a bloated image, and `<!-- miss_cost: medium -->` is a claim with no evidence behind it<br>• ⚠️ **No recorded use:** `docs/audits/rule_usage_history.csv` shows 0 applied and 0 loaded across 115–146 sessions in all six 2026-10-01 rows |
| **Token Cost Justification** | N/A | 2026-10-25 | • 🎯 **Path-scoped:** loads only for Dockerfiles and compose files, so it isn't in the average<br>• ⚠️ **Wasted load:** compose files load a guide with no compose content (see Clarity) |
| **Structural Compliance** | 6/10 | 2026-10-25 | • ✅ **Parent clean:** 20 lines, frontmatter then the metadata header, emoji H1, a Purpose line, and both children linked<br>• ⚠️ **No bold keywords:** child bullets have no leading bold keyword (`_fundamentals.md` lines 18–20 and 66–68, `_advanced.md` lines 19–21 and 53–57)<br>• ⚠️ **Multi-sentence bullets:** `_fundamentals.md` line 20 ("…image size. Only use full images…") and `_advanced.md` lines 53–54<br>• ⚠️ **Negative framing:** "Do not run…", "Never embed…" and "Do not use `ADD`…" break the positive-actions rule<br>• ⚠️ **At the limit:** `_advanced.md` is 109 lines, right at the 110-line tolerance |
| **Currency** | 8/10 | 2026-10-28 | • ✅ **Links resolve:** both child links exist, and the commands (`apt-get`, `pip --no-cache-dir`, `useradd`, `COPY --from`) are current<br>• ⚠️ **Old Compose name:** `paths:` matches only `docker-compose*`, and misses the current Compose file names `compose.yaml` / `compose.yml` |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Structural test:** `test_lazy_load_rule_structure.py` tracks `infra/docker.md` (line 55) and checks the header, Purpose line, child links, link resolution and the "Structure" H2<br>• 🧪 **Children checked:** each child is checked for the `_` prefix and a Purpose line (lines 351–360)<br>• ⚠️ **Not run in this review:** no pass result was seen, and nothing checks child bullet style or whether `paths:` globs match content<br>• ✅ **No incident test needed:** the rule documents no incident, so no content-regression test is required |
| **Overall** | **6.5/10** | 2026-10-28 | • 💪 **Practical examples:** concrete Good/Bad Dockerfiles, plus a working multi-stage template<br>• ⚠️ **Gaps:** Compose is in `paths:` but has no content, no evidence of need or use is recorded, and the child pages slip on house style |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/infra/docker.md` — the rule being scored
- `src/claude/_reference/_style_guide_standards/infra/docker/_fundamentals.md` — Clarity, Structural Compliance
- `src/claude/_reference/_style_guide_standards/infra/docker/_advanced.md` — Clarity, Structural Compliance
- `src/claude/_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` — Test Coverage
- `docs/audits/rule_usage_history.csv` — Evidence of Need
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
