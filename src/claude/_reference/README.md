---
created: 2025-09-01
last_modified: 2026-10-10
---

# 📚 Reference Files Index

Background documentation on how the Claude config is designed, plus settings and team standards. These files explain the *why* — they are consulted when learning the system or making a decision, not followed as rules.

**Never imported:** nothing in this folder is `@import`ed, so none of it costs always-on context — rules point to these files with a "Read on demand" line instead. `test_rules_structure.py::test_always_on_files_do_not_import_reference` enforces this.

---

## 📋 What's here

| File | Read it when |
|---|---|
| [`claude_prompting_best_practices.md`](claude_prompting_best_practices.md) | Writing a prompt, rule or skill — high-impact prompting techniques |
| [`claude_config_architecture.md`](claude_config_architecture.md) | Learning how the config is laid out and why — its security and testing deep-dives now live with their rules, in `_rules_lazy_load/security_design.md` and `rules/04_path_scoped/testing/` |
| [`settings_json_recommendations.md`](settings_json_recommendations.md) | Changing `settings.json` — Tier 1 essentials |
| ↳ [`settings_json_recommendations/_tier2_3.md`](settings_json_recommendations/_tier2_3.md) | Considering Tier 2–3 settings |
| ↳ [`settings_json_recommendations/_enterprise.md`](settings_json_recommendations/_enterprise.md) | Considering enterprise-managed settings |
| [`standards/codeowners.md`](standards/codeowners.md) | Setting up CODEOWNERS (children: `codeowners/fundamentals.md`, `codeowners/patterns.md`) |
| [`standards/versioning_strategy.md`](standards/versioning_strategy.md) | Versioning a skill or release |

**Child files** (`_` prefix, in a folder named after their parent) are deep-dives on the parent's topic.

**Domain rules aren't here:** style guides, automation controls and environment setup live in `~/.claude/_rules_lazy_load/` — see its README.

---

## 🛠️ Maintenance

- **Adding a file:** place it here only if it's background reading rather than a rule, add a row to the table above, and don't `@import` it.
- **Keeping it current:** describe principles and point to the authoritative README or file, rather than copying counts, line numbers or directory trees that go stale — see "False truth rots silently" in `guiding_principles.md`.
- **Audits:** quality audits of these files live in the playbook repo under `src/claude/_admin/_audits/` (`audit_reference_files.md`, scored with `SCORING_GUIDE.md`); they aren't installed into `~/.claude/`.

---

## 🔗 Related rules

Parent, sibling and dependency links for each file in this tier — kept here, not in the file, because READMEs aren't `@import`ed (#121).

### `claude_config_architecture.md`

- **Guiding principles:** `~/.claude/rules/01_essentials/guiding_principles.md`
- **Test coverage:** `~/.claude/_tests/README.md`
- **Lazy-load guide:** `~/.claude/_rules_lazy_load/README.md`

### `claude_prompting_best_practices.md`

These practices are integrated into the global Claude config:

- **`behaviour.md`** — "colleague test", "never speculate about code", "tune exploration"
- **`writing_style.md`** — "frame as positive actions"
- **`claude_operational_efficiency.md`** — "when NOT to spawn"

For the full rules and additional context, see `~/.claude/rules/` and `~/.claude/_rules_lazy_load/`.

### `settings_json_recommendations/_enterprise.md`

- **Parent (Tier 1 essentials):** `settings_json_recommendations.md`
- **Tier 2–3 settings:** `_tier2_3.md`
- **Official schema:** <https://code.claude.com/docs/en/settings>

### `settings_json_recommendations/_tier2_3.md`

- **Parent (Tier 1 essentials):** `settings_json_recommendations.md`
- **Enterprise settings:** `_enterprise.md`
- **Official schema:** <https://code.claude.com/docs/en/settings>

### `settings_json_recommendations.md`

- **Parent:** This doc
- **Tier 2–3 settings:** [settings_json_recommendations/_tier2_3.md](settings_json_recommendations/_tier2_3.md)
- **Enterprise settings:** [settings_json_recommendations/_enterprise.md](settings_json_recommendations/_enterprise.md)
- **Security rules:** `~/.claude/rules/02_claude_standards/security.md`
