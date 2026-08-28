---
created: 2025-10-01
last_modified: 2026-08-19
---

# ⚙️ Tier 4 Settings — Enterprise & Managed (Out of Scope)

Reference for Tier 4 (rare/enterprise) `settings.json` options. These are included for completeness but are **out of scope** for single-user, local development setups.

---

## 🏢 Enterprise / managed settings

| Setting | What it does | Industry impact | Confidence | Philosophy fit | Verdict |
|---|---|---|---|---|---|
| `forceLoginOrgUUID` | Pin login to an org UUID (managed environment) | Tier 4 | ✅ | **Skip** | Managed-policy; single-user setup. (`forceLoginMethod` as named in some guides is ❌ not a current key.) |
| `sandbox.*` | OS-level sandbox / credential masking | Tier 4 | ✅ | **Skip** | Specialist isolation; not needed for local single-user work. |
| `attribution.commit` / `attribution.pr` | Git commit/PR attribution strings | Tier 4 | ✅ | **Skip** | `git.md` already governs commit/PR conventions; no need for additional field mapping. |
| `apiKeyHelper` | Custom command to mint auth values | Tier 4 | ✅ | **Skip** | For programmatic/enterprise auth scenarios; not applicable to local development. |
| `allowManagedPermissionRulesOnly` / `allowManagedHooksOnly` | Lock down to managed policy | Tier 4 | ✅ | **Skip** | Managed-fleet controls; single-user setup has no fleet to manage. |

---

## When these apply

These settings are relevant only in:

- **Managed environments:** Organizations centrally controlling Claude Code config across teams
- **Compliance scenarios:** Orgs requiring audit trails, credential masking, or login enforcement
- **Large teams:** Multi-user setups with shared infrastructure
- **Enterprise deployments:** Custom auth, sandboxing, or attribution requirements

**For single-user, local development:** None of these are needed. Use Tier 1 essentials instead.

---

## If you need enterprise settings

If your use case falls into the categories above:

1. **Check the official docs:** <https://code.claude.com/docs/en/settings> — enterprise keys may have changed
2. **Consult your IT team or Claude Code admin** — they should provide the policy configuration
3. **Test in a non-prod environment first** — managed settings can lock down the harness in surprising ways

---

## 🔗 Related docs

- **Parent (Tier 1 essentials):** `settings_json_recommendations.md`
- **Tier 2–3 settings:** `_tier2_3.md`
- **Official schema:** <https://code.claude.com/docs/en/settings>
