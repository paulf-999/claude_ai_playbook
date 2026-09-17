# 🚪 Complexity Exceptions

**Purpose:** Document when complex code is acceptable and how to justify it.

---

## 🎯 When to Accept Complex Code

Complex code is acceptable when:

**Justified by problem domain:**
- State machines or decision trees (inherent complexity)
- Data processing pipelines (many sequential steps)
- Configuration/setup code (many options and branches)

**With proper documentation:**
- Explain WHY the complexity exists
- Label major phases or branches
- Add comments helping readers navigate

---

## 📝 Documentation Format

When exceeding complexity thresholds, document like this:

```python
def complex_operation():
    """Brief description of what it does.

    NOTE: Cyclomatic complexity is X due to [reason].
    This is acceptable because [justification: business logic / performance / etc].

    Phases:
    1. [Phase A]: Describe what happens here
    2. [Phase B]: Describe what happens here
    """
```

---

## 📋 Complexity Scorecard

Before submitting code for review:

- [ ] CC < 10 (or documented exception)
- [ ] LOC < 30-40 (or documented exception)
- [ ] Nesting depth < 3 (or documented exception)
- [ ] Parameters < 5 (or documented exception)
- [ ] Line length < 120 chars
- [ ] One-sentence summary: Can you explain it?
- [ ] If complex: Exception documented with reasoning

---

## Related

- Parent: `_code_complexity.md` — Overview and quick reference
- Sibling: `_code_complexity_metrics.md` — Detailed metrics
