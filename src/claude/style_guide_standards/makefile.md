# 🛠️ Makefile Style Guide & Standards

Defines the team's standards for writing and structuring Makefiles.

---

## 🏷️ Naming conventions

### Targets

Target names must use lowercase letters. Words are separated with an underscore (`_`):

```makefile
test_debug:
    $(build_dir)/debug/bin
```

### Variables

Variables that are not special to Make or inherited from the environment must be in lowercase, with words separated by underscores:

```makefile
src_dir := $(current_dir)/src
build_dir := $(current_dir)/build
```

---

## ⚙️ Misc

### `SHELL` variable

Every Makefile must define the `SHELL` variable to avoid inheriting an unexpected shell from the environment:

```makefile
SHELL = /bin/sh
```

### Displaying text

Use the GNU Make built-ins for output — do not use `echo`:

```makefile
$(error   text…)   # fatal — halts execution
$(warning text…)   # non-fatal warning
$(info    text…)   # informational
```

### `:=` simply expanded operator

When assigning variables, prefer the `:=` (simply expanded) operator over `=` (recursively expanded). This avoids unexpected behaviour from deferred evaluation:

```makefile
build_dir := $(current_dir)/build   # preferred
build_dir = $(current_dir)/build    # avoid
```

See: [makefiletutorial.com — Flavors and Modification](https://makefiletutorial.com#flavors-and-modification)

### Command silencing (`@`)

Prefix a command with `@` to suppress it from being echoed to the terminal:

```makefile
install:
    @echo "Installing dependencies..."
    @pip install -r requirements.txt
```

### `$@` automatic variable

`$@` expands to the name of the current target — use it to avoid repeating the target name:

```makefile
build:
    mkdir -p $@
```

---

## 📄 Makefile template

Use `src/templates/makefile_template.mk` as the starting point for any new Makefile.

---

## 🔗 Credits

- [Makefile style guide](https://style-guides.readthedocs.io/en/latest/makefile.html)
- [General Conventions for Makefiles — GNU](https://www.gnu.org/prep/standards/html_node/Makefile-Basics.html#Makefile-Basics)
- [Naming conventions — Stack Overflow](https://stackoverflow.com/questions/32130664/is-there-a-naming-convention-for-makefile-targets-and-variables)
