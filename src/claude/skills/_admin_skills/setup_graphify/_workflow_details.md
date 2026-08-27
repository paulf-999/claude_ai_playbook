# 🛠️ Workflow Details — Five Setup Phases

---

## Phase 1 — Install graphify CLI

```bash
pip install graphifyy
graphify install --platform claude
```

The `graphify install --platform claude` command installs the `/graphify` query skill into `~/.claude/skills/`.

---

## Phase 2 — Extract the knowledge graph

Run from the **project root** to generate `graphify-out/graph.json` at the correct level:

```bash
cd <repo-root>
graphify extract <target-dir>
```

**Cost note:** Graphify uses semantic extraction (LLM) for non-code files. First run may cost ~$0.05–$0.10 depending on codebase size. Subsequent runs are incremental — only changed files are re-processed.

---

## Phase 3 — Add to .gitignore

The `graphify-out/` directory is generated output — never commit:

```bash
printf '\n# Graphify — generated knowledge graph output (do not commit)\ngraphify-out/\n' >> .gitignore
```

---

## Phase 4 — Update the repo CLAUDE.md

Add a Graphify section to your repo's `CLAUDE.md` pointing to the graph path. Example:

```markdown
## Graphify

The knowledge graph is at: `graphify-out/graph.json`

Use the `/graphify` skill to query it — ask structural questions and the skill will query the graph directly.
```

---

## Verification

After setup:
1. Open a Claude session in the repo directory
2. Ask a structural question (e.g., "What calls function X?")
3. The `/graphify` skill should answer from the graph without reading individual files
