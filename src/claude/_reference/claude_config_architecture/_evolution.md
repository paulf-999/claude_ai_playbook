---
created: 2025-11-15
last_modified: 2026-09-29
---

# 🔄 Evolution & Maintenance

Guide to maintaining, evolving, and improving the Claude config over time.

---

## Regular maintenance cycles

Configuration requires periodic review to stay intentional:

### Monthly

- Spot-check for unused features — any hooks not firing? Any rules not referenced?
- Audit recent rule changes — do they still make sense?
- Review transcripts — do new patterns emerge?

### Quarterly

- Test coverage review — are new features tested?
- Lazy-load candidates — any top-level rules used in <50% of sessions? Consider moving to lazy-load.
- Always-on size — is the baseline creeping up? Re-measure it; `_rules_lazy_load/_tier_readmes/00_rules_overview.md` records the last measured tier sizes.

### Every ~6 months

Per Boris Cherny's recommendation, perform a **full reset**:
1. Archive current `~/.claude/` to `~/.claude_releases/YYYY_MM_DD/`
2. Start fresh with essential rules only
3. Force intentionality review for each rule as you re-add it

---

## Adding a new rule

### Step 1: Determine scope

- **Core rule?** Used across multiple domains, or security-critical? → an always-on tier (`01_essentials/` to `03_authoring_guidelines/`, per `_rules_lazy_load/_tier_readmes/00_rules_overview.md`)
- **Domain-specific?** Applies to one area (SQL, Airflow, dbt)? → `_rules_lazy_load/`
- **Niche?** Referenced infrequently or only in specific projects? → `_rules_lazy_load/`

### Step 2: Write the rule

- **~100 lines, 110 at most.** If longer, split into parent + child files.
- **One concept per file.** Don't bundle unrelated rules.
- **Follow style:** Emoji headers, bold keywords, progressive disclosure.
- **Related links go in the tier README,** under "🔗 Related rules" — not in the rule, which is loaded every session.

### Step 3: Add tests

- **Enforcement rule or hook?** A test in `_tests/rules/` or `_tests/hooks/` is required.
- **Instructional rule?** `test_rules_structure.py` already covers its format.
- **Rule recording a real incident?** Add a content-regression test for its key phrases — see `testing.md`.

### Step 4: Update documentation

Work through the **Docs** and **Wiring** sections of `_rules_lazy_load/authoring_rules/_hard_gates_checklist.md` — that checklist is the current source of truth, so it isn't copied here.

### Step 5: Commit

Commit per `git.md`: Conventional Commits (`feat(rules): add <rule_name>`), files staged by name.

---

## Promoting a rule from lazy to top-level

Rare, but necessary when a rule becomes foundational.

### Promotion criteria

A rule should move from `_rules_lazy_load/` to an always-on tier when:

1. **Used in most sessions** — audit transcripts show >70% of sessions reference it
2. **Security-critical** — blocks risky actions or prevents vulnerabilities
3. **Referenced frequently from other rules** — forms a foundational dependency

### Promotion example

**MCP trust model** shows where the line sits: it stays lazy-loaded at `_rules_lazy_load/mcp_trust_model.md`.
- It's security-critical (prevents prompt injection), so it meets criterion 2.
- But it's only needed in sessions that use MCP tools, so it doesn't meet criterion 1 — reading it on demand covers it.

### Promotion process

1. **Verify criteria** — audit transcripts; confirm usage patterns
2. **Move file** — from `_rules_lazy_load/` into the matching tier under `rules/` (`01_essentials/` to `03_authoring_guidelines/`), where it loads natively
3. **Point to it** — if it's a child, add a `**Loads on its own from:**` line to its parent, and note the size it adds
4. **Run the suite** — `test_always_on_reachability.py` confirms nothing under `rules/` is a README, `_lazy_load/` folder or `@import`
5. **Update docs** — remove from lazy-load index; add to top-level rule index
6. **Commit** — `refactor(rules): promote <rule_name> from lazy to top-level`

---

## Removing unused rules

If a rule is no longer used:

1. **Audit usage** — confirm it's unused via transcript review
2. **Remove rule file** and associated test
3. **Remove from imports** — if top-level, remove from CLAUDE.md
4. **Update docs** — remove from all README and index files
5. **Commit** — `chore(rules): remove <rule_name>`

---

## Design tensions & tradeoffs

Every config makes tradeoffs. Understanding them helps future decisions:

### Breadth vs. depth

- **Breadth:** Many rules covering many domains (see each tier's README for the current set)
- **Depth:** Few rules, highly specific (fewer imports, but harder to find)
- **Current choice:** Breadth with lazy-load — discover rules as needed, don't lose them
- **If changed:** Would require consolidating rules or moving some to external docs

### Automation vs. explicitness

- **Automation:** Hooks silently enforce rules (reduces friction, but behavior is hidden)
- **Explicitness:** Every always-on rule sits in a `rules/` tier folder, so the folder listing is the always-on list (easy to audit)
- **Current choice:** Balance — enforcement hooks for safety-critical rules, explicit lists for others
- **If changed:** More automation risks silent rule changes; less automation increases maintenance friction

### Consistency vs. flexibility

- **Consistency:** Rigid structure prevents drift (easier to maintain long-term)
- **Flexibility:** Ad-hoc rules for edge cases (faster to ship new features)
- **Current choice:** Consistent structure (folders, naming), flexible content
- **If changed:** More flexibility risks fragmentation; stricter consistency risks slow adoption

---

## Improvement opportunities (2026 and beyond)

### Near-term (next 2–3 months)

- Monitor which lazy-load rules are frequently loaded; consider promotion if >50% of sessions use them
- Audit always-on size against Claude Code's 150k-character warning
- Add test coverage for new enforcement hooks as they're created

### Medium-term (6–12 months)

- Evaluate whether `03_authoring_guidelines/` can be lazy-loaded — it is used in only some sessions
- Consider a "seasonal" rule set (e.g., "quarterly planning rules" loaded only during planning season)
- Review MCP trust model; consider whether additional MCP-specific rules are needed

### Long-term (>12 months)

- Full reset per Boris Cherny's ~6-month cycle (archive to `~/.claude_releases/YYYY_MM_DD/`, start fresh)
- Evaluate whether new always-on rules in `rules/` are still justified
- Consider whether lazy-load structure has natural groupings (e.g., `_rules_lazy_load/mcp/`, `_rules_lazy_load/infrastructure/`)
