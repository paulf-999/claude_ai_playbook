<!-- version: 1.0.0 -->
<!-- created: 2026-10-11 -->
<!-- updated: 2026-10-11 -->
<!-- miss_cost: low — slower recovery from a runaway run the always-on controls already stop -->
<!-- loading: lazy — only needed when a /loop, /goal or /batch run goes wrong or is being chosen -->
# 🩺 Automation Troubleshooting

**Purpose:** Recover from a misbehaving `/loop`, `/goal` or `/batch` run, pick the right one and check it before starting — the caps and kill-switch themselves load every session in `_automation_controls.md`.

---

## 📊 Common Failure Scenarios & Recovery

### `/loop` runaway

**Symptom:** Loop fires every 5m for 2+ hours, accumulating tokens

**Recovery:**
1. Stop immediately: `TaskStop`
2. Extend interval: was 5m → try 15m
3. Clarify condition: is the endpoint responding? Is the logic sound?
4. Restart: approve new interval explicitly

### `/goal` never converges

**Symptom:** 20+ turns, condition never met, tokens wasted

**Recovery:**
1. Check transcript: is the agent actually making progress?
2. Verify condition: is it achievable? Is it measurable?
3. Fallback to `/loop`: if the goal is unbounded, use `/loop` instead with a timeout
4. Narrow scope: smaller changes converge faster

### `/batch` conflicts

**Symptom:** Subagents clash on shared files, PRs conflict

**Recovery:**
1. Stop batch: kill remaining agents
2. Split items: ensure each PR touches disjoint files
3. Sequence manually: do 3 items in sequence instead of 12 parallel
4. Review PR merging order: must merge in dependency order

---

## 🎯 Decision Tree: Which Automation?

```
Need something done repeatedly on a schedule?
├─ YES → Use /loop (e.g., "check deploy every 5m")
│
Need something done once, but iteratively until a condition?
├─ YES → Use /goal (e.g., "implement until tests pass")
│
Need to do the same change 10+ times in parallel?
├─ YES → Use /batch (e.g., "migrate 12 microservices")
│
Otherwise → Manual invocation (faster, clearer)
```

---

## ✅ Verification Checklist

Before invoking any automation feature:

- [ ] Condition/goal/interval is explicit and measurable
- [ ] Success criteria are defined upfront
- [ ] Kill-switch procedure is clear
- [ ] Side effects are understood and acceptable
- [ ] Token budget is estimated and acceptable
- [ ] Manual alternative was considered and rejected
