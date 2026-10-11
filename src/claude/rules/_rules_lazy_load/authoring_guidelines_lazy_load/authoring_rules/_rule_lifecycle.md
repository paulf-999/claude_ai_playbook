<!-- version: 2.1.1 -->
<!-- created: 2025-11-15 -->
<!-- updated: 2026-10-11 -->
# 🔄 Rule Lifecycle

**Purpose:** Explain how to promote a lazy rule to always-on, how to remove an unused rule, and the design trade-offs behind those choices.

- **Adding a rule:** follow `authoring_rules.md` and `claude_rule_loading_strategy.md`, so the steps aren't repeated here.
- **Review cadence:** monthly, quarterly and 6-month reset reviews live in `guiding_principles.md`.

---

## ⬆️ Promoting a rule from lazy to always-on

Promote a rule when a miss would go unnoticed and only a pointer loads it, or when it becomes foundational.

### 🎯 Promotion criteria

Use the two numbers in the playbook repo's `docs/audits/audit_rule_usage.md`, read against the table in `claude_rule_loading_strategy.md`:

- **Applied %:** the share of sessions matching the rule's `applies_to` globs, from `make audit_rule_usage`.
- **Miss cost:** what breaks when the rule applies but isn't loaded, from its `miss_cost` header.
- **Promote when:** the rule has `miss_cost: high` and no `paths:` frontmatter or hook loads it — a pointer alone is never enough.
  - **Why:** a high miss is silent or unsafe by definition, and a pointer works only if Claude remembers to follow it.
  - **Enforced by:** `test_high_cost_lazy_rules_load_mechanically` in `test_rule_headers.py`.
- **Medium can stay on a pointer:** a medium miss is rework you'd catch, so promote it only when it's applied in half of sessions or more.
- **Promote when:** a low-cost rule is small and applied in half of sessions or more.
- **Not enough data:** for the applied % checks, make no decision with fewer than 10 applied sessions.

### 📌 Promotion example

**MCP trust model** shows the high-cost criterion at work: it moved to `rules/02_claude_standards/security/_mcp_trust_model.md`.

- **High cost:** a miss lets an injected instruction be followed with no warning.
- **No trigger:** no file type marks the sessions that use MCP tools, so only a pointer could load it.
- **Outcome:** it loads every session as a child of `security.md`, even though its applied % is low.

### 🛠️ Promotion process

1. **Verify criteria:** run `make audit_rule_usage` and confirm the numbers above.
2. **Move file:** take it from `_rules_lazy_load/` into the matching tier under `rules/` (`01_essentials/` to `03_authoring_guidelines/`), where it loads natively.
3. **Update headers:** change its `loading:` header to `always-on` and add `applies_to` if it lacks one.
4. **Point to it:** if it's a child, add a `**Loads on its own from:**` line to its parent, and note the size it adds.
5. **Run the suite:** `test_always_on_reachability.py` confirms nothing under `rules/` is a README, `_lazy_load/` folder or `@import`.
6. **Update docs:** remove its entry from `_rules_lazy_load/README.md`, since always-on rules keep no index entry.
7. **Commit:** `refactor(rules): promote <rule_name> from lazy to always-on`.

---

## 🗑️ Removing unused rules

1. **Audit usage:** confirm it's unused through the **Stale** flag in `audit_rule_usage.md` (no use for 90 days).
2. **Delete the file:** remove the rule file and its test.
3. **Delete its pointers:** remove every `**Loads on its own from:**` and `**Read on demand:**` line that names it.
4. **Update docs:** if it was lazy or path-scoped, remove it from `_rules_lazy_load/README.md`.
5. **Commit:** `chore(rules): remove <rule_name>`.

---

## ⚖️ Design tensions and trade-offs

Every config makes trade-offs, and knowing them helps future decisions.

| Tension | Option A | Option B | Current choice | If changed |
|---|---|---|---|---|
| **Breadth vs. depth** | • **Breadth:** many rules across many domains | • **Depth:** few, highly specific rules that are harder to find | • **Breadth with lazy-load:** rules are found when needed and not lost | • **Cost:** rules would need consolidating or moving to external docs |
| **Automation vs. explicitness** | • **Automation:** hooks enforce rules silently, with less friction but hidden behaviour | • **Explicitness:** every always-on rule sits in a `rules/` tier folder, so the folder listing is the always-on list | • **Balance:** hooks for safety-critical rules, folder placement for the rest | • **Risk:** more automation hides rule changes, while less raises maintenance friction |
| **Consistency vs. flexibility** | • **Consistency:** a rigid structure prevents drift | • **Flexibility:** ad-hoc rules for edge cases ship faster | • **Mixed:** consistent structure (folders, naming) with flexible content | • **Risk:** more flexibility fragments the config, while stricter consistency slows adoption |
