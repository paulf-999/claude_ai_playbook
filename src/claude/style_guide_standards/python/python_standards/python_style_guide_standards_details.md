# 🐍 Python Standards

Exhaustive reference for the team's Python coding standards, which largely replicate PEP 8, covering:

* Naming conventions
* Imports
* String formatting
* Type hints
* Docstrings
* Error handling
* and code layout.

## 🏷️ Naming conventions

| Construct | Convention |
|---|---|
| Modules and packages | `snake_case` |
| Functions and methods | `snake_case` |
| Variables | `snake_case` |
| Classes | `CamelCase` (PascalCase) |
| Constants | `SCREAMING_SNAKE_CASE` |

- Names must be meaningful and descriptive — avoid abbreviations.
- Do not use single-letter variable names outside of loop counters.
- Do not capture change history in code — that belongs in git.

---

## 📥 Imports

- One module per import line.
- Use absolute imports.
- No wildcard imports (`from module import *`).
- Group in order, separated by blank lines:
  1. Standard library
  2. Third-party
  3. Local

---

## 💬 String formatting

Use f-strings. Do not use `str.format()` or `%` formatting.

---

## 🔖 Type hints

Add type hints to all function signatures:

```python
def get_secret_by_name(secret_name: str) -> str:
```

---

## 🔧 Functions and methods

- Default arguments go at the end of the argument list.
- No spaces around `=` in keyword arguments: `func(name="foo")` not `func(name = "foo")`.
- Single space after commas in function calls and definitions.

---

## 📝 Docstrings

All functions, classes, and modules must have docstrings. Use **reST format**:

```python
def get_secret_by_name(secret_name: str) -> str:
    """Retrieve a secret value by name from the configured secret manager.

    :param secret_name: The name of the secret to retrieve.
    :type secret_name: str
    :raises KeyError: If the secret name does not exist.
    :return: The secret value.
    :rtype: str
    """
```

Do not use Google-style or NumPy-style docstrings.

---

## ⚠️ Error handling

- Catch specific exceptions, not bare `except Exception:` or `except:`.
- Use `try-except-else` where appropriate.
- Use `finally` only when necessary for cleanup.

---

## 🗂️ Code layout

- 4 spaces for indentation — no tabs.
- Two blank lines between top-level functions and classes.
- One blank line between methods within a class.
- Space logically within functions to maintain readability.

---

## 📌 General

- Use `pathlib.Path` over `os.path` for file operations.
- Avoid mutable default arguments — use `None` and assign inside the function.
