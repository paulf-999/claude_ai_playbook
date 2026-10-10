<!-- version: 2.0.1 -->
<!-- created: 2026-09-28 -->
<!-- updated: 2026-10-06 -->
# ✅ Rule Hard Gates Checklist

**Purpose:** Final tick-box check before finishing a rule — verify placement, content, testing, wiring and docs, then run the before-merging review.

---

## ✅ Before finishing a rule, verify ALL of these:

### 📍 Placement
- [ ] Name is snake_case and self-describing, per `naming_standards.md`
- [ ] Folder chosen deliberately (`rules/01_essentials/`–`04_path_scoped/` or `_rules_lazy_load/`), with always-on token cost justified
- [ ] No existing rule already covers this concept (checked `claude_rule_loading_strategy.md` and searched `rules/` and `_rules_lazy_load/`)
- [ ] Child files sit in a `<parent>/` subdirectory with an `_` prefix, and there are 2 or more of them

### 📝 Content
- [ ] Metadata header on lines 1–3 (`version`, `created`, `updated`), bumped on every edit
- [ ] H1 heading has an emoji
- [ ] One-line **Purpose** statement sits directly under the H1
- [ ] One concept per file
- [ ] Contents section only if the rule has 3 or more real `##` headings
- [ ] 110 lines or fewer; split into parent and children if longer
- [ ] Bullets open with a bold keyword and hold one sentence each
- [ ] Evidence of need is recorded (incident, PR or repeated failure), not a hypothetical
- [ ] No hardcoded paths or usernames, per `portable_paths.md`
- [ ] File ends with exactly one newline

### 🧪 Testing
- [ ] Enforcement rule has a test in `_tests/rules/` or `_tests/hooks/`, named after the rule file
- [ ] Rule that records a real incident has a content-regression test for its key phrases, per `testing.md`
- [ ] New tests carry the metadata header and meet the quality ≥9 and complexity ≥7 floors

### 🔗 Wiring
- [ ] Every child sits in the folder that matches how it should load, and the parent names it in a `**Loads on its own from:**` or `**Read on demand:**` line
- [ ] Nothing under `rules/` is `@import`ed, and no README sits under `rules/`
- [ ] The rule has no `## Related` section — its parent, sibling and dependency links sit in the tier README in `_rules_lazy_load/_tier_readmes/` under "🔗 Related rules" (tiers 02–05 only, as `01_essentials/` keeps none)

### 📚 Docs
- [ ] Quality scorecard created or updated at `_admin/_quality_scorecards/rules/<tier>/scorecard_<rule_name>.md`
- [ ] Tier README (`_rules_lazy_load/_tier_readmes/<tier>.md`) and `_rules_lazy_load/_tier_readmes/00_rules_overview.md` list the new file
- [ ] `docs/whats_installed.md` rules description updated

---

## 🔎 Before merging

1. **Run the suite:** `pytest src/claude/_tests/` passes, including `test_rules_structure.py`, `test_always_on_reachability.py` and `test_file_structure_compliance.py`.
2. **Re-read the scorecard:** its scores still match the rule as written, not the first draft.
3. **Scan the docs:** check `quickstart.md`, `training.md` and `docs/reference/` for pages that mention the area you changed.
