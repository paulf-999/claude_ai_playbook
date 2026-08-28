---
created: 2025-10-01
last_modified: 2026-08-19
---

# ⚙️ Claude Code — `settings.json` industry recommendations

Reference for essential `settings.json` configuration, ranked by impact and filtered through intentionality principles (context-efficiency · evidence-gated). Covers Tier 1 (essential) settings with recommendations.

> ⚠️ **The schema is version-dependent.** Confirm any key against the official docs: <https://code.claude.com/docs/en/settings>

**Quick Start:** Set `permissions.allow` (22 patterns already listed) + `permissions.deny` (secrets + destructive ops) + `model` (Haiku) → done. See Tier 1 section below.

---

## 📖 How to read this

### Confidence legend

- ✅ **Verified** — present in official docs or proven working in live `settings.json`.
- 🟡 **Community-claimed** — surfaced in blogs/repos but not found in current official docs; treat as unconfirmed.
- ❌ **Likely fabricated / renamed** — docs use a different key, or it doesn't exist.

### Philosophy-fit legend

- **Have** — already in the live config.
- **Adopt** — passes the intentionality bar; worth adding.
- **Consider** — evidence-gated; adopt only with a concrete, recurring use case.
- **Skip** — real key, but no recurring problem here.
- **Reject** — actively conflicts with a prior decision or principle.

### Industry-impact tiers

- **Tier 1 (essential):** ~70 %+ adoption; most serious configs set it.
- **Tier 2 (common):** ~30–60 % adoption; frequently set for cost/hygiene.
- **Tier 3 (niche):** ~10–30 % adoption; situational; minority adopt.
- **Tier 4 (rare/enterprise):** <10 % adoption; managed-policy or specialist only.

---

## 🔐 Tier 1 essentials

| Setting | Purpose | Confidence | Status | Next step |
|---|---|---|---|---|
| `permissions.allow` | Unblock tools | ✅ | Have | Audit quarterly; add patterns as needed |
| `permissions.deny` | Block secrets + destructive ops | ✅ | **Adopt** | Add blocklist (see below) |
| `permissions.defaultMode` | Start in plan mode | ✅ | Have | Keep as-is |
| `model` | Default: Haiku | ✅ | Have | Confirm in settings.json |
| `autoMemoryEnabled` | Track personal context | ✅ | Have | Confirm `true` |

### Tier 1 common edge cases

**`permissions.allow` edge case:** Adding a pattern that's too broad.
- ❌ `Bash(git:*)` — permits dangerous `git push --force`, `git reset --hard`
- ✅ `Bash(git status:*)`, `Bash(git log:*)`, `Bash(git diff:*)` — read-only, safe

**`permissions.deny` edge case:** Blocking a tool you genuinely need.
- ✅ If needed for a task, remove temporarily from `deny` list, complete task, re-add
- ❌ Never remove deny rules permanently without understanding why they were added

---

## 🎯 Adoption recommendations

### ✅ Adopt — `permissions.deny`

Secrets + destructive-op firewall. Add to `settings.json`:

```jsonc
"permissions.deny": [
  "Read(./.env)", "Read(./.env.*)",
  "Read(~/.ssh/**)", "Read(~/.aws/**)",
  "Bash(rm -rf:*)", "Bash(sudo:*)"
]
```

**Why:** Zero context cost; backs `security.md` rules. **Verify** patterns at <https://code.claude.com/docs/en/settings> before deploying.

### 🟡 Consider — Tier 2–3 and Enterprise

See **[settings_json_recommendations/_tier2_3.md](settings_json_recommendations/_tier2_3.md)** and **[settings_json_recommendations/_enterprise.md](settings_json_recommendations/_enterprise.md)**.

---

## 📚 Sources

**Official (✅ basis):**

- Claude Code settings reference — <https://code.claude.com/docs/en/settings> — schema of record.
- Claude Code hooks reference — <https://code.claude.com/docs/en/hooks>
- Claude Code IAM / permissions — <https://code.claude.com/docs/en/iam>

**Community (🟡 basis — treat as unconfirmed):**

- Trail of Bits Claude Code hardened-config write-ups
- `awesome-claude-code` GitHub collections
- Marco Lancini — "My 2026 Claude Code setup"
- Security blog posts on permission firewalls

---

## 🔗 Related docs

- **Parent:** This doc
- **Tier 2–3 settings:** [settings_json_recommendations/_tier2_3.md](settings_json_recommendations/_tier2_3.md)
- **Enterprise settings:** [settings_json_recommendations/_enterprise.md](settings_json_recommendations/_enterprise.md)
- **Security rules:** `~/.claude/_rules/security.md`
