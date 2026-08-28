# 🚨 Logging in Error Handling

**Purpose:** Establish logging patterns for exception handling — ensuring errors are logged with context before being raised or handled.

---

## ✅ Always log before re-raising

Log errors with context before re-raising exceptions — provides debugging information without silencing the error.

```python
try:
    with open(config_path) as f:
        config = yaml.safe_load(f)
except FileNotFoundError:
    logger.error(f"Config file not found: {config_path}")
    raise
except yaml.YAMLError as e:
    logger.error(f"Invalid YAML in {config_path}: {e}")
    raise
```

**Why:**
- Logs provide debugging context (which file, why it failed)
- Re-raising preserves the stack trace for the caller
- Caller can decide how to handle the error (retry, fallback, fail)

---

## ✅ Specific exception types

Catch specific exceptions, not generic `Exception`:

```python
# ✅ GOOD — catches specific error, logs context
try:
    os.environ['REQUIRED_VAR']
except KeyError:
    logger.error("Required environment variable not set: REQUIRED_VAR")
    raise EnvironmentError("REQUIRED_VAR is not set")
```

**Why:** Specific exception types help isolate the problem and prevent masking unrelated errors.

---

## ✅ Use appropriate log level for error context

| Scenario | Level | Example |
|----------|-------|---------|
| **Expected validation error** | WARNING | `logger.warning(f"Skipping invalid connection: {e}")` |
| **Unexpected system error** | ERROR | `logger.error(f"System error during migration: {e}")` |
| **Critical failure** | CRITICAL | `logger.critical(f"Cannot start: {e}")` |

### Expected errors (WARNING level):

```python
# Validation errors expected from user input
try:
    validate_config(user_config)
except ValueError as e:
    logger.warning(f"Invalid user config: {e}")
    # Maybe retry or use fallback
```

### Unexpected errors (ERROR level):

```python
# System errors not expected to happen
try:
    client = AirbytClient()
except ConnectionError as e:
    logger.error(f"Failed to connect to Airbyte server: {e}")
    raise
```

---

## ✅ Use `finally` for guaranteed cleanup with logging

```python
try:
    client = AirbytClient()
    result = client.migrate(connections)
except ConnectionError as e:
    logger.error(f"Migration failed: {e}")
    raise
finally:
    try:
        client.close()
        logger.debug("Client closed successfully")
    except Exception as e:
        logger.warning(f"Error closing client: {e}")
```

**Why:** `finally` runs regardless of success or exception. Ensure critical cleanup happens and log any cleanup errors.

---

## ❌ Bad patterns to avoid

### 1. Bare except clause — catches everything, including system exceptions

```python
# ❌ WRONG — catches KeyboardInterrupt, SystemExit, etc.
try:
    do_something()
except:
    pass
```

**Problem:** Masks unexpected exceptions; hides bugs.

### 2. Generic Exception — too broad

```python
# ❌ WRONG — catches unrelated exceptions
try:
    config = load_config(path)
except Exception:
    logger.error("Failed")
    return None
```

**Problem:** Catches the wrong exceptions; makes debugging harder.

### 3. Swallowing without logging — no debugging context

```python
# ❌ WRONG — no way to know what failed
try:
    os.environ['REQUIRED_VAR']
except KeyError:
    pass  # Silent failure
```

**Problem:** Impossible to debug why the program behaves unexpectedly.

### 4. Catching specific exception without re-raising — changes control flow silently

```python
# ❌ WRONG — caller has no idea this failed
try:
    validate_config(config)
except ValueError:
    logger.error("Invalid config")
    # No re-raise; caller thinks validation passed
```

**Problem:** Caller unaware of error; program continues with invalid state.

### 5. Logging the full traceback — too verbose and exposes internals

```python
# ❌ WRONG
try:
    process()
except Exception as e:
    logger.error(f"Error: {traceback.format_exc()}")
    raise
```

**Problem:** Full tracebacks are noisy; exception message is usually sufficient.

---

## 📋 Decision tree: When to log vs. re-raise

```
Exception occurs
    │
    ├─ Is this expected (e.g., validation error)?
    │  ├─ YES: Log at WARNING level, maybe continue with fallback
    │  └─ NO: Log at ERROR level, re-raise (caller decides what to do)
    │
    ├─ Do I have context to add (file path, values)?
    │  ├─ YES: Log with context, then re-raise
    │  └─ NO: Just re-raise (logging won't add value)
    │
    └─ Is this the last handler (main function)?
       ├─ YES: Log and handle/exit (no re-raise)
       └─ NO: Log and re-raise (let caller handle)
```

---

## 🔗 Related

- Parent: `logging.md` — Logging overview and links
- Sibling: `logging/_setup_and_levels.md` — Logger setup and log levels
- Sibling: `logging/_what_to_log.md` — What to log and what NOT to log
- Related: `python.md` (parent) → Error handling section
