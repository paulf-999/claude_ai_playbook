# 🔍 Python Style Guide Examples

Reference code examples demonstrating patterns from the Python style guide.

## 📚 Examples

### `_inline_comments_example.py`
**From:** `python.md` — Inline comments section

Demonstrates:
- When to comment (non-obvious logic, fallback behaviour, logical phases)
- Comment placement (above code, not at end of line)
- Avoiding restatement of obvious code
- Labeling groups of related constants

### `error_handling_patterns.py`
**From:** `logging/_error_handling.md` and `python.md` — Error handling section

Demonstrates:
- Logging before re-raising exceptions
- Using specific exception types (not bare `except:` or `Exception`)
- Logging at appropriate levels (WARNING for expected, ERROR for unexpected)
- Using `finally` for guaranteed cleanup
- Providing debugging context in error messages

### `module_organisation_example.py`
**From:** `module_organisation/` child files

Demonstrates:
- Module docstring format (Description, Date created)
- `__author__` and `__version__` metadata
- Public functions (no underscore prefix)
- Private functions (underscore prefix)
- Constants grouped with descriptive comments
- Clear module API boundaries

### `testing_example.py`
**From:** `testing/` child files

Demonstrates:
- Test naming: `test_<function>_<scenario>`
- Test structure: Setup → Execute → Assert
- Custom fixtures: `_make_client()`, `_entry()` helpers
- Mocking with `MagicMock` and mock assertions
- Exception testing with `pytest.raises`
- Using `monkeypatch` fixture for environment variables
- Grouping related tests with comments

### `logging_patterns.py`
**From:** `logging/` child files

Demonstrates:
- Logger setup at module level (correct pattern)
- Log levels: DEBUG, INFO, WARNING, ERROR with use cases
- What to log: entry/exit, state changes, counts, configuration
- What NOT to log: secrets, credentials, PII, full tracebacks
- Logging in error handling with proper context
- Avoiding excessive logging (noise reduction)

---

## 🎯 How to use

Reference these examples when:
- Writing new code and need concrete patterns to follow
- Reviewing code and want to check against established examples
- Learning the style guide — these examples show intent and best practices together

All examples follow the conventions documented in `python.md` and child files.
