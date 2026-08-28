# 🏷️ Makefile Naming Conventions

## 📋 Contents

- [Targets](#-targets)
- [Variables](#-variables)

---

## Targets

Target names must use lowercase letters. Words are separated with an underscore (`_`):

```makefile
test_debug:
    $(build_dir)/debug/bin
```

---

## Variables

Variables that are not special to Make or inherited from the environment must be in lowercase, with words separated by underscores:

```makefile
src_dir := $(current_dir)/src
build_dir := $(current_dir)/build
```
