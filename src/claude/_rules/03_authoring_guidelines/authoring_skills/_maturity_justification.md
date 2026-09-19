# 📈 Skill Maturity Justification

**Purpose:** Maturity level (draft, tactical, strategic) must be justified with evidence, not aspirations.

---

## How to Choose Your Maturity Level

Use this decision framework:

| Evidence | Draft | Tactical | Strategic |
|----------|-------|----------|-----------|
| **Real problem** | Speculative or one-time | Recurring, observed need | Core workflow, heavy use |
| **Use frequency** | <2/month | 5–20/month | 20+/month or always-on |
| **Test coverage** | 5–8 evals (happy paths) | 8–12 evals (paths + errors) | 12+ evals (+ edge cases) |
| **Dependencies** | Experimental tools | Battle-tested tools | Core infrastructure |
| **Documentation** | Basic how-to | Clear + reference docs | Ultra-lean + comprehensive refs |
| **Scope maturity** | Still exploring | Well-defined boundaries | Stable, frozen scope |

## Testing by Maturity Level

**Draft (5–8 evals)**
- Happy paths: user invokes skill, gets expected output
- Basic validation: inputs are checked, bad inputs fail gracefully
- No error cases or edge cases required (scope still evolving)

**Tactical (8–12 evals)**
- All from Draft, PLUS:
- Error cases: network failures, invalid API responses, permission denied
- Retry logic: does the skill recover from transient failures?
- User interactions: does the skill ask clarifying questions when needed?

**Strategic (12+ evals)**
- All from Tactical, PLUS:
- Edge cases: unusual inputs, boundary conditions, race conditions
- Adversarial inputs: what if the user passes malicious or contradictory data?
- Performance: does the skill scale? Does it handle large datasets?
- Security: are secrets handled safely? Are inputs validated against injection?

## Writing Your Maturity Justification

Document in `_quality_scorecard.md`:

```markdown
## Maturity Justification

**Real problem solved:** <What recurring user need does this skill address?>

**Use frequency:** <How often is this used per month? Data from sessions?>

**Test coverage:** <# evals total; what's covered (happy paths, errors, edge cases)>

**Dependency assessment:** <Battle-tested tools? Experimental?>

**Scope assessment:** <Clear boundaries? Stable for v1.0? Future enhancements documented?>

**Conclusion:** This skill justifies [Draft|Tactical|Strategic] maturity because:
- [Evidence point 1]
- [Evidence point 2]
- [Evidence point 3]
```

---

## 🔗 Related

- Parent: `authoring_skills.md` — quick navigation and hard gates checklist
