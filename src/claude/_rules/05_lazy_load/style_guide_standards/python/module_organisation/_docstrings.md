# 📝 Module Docstrings & Metadata

**Purpose:** Establish module docstring format and metadata conventions for self-documenting modules.

---

## 📝 Module docstrings

Every module must have a docstring at the top describing its purpose. Place it before imports and `__author__`/`__version__` metadata.

### Format

**Module docstrings must follow progressive disclosure** (see `writing_style.md` § Progressive disclosure):
- **Opening line:** One-sentence summary of module purpose
- **Details:** Reserve for README, separate docs, or code comments — NOT the module docstring

```python
"""
[One-sentence purpose — this is sufficient]
"""
```

**Only add sections if absolutely necessary for critical context:**

```python
"""
[One-sentence purpose]

[Optional: 1-2 sentences of critical context OR reference external docs]
"""
```

**Never include** in module docstrings:
- ❌ Usage examples or instructions (belongs in README.md)
- ❌ Requirements or setup steps (belongs in README.md)
- ❌ Detailed workflow steps (document this in code comments or external docs)
- ❌ Dates (belongs in git history, not code)
- ❌ Author info (use `__author__` metadata instead)

### ✅ Good examples

**Correct — brief, discoverable:**

```python
#!/usr/bin/env python3
"""YAML config loader with ${ENV_VAR} interpolation."""

__author__ = "Paul Fry"
__version__ = "0.1"

import yaml
```

**Correct — brief with critical context:**

```python
#!/usr/bin/env python3
"""Migrates connections from source to target Airbyte server.

See README.md for usage and requirements.
"""

__author__ = "Paul Fry"
__version__ = "0.1"
```

---

### ❌ WRONG — Too verbose (violates progressive disclosure)

**Verbose with Requirements, Usage, Workflow:**

```python
#!/usr/bin/env python3
"""
Description: Airbyte connection migrator — migrates connections from source to target server
             based on migration plan CSV.
Date created: 2026-07-03

Workflow:
    1. Load migration plan from CSV (which connections to migrate, which target server)
    2. Load connection inventory from YAML (extracted from source server)
    3. For each connection in plan: migrate or skip based on target server + status

Input files:
    - plan_path: CSV with columns (source_name, target_server, ...)
    - inventory_path: YAML with connections extracted from source Airbyte server

Output:
    - Creates connections on target server (if --apply flag set)
    - Writes migration_log.yaml with audit trail of what was created

Requirements:
    Environment variables must be set in .env
    See README.md for setup instructions
"""
```

**Problem:** This violates `writing_style.md` § Progressive disclosure. Module docstrings should be brief and discoverable via `help(module)` or IDE tooltips. Workflow, requirements, and usage belong in **README.md or separate documentation**, not in the module docstring.

### ✅ Recommended sections

- **Description:** [Required] One-line purpose, or brief multi-line explanation
- **Date created:** [Recommended] When the module was created (helps with understanding scope and maturity)
- **Workflow:** [Optional] Step-by-step process if the module orchestrates complex logic
- **Input/Output:** [Optional] What files or data structures the module expects/produces
- **Requirements:** [Optional] Environment variables, external services, or configuration needed

### ❌ What NOT to include

```python
# ❌ WRONG — too generic
"""Config loader module"""

# ❌ WRONG — implementation detail, not purpose
"""This module loads YAML files and parses them"""

# ❌ WRONG — author info in docstring (use __author__ below)
"""
Author: Paul Fry
Purpose: Load config
"""
```

---

## 🏷️ Module metadata

After the docstring and before imports, declare module-level metadata.

### ✅ Standard metadata

```python
"""
Description: YAML config loader with ${ENV_VAR} interpolation
Date created: 2026-06-26
"""

__author__ = "Paul Fry"
__version__ = "0.1"

import os
import yaml
```

### Metadata fields

- **`__author__`:** Who wrote/maintains this module (for questions, maintenance)
- **`__version__`:** Version number of this module (helpful for tracking API changes)

### ❌ What NOT to include

```python
# ❌ WRONG — belongs in docstring, not metadata
__description__ = "Loads YAML config files"

# ❌ WRONG — belongs in git history, not code
__history__ = "Added in PR #42"

# ❌ WRONG — too granular; commit message has this
__last_modified__ = "2026-08-20"
```

---

## 📐 Function Ordering

**Order functions by call hierarchy, not definition order:**

```python
# ❌ WRONG — helpers defined before main entry point
def _setup_parser():
    ...

def _dispatch_command(args):
    ...

def main(args=None):
    parser = _setup_parser()
    parsed_args = parser.parse_args(args)
    _dispatch_command(parsed_args)

# ✅ RIGHT — entry point first, then functions it calls
def main(args=None):
    parser = _setup_parser()
    parsed_args = parser.parse_args(args)
    _dispatch_command(parsed_args)

def _setup_parser():
    ...

def _dispatch_command(args):
    ...
```

**Why:** Reading the file top-to-bottom tells the story of what the code does. Entry point (main) → supporting functions. Aids maintainability and understanding.

---

## 🔗 Related

- Parent: `module_organisation.md` — Module organisation overview
- Sibling: `module_organisation/_public_private.md` — Public vs private functions and constants
