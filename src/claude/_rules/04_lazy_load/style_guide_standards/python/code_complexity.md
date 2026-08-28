# 📊 Code Complexity

**Purpose:** Establish metrics to identify and prevent overly complex Python code. Reduces mental load and improves maintainability.

---

## 📋 Contents

- [Overview](#-overview)
- [Single responsibility](#-single-responsibility)
- [Quick reference](#-quick-reference)
- [Detailed metrics](#-detailed-metrics) — See `code_complexity/_code_complexity_metrics.md`
- [Escape hatches](#-escape-hatches) — See `code_complexity/_code_complexity_exceptions.md`

---

## 🎯 Overview

**Why it matters:** Complex code is hard to understand, maintain, and test. Mental load increases risk of bugs.

**Two types of complexity:**
1. **Structural** — decision points, nesting, parameters (measured by metrics)
2. **Cognitive** — how hard it is for humans to understand (measured by readability)

**Approach:** Use metrics as early warning signs. When metrics exceed thresholds, refactor or document why.

---

## 🎯 Single Responsibility Principle

**Each function should do one thing and do it well.**

**Indicators that a function does too much:**
- **High LOC:** > 30-40 lines suggests multiple responsibilities
- **High CC:** > 10 suggests multiple decision paths
- **Hard to name:** Can't explain in one sentence = too many responsibilities
- **Multiple reasons to change:** Each reason suggests a separate responsibility

**How to split:**
- Extract helpers for distinct concerns (e.g., setup logic separate from main logic)
- Use descriptive function names to clarify purpose
- Group related parameters together

**Example (too much responsibility):**
```python
def process_data(items, config, output_dir):
    # Validate items
    for item in items:
        if not validate(item):
            raise ValueError(...)

    # Transform items
    transformed = [transform(item) for item in items]

    # Write output
    write_results(transformed, output_dir)
```

**Better (split into helpers):**
```python
def process_data(items, config, output_dir):
    validate_items(items)
    transformed = transform_items(items)
    write_results(transformed, output_dir)
```

---

## ⚡ Quick Reference

| Metric | Target | Tool |
|--------|--------|------|
| **Cyclomatic Complexity** | < 10 | `radon cc` |
| **Lines of Code** | < 30-40 | `radon metrics` |
| **Nesting Depth** | < 3 | Manual review |
| **Parameters** | < 5 | Manual review |
| **Line Length** | < 120 chars | `ruff check` |

**Readability test:** Can you explain the function in one sentence?

---

## 📐 Detailed Metrics

@`_code_complexity_metrics.md` — Full explanation of each metric, thresholds, and examples.

---

## 🚪 Escape Hatches

@`_code_complexity_exceptions.md` — When complex code is acceptable and how to document it.

---

## 🛠️ Workflow

1. **Before submitting:** Run `radon cc` and `ruff check`
2. **If metrics exceed thresholds:** Refactor or document exception
3. **If documented:** Add comments explaining why complexity is necessary
4. **Review checklist:** Use scorecard in exceptions doc

---

## Related

- Parent: `../python.md` — Python coding standards
- Sibling: `../_inline_comments_example.py` — Commenting complex code
