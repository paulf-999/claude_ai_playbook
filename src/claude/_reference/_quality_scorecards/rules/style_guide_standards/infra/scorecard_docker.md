# Quality Scorecard — docker.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 6.3/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Make the multi-stage example in `docker/advanced.md` lines 99–104 switch to a non-root user, as line 51 requires
- Reconcile the Docker Hub base-image rule (`fundamentals.md` line 16) with the distroless advice on line 18
- Give the children `_` prefixes and Purpose lines, and record evidence of need

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Concrete:** most guidance pairs a "Good" and a "Bad" Dockerfile example, so it's easy to act on.<br>• ⚠️ **Self-contradiction:** `infra/docker/advanced.md` line 51 says not to run as root, but the multi-stage example at lines 99–104 never switches to a non-root user.<br>• ⚠️ **Conflicting base-image advice:** `infra/docker/fundamentals.md` line 16 requires "an official base image from Docker Hub", while line 18 recommends distroless images, which aren't hosted on Docker Hub.<br>• ⚠️ **Vague exception:** `advanced.md` line 51, "unless the base image or tooling requires root", gives no test for when that applies. |
| **Complexity** | 6/10 | 2026-10-25 | • 🧮 **Raw complexity 4:** Concepts 3 (base images, structure, naming, layers, security, .dockerignore and multi-stage builds are 6+) + Scope 1 (a parent plus two children in one folder) + Dependencies 0 + Prerequisites 0.<br>• ⚠️ **Many concepts:** the 6+ concepts across `docker/fundamentals.md` and `docker/advanced.md` are what keep the score down. |
| **Evidence of Need** | 4/10 | 2026-10-25 | • ❓ **No recorded need:** no incident, PR or usage record appears in any file read.<br>• ⚠️ **Claim only:** `infra/docker.md` line 10 (`miss_cost: medium — images that fail review or bloat`) and line 14 ("the team's standards") assert a need but point to no evidence. |
| **Token Cost Justification** | N/A | 2026-10-25 | • N/A — lazy-load rule, so the rubric leaves this out of the average |
| **Structural Compliance** | 6/10 | 2026-10-25 | • ✅ **Parent clean:** `infra/docker.md` is 20 lines, with `paths:` frontmatter, a metadata header, an emoji H1 and a Purpose line.<br>• ⚠️ **Child naming:** the children are `docker/fundamentals.md` and `docker/advanced.md` with no `_` prefix, which fails `_hard_gates_checklist.md` line 16.<br>• ⚠️ **No Purpose in children:** neither child has a `**Purpose:**` line under its H1 (`fundamentals.md` line 4, `advanced.md` line 4), which `_hard_gates_checklist.md` line 21 requires.<br>• ⚠️ **Bullet style:** the bullets have no bold keyword (`fundamentals.md` lines 16–18 and 64–66, `advanced.md` lines 17–19 and 51–55).<br>• ⚠️ **Multi-sentence bullets:** `fundamentals.md` line 18 and `advanced.md` lines 51–52 each hold two sentences. |
| **Currency** | 7/10 | 2026-10-25 | • ✅ **Links resolve:** both child links in `infra/docker.md` lines 18–19 exist, and `test_every_relative_link_resolves` checks them.<br>• ⚠️ **Dated example:** the `python:3.10` pins in `fundamentals.md` line 22 and `advanced.md` lines 94 and 100 point at a Python release that reaches end-of-life in October 2026.<br>• ⚠️ **Mislabelled versioning:** `fundamentals.md` line 65 calls `1.0` and `1.1` "semantic versioning", but semver tags have three parts (X.Y.Z). |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Structural guard:** `_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` line 54 tracks this rule and checks its header, Purpose line, child links, relative links and Contents entries.<br>• ✅ **No incident:** the rule records no incident, so no content-regression test is needed.<br>• ⚠️ **Children unchecked:** that test reads only the parent, so missing Purpose lines and headers in `docker/fundamentals.md` and `docker/advanced.md` go unnoticed, as line 220 shows (`_rule_texts` covers only the tracked rules). |
| **Overall** | **6.3/10** | 2026-10-25 | • 💪 **Actionable examples:** a small path-scoped parent, with concrete good-and-bad Dockerfile snippets.<br>• ⚠️ **Gaps:** no recorded evidence of need, child files outside house style, and an example that breaks the guide's own non-root rule. |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/infra/docker.md` — the rule being scored
