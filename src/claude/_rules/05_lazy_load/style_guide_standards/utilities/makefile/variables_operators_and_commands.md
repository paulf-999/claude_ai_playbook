# ⚙️ Makefile Variables, Operators & Commands

## 📋 Contents

- [`SHELL` variable](#-shell-variable)
- [Displaying text](#-displaying-text)
- [`:=` simply expanded operator](#-simply-expanded-operator)
- [Command silencing (`@`)](#-command-silencing)
- [`$@` automatic variable](#-automatic-variable)

---

## `SHELL` variable

Every Makefile must define the `SHELL` variable to avoid inheriting an unexpected shell from the environment:

```makefile
SHELL = /bin/sh
```

---

## Displaying text

Use the GNU Make built-ins for output — do not use `echo`:

```makefile
$(error   text…)   # fatal — halts execution
$(warning text…)   # non-fatal warning
$(info    text…)   # informational
```

---

## `:=` simply expanded operator

When assigning variables, prefer the `:=` (simply expanded) operator over `=` (recursively expanded). This avoids unexpected behaviour from deferred evaluation:

```makefile
build_dir := $(current_dir)/build   # preferred
build_dir = $(current_dir)/build    # avoid
```

See: [makefiletutorial.com — Flavors and Modification](https://makefiletutorial.com#flavors-and-modification)

---

## Command silencing (`@`)

Prefix a command with `@` to suppress it from being echoed to the terminal:

```makefile
install:
    @echo "Installing dependencies..."
    @pip install -r requirements.txt
```

---

## `$@` automatic variable

`$@` expands to the name of the current target — use it to avoid repeating the target name:

```makefile
build:
    mkdir -p $@
```
