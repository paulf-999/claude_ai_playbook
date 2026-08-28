# 🔧 Logger Setup & Log Levels

**Purpose:** Establish logger initialization and log level conventions for different message types.

---

## 🔧 Logger setup

**Initialize at module level — never in functions:**

```python
import logging

logger = logging.getLogger(__name__)
```

**Why:** Using `__name__` creates a logger hierarchy matching the module structure, allowing granular control of log levels per module.

**Never create loggers inside functions:**

```python
# ❌ WRONG — creates a new logger on every call
def load_config(path):
    logger = logging.getLogger(__name__)
    ...
```

---

## 📊 Logging levels

| Level | Purpose | When to use | Example |
|---|---|---|---|
| **DEBUG** | Detailed info for debugging during development | Development only; very verbose | Variable values, function entry/exit, loop iterations |
| **INFO** | General informational messages | Important progress and milestones | "Config loaded from /path/to/file", "Migration started", "3 connections processed" |
| **WARNING** | Something unexpected, but code continues | Unusual conditions that are recoverable | "Fallback to default config", "Connection disabled (not found on target)" |
| **ERROR** | A serious error that code cannot recover from | Errors before raising exceptions | "Config file not found", "Authentication failed" |
| **CRITICAL** | A severe error requiring immediate attention | Rarely used | System-level failures |

---

## ✅ Good logging patterns

### DEBUG — development details

```python
def load_config(path: str) -> dict:
    logger.debug(f"Loading config from: {path}")
    try:
        with open(path) as f:
            config = yaml.safe_load(f)
        logger.debug(f"Successfully loaded config with {len(config)} items")
        return config
    except FileNotFoundError:
        logger.error(f"Config file not found: {path}")
        raise
```

**When to use:** Intermediate values, function calls, loop progress for development troubleshooting. DEBUG logs are disabled in production.

### INFO — progress and results

```python
def migrate_connections(client, connections: list) -> int:
    logger.info(f"Starting migration of {len(connections)} connections")
    created = 0
    for conn in connections:
        client.create_connection(conn)
        created += 1
    logger.info(f"Migration complete: {created} connections created")
    return created
```

**When to use:** Workflow milestones, status updates, summary results. Users should be able to follow progress from INFO logs alone.

### WARNING — unexpected but recoverable

```python
def get_connection_by_name(client, name: str):
    try:
        return client.get_connection(name)
    except ConnectionNotFound:
        logger.warning(f"Connection '{name}' not found, using fallback default")
        return client.get_connection("default")
```

**When to use:** Unexpected but handled gracefully. The program continues but with degraded or unexpected behavior.

### ERROR — serious before raising

```python
def load_required_var(var_name: str) -> str:
    value = os.environ.get(var_name)
    if value is None:
        logger.error(f"Required environment variable '{var_name}' is not set")
        raise EnvironmentError(f"{var_name} is not set")
    return value
```

**When to use:** Always log before raising exceptions. Provides debugging context without hiding the error.

---

## 🔗 Related

- Parent: `logging.md` — Logging overview and links
- Sibling: `logging/_what_to_log.md` — What to log and what NOT to log
- Sibling: `logging/_error_handling.md` — Logging in error handling context
