---
created: 2025-09-01
last_modified: 2026-08-19
---

# 📚 Reference Files Index

Quick-reference documentation on Claude config design, automation, and standards. These files are organizational knowledge, not code — they're consulted when learning about the system or making decisions.

---

## 📋 Quick Navigation

**Core Claude Config:**
- [`claude_prompting_best_practices.md`](claude_prompting_best_practices.md) — 5 high-impact prompting techniques: colleague test, positive framing, model-tuned exploration, never speculate about code, subagent discipline

**Architecture & Design:**
- [`claude_config_architecture/claude_config_architecture.md`](claude_config_architecture/claude_config_architecture.md) — System overview: design philosophy, import strategy, security model, testing approach
  - Child docs: [`claude_config_architecture/_security.md`](claude_config_architecture/_security.md), [`claude_config_architecture/_testing.md`](claude_config_architecture/_testing.md), [`claude_config_architecture/_evolution.md`](claude_config_architecture/_evolution.md) — specialized deep-dives

**Settings & Configuration:**
- [`settings_json_recommendations/settings_json_recommendations.md`](settings_json_recommendations/settings_json_recommendations.md) — Industry-standard `settings.json` options (Tier 1 essentials); ranked by impact and philosophy-fit
  - Child docs: [`settings_json_recommendations/_tier2_3.md`](settings_json_recommendations/_tier2_3.md), [`settings_json_recommendations/_enterprise.md`](settings_json_recommendations/_enterprise.md) — Tier 2–3 and enterprise options

**Standards (GitHub & Team):**
- [`standards/codeowners.md`](standards/codeowners.md) — Parent index for CODEOWNERS standards
  - [`standards/codeowners/fundamentals.md`](standards/codeowners/fundamentals.md) — When to use, file location, rule ordering, structure
  - [`standards/codeowners/patterns.md`](standards/codeowners/patterns.md) — Self-ownership rules, team handles, comment conventions
- [`standards/versioning_strategy.md`](standards/versioning_strategy.md) — Semantic versioning for skills and releases

**Lazy-Loaded Files (not baselined in core config):**
- **Automation commands** → `~/.claude/_rules/lazy_load/automation/automation_commands.md` — `/goal`, `/loop`, `/batch` reference (load when using automation)
- **Environment setup** → `~/.claude/_rules/lazy_load/environment_setup/ohmyzsh_setup.md` — Oh My Zsh provisioning (load when setting up new machine)
- **Engineering standards** → `~/.claude/_rules/lazy_load/standards/payroc_engineering_naming_standards.md` — Payroc naming (load when naming resources)

---

## 🎯 How to Use Reference Files

1. **Quick answers:** When you wonder "how do I...?" (e.g., "how do I version a skill?") → search this folder
2. **Decision support:** When you're about to create a new file/rule/hook → read the relevant standard
3. **Design context:** When learning the config architecture → start with `claude_config_architecture.md`

---

## 📊 Quality & Maintenance

All reference files are audited using a 7-dimension scoring rubric (Complexity, Clarity, Comprehensiveness, Currency/Relevance, Structure/Organization, Documentation, Standards Compliance). See [`~/.claude/_audits/SCORING_GUIDE.md`](~/.claude/_audits/SCORING_GUIDE.md) for methodology.

**Latest audit:** 2026-08-19 (see [`~/.claude/_audits/reference_files.md`](~/.claude/_audits/reference_files.md) for full results)

**File quality summary:**
- 6 reference files score 9.0+ (excellent; optimized 2026-08-19)
- All files follow style guide (emoji headers, bullet formatting, clarity)
- Files marked **lazy-loaded** below are not baselined; load on-demand
- All `.md` files include frontmatter with `created` and `last_modified` dates (see file_metadata rule)

---

## 🔄 Lazy-Loaded Reference Files

Files relocated to `~/.claude/_rules/lazy_load/` for baseline efficiency (infrequently used outside their domain):

- **`automation/automation_commands.md`** — `/goal`, `/loop`, `/batch` reference; load when using automation commands
- **`environment_setup/ohmyzsh_setup.md`** — One-time developer setup; load when provisioning a machine
- **`standards/payroc_engineering_naming_standards.md`** — Company naming; load when naming Payroc resources

**Baseline savings:** ~150 tokens/session (moved 2 files; previously in baseline)

These are not baselined in CLAUDE.md; load on-demand via ToolSearch or direct file read.

---

## 📐 File Organization

**Top-level reference files:** Architecture and settings
```
├── claude_config_architecture/                    (parent + children)
│   ├─ claude_config_architecture.md               (parent, 107 lines)
│   ├─ _security.md                                (child, ~100 lines)
│   ├─ _testing.md                                 (child, ~80 lines)
│   └─ _evolution.md                               (child, ~70 lines)
└── settings_json_recommendations/                 (parent + children)
    ├─ settings_json_recommendations.md            (parent, 107 lines)
    ├─ _tier2_3.md                                 (child, ~85 lines)
    └─ _enterprise.md                              (child, ~65 lines)
```

**Standards subdirectory:** GitHub, team, and engineering standards
```
standards/
├── codeowners.md                          (17 lines, parent index)
│   └─ codeowners/
│       ├─ fundamentals.md                 (73 lines)
│       └─ patterns.md                     (73 lines)
└── versioning_strategy.md                 (57 lines)
```

**Lazy-load reference files:** Domain-specific, infrequently-used standards (loaded on-demand)
```
~/.claude/_rules/lazy_load/
├── automation/
│   ├─ README.md                           (13 lines)
│   └─ automation_commands.md              (87 lines) — moved from _reference/
├── environment_setup/
│   ├─ README.md                           (13 lines)
│   └─ ohmyzsh_setup.md                    (71 lines) — moved from _reference/
└── standards/
    └─ payroc_engineering_naming_standards.md (177 lines)
```

**Child files (underscore prefix):** Detailed deep-dives on parent topics; referenced from parent docs.

---

## ✅ Standards Compliance

All reference files follow `~/.claude/_rules/writing_style.md`:

- ✅ Emoji headers on all `##` sections
- ✅ Bold **keyword:** opening on bullets
- ✅ <110 lines per file (parent docs); children organized with `_` prefix
- ✅ Trailing newlines
- ✅ Clarity: 60-second comprehension test on opening paragraph

---

## 🔗 Related Files

- **Scoring methodology:** [`SCORING_GUIDE.md`](SCORING_GUIDE.md) — 7-dimension rubric for skills and reference files
- **Audit results:** [`AUDIT_SCORECARD.md`](AUDIT_SCORECARD.md) — All 9 files scored with dimension breakdown and refactor recommendations
- **Global config:** `~/.claude/CLAUDE.md` — Entry point for core Claude config rules
- **Writing style:** `~/.claude/_rules/writing_style.md` — Standards for all written content

---

## 📝 Maintenance Schedule

| Frequency | Task |
|---|---|
| **Monthly** | Spot-check 1–2 files for currency (especially external mirrors) |
| **Quarterly** | Review lazy-load usage; consider promoting back if frequently loaded |
| **Annually** | Full audit (see `AUDIT_SCORECARD.md`) |

---

## 🎯 Next Steps

1. **For improvements:** See `AUDIT_SCORECARD.md` Phase 1–3 (refactoring, lazy-load promotion, documentation updates)
2. **For new standards:** Create as `standards/<standard_name>.md`, audit against `SCORING_GUIDE.md`, add to this index
3. **For updates:** Update `AUDIT_SCORECARD.md` annually; keep scores fresh

---

Last updated: **2026-08-19**
