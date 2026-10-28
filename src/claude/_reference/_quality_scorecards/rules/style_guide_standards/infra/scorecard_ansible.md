# Quality Scorecard — ansible.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-28

**Overall score:** 6.5/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Widen the `paths:` frontmatter to cover `**/group_vars/**`, `**/host_vars/**` and `**/inventory/**`, with both `.yml` and `.yaml`, so `_variables.md` loads when someone edits a variables file.
- Replace "this repo" in the Repo structure bullets with wording that holds for any Ansible repo, or say which repo it means.
- Add a note explaining that inventory scope folders deliberately use hyphens (`acme-prd-cde`) while everything else uses snake_case.
- Split the `rescue`-block bullet in `_roles_and_tasks.md` into child bullets, and give each of the two-sentence bullets one sentence.
- Open the parent's Repo structure and Linting bullets, and every child bullet, with a bold keyword and a colon.
- Move each child's Contents section up to sit under its Purpose line.
- Add a `Why:` line or a dated incident behind `miss_cost: medium`, so the need is recorded rather than only claimed.
- Extend `test_lazy_load_rule_structure.py` so it also checks the metadata headers and relative links of style-guide children.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 7/10 | 2026-10-25 | • 🔍 **Clear core:** the naming table, the FQCN rule and the lint gates are specific and actionable<br>• ⚠️ **"This repo":** lines 71–73 ("this repo does not use a config-driven YAML inputs pattern") read like notes about one particular repo, not a general standard<br>• ⚠️ **Naming clash:** `[org]-[env]-[qualifier]` (line 83) uses hyphens with no note, while tags and variables use snake_case, so readers could disagree on which applies<br>• ⚠️ **Crammed bullet:** in `_roles_and_tasks.md`, line 63 packs four separate `rescue` instructions into one bullet |
| **Complexity** | 4/10 | 2026-10-28 | • 🧮 **Raw complexity 6:** Concepts 3 (structure, naming, linting, tags, play standards, role layout, task standards, versioning, Docker tasks, the vars hierarchy, host_vars) + Scope 1 (the parent plus its `ansible/` folder) + Dependencies 2 (`yamllint`, `ansible-lint`, `ansible-galaxy`, pre-commit) + Prerequisites 0<br>• ⚠️ **Broad by nature:** one guide covering a whole tool's repo, and although the children split it well, the raw sum stays high |
| **Evidence of Need** | 6/10 | 2026-10-28 | • 🔗 **Grounded detail:** the single lint skip (`role-name[path]`), the capability folders and the air-gapped templates point to conventions drawn from a real repo<br>• ⚠️ **No record:** `<!-- miss_cost: medium — playbooks that fail review or idempotency checks -->` is a claim, and no file records a dated incident or repeat use |
| **Token Cost Justification** | N/A | 2026-10-25 | • 🎯 **Path-scoped:** it loads only for `**/playbooks/**/*.yml` and `**/roles/**/*.yml`, so it's left out of the average<br>• ⚠️ **Under-scoped paths:** `group_vars/`, `host_vars/` and `inventory/` files (and `vars.yaml`, line 48) never trigger it, though `_variables.md` is about exactly those files |
| **Structural Compliance** | 6/10 | 2026-10-25 | • ✅ **Header and length:** frontmatter, a three-line metadata header, a Purpose line, emoji H2s and 100 lines, with a Contents section earned by three real headings<br>• ⚠️ **No bold keywords:** parent lines 71–73 and 96–99, and every child bullet, have no `**Keyword:**` lead, and line 90 is loose prose<br>• ⚠️ **Multi-sentence bullets:** `_roles_and_tasks.md` lines 82 and 92 each run two sentences in one bullet<br>• ⚠️ **Contents placement:** all three children put Contents after their first section, not under the Purpose line |
| **Currency** | 8/10 | 2026-10-28 | • ✅ **Paths resolve:** all three child pages, `ansible/templates/template_{tasks_main,docker_airgapped,helm_deploy}.yml` and `rules/_rules_lazy_load/org.md` exist<br>• ✅ **Prefix matches:** `~/.claude/_rules_lazy_load/org.md` uses the same prefix as the repo's other read-on-demand pointers<br>• ⚠️ **Precedence oversimplified:** `_variables.md` line 86 states L6 > … > L1 as fixed, but it holds only through same-depth alphabetical group ordering or parent/child groups, and `ansible_group_priority` isn't mentioned |
| **Test Coverage** | 8/10 | 2026-10-25 | • 🧪 **Parent guarded:** `test_lazy_load_rule_structure.py` checks the header, the Purpose line, the required H2s (Child pages, Repo structure, Naming conventions, Linting), that every child is linked, that every link resolves, and that Contents entries match headings<br>• 🧪 **Children partly guarded:** children are checked only for the `_` prefix and a Purpose line<br>• ⚠️ **Child gaps:** the children's metadata headers and relative links (`_variables.md`, `templates/*.yml`) aren't tested<br>• ✅ **No regression test needed:** the guide documents no incident |
| **Overall** | **6.5/10** | 2026-10-28 | • 💪 **Concrete and current:** specific naming patterns, an FQCN rule and lint gates, and every reference resolves<br>• ⚠️ **Held back by:** high raw complexity, no recorded evidence of need, house-style slips across the children, and path triggers that miss the variables files |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/infra/ansible.md` — the rule being scored
- `src/claude/_reference/_style_guide_standards/infra/ansible/_playbooks.md` — Structural Compliance, Currency
- `src/claude/_reference/_style_guide_standards/infra/ansible/_roles_and_tasks.md` — Clarity, Structural Compliance, Currency
- `src/claude/_reference/_style_guide_standards/infra/ansible/_variables.md` — Token Cost Justification, Currency
- `src/claude/_reference/_style_guide_standards/infra/ansible/templates/template_tasks_main.yml` — Currency
- `src/claude/_reference/_style_guide_standards/infra/ansible/templates/template_docker_airgapped.yml` — Currency
- `src/claude/_reference/_style_guide_standards/infra/ansible/templates/template_helm_deploy.yml` — Currency
- `src/claude/rules/_rules_lazy_load/org.md` — Currency
- `src/claude/_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` — Test Coverage
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
