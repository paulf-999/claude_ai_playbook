# 🔌 Plugins

Plugin support files — patch scripts and reference documents applied to Claude Code plugins after installation.

These files live here rather than under `skills/` to avoid being mis-scanned and installed as skills during `make install`.

---

## 📁 Files

| File | Purpose |
|------|---------|
| `skill-creator-patch.py` | Patches the `skill-creator` plugin after installation. Run via `make patch_plugins` (after `make install_plugins`). Adds the maturity tier question, injects Tier 1 tag stamping and scope gate instructions, and copies `claude-tag-schema.md` into the plugin's `references/` directory. Idempotent — safe to re-run. |
| `claude-tag-schema.md` | YAML frontmatter tag schema for all Claude components (skills, rules, process docs). Defines Tier 1 mandatory tags (`maturity`, `criticality`, `status`, `tested`) and optional Tier 2 tags (`domain`, `owner`, `depends-on`, `last-reviewed`). Used by the merge lint check, component audit, and quality report. |

---

## 🚀 Usage

```bash
make install_plugins   # Install Claude Code plugins
make patch_plugins     # Apply team patches (run after install_plugins)
```
