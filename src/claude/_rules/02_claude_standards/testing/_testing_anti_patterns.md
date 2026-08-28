# 🚫 Testing Anti-Patterns

**Purpose:** Identify common testing mistakes and understand why they undermine confidence.

---

## Anti-Patterns to Avoid

### 🟥 **Empty Test**

**What:** A test that always passes (no real assertions).

**Example:**
```python
def test_hook_loads():
    hook = load_hook("my_hook")
    # No assertions; test always passes
```

**Why it fails:** Creates false confidence. The test tells you nothing about whether the hook actually *works*.

**Fix:** Add assertions that validate intended behavior.

---

### 🟥 **Over-Mocking**

**What:** Mocking so much that the test doesn't reflect real behavior.

**Example:**
```python
def test_git_operations():
    mock_git = Mock()
    mock_git.status.return_value = "clean"
    # Real git behavior never tested
```

**Why it fails:** Mocks create idealized scenarios. Tests pass in isolation but fail in production when real git behaves differently.

**Fix:** Use real dependencies for integration tests; mock only external services.

---

### 🟥 **Fragile Test**

**What:** Test breaks on unrelated changes; coupled to implementation details instead of behavior.

**Example:**
```python
def test_user_created():
    user = User.create(name="Alice")
    assert user.id == 1  # Fails if another test creates user first
```

**Why it fails:** Test is coupled to internal state (id=1), not behavior (user exists). Any change to test order breaks it.

**Fix:** Test behavior, not implementation. Assert `user.id is not None`, not `== 1`.

---

### 🟥 **Slow Test**

**What:** Test takes >5 seconds to run; developers skip it.

**Example:**
```python
def test_deploy():
    deploy_to_production()  # 30 second wait
```

**Why it fails:** Slow tests create friction. Developers skip them during active development and find issues later.

**Fix:** Use fast integration tests; reserve slow tests for CI only. Mock expensive operations in local tests.

---

### 🟥 **Unclear Goal**

**What:** Test passes/fails but doesn't communicate what it's validating.

**Example:**
```python
def test_config():
    result = validate_config(CONFIG)
    assert result == True
    # What aspect of config? What should pass/fail?
```

**Why it fails:** In a year, you'll have forgotten what this test meant. Failing test is a mystery.

**Fix:** Use descriptive goal statement (see `_testing_design_pattern.md`).
