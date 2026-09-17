# ✅ Assertions & Exception Testing

**Purpose:** Establish assertion and exception testing conventions for validating expected behaviour.

---

## ✅ Assertions

**Use plain assertions — pytest rewrites them for clear failure messages:**

```python
# ✅ GOOD — pytest shows clear diff on failure
assert args.config == "foo.yaml"
assert isinstance(result, list)
assert not log_path.exists()

# ✅ GOOD — comparison operators
assert len(log["migrations"]) == 1
assert cost < 500

# ✅ Use `in` for membership
assert "created_at" in logged
assert log_path in tmp_path.iterdir()
```

### Assertion messages — explain what went wrong

```python
# ❌ WEAK — no context
assert cost < 500

# ✅ GOOD — explains expected vs actual
assert cost < 500, f"Token cost too high: {cost} (expected <500)"
```

---

## 🚨 Exception testing

**Use `pytest.raises` to assert exceptions:**

```python
import pytest

def test_load_config_raises_on_file_not_found():
    """Verify FileNotFoundError is raised when config file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        load_config("/nonexistent/path.yaml")


def test_load_config_raises_on_invalid_yaml():
    """Verify YAMLError is raised for malformed YAML."""
    with pytest.raises(yaml.YAMLError):
        load_config("/path/to/invalid.yaml")


def test_validate_config_raises_with_pattern_match():
    """Verify ValueError message contains expected text."""
    with pytest.raises(ValueError, match="Invalid table_descriptor"):
        validate_config({"connections": [{"table_descriptor": "invalid"}]})
```

**Why:** Testing exceptions ensures error handling works and provides clear error messages.

---

## 📁 Test organisation

**Group related tests with comments:**

```python
# --- load_config tests ---

def test_load_config_reads_yaml_file():
    """File is read and parsed correctly."""
    ...

def test_load_config_interpolates_env_vars():
    """${ENV_VAR} references are resolved from environment."""
    ...

def test_load_config_raises_on_missing_env_var():
    """Raises EnvironmentError if ${VAR} is not set."""
    ...


# --- validate_config tests ---

def test_validate_config_passes_valid_config():
    """Valid config passes validation."""
    ...

def test_validate_config_raises_on_invalid_table_descriptor():
    """Raises ValueError for unknown table_descriptor."""
    ...
```

**Why:** Comments make test intent scannable and group related tests visually.

---

## ⚡ Quick reference

| Goal | Pattern | Example |
|---|---|---|
| **Test exception raised** | `pytest.raises()` | `with pytest.raises(ValueError, match="pattern"):` |
| **Verify assertion message** | Use `assert` with message | `assert x < 10, f"Expected x < 10, got {x}"` |
| **Group related tests** | Comment dividers | `# --- load_config tests ---` |

---

## 🔗 Related

- Parent: `testing.md` — Testing conventions overview
- Sibling: `testing/_naming_structure.md` — Test naming and structure
- Sibling: `testing/_fixtures_mocking.md` — Pytest fixtures and mocking
