# Phase 3: Output Format & Recommendations

## 💡 Recommendations table

Produce a recommendations table using Must / Should / Could / Want severity, with one bullet per finding. Format:

```
| # | Theme | Severity | Recommendation |
|:---|:---|:---|:---|
| 1 | **🔀 Config complexity** | **Should** | • <finding> |
```

Omit the table entirely if there is nothing to recommend.

---

## 📋 Output format

Produce output in this order:

1. **Summary** — 2 bullets: overall signal, and the single most important gap
2. **Overall verdict** — `X.X/10 — Grade`
3. **Recommendations table** — severity-ordered (Must first), omit if empty
4. **Scorecard table** — one row per theme
5. **MoSCoW table** — artefact × Must/Should/Could/Want, with present/absent/partial status

Write the full output to `~/_drafts/general/$(date +%Y-%m-%d)_claude_config_review.md` using a `bash` call, then print the content to the user.
