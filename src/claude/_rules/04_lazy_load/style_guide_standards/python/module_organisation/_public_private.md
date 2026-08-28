# 🔒 Public vs Private Functions & Constants

**Purpose:** Establish conventions for distinguishing public API from internal helpers — ensuring module interfaces are clear and changes to internals don't break users.

---

## 🔒 Public vs private functions

Use underscore prefix to signal whether a function is part of the module's public API or an internal helper.

### ✅ Public functions (no underscore)

```python
def load_config(path: str) -> dict:
    """Load YAML config and interpolate ${ENV_VAR} references.

    This is the main API for users of this module.
    """
    ...

def validate_config(config: dict) -> None:
    """Validate config structure and required keys.

    Raises ValueError if config is invalid.
    """
    ...
```

**Why:** Functions without underscore are the module's public interface. Users can rely on these and will be notified of breaking changes.

### ✅ Private functions (with underscore)

```python
def _derive_connection_name(source_system: str, table_descriptor: str) -> str:
    """Internal helper — derive connection name from source and descriptor."""
    ...

def _interpolate(obj) -> dict:
    """Internal helper — recursively interpolate ${ENV_VAR} in strings."""
    ...
```

**Why:** Underscore prefix signals "internal use only." Changes to these are free; users don't depend on them.

### Guideline

- **Public (`no_underscore`):** Functions that other modules import and call
  - Core operations: `load_config()`, `validate_config()`, `migrate_connections()`
  - Filtering/transformation: `get_connection_by_name()`, `apply_connection_names()`
- **Private (`_underscore`):** Helpers used only within this module
  - Setup/initialization: `_make_client()`, `_load_plan()`
  - Processing steps: `_interpolate()`, `_apply_connection_names()`
  - Data construction: `_entry()`, `_write_inventory()`

### ❌ Wrong patterns

```python
# ❌ WRONG — inconsistent: both should be public or both private
def load_config(path):  # public
def process_config(config):  # public but could be confused with private

# ❌ WRONG — public function with leading underscore (confuses users)
def _load_config(path):  # looks private but is the main API
    ...

# ❌ WRONG — helper without underscore (unclear it's internal)
def interpolate_env_vars(obj):  # looks like public API but is just a helper
    ...
```

---

## 🏷️ Constants grouping

Group related module-level constants and label the group with a comment.

```python
# Migration action states
CREATE = "CREATE"
UPDATE = "UPDATE"
DISABLE = "DISABLE"
NOOP = "NOOP"

# Default configuration values
DEFAULT_TIMEOUT = 30
DEFAULT_RETRIES = 3
DEFAULT_BATCH_SIZE = 100

# Environment variables required at startup
REQUIRED_ENV_VARS = ["AIRBYTE_API_URL", "AIRBYTE_USERNAME", "AIRBYTE_PASSWORD"]
```

**Why:** Comments make intent clear and group related constants visually.

### ✅ Naming

- **Format:** `SCREAMING_SNAKE_CASE` (all uppercase with underscores)
- **Grouping:** Related constants should be grouped together
- **Comments:** Each group should have a descriptive comment above it

### ✅ When to use constants

```python
# ✅ GOOD — magic numbers and strings extracted to named constants
CREATE = "CREATE"
UPDATE = "UPDATE"
DISABLE = "DISABLE"

if action == CREATE:
    ...
elif action == UPDATE:
    ...

# ❌ BAD — magic strings in code
if action == "CREATE":
    ...
elif action == "UPDATE":
    ...
```

---

## ⚡ Quick reference

| Element | Convention | Example |
|---------|-----------|---------|
| **Public function** | No underscore | `def load_config():` |
| **Private function** | Leading underscore | `def _make_client():` |
| **Constants** | SCREAMING_SNAKE_CASE, grouped | `TIMEOUT = 30` |
| **Constant group label** | Comment above group | `# Defaults` |

---

## 🔗 Related

- Parent: `module_organisation.md` — Module organisation overview
- Sibling: `module_organisation/_docstrings.md` — Module docstrings and metadata
