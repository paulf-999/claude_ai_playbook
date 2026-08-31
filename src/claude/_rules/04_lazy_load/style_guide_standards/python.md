# 🐍 Python Coding Standards

**Purpose:** Establish Python coding conventions extending PEP 8, ensuring consistent, readable, and maintainable code across the team.

PEP 8 is the baseline. One override: maximum line length is **120 characters** (enforced by `ruff`).


## 📋 Contents

- [🗂️ Code layout](#-code-layout)
- [🏷️ Naming conventions](#-naming-conventions)
- [📥 Imports](#-imports)
- [💬 String formatting](#-string-formatting)
- [⚠️ Error handling](#-error-handling)
- [📝 Docstrings](#-docstrings)
- [🔧 Functions and methods](#-functions-and-methods)
- [🔖 Type hints](#-type-hints)
- [💬 Inline comments](#-inline-comments)
- [📌 General](#-general)
- [Related](#-related)

---
## 🗂️ Code layout

- **Indentation:** 4 spaces — no tabs
- **Between top-level:** two blank lines between functions and classes
- **Between methods:** one blank line between methods within a class
- **Within functions:** space logically to maintain readability

## 🏷️ Naming conventions

- **Modules/packages:** `snake_case`
- **Functions/methods:** `snake_case`
- **Variables:** `snake_case`
- **Classes:** `PascalCase`
- **Constants:** `SCREAMING_SNAKE_CASE`
  - **Meaningful names:** avoid abbreviations; no single-letter variables outside loop counters
  - **No history in names:** change history belongs in git, not code

## 📥 Imports

- **One per line:** one module per import statement
- **Absolute imports:** no wildcard imports (`from module import *`)
- **Group and order:** standard library → third-party → local, separated by blank lines

## 💬 String formatting

- **Use f-strings:** exclusively; do not use `str.format()` or `%` formatting

## ⚠️ Error handling

- **Specific exceptions:** never bare `except:` or `except Exception:`
- **Control flow:** use `try-except-else` where appropriate; `finally` only for cleanup

## 📝 Docstrings

All functions, classes, and modules must have docstrings using reST format:

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

- **Format:** reST only — no Google-style or NumPy-style docstrings

## 🔧 Functions and methods

- **Defaults at end:** default arguments go at the end of the argument list
- **Keyword arguments:** no spaces around `=` (e.g., `func(name="foo")`)
- **Spacing:** single space after commas in calls and definitions

## 🔖 Type hints

Add type hints when they add value — i.e., when the type is non-obvious or specific.

- **Omit `-> None`:** absence of return annotation already implies `None`
- **Avoid bare types:** `dict`, `list`, `tuple` without parameterization are not informative — use specific forms (`dict[str, Any]`, `list[str]`) or omit entirely

## 💬 Inline comments

Comments reduce cognitive load — err on the side of over-commenting rather than under-commenting.

- **Non-obvious logic:** anything a reader would need to pause to understand
- **Non-trivial conditionals:** explain the purpose, not just mechanics
- **Fallback behaviour:** constraints not apparent from code
- **Logical phases:** label distinct steps in functions longer than ~10 lines
- **`TODO` / `FIXME`:** always include brief explanation of what and why
  - **Placement:** always above the code they describe — never at end of line
  - **Accuracy:** keep comments accurate — stale comments are worse than none
  - **No restatement:** do not restate obvious code (e.g., `i += 1  # increment i`)

Also label groups of related module-level constants:

```python
# The four possible actions a planned change can resolve to
CREATE = "CREATE"
UPDATE = "UPDATE"
DISABLE = "DISABLE"
NOOP = "NOOP"
```

## 📌 General

- **File paths:** use `pathlib.Path` over `os.path`
- **Mutable defaults:** avoid — use `None` and assign inside function

## Related

- `[[python_environment]]` — Virtual environment setup, dependency management, and tooling
