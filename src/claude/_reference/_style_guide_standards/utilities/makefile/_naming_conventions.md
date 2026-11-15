<!-- version: 1.1.0 -->
<!-- created: 2026-08-28 -->
<!-- updated: 2026-10-29 -->
# 🏷️ Makefile Naming Conventions

**Purpose:** Set how Makefile targets and variables are named.

## 🎯 Targets

- **Rule:** target names must be lowercase, with words separated by underscores.

```makefile
test_debug:
	$(build_dir)/debug/bin
```

---

## 📦 Variables

- **Rule:** variables you define must be lowercase, with words separated by underscores.
- **Exceptions:** variables special to Make (such as `SHELL`) or inherited from the environment keep their own case.

```makefile
src_dir := $(current_dir)/src
build_dir := $(current_dir)/build
```
