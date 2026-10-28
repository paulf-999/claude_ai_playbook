# Quality Scorecard — _claude_config_metadata.md

**Date Created:** 2026-09-28
**Date Updated:** 2026-10-27

**Overall score:** 8.1/10

**Recommended improvements:**
- Define "the audit's built-in defaults" on line 70, or point to where they live in `audit_rule_usage.py`.
- Split line 51's "Single source of version" bullet at the semicolon into two child bullets.
- Add a `shared_standards.md` parent, or move both children under the parent that points to them, so the folder follows `multifile_document_organisation.md`.
- Record one dated case where an `updated` or `version` value drove a staleness or audit decision.
- Add a check that `created` never changes and that `version` moves whenever `updated` moves, or say in the rule that these two are not checked.

| Dimension | Score | Date Updated | Notes |
|---|---|---|---|
| **Clarity** | 8/10 | 2026-10-25 | • 🔍 **Clear core:** the three-field table, the semver bullets and the per-artefact placement table leave little room for different readings<br>• ⚠️ **Undefined default:** line 70 says lazy rules can skip `applies_to` because "the audit's built-in defaults apply otherwise", but never says what those defaults are<br>• ⚠️ **Undefined term:** "Entry-point rules" (line 60) is only explained by contrast in line 76 ("a child file inherits its parent's fields") |
| **Complexity** | 6/10 | 2026-10-25 | • 🧮 **Raw complexity 4:** Concepts 2 (three fields, semver bump policy, placement, three usage fields) + Scope 2 (rules, skills, agents and hooks folders) + Dependencies 0 + Prerequisites 0<br>• ⚠️ **Two jobs in one file:** the shared header standard and the rule-only usage fields (`applies_to`, `miss_cost`, `loading`) are separate concerns in the same file |
| **Evidence of Need** | 8/10 | 2026-10-27 | • 🔗 **Stated need:** line 20 says "git history doesn't travel with the live copy", and line 21 says `updated` is "the main signal in audits and 6-month resets"<br>• 📈 **Used everywhere:** five test files enforce the header on every rule, skill, agent and hook, and `audit_rule_usage.py` reads `applies_to` and `miss_cost` (14 references)<br>• ⚠️ **No dated incident:** no file records an audit or reset decision driven by these fields, and line 28 says they show change, not use |
| **Token Cost Justification** | 9/10 | 2026-10-27 | • 🎯 **Scoped load:** `paths:` frontmatter (`**/.claude/**`, `**/claude/**`) loads it only when a config file is open, which is when the standard applies<br>• ✅ **Header is free:** line 53 records a dated check (2026-09-28) that HTML comment headers add no input tokens |
| **Structural Compliance** | 8/10 | 2026-10-27 | • ✅ **Within limits:** 78 lines including frontmatter and header, with emoji headings, a Purpose line and bold-keyword bullets<br>• ⚠️ **Two-sentence bullet:** line 51, "skills and agents drop `version:` from frontmatter; a skill's `skill.contract.yaml` version must match its header", joins two sentences with a semicolon<br>• ⚠️ **No parent folder match:** `shared_standards/` has no `shared_standards.md` parent, but `multifile_document_organisation.md` says children "live in a subdirectory named after the parent" |
| **Currency** | 9/10 | 2026-10-27 | • 🔍 **Claims checked:** hook lines 2–4 after the shebang, skill header matching the contract version, the line-limit exemption, `make audit_rule_usage`, `test_rule_headers.py` and `testing_lazy_load/_test_metadata.md` all exist and match the rule<br>• 🔍 **Minor nit:** line 20 says the live copy is `~/.claude/`, while `portable_paths.md` says it is deliberately installed at `~/claude` |
| **Test Coverage** | 9/10 | 2026-10-27 | • 🧪 **Enforced by tests:** `test_claude_config_metadata.py` checks every rule header, `test_rule_headers.py` checks `applies_to`, `miss_cost`, `loading` and that `loading` matches the folder, the hook, skill and agent header tests cover the other types, and `test_rules_structure.py` checks the line-limit exemption<br>• ⚠️ **Edit rules not checked:** nothing checks "never change `created`" or "bump `version` whenever `updated` moves" (line 24)<br>• ⚠️ **Not run here:** the reviewer read the tests but couldn't run pytest, because it only has read access |
| **Overall** | **8.1/10** | 2026-10-27 | • 💪 **Strength:** one standard for four artefact types, with nearly every claim backed by a test<br>• ⚠️ **Gaps:** the "built-in defaults" wording is vague, there's a folder-structure slip, the edit rules aren't checked and no dated incident is recorded |

## 🔗 Related files

- `src/claude/rules/03_authoring_guidelines/shared_standards/_claude_config_metadata.md` — the rule being scored
- `src/claude/rules/03_authoring_guidelines/shared_standards/_complexity_scoring.md` — Complexity formula
- `src/claude/_tests/rules/03_authoring_guidelines/test_claude_config_metadata.py` — Test Coverage
- `src/claude/_tests/rules/03_authoring_guidelines/test_rule_headers.py` — Test Coverage, Currency
- `src/claude/_tests/rules/test_rules_structure.py` — Test Coverage, Currency (line-limit exemption)
- `src/claude/_tests/hooks/test_hook_metadata_header.py` — Currency, Test Coverage
- `src/claude/_tests/skills/_all_skills/test_skill_metadata_header.py` — Currency, Test Coverage
- `src/claude/_tests/agents/test_agent_metadata_header.py` — Test Coverage
- `src/claude/_tests/_shared_checks/test_metadata_header_format.py` — Test Coverage
- `src/claude/scripts/_audit_scripts/audit_rule_usage.py` — Evidence of Need, Currency
- `src/claude/rules/_rules_lazy_load/testing_lazy_load/_test_metadata.md` — Currency
- `src/claude/rules/01_essentials/claude_usage_standards/multifile_document_organisation.md` — Structural Compliance
- `src/claude/rules/02_claude_standards/claude_working_practices/portable_paths.md` — Currency
