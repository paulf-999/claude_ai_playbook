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
```

**Accuracy rules:**
- **Only document what the function directly does:** Do not document `:return:` or `:rtype:` for functions that return `None` (omit these fields entirely).
- **Only document exceptions the function directly raises:** Do not list exceptions that might bubble up from called functions unless the function explicitly re-raises or wraps them.
- **Keep docstrings minimal and accurate:** Stale docstrings are worse than none—if you document something, keep it current as the function evolves.

**Module docstrings:** See `module_organisation/_docstrings.md` for format and guidelines.

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
- **Logical phases** — label each distinct step in a sequence (e.g., "parse args", "initialize", "execute"). Even short functions benefit from phase labels.
- **`TODO` / `FIXME`** — always include a brief explanation of what and why.
- **Imported class instantiation** — when a class is imported from another file and instantiated, mention the source file for clarity (e.g., `# (from airbyte_manager.helpers.api.airbyte_client)`).

Also label groups of related module-level constants with a one-line comment stating what the group represents:

```python
# The four possible actions a planned change can resolve to
CREATE = "CREATE"
UPDATE = "UPDATE"
DISABLE = "DISABLE"
NOOP = "NOOP"
```

- **Placement:** always place comments on the line above the code they describe — never at end of line.
- **Spacing:** add a blank line before a comment block that marks a new logical phase or major step — aids readability by visually separating phases.
  ```python
  # ❌ WRONG — phases run together
  parsed_args = parse_args(args)
  # Initialize client
  client = AirbyteClient()

  # ✅ RIGHT — blank line separates phases
  parsed_args = parse_args(args)

  # Initialize client
  client = AirbyteClient()
  ```
- **Accuracy:** keep comments accurate — stale comments are worse than none.
- **No restatement:** do not restate what the code does: `i += 1  # increment i` is not a comment.

### ✅ Example: Imported class instantiation with source reference

```python
# Initialize API client (from airbyte_manager.helpers.api.airbyte_client)
client = AirbyteClient.from_server(parsed_args.server)

# Extract connections from source server (from airbyte_manager.helpers.connections.connection_extractor)
entries, summary_entries = ConnectionExtractor(client).extract(tag_name)

# Generate reconciliation plan (from airbyte_manager.helpers.connections.connection_reconciler)
reconciler = ConnectionReconciler(client, config)
```

**Why:** Readers can quickly find the class definition without searching through imports or module structure.

## 📌 General

- Use `pathlib.Path` over `os.path` for file operations.
- Avoid mutable default arguments — use `None` and assign inside the function.
