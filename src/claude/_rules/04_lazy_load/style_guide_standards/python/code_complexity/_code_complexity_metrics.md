# 📐 Complexity Metrics

**Purpose:** Detailed explanation of each metric, thresholds, and how to measure them.

---

## 🎯 Cyclomatic Complexity (McCabe)

**What:** Count of decision points (if, elif, for, while, and, or).

**Why:** Industry standard, tool-supported, proven baseline.

**Thresholds:**
- **1-5**: Simple, easy to understand
- **6-10**: Moderate, acceptable
- **11+**: Complex, refactor needed

**Tool:** `radon cc src/py/airbyte_manager/ -a`

**Example (CC=3):**
```python
def process(items):
    result = []
    for item in items:  # +1
        if item.valid:  # +1
            result.append(item.transform())
    return result
```

---

## 🧠 Cognitive Complexity

**What:** Mental load — how hard is the code to understand?

**Why:** Complements cyclomatic complexity. Low CC + high nesting = still hard to follow.

**Factors:**
- **Nesting depth**: Each level increases cognitive load
- **Boolean chains**: Multiple conditions on one line
- **Conditional jumps**: Early returns, exception handling

**When to apply:** When CC passes but code still "feels" complex.

**Example (CC=6, but high cognitive load):**
```python
if a and b or c and (d or e):  # Confusing, break it down
    # ...
```

**Better:**
```python
is_valid = a and b or c and (d or e)
if is_valid:
    # ...
```

---

## 📏 Lines of Code (LOC)

**What:** Number of lines in a function.

**Why:** CC doesn't capture length. Long linear functions are hard to understand.

**Threshold:** < 30-40 lines
- Exceeds 40? Consider extracting helper functions
- Exception: Data processing, setup code, linear sequences

**Tool:** `radon metrics src/py/airbyte_manager/ -s`

---

## 📍 Nesting Depth

**What:** How many levels deep code is nested (if/for/while/def inside each other).

**Why:** Each level exponentially increases cognitive load.

**Threshold:** < 3 levels

**How to reduce:**
- **Early returns**: Exit function early instead of deep nesting
- **Extract functions**: Move nested logic into helpers
- **Use guard clauses**: Invert conditionals to reduce nesting

**Example (depth=4, bad):**
```python
if x:
    if y:
        for item in items:
            if item.valid:
                # Deep nesting!
```

**Better (depth=2):**
```python
if not x or not y:
    return
for item in items:
    if not item.valid:
        continue
    # Process item
```

---

## 🔧 Parameter Count

**What:** Number of function parameters.

**Why:** Many parameters = complex interface and high cognitive load.

**Threshold:** < 5 parameters

**How to reduce:**
- **Group related params**: Use dataclasses or dicts for related options
- **Use kwargs**: Accept `**options` for flexible configuration
- **Partial application**: Pre-fill common parameter values

---

## 📏 Line Length

**What:** Characters per line (from your style guide).

**Threshold:** < 120 characters

**Why:** Long lines hide complexity or indicate poor naming.

**Exception:** Long strings, URLs, unavoidable literals.

**Tool:** `ruff check` (already configured)

---

## Related

- Parent: `_code_complexity.md` — Overview and quick reference
- Sibling: `_code_complexity_exceptions.md` — When to make exceptions
