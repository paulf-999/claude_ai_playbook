# 🧪 `rules/` tests

**Purpose:** Tests for structural properties and behavioural compliance of files in `~/.claude/rules/` and `~/.claude/_rules_lazy_load/`.

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_rules_structure.py` | Per-file format across all `rules/` files — line limits, H1 and H2 heading emoji, trailing newlines, and no Related or unearned Contents sections | 10/10 | 2026-08-28 | 2026-10-11 | 2.5.4 |
| `test_rules_structure_layout.py` | Where `rules/` files live, every import in `CLAUDE.md` and `rules/` resolves, and no import chain reaches `_reference/` | 7/10 | 2026-10-01 | 2026-10-11 | 5.0.0 |
| `test_rule_cross_references.py` | Rule files point at things that exist and agree with the files that repeat them, across six rules, including git.md's branch pattern and its examples | 10/10 | 2026-10-11 | 2026-10-11 | 2.0.1 |

## 📁 `01_essentials/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_guiding_principles.py` | CLAUDE.md imports only memory and aliases, each with a purpose comment, unique and under the Imports heading | 9/10 | 2026-08-28 | 2026-10-11 | 3.0.3 |
| `test_rule_directory_organisation.py` | `01_essentials/` holds its expected files and folders, and tiers 01–03 follow the parent-and-children layout (`_` prefix, 2+ children, parent beside each folder) | 9/10 | 2026-08-28 | 2026-10-11 | 2.4.1 |

## 📁 `02_claude_standards/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_always_on_reachability.py` | Every file under `rules/` loads the way its folder says — no README, `_lazy_load/` folder, `@import` or unscoped `02_claude_standards/path_scoped_rules/` file — and every 'Read on demand' pointer | 9/10 | 2026-09-18 | 2026-10-11 | 3.2.5 |
| `test_claude_rule_loading_strategy.py` | The five-folder table matches the real `rules/` and `_rules_lazy_load/` folders, and its example files exist, matching each tier's loading claim | 9/10 | 2026-09-30 | 2026-10-11 | 4.0.0 |
| `test_concurrent_sessions.py` | `git/_concurrent_sessions.md` stays reachable from `git.md` and keeps its 2026-09-21 incident record | 9/10 | 2026-09-21 | 2026-10-11 | 3.0.0 |
| `test_no_wording_pinning.py` | No test pins an instructional rule's prose (a multi-word literal checked against a real file's text) or guards a finished migration (`assert not <path>.exists()`), unless tagged `# wording-check:` or `# absence-check:` with a reason | 10/10 | 2026-10-11 | 2026-10-17 | 1.2.0 |
| `test_path_scoped_rules.py` | Path-scoped rules in `rules/` carry no `@` imports, `rules/` holds real files not links, and every `02_claude_standards/path_scoped_rules/` file has `paths:` | 7/10 | 2026-10-01 | 2026-10-11 | 2.3.2 |
| `test_path_scoped_rules_live.py` | Proves in a live session that a `paths:` rule loads when, and only when, a matching file is read | 9/10 | 2026-10-01 | 2026-10-11 | 1.2.3 |
| `test_plan_mode_phase_gates.py` | `_plan_mode_phase_gates.md` keeps its plan-persistence section and 2026-09-19 incident record | 9/10 | 2026-09-16 | 2026-10-11 | 4.0.0 |
| `test_portable_paths_hooks.py` | Hooks resolve the config dir from their own location — no hardcoded `~/.claude/` file operations or guard substrings | 10/10 | 2026-09-18 | 2026-10-11 | 2.0.3 |
| `test_portable_paths_python.py` | Python test files use `CLAUDE_DIR` — no `.expanduser()` outside `_shared_paths.py`, home-directory constants or one-convention import prefixes | 8/10 | 2026-09-18 | 2026-10-17 | 2.1.1 |
| `test_testing.py` | Every enforcement hook has a test (aspect splits allowed), no orphaned hook tests, and testing.md's pointers exist | 10/10 | 2026-08-28 | 2026-10-11 | 2.1.0 |

## 📁 `03_authoring_guidelines/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_authoring_agents.py` | `authoring_agents.md` points to each of its 5 on-demand children, which are present and well-formed | 9/10 | 2026-09-28 | 2026-10-10 | 2.2.2 |
| `test_authoring_skills.py` | `authoring_skills.md` and its children: SKILL.md's six sections, the frontmatter example, contract fields matching the checklist, and the maturity table matching the checklist and complexity formula | 9/10 | 2026-09-16 | 2026-10-11 | 5.0.1 |
| `test_claude_config_metadata.py` | Every rule opens with the three-line version, created and updated metadata header | 9/10 | 2026-09-28 | 2026-10-17 | 3.0.1 |
| `test_rule_headers.py` | Validates the rule-only `applies_to`, `miss_cost` and `loading` headers defined in _claude_config_metadata.md | 8/10 | 2026-10-01 | 2026-10-11 | 1.9.6 |
| `test_skill_domains.py` | Keeps skill_domains.yaml and the real skills/ layout in step | 10/10 | 2026-09-30 | 2026-10-11 | 1.0.4 |

## 📁 `rules_lazy_load/`

| File | What it tests | Quality | Created | Updated | Version |
|---|---|---|---|---|---|
| `test_lazy_load_coverage.py` | Every `_rules_lazy_load/` file is reachable from at least one hook (direct or via a parent index file) | 8/10 | 2026-09-16 | 2026-10-11 | 2.5.8 |
| `test_lazy_load_rule_structure.py` | The 14 rules once lacking a dedicated test keep their metadata header, Purpose line, linked child pages, working links and accurate Contents | 10/10 | 2026-10-01 | 2026-10-11 | 2.0.0 |
| `test_lazy_load_triggers.py` | Validates that every lazy rule has something that makes Claude load it | 9/10 | 2026-10-01 | 2026-10-11 | 2.0.0 |
| `test_org.py` | Organisation-specific terms stay inside _rules_lazy_load/org/ and never leak into shared files | 8/10 | 2026-10-01 | 2026-10-11 | 1.3.6 |
| `test_test_metadata.py` | Every test's metadata header, in `_tests/` and the repo's `src/claude/_install/_tests/` and `tests/`, is complete, in order and well formed (banners, dates, semver, scores) | 10/10 | 2026-10-01 | 2026-10-17 | 1.4.0 |
| `test_test_quality_score.py` | Every test header's quality score is exactly what its file earns from four content checks: failure messages, docstrings, a non-vacuous scan and a test proven to fail | 10/10 | 2026-10-02 | 2026-10-11 | 2.0.0 |
| `test_test_score_floor.py` | Every test, in `_tests/` and the repo's `src/claude/_install/_tests/`, meets quality 7, complexity 7 and style Yes, and the minimums match `_test_metadata.md` | 8/10 | 2026-10-01 | 2026-10-11 | 4.0.0 |

[← All tests](../README.md)
