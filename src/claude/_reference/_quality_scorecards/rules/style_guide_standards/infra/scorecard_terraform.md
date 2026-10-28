# Quality Scorecard — terraform.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-28

**Overall score:** 6.2/10 (6-dimension average, Token Cost N/A)

**Recommended improvements:**
- Read the Snowflake private key path from a variable instead of `file("~/.ssh/snowflake_key.p8")`, or state it as the one allowed exception to "never hardcoded".
- Reword the Purpose line so it says the guide covers Snowflake infrastructure deployed through Azure Pipelines, because `paths: **/*.tf` loads it for every Terraform file.
- Replace "prefixed with purpose" in `_conventions.md` with a concrete naming pattern that matches the `module_grant_...` example.
- Record real uses of the guide, such as a dated review or a `rule_usage_history.csv` row with loads above 0, or give a reason to keep it while it shows zero loads.
- Remove "One blank line between resource blocks" from the list of rules `terraform fmt` enforces, since `fmt` doesn't add blank lines between blocks.
- Change the core-principle bullets from `**Keyword** —` to `**Keyword:**`, and move each child's Contents section above its first H2 section.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 6/10 | 2026-10-28 | • ⚠️ **Self-contradiction:** the parent says no values are hardcoded and `_providers.md` says "never hardcoded", but the same file's example hardcodes `private_key = file("~/.ssh/snowflake_key.p8")` and calls that path "the team standard"<br>• ⚠️ **Generic opening:** the Purpose line says "writing and structuring Terraform code", but the content only covers Snowflake infrastructure with Azure Pipelines, and the file loads for any `.tf` file<br>• ⚠️ **Vague naming rule:** `_conventions.md` says non-primary resources are "prefixed with purpose", but its example `module_grant_ownership_snowflake_warehouse` starts with `module_`<br>• 🔍 **Concrete guidance:** the role-name regex, the layered create → ownership → usage pattern and the `for_each` rules are exact and easy to act on |
| **Complexity** | 4/10 | 2026-10-28 | • 🧮 **Raw complexity 6:** Concepts 3 (six areas: structure, providers, naming, declarations, modules, CI) + Scope 1 (the parent plus one child folder) + Dependencies 2 (Terraform, the Snowflake provider, Azure Pipelines, pre-commit) + Prerequisites 0<br>• ⚠️ **Wide scope:** six child pages make this one of the broader style guides |
| **Evidence of Need** | 4/10 | 2026-10-28 | • ⚠️ **No recorded use:** every terraform row in `docs/audits/rule_usage_history.csv` (2026-10-01) shows `applied 0, loaded 0, misses 0` across 115 sessions<br>• ⚠️ **No incident:** the only justification is `<!-- miss_cost: medium — modules that fail review or plan checks -->`, which names no dated case<br>• 🔍 **Grounded content:** specific module names and pipeline templates suggest it describes a real repo, but no file in this repo shows that |
| **Token Cost Justification** | N/A | 2026-10-25 | • 🎯 **Path-scoped:** `paths: "**/*.tf"` loads the 32-line parent only when a Terraform file is open, and the children stay read-on-demand, so this is excluded from the average |
| **Structural Compliance** | 7/10 | 2026-10-28 | • ✅ **Within limits:** the parent is 32 lines and the longest child is 95, each with a metadata header, a Purpose line and emoji headings<br>• ⚠️ **Keyword format:** the core-principle bullets use `**Separation by environment** —` instead of `**Keyword:**`<br>• ⚠️ **Contents placement:** `_structure.md`, `_conventions.md`, `_modules.md` and `_ci_and_tooling.md` put their Contents section after the first H2 section<br>• ⚠️ **Prose over bullets:** some children use multi-sentence paragraphs and bullets with no bold keyword (e.g. `_ci_and_tooling.md` line 23, the `_structure.md` "What must not be committed" list) |
| **Currency** | 7/10 | 2026-10-25 | • ✅ **Links resolve:** all six child links exist, and `test_every_relative_link_resolves` checks them<br>• ⚠️ **Inaccurate claim:** `_ci_and_tooling.md` lists "One blank line between resource blocks" as a `terraform fmt` rule, but `fmt` doesn't enforce that<br>• 🔍 **Can't verify:** `src/cicd/pipelines/pr_pipeline_terraform_validate_and_plan.yml`, `code_deployment_terraform_apply.yml` and the `terraform/modules/` tree are in a team repo outside this one |
| **Test Coverage** | 9/10 | 2026-10-28 | • 🧪 **Structural tests run:** `test_lazy_load_rule_structure.py` checks the header, the Purpose line, the required "Child pages" and "Core principles" headings, child links and link resolution<br>• 🧪 **Children checked:** the same file checks each child's `_` prefix and Purpose line, and `test_rules_structure.py` checks the style-guide folder for line limits, emoji headings and the Contents rule<br>• 🔍 **No regression test needed:** the guide documents no incident, so a content-regression test isn't required, and nothing checks the regex or the example code |
| **Overall** | **6.2/10** | 2026-10-25 | • 💪 **Well split and tested:** a short path-scoped parent with six focused children, all under structural tests<br>• ⚠️ **Weak evidence and consistency:** zero recorded loads, a contradiction about hardcoded values and a `fmt` claim that is wrong |

## 🔗 Related files

- `src/claude/_reference/_style_guide_standards/infra/terraform.md` — the rule being scored
- `src/claude/_reference/_style_guide_standards/infra/terraform/_providers.md` — Clarity (the hardcoded key path)
- `src/claude/_reference/_style_guide_standards/infra/terraform/_conventions.md` — Clarity and Structural Compliance
- `src/claude/_reference/_style_guide_standards/infra/terraform/_structure.md` — Structural Compliance
- `src/claude/_reference/_style_guide_standards/infra/terraform/_modules.md` — Structural Compliance
- `src/claude/_reference/_style_guide_standards/infra/terraform/_ci_and_tooling.md` — Currency and Structural Compliance
- `src/claude/_reference/_style_guide_standards/infra/terraform/_declarations.md` — Clarity (the regex and validation pattern)
- `docs/audits/rule_usage_history.csv` — Evidence of Need
- `src/claude/_tests/rules/rules_lazy_load/test_lazy_load_rule_structure.py` — Test Coverage
- `src/claude/_tests/rules/test_rules_structure.py` — Test Coverage
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity
