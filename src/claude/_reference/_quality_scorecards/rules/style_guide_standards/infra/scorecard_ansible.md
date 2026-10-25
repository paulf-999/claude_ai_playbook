# Quality Scorecard — ansible.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-25

**Overall score:** 6.3/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Make the example on line 84 match its `[provider]_[account/site]_[plugin].yml` pattern
- Stop skipping `var-naming[no-role-prefix]` on line 99, since lines 85 and `roles_and_tasks.md` line 71 require the prefix
- Remove or create the `secrets_and_inventory.md` that line 25 names, and reference or remove the two orphaned templates
- Give the children Purpose lines, and record evidence of need

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Concrete tables:** the naming table (`ansible.md` lines 79–88) and the repo tree (lines 37–69) can be acted on directly.<br>• ⚠️ **Example contradicts its pattern:** `ansible.md` line 84 gives the pattern `[provider]_[account/site]_[plugin].yml`, but its example `aws_28122221233-aws_ec2.yml` uses a hyphen before the plugin.<br>• ⚠️ **Lint skip clashes with the rule:** `ansible.md` line 99 skips `var-naming[no-role-prefix]`, while line 85 and `ansible/roles_and_tasks.md` line 71 require the role prefix, so lint never checks a rule the guide calls mandatory.<br>• ⚠️ **Vague exclusion note:** `ansible.md` line 25 says to "handle vault secrets and dynamic inventory configuration directly in the repo" and gives no standard or pointer. |
| **Complexity** | 5/10 | 2026-10-25 | • 🧮 **Raw complexity 5:** Concepts 3 (repo layout, naming, linting, tags, CODEOWNERS, role versioning, variable hierarchy) + Scope 1 (the parent and its `ansible/` folder) + Dependencies 1 (`yamllint` and `ansible-lint` through pre-commit, `ansible.md` lines 96–98) + Prerequisites 0, per `_complexity_scoring.md`.<br>• ⚠️ **Repeated content:** variable naming appears three times (`ansible.md` lines 85–86, `ansible/roles_and_tasks.md` line 71, `ansible/variables.md` lines 50–68), and CODEOWNERS twice (`ansible/playbooks.md` line 46, `ansible/roles_and_tasks.md` lines 93–100). |
| **Evidence of Need** | 5/10 | 2026-10-25 | • ❓ **No recorded need:** `ansible.md` line 13 says only "Define the team's standards", and no file records an incident, PR, review failure or use.<br>• 🔗 **Inferred need only:** `miss_cost: medium` on line 9 names a plausible failure ("playbooks that fail review or idempotency checks") but cites no case where it happened. |
| **Token Cost Justification** | N/A | 2026-10-25 | • N/A — lazy-load rule, so the rubric leaves this out of the average |
| **Structural Compliance** | 6/10 | 2026-10-25 | • ✅ **Header and shape:** `paths:` frontmatter, a metadata header (lines 6–10), an emoji H1, a Purpose line, 100 lines, and child files in `ansible/` with three named children.<br>• ⚠️ **No bold keywords:** the bullets at `ansible.md` lines 71–73 and 96–99 don't open with a bold keyword, and line 90 is a loose sentence.<br>• ⚠️ **Children lack Purpose lines:** `ansible/playbooks.md`, `ansible/roles_and_tasks.md` and `ansible/variables.md` have no `**Purpose:**` line under the H1, and each puts its Contents section after the first section.<br>• ⚠️ **Multi-sentence bullets:** `ansible/roles_and_tasks.md` lines 61, 80 and 89 each pack several sentences or clauses into one bullet.<br>• ⚠️ **Orphaned templates:** `ansible/templates/template_docker_airgapped.yml` and `template_helm_deploy.yml` are named by no file in the guide. |
| **Currency** | 7/10 | 2026-10-25 | • ✅ **Paths exist:** all three child pages, `ansible/templates/template_tasks_main.yml` and `rules/_rules_lazy_load/org.md` exist.<br>• ⚠️ **Ghost file reference:** `ansible.md` line 25 names `secrets_and_inventory.md`, a file that exists nowhere in the guide.<br>• ⚠️ **Placeholder owners shown as real:** `ansible/roles_and_tasks.md` lines 97–98 call `@acme/database-administration` and `@jane-doe` "Key ownerships", which reads as current fact. |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Parent guarded:** `_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` line 48 tracks `infra/ansible.md`, checking its header, Purpose line, required H2s, child links, relative links and Contents entries.<br>• ✅ **No incident to pin:** the rule records no incident, so it needs no content-regression test.<br>• ⚠️ **Children unguarded:** the test checks only the parent, so the missing child Purpose lines and the orphaned `ansible/templates/*.yml` files go uncaught. |
| **Overall** | **6.3/10** | 2026-10-25 | • 💪 **Concrete and tested:** clear tables and trees, with a running structural test on the parent.<br>• ⚠️ **Gaps:** no recorded evidence of need, style slips across the parent and children, two orphaned templates, and a pattern/example mismatch on line 84. |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/infra/ansible.md` — the rule being scored
