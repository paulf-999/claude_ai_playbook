# 🔄 Test Maintenance

**Purpose:** Keep tests current, relevant, and free of technical debt as the codebase evolves.

---

## Maintenance Practices

### 🔄 **Update Tests with Code**

**Rule:** When you change behavior, update the test at the same time — not separately.

**Why:** Decoupled updates create gap periods where broken code passes tests.

**How:** In the same commit that changes behavior, update its test.

---

### 🗑️ **Delete Dead Tests**

**Rule:** If a feature is removed, remove its test.

**Why:** Dead tests clutter the test suite and confuse future readers about what's actually tested.

**How:** When deprecating a feature, remove its test file at the same time.

---

### 🧹 **Refactor Tests**

**Rule:** Over time, tests accrue duplication and technical debt — refactor without changing goals.

**How:**
1. Identify duplication (repeated setup, assertions, helpers)
2. Extract to shared helper functions or fixtures
3. Verify tests still pass with same goal
4. Document the refactoring

**Example:** If 5 tests all call `setup_config()`, move it to a pytest fixture.

---

### 📝 **Document Goals**

**Rule:** If a test's purpose isn't obvious, add a one-line comment explaining what it validates.

**Example:**
```python
def test_skill_complexity_gate():
    """
    Validates that complexity scorer blocks skills >8 points for strategic maturity.
    Prevents scope creep in strategic-tier skills.
    """
    # Test code here
```

**Why:** Goal comment survives refactoring. A test that breaks is less mysterious if you know what it was meant to do.
