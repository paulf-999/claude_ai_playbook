# 📊 Rule usage audit

**Generated:** 2026-10-01 by `make audit_rule_usage` · **Sessions:** 115 across 10 projects · **Window:** 2026-08-31 to 2026-10-01

**Always-on load:** ≈35,025 tokens per session (characters ÷ 4).

## 📖 How to read this

- **Applied:** sessions that touched a file matching the rule's `applies_to` globs (or its `paths:` or a built-in default for lazy rules); `*` means every session.
- **Loaded:** sessions where the rule reached Claude's context — imported, auto-loaded by `paths:`, or read.
- **Misses:** sessions where the rule applied but was never loaded.
- **Miss cost:** read from a `<!-- miss_cost: … -->` header; `—` until Phase 5 adds them.
- **Not enough data:** fewer than 10 applied sessions, so no other flag is set.
- **No trigger:** a lazy rule with no `paths:` or default glob, so nothing can measure when it applies.
- **Cut-offs:** 10 sessions, 50% and 90 days are first guesses, to review after 3 reports.

## 📋 Rules

| Rule | Tier | Tokens | Applied | Loaded | Misses | Miss cost | Last applied | Last loaded | Flag |
|---|---|---|---|---|---|---|---|---|---|
| `01_essentials/claude_response_standards.md` | 01 | 1,541 | 100% (115) | 90% (104) | 11 | — | 2026-10-01 | 2026-10-01 | — |
| `01_essentials/claude_usage_standards.md` | 01 | 6,643 | 100% (115) | 76% (87) | 28 | — | 2026-10-01 | 2026-10-01 | — |
| `01_essentials/guiding_principles.md` | 01 | 2,478 | 77% (88) | 90% (104) | 5 | — | 2026-10-01 | 2026-10-01 | — |
| `02_claude_standards/behaviour.md` | 02 | 6,371 | 100% (115) | 90% (104) | 11 | — | 2026-10-01 | 2026-10-01 | — |
| `02_claude_standards/claude_plans.md` | 02 | 2,124 | 100% (115) | 76% (87) | 28 | — | 2026-10-01 | 2026-10-01 | — |
| `02_claude_standards/git.md` | 02 | 2,553 | 100% (115) | 90% (104) | 11 | — | 2026-10-01 | 2026-10-01 | — |
| `02_claude_standards/portable_paths.md` | 02 | 955 | 23% (27) | 76% (87) | 2 | — | 2026-10-01 | 2026-10-01 | — |
| `02_claude_standards/security.md` | 02 | 1,630 | 100% (115) | 90% (104) | 11 | — | 2026-10-01 | 2026-10-01 | — |
| `02_claude_standards/testing.md` | 02 | 3,752 | 32% (37) | 90% (104) | 1 | — | 2026-10-01 | 2026-10-01 | — |
| `03_authoring_guidelines/authoring_agents.md` | 03 | 579 | 2% (2) | 70% (81) | 1 | — | 2026-09-29 | 2026-10-01 | not enough data |
| `03_authoring_guidelines/authoring_rules.md` | 03 | 2,130 | 28% (32) | 76% (87) | 5 | — | 2026-10-01 | 2026-10-01 | — |
| `03_authoring_guidelines/authoring_skills.md` | 03 | 754 | 15% (17) | 76% (87) | 4 | — | 2026-09-30 | 2026-10-01 | — |
| `04_claude_reference/claude_operational_efficiency.md` | 04 | 2,647 | 100% (115) | 76% (87) | 28 | — | 2026-10-01 | 2026-10-01 | — |
| `04_claude_reference/claude_rule_loading_strategy.md` | 04 | 868 | 30% (35) | 51% (59) | 19 | — | 2026-10-01 | 2026-10-01 | — |
| `05_lazy_load/automation_controls.md` | 05 | 1,621 | — | 0% (0) | — | — | — | — | no trigger |
| `05_lazy_load/delegating_to_subagent.md` | 05 | 982 | — | 0% (0) | — | — | — | — | no trigger |
| `05_lazy_load/environment_setup/ohmyzsh_setup.md` | 05 | 646 | — | 0% (0) | — | — | — | — | no trigger |
| `05_lazy_load/hooks_decision_framework.md` | 05 | 969 | 3% (3) | 0% (0) | 3 | — | 2026-09-30 | — | not enough data |
| `05_lazy_load/latency_optimisation.md` | 05 | 973 | — | 3% (3) | — | — | — | 2026-10-01 | no trigger |
| `05_lazy_load/mcp_trust_model.md` | 05 | 1,045 | — | 0% (0) | — | — | — | — | no trigger |
| `05_lazy_load/response_standards_enforcement.md` | 05 | 880 | 2% (2) | 1% (1) | 1 | — | 2026-09-30 | 2026-09-30 | not enough data |
| `05_lazy_load/style_guide_standards/airflow.md` | 05 | 1,117 | 0% (0) | 0% (0) | 0 | — | — | — | not enough data |
| `05_lazy_load/style_guide_standards/bash.md` | 05 | 635 | 10% (11) | 1% (1) | 10 | — | 2026-10-01 | 2026-09-19 | — |
| `05_lazy_load/style_guide_standards/dbt.md` | 05 | 1,455 | 0% (0) | 0% (0) | 0 | — | — | — | not enough data |
| `05_lazy_load/style_guide_standards/infra/ansible.md` | 05 | 979 | 0% (0) | 0% (0) | 0 | — | — | — | not enough data |
| `05_lazy_load/style_guide_standards/infra/docker.md` | 05 | 115 | 0% (0) | 0% (0) | 0 | — | — | — | not enough data |
| `05_lazy_load/style_guide_standards/infra/terraform.md` | 05 | 387 | 0% (0) | 0% (0) | 0 | — | — | — | not enough data |
| `05_lazy_load/style_guide_standards/jira.md` | 05 | 380 | — | 0% (0) | — | — | — | — | no trigger |
| `05_lazy_load/style_guide_standards/payroc_engineering_naming_standards.md` | 05 | 429 | — | 0% (0) | — | — | — | — | no trigger |
| `05_lazy_load/style_guide_standards/python.md` | 05 | 1,167 | 26% (30) | 1% (1) | 29 | — | 2026-10-01 | 2026-09-19 | — |
| `05_lazy_load/style_guide_standards/sql.md` | 05 | 1,223 | 4% (5) | 3% (4) | 1 | — | 2026-10-01 | 2026-10-01 | not enough data |
| `05_lazy_load/style_guide_standards/utilities/datetime.md` | 05 | 540 | — | 0% (0) | — | — | — | — | no trigger |
| `05_lazy_load/style_guide_standards/utilities/makefile.md` | 05 | 121 | 4% (5) | 1% (1) | 5 | — | 2026-10-01 | 2026-09-28 | not enough data |
| `05_lazy_load/style_guide_standards/utilities/mermaid.md` | 05 | 162 | 0% (0) | 0% (0) | 0 | — | — | — | not enough data |
| `05_lazy_load/testing_guidance.md` | 05 | 185 | 24% (28) | 0% (0) | 28 | — | 2026-10-01 | — | — |
| `05_lazy_load/turn_budgets.md` | 05 | 420 | — | 0% (0) | — | — | — | — | no trigger |

## 📐 Largest always-on sections (top 15)

| File | Section | Tokens |
|---|---|---|
| `02_claude_standards/behaviour/_artefact_proposal_gates.md` | 🚪 The Three Gates | 684 |
| `01_essentials/claude_response_standards.md` | 📤 Response Format & Style | 679 |
| `01_essentials/claude_usage_standards/writing_style.md` | 🎨 Style — all content | 567 |
| `02_claude_standards/git/_commits.md` | 📝 Commits | 507 |
| `04_claude_reference/claude_rule_loading_strategy.md` | 📁 The five tiers | 487 |
| `04_claude_reference/claude_operational_efficiency/_task_request_conventions.md` | 📝 Task logging convention | 479 |
| `02_claude_standards/behaviour.md` | ✅ Before claiming completion | 468 |
| `03_authoring_guidelines/authoring_rules.md` | ✅ Pre-Creation Checklist | 466 |
| `02_claude_standards/behaviour/_before_acting.md` | 2️⃣ **Apply gates by complexity** | 452 |
| `02_claude_standards/claude_plans/_plan_mode_phase_gates.md` | 📁 Persist the plan to `_plans/` | 440 |
| `03_authoring_guidelines/authoring_skills.md` | 📁 File Organization | 435 |
| `01_essentials/claude_usage_standards/naming_standards/_naming_principles.md` | 📋 Core Principles | 425 |
| `03_authoring_guidelines/authoring_rules.md` | 📏 Quality Gates | 421 |
| `01_essentials/guiding_principles.md` | 📊 How to gather usage evidence | 400 |
| `03_authoring_guidelines/shared_standards/_claude_config_metadata.md` | 📍 One format, three lines, every artefact | 379 |

## 🗺️ Session spread

Project names are hidden, since this report is committed to a public repo.

| Project | Sessions |
|---|---|
| project 1 | 87 |
| project 2 | 8 |
| project 3 | 6 |
| project 4 | 5 |
| project 5 | 2 |
| project 6 | 2 |
| project 7 | 2 |
| project 8 | 1 |
| project 9 | 1 |
| project 10 | 1 |

## ⚠️ Limits

- **Always-on misses:** a session misses an always-on rule when its startup file list doesn't name it — usually because the file was added or renamed after that session ran.
- **Edits count as loads:** reading a rule file to edit it counts as loading it.
- **Sub-agents skipped:** only main-session transcripts are read.
- **Followed is not measured:** loaded means the rule was in context, not that Claude acted on it.
