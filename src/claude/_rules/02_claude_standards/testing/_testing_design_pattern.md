# 🏗️ Test Design Pattern

**Purpose:** Establish a standard pattern for writing tests that validate intended behavior and communicate goals clearly.

---

## 4-Step Pattern

When writing a test for a new feature, follow this pattern:

### 1️⃣ **State the Goal**

**What:** One sentence describing what this test validates.

✅ **Good example:**
```
"Validates that new hooks inject context without blocking execution."
```

❌ **Bad example:**
```
"Tests the hook."
```

**Why:** Goal statement makes test purpose clear to future readers. Without it, a failing test is a mystery.

---

### 2️⃣ **Test Intended Behavior**

**What:** Validate that the feature does what you intended, not just that "the code runs."

✅ **Good example:**
```
"Verify the `git show` permission reduces prompts on common git operations."
```

❌ **Bad example:**
```
"Ensure `git show` is in the allowlist."
```

**Why:** Testing intended behavior prevents false confidence. A permission in an allowlist means nothing if it doesn't reduce prompts.

---

### 3️⃣ **Use Assertion Messages**

**What:** When a test fails, the message should explain what went wrong and how to fix it.

✅ **Good example:**
```python
assert cost < 500, f"Settings context cost too high: {cost} tokens (target: <500)"
```

❌ **Bad example:**
```python
assert cost < 500
```

**Why:** Good assertion messages reduce debugging time and prevent silent failures.

---

### 4️⃣ **Spot-Check Critical Cases**

**What:** Don't test everything. Test the invariants that matter.

✅ **Good example:**
```
Spot-check 3-5 representative aliases for behavior match.
```

❌ **Bad example:**
```
Test every conceivable code path (over-engineered).
```

**Why:** Over-testing creates brittle tests that break on unrelated changes. Spot-checking catches real issues with less maintenance.
