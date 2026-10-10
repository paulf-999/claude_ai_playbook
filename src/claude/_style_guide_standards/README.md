# 🎨 Style guides

**Purpose:** Coding standards for the technologies the team uses — SQL, dbt, Airflow, Python, Bash, Terraform, Ansible, Docker, Makefiles, Mermaid and Jira — all in this one folder.

---

## 🚀 How they load

- **Entry files:** a guide such as `sql.md` has `paths:` frontmatter, so Claude Code loads it by itself whenever Claude reads a matching file.
- **Detail files:** the folder beside an entry file, such as `sql/`, holds its detail pages, which Claude reads on demand when the entry file points to them.
- **Standalone guides:** a guide with no `paths:`, such as `jira.md`, is read on demand through a pointer in another rule.

## 📦 Where they install

`make install` splits this folder, because Claude Code only loads `paths:` rules from `rules/`:

| File | Installs to |
|---|---|
| **Has `paths:` frontmatter** | `rules/04_path_scoped/style_guide_standards/` |
| **Everything else** | `_rules_lazy_load/style_guide_standards/` |

- **Why:** a detail file under `rules/` would load in every session, so only entry files go there.
- **Pointers:** `**Read on demand:**` pointers name the installed path, e.g. `~/.claude/_rules_lazy_load/style_guide_standards/sql/formatting.md`.

## ➕ Adding a guide

- **Entry file:** add `<topic>.md` here with `paths:` frontmatter naming the files it covers.
- **Detail files:** put them in `<topic>/` and link each one from the entry file.
