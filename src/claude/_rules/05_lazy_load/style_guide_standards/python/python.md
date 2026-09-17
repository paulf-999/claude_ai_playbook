# 🐍 Python — coding standards

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

---
## 🗂️ Code layout

- 4 spaces for indentation — no tabs.
- Two blank lines between top-level functions and classes.
- One blank line between methods within a class.
- Space logically within functions to maintain readability.

## 🏷️ Naming conventions

| Construct | Convention |
|---|---|
| Modules and packages | `snake_case` |
| Functions and methods | `snake_case` |
| Variables | `snake_case` |
| Classes | `PascalCase` |
| Constants | `SCREAMING_SNAKE_CASE` |

- **Meaningful names:** avoid abbreviations; no single-letter variables outside loop counters.
- **No history in code:** do not capture change history in names — that belongs in git.

## 📥 Imports

- One module per import line.
- Use absolute imports; no wildcard imports (`from module import *`).
- Group in order, separated by blank lines: standard library → third-party → local.

## 💬 String formatting

Use f-strings. Do not use `str.format()` or `%` formatting.

## ⚠️ Error handling

- Catch specific exceptions — never bare `except:` or `except Exception:`.
- Use `try-except-else` where appropriate; `finally` only for cleanup.

## 📝 Docstrings

All functions, classes, and modules must have docstrings. Use reST format:

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

## 🔧 Functions and methods

- Default arguments go at the end of the argument list.
- No spaces around `=` in keyword arguments: `func(name="foo")`.
- Single space after commas in function calls and definitions.

## 🔖 Type hints

Add type hints when they add value — i.e., when the type is non-obvious or specific.

```python
def get_secret_by_name(secret_name: str) -> str:
```

- **Omit `-> None`:** the absence of a return annotation already implies `None`.
- **Avoid bare container types:** `dict`, `list`, `tuple` without parameterization are not informative — either use a specific form (`dict[str, Any]`, `list[str]`) or omit the hint entirely.

## 💬 Inline comments

**When in doubt, add a comment.** Err on the side of over-commenting rather than under-commenting.

Add a comment for:
- **Non-obvious logic** — anything a reader would need to pause to understand.
- **Non-trivial conditionals** — explain the purpose of the condition, not just its mechanics.
- **Fallback behaviour and constraints** not apparent from the code itself.
- **Logical phases** within a function longer than ~10 lines — label each distinct step.
- **`TODO` / `FIXME`** — always include a brief explanation of what and why.

Also label groups of related module-level constants with a one-line comment stating what the group represents:

```python
# The four possible actions a planned change can resolve to
CREATE = "CREATE"
UPDATE = "UPDATE"
DISABLE = "DISABLE"
NOOP = "NOOP"
```

- **Placement:** always place comments on the line above the code they describe — never at end of line.
- **Accuracy:** keep comments accurate — stale comments are worse than none.
- **No restatement:** do not restate what the code does: `i += 1  # increment i` is not a comment.

## 📌 General

- Use `pathlib.Path` over `os.path` for file operations.
- Avoid mutable default arguments — use `None` and assign inside the function.
