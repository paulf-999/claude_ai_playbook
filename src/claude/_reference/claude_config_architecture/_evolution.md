---
created: 2025-11-15
last_modified: 2026-08-19
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
- Token cost tracking — is baseline creeping up?

### Annually

Per Boris Cherny's recommendation, perform a **full reset**:
1. Archive current `~/.claude/` to `~/.claude_releases/YYYY-MM-DD/`
2. Start fresh with essential rules only
3. Force intentionality review for each rule as you re-add it

---

## Adding a new rule

### Step 1: Determine scope

- **Core rule?** Used across multiple domains, or security-critical? → Top-level import
- **Domain-specific?** Applies to one area (SQL, Airflow, dbt)? → `lazy_load/`
- **Niche?** Referenced infrequently or only in specific projects? → `lazy_load/`

### Step 2: Write the rule

- **Max 100 lines.** If longer, split into parent + child files.
- **One concept per file.** Don't bundle unrelated rules.
- **Follow style:** Emoji headers, bold keywords, progressive disclosure.
- **Reference related rules** with `[[name]]` links.

### Step 3: Add tests

- **Enforcement hook?** Write corresponding test in `_tests/hooks/`.
- **Behavior rule?** Add behavior test to validate documented functionality.
- **Structure rule?** Already covered by `test_rules_structure.py`.

**No rule goes live without a test.**

### Step 4: Update documentation

Update all of the following (failing to update any is incomplete):

| Document | What to update |
|---|---|
| `~/.claude/_rules/README.md` (if top-level) or `~/.claude/_rules/lazy_load/README.md` (if lazy) | Add entry to rule index |
| `~/.claude/CLAUDE.md` | Add `@import` for top-level rules only |
| `docs/whats_installed.md` | Add rule to the appropriate section |
| `~/.claude/_tests/README.md` | Note new test file location |
| Any related `_rules/*.md` files | Update cross-references |

### Step 5: Commit

```bash
git add <rule_file> <test_file> <doc_updates>
git commit -m "feat(rules): add <rule_name>

<One sentence explaining why this rule exists and what problem it solves.>

Co-authored by Claude Code"
```

---

## Promoting a rule from lazy to top-level

Rare, but necessary when a rule becomes foundational.

### Promotion criteria

A rule should move from `lazy_load/` to top-level (imported in CLAUDE.md) when:

1. **Used in most sessions** — audit transcripts show >70% of sessions reference it
2. **Security-critical** — blocks risky actions or prevents vulnerabilities
3. **Referenced frequently from other rules** — forms a foundational dependency

### Promotion example

**MCP trust model** (originally lazy) was promoted because:
- Every MCP tool use references it
- It's security-critical (prevents prompt injection)
- Sessions using MCP tools form ~30–40% of all sessions; when MCP is used, the rule is always needed

### Promotion process

1. **Verify criteria** — audit transcripts; confirm usage patterns
2. **Move file** — from `lazy_load/` to top-level `_rules/`
3. **Add to CLAUDE.md** — add `@import` with token cost and justification
4. **Update tests** — if compliance tests flag it as "should not be imported," update the test
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

- **Breadth:** Many rules covering many domains (current: 14 top-level, 10+ lazy)
- **Depth:** Few rules, highly specific (fewer imports, but harder to find)
- **Current choice:** Breadth with lazy-load — discover rules as needed, don't lose them
- **If changed:** Would require consolidating rules or moving some to external docs

### Automation vs. explicitness

- **Automation:** Hooks silently enforce rules (reduces friction, but behavior is hidden)
- **Explicitness:** All rules visible in CLAUDE.md (easier to audit, but more to read)
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
- Audit baseline import token cost; target <2,000 tokens
- Add test coverage for new enforcement hooks as they're created

### Medium-term (6–12 months)

- Evaluate whether `claude_internal/` can be split — may have rules infrequently used
- Consider a "seasonal" rule set (e.g., "quarterly planning rules" loaded only during planning season)
- Review MCP trust model; consider whether additional MCP-specific rules are needed

### Long-term (>12 months)

- Full reset per Boris Cherny's cycle (archive to `~/.claude_releases/2026-Q4/`, start fresh)
- Evaluate whether new top-level imports are still justified
- Consider whether lazy-load structure has natural groupings (e.g., `lazy_load/mcp/`, `lazy_load/infrastructure/`)

---

## Related documents

- **Guiding principles:** `~/.claude/_rules/guiding_principles.md`
- **Lazy-load guide:** `~/.claude/_rules/lazy_load/README.md`
- **Testing rules:** `~/.claude/_rules/testing.md`
- **Naming standards:** `~/.claude/_rules/naming_standards.md`
- **Parent doc:** `claude_config_architecture.md`
