# 📊 Rule Quality Scorecards

**Purpose:** Apply the same quality-scorecard discipline skills already have (`quality_scorecard.md`) to `_rules/` files — centralized here rather than colocated, since rule audits happen *across* rules on a cadence, not per-rule at creation time.

---

## 📁 Location convention

One file per scored rule, mirroring the tier path: `_rules/quality_scorecards/<tier>/<rule_name>.md`.

**Example:** `_rules/01_essentials/guiding_principles.md` → `_rules/quality_scorecards/01_essentials/guiding_principles.md`

**Never `@import` these files.** They're authoring/review artifacts, not content Claude reads while operating — the whole point is keeping always-on rule files free of scorecard token cost, the same reasoning that already keeps skills' `quality_scorecard.md` un-imported.

**Child rules** (e.g. `git/_commits.md`) get their own scorecard file at the equivalent nested path: `quality_scorecards/02_claude_standards/git/_commits.md`.

---

## 📋 Template

```markdown
# Quality Scorecard — <rule_name>.md

| Dimension | Score | Notes |
|---|---|---|
| **Clarity** | X/10 | • 🔍 **<keyword>:** is the guidance unambiguous and actionable?<br>• 🔍 **<keyword>:** [second point, if needed] |
| **Complexity** | X/10 | • 🧮 **Raw complexity N:** Concepts+Scope+Dependencies+Prerequisites — see `_complexity_scoring.md` |
| **Evidence of Need** | X/10 | • 🔗 **<keyword>:** backed by real, recurring problems, or speculative? |
| **Token Cost Justification** | X/10 | • 🎯 **<keyword>:** if always-on, is placement justified by session coverage? |
| **Structural Compliance** | X/10 | • ✅ **<keyword>:** writing_style.md / naming_standards.md adherence |
| **Currency** | X/10 | • 🔍 **<keyword>:** any stale references? Content still accurate? |
| **Test Coverage** | X/10 | • 🧪 **<keyword>:** structural test passes; content-regression test if it documents a real incident |
| **Overall** | **X.X/10** | • 💪 **<keyword>:** [strength]<br>• ⚠️ **<keyword>:** [gap, if any] |
```

**Notes column format:** bullet points, one per line, joined with `<br>` (standard markdown lists don't render inside table cells) — `• <emoji> **<bold keyword>:** <one point>`. Never a single run-on sentence. One point per bullet, matching `writing_style.md`'s general bullet convention and the same pattern used in `claude_plans/_plan_file_format.md`.

---

## 🎯 Per-dimension criteria

**Clarity** — Would two readers interpret this the same way?
- 10 = unambiguous, actionable, no room for conflicting interpretation
- 1 = vague, contradictory, or requires outside context to apply

**Complexity** — Use the shared formula in `authoring_guidelines/_complexity_scoring.md` (Concepts + Scope + Dependencies + Prerequisites), inverted: 10 = simple, single-concept, single-file; 1 = tangled, many concepts, wide scope. No maturity gate exists for rules yet (see that file) — this dimension scores the rule as-is, it doesn't cap anything.

**Evidence of Need** — Per `guiding_principles.md`'s own "Intentionality gates everything":
- 10 = documented recurring problem, real incident, or usage evidence
- 1 = speculative, "might be useful someday," no observed need

**Token Cost Justification** — Only meaningful for always-on tiers (`01_essentials/`–`04_claude_reference/`):
- 10 = high session coverage, safety-critical, or foundational — cost clearly earns its keep
- 1 = narrow applicability that should be lazy-loaded instead
- N/A for `05_lazy_load/` rules (already scoped to on-demand)

**Structural Compliance** — Does it follow this config's own conventions?
- Emoji headers, Purpose statement, ~100-line limit (or split into parent+children), trailing newline, bold-keyword bullets

**Currency** — Per `guiding_principles.md`'s own "False truth rots silently":
- 10 = verified current, no stale references to renamed/removed things
- 1 = known stale references, outdated examples, or drifted from actual practice

**Test Coverage** — Per `testing.md`'s instructional-content exception:
- 10 = passes `test_rules_structure.py`, plus a content-regression test if the rule documents a real incident
- Lower scores reflect missing coverage where the exception criteria says one is warranted, not the absence of a behavior-compliance test (never required)

**Overall** — `(Clarity + Complexity + Evidence + Token Cost + Structural + Currency + Test Coverage) / 7`, rounded to nearest 0.1. Omit **Token Cost Justification** from the average (and note "N/A") for lazy-loaded rules where it doesn't apply.

---

## 📅 When to score

- **On creation** — every new rule gets a scorecard alongside it, same as skills
- **During quarterly/6-month audits** — per `guiding_principles.md`'s existing audit cadence; this is the primary reason these live centralized, not colocated — an auditor sweeps `quality_scorecards/` in one pass instead of opening every rule file

---

## 🔗 Related

- `authoring_rules.md` — rule creation process; references this convention
- `authoring_skills/_quality_scorecard_template.md` — the skill-scorecard equivalent this mirrors
- `authoring_guidelines/_complexity_scoring.md` — shared complexity formula used by the Complexity dimension
- `guiding_principles.md` — source of the Intentionality and Currency principles this scorecard operationalizes
