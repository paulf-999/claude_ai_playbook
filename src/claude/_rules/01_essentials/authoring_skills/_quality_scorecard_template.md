# Quality Scorecard — Template

Every skill includes a `reference/_quality_scorecard.md` containing only this table (no justification or rationale sections).

---

## Template

```markdown
# Quality Scorecard

| Dimension | Score | Notes |
|---|---|---|
| **Design** | X/10 | [Brief note on design quality] |
| **Complexity** | X/10 | [Brief note on code complexity] |
| **Test Coverage** | X/10 | [Brief note on test coverage] |
| **Code Quality** | X/10 | [Brief note on code quality/safety] |
| **Security** | X/10 | [Brief note on security measures] |
| **Documentation** | X/10 | [Brief note on documentation completeness] |
| **Standards Compliance** | X/10 | [Brief note on compliance with standards] |
| **Overall** | **X.X/10** | [One-sentence overall assessment] |
```

---

## Scoring Guidelines

| Score | Meaning |
|---|---|
| **10/10** | Exemplary. Meets all criteria for the dimension. No improvements needed. |
| **9/10** | Very strong. Meets most criteria. Minor gaps acceptable for maturity level. |
| **8/10** | Strong. Meets core criteria. Some gaps or edge cases unhandled. |
| **7/10** | Adequate. Meets basic criteria. Significant gaps or limitations. |
| **6/10** | Weak. Minimal criteria met. Major gaps or concerning patterns. |
| **<6/10** | Insufficient. Does not meet basic criteria. Rework needed. |

---

## Per-Dimension Criteria

**Design** — Is the skill's approach clear, defensible, and user-friendly?  
- Single clear purpose ✓
- Intuitive workflow or command structure ✓
- Thoughtful defaults and options ✓

**Complexity** — How much logic/branching does the implementation require?  
- 10/10 = simple, minimal branching, linear validation
- 1/10 = over-engineered, excessive abstraction, nested conditionals

**Test Coverage** — Are all code paths and error cases tested?  
- Draft: 5–8 evals covering happy paths + basic errors
- Tactical: 8–12 evals covering happy paths + errors + edge cases
- Strategic: 12+ evals covering all above + adversarial inputs

**Code Quality** — Is the code safe, maintainable, and well-structured?  
- Input validation ✓
- Error handling ✓
- Safe operation patterns ✓
- Clear error messages ✓

**Security** — Are secrets, permissions, and injection risks handled?  
- No hardcoded secrets ✓
- Least-privilege access ✓
- Input validation against injection ✓
- Safe file operations (symlinks, permissions) ✓

**Documentation** — Is the skill documented clearly enough for users?  
- SKILL.md explains purpose and usage ✓
- Examples show real-world scenarios ✓
- Troubleshooting covers common errors ✓
- FAQ answers predictable questions ✓

**Standards Compliance** — Does the skill follow naming, structure, and maturity conventions?  
- `domain_action` naming ✓
- Canonical SKILL.md structure ✓
- skill.contract.yaml complete ✓
- evals.yaml comprehensive ✓
- reference/ files organized and concise ✓

**Overall** — Holistic assessment of skill quality and production readiness.  
- Formula: `(Design + Complexity + Test + Code + Security + Documentation + Standards) / 7`
- Rounded to nearest 0.1
- Reflects maturity level (Draft ≤7, Tactical ≤8.5, Strategic ≤9.5)

---

## Notes

- Each dimension is scored **independently** — a 10/10 in Design doesn't guarantee 10/10 in Code Quality
- Scores reflect the **current version** — update when significant changes occur
- Overall score is **not a grade** — a 9.5/10 skill is production-ready, not "A-"
- Maturity justification and design rationale belong in SKILL.md or authoring_skills.md, not in the scorecard
