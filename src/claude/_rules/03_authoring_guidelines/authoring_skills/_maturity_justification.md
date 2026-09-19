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

Document it in **SKILL.md's Best For line**, not in `_quality_scorecard.md` —
that file is table-only (see `_quality_scorecard_template.md`); justification
narrative belongs where a reader actually looks for it.

Keep it to one sentence woven into the existing "Best for:" line: name the
stage and the one or two things that stage doesn't yet cover.

**Example:**
```markdown
**Best for:** One-off pages using the general_page pattern. Currently at the
**tactical** development stage — main path plus light error handling, not
full edge-case coverage yet.
```

Use the evidence table above (real problem, use frequency, test coverage,
dependencies, scope maturity) to *choose* the stage — you don't need to write
all five out per skill, just let them justify the one sentence you land on.

---

## 🔗 Related

- Parent: `authoring_skills.md` — quick navigation and hard gates checklist
