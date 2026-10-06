<!-- version: 1.0.1 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-09-29 -->
# 🏷️ Test Naming & Structure

**Purpose:** Establish test naming conventions and test structure patterns for readable, maintainable tests.

---

## 🏷️ Test naming

**Pattern:** `test_<function>_<scenario>` — descriptive names explain what is being tested.

```python
# ✅ GOOD — scenario is clear
def test_resolve_configs_returns_explicit_path():
    """When given an explicit path, return it unchanged."""

def test_resolve_configs_returns_list_when_no_explicit_path():
    """When no path provided, return list of discovered configs."""

# ✅ GOOD — long names are OK if they clarify the scenario
def test_run_apply_creates_and_logs_migration():
    """Verify that --apply flag creates migrations and writes log."""

# ❌ BAD — scenario unclear
def test_resolve_configs():
    """What scenario?"""

def test_something():
    """Too vague."""
```

**Why:** Descriptive test names document behaviour without reading the test body. A failing test name immediately tells you what scenario broke.

---

## 🔨 Test structure

Follow the **Setup → Execute → Assert** pattern:

```python
def test_parse_args_config_and_apply(monkeypatch):
    # Setup: prepare test data and context
    monkeypatch.setattr(
        "sys.argv",
        ["airbyte_connection_creator.py", "--config", "foo.yaml", "--apply"],
    )

    # Execute: call the function being tested
    args = parse_args()

    # Assert: verify the expected behaviour
    assert args.config == "foo.yaml"
    assert args.apply is True
```

**Why:** This pattern is instantly recognisable and keeps tests focused on one scenario.
