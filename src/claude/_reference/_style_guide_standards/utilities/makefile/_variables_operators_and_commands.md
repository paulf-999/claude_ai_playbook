<!-- version: 1.1.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-29 -->
# ⚙️ Makefile Variables, Operators & Commands

**Purpose:** Set how Makefiles define `SHELL`, print output, assign variables and silence commands.

## 📋 Contents

- [🐚 `SHELL` variable](#-shell-variable)
- [💬 Displaying text](#-displaying-text)
- [🧮 `:=` simply expanded operator](#--simply-expanded-operator)
- [🔇 Command silencing (`@`)](#-command-silencing-)
- [🎯 `$@` automatic variable](#--automatic-variable)

---

## 🐚 `SHELL` variable

- **Rule:** every Makefile must set `SHELL` explicitly, so it never inherits an unexpected shell from the environment.
- **Value:** any explicit shell is fine, such as `/bin/sh` for portable recipes or `/bin/bash` when recipes use bash features.

```makefile
SHELL := /bin/sh
```

---

## 💬 Displaying text

- **Rule:** print messages with GNU Make's built-in functions, which report through Make itself rather than a shell.
- **Timing:** `$(info)` inside a recipe prints when Make expands the recipe, before any of its shell lines run.
- **When to use `@echo`:** use it instead when the message must appear in order between shell lines, such as a progress line.

```makefile
$(error   text…)   # fatal — halts execution
$(warning text…)   # non-fatal warning
$(info    text…)   # informational
```

---

## 🧮 `:=` simply expanded operator

- **Rule:** assign variables with `:=` (simply expanded), not `=` (recursively expanded).
- **Why:** `:=` evaluates once, so a variable can't change later because something it refers to changed.

```makefile
# use
build_dir := $(current_dir)/build

# not
build_dir = $(current_dir)/build
```

- **Reference:** [makefiletutorial.com — Flavors and Modification](https://makefiletutorial.com#flavors-and-modification)

---

## 🔇 Command silencing (`@`)

- **Rule:** prefix a command with `@` to stop Make printing the command itself before running it.

```makefile
install:
	$(info Installing dependencies...)
	@pip install -r requirements.txt
```

---

## 🎯 `$@` automatic variable

- **Rule:** use `$@`, which expands to the current target's name, instead of repeating the name in the recipe.

```makefile
build:
	mkdir -p $@
```
