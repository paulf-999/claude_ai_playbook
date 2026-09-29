<!-- version: 1.0.0 -->
<!-- created: 2026-09-28 -->
<!-- updated: 2026-09-28 -->
# ✅ Rule Hard Gates Checklist

**Purpose:** Final tick-box check before finishing a rule — verify placement, content, testing, wiring and docs, then run the before-merging review.

---

## Before finishing a rule, verify ALL of these:

### 📍 Placement
- [ ] Name is snake_case and self-describing, per `naming_standards.md`
- [ ] Tier chosen deliberately (`01_essentials/`–`05_lazy_load/`), with always-on token cost justified
- [ ] No existing rule already covers this concept (checked `claude_rule_loading_strategy.md` and searched `_rules/`)
- [ ] Child files sit in a `<parent>/` subdirectory with an `_` prefix, and there are 2 or more of them

### 📝 Content
- [ ] Metadata header on lines 1–3 (`version`, `created`, `updated`), bumped on every edit
- [ ] H1 heading has an emoji
- [ ] One-line **Purpose** statement sits directly under the H1
- [ ] One concept per file
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
- [ ] Every child the parent describes has a real `@import` line, not just a mention in prose
- [ ] Always-on rules are reachable from `CLAUDE.md`, and lazy-load rules are not imported
- [ ] A **Related** section links the rule's parent, siblings and dependencies

### 📚 Docs
- [ ] Quality scorecard created or updated at `_rules/quality_scorecards/<tier>/scorecard_<rule_name>.md`
- [ ] Tier README (`_rules/<tier>/README.md`) and `_rules/README.md` list the new file
- [ ] `docs/whats_installed.md` rules description updated

---

## 🔎 Before merging

1. **Run the suite:** `pytest src/claude/_tests/` passes, including `test_rules_structure.py`, `test_always_on_reachability.py` and `test_file_structure_compliance.py`.
2. **Re-read the scorecard:** its scores still match the rule as written, not the first draft.
3. **Scan the docs:** check `quickstart.md`, `training.md` and `docs/reference/` for pages that mention the area you changed.

---

## 🔗 Related

- Parent: `authoring_rules.md` — pre-creation checklist, creation steps and quality gates
- Sibling: `_common_mistakes.md` — the mistakes these gates are designed to catch
