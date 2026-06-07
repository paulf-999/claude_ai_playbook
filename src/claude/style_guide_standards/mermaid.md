# 🔀 Mermaid Diagram Standards

[Mermaid](https://mermaid.js.org) is a Markdown-native diagramming language that renders flowcharts, sequence diagrams, and more directly in GitHub — no external tooling required. These standards apply to the flowcharts used in skill `flow.md` files and role READMEs.

---

## ✅ When to use

Add a diagram when **either** of these conditions is met:

- At least **two decision nodes** are present
- At least **one conditional stop path** exists — where the shape of execution would otherwise require hunting across multiple prose paragraphs

Do **not** add a diagram to a simple linear workflow — numbered phase headings are sufficient.

---

## 📍 Placement

| Context | Location | How to reference |
|---|---|---|
| Skills | `flow.md` child page, co-located with `SKILL.md` | `See [\`flow.md\`](flow.md) for the full decision flow.` |
| Role READMEs | Inline under `## Install sequence` or equivalent heading | — |

- Do not embed diagrams directly in `SKILL.md` — child pages preserve the 100-line limit.

---

## 📐 Diagram level

Keep diagrams at **phase/step level**:

- A reader should grasp the shape of the flow from the diagram
- Implementation detail belongs in the corresponding prose — not in the diagram

| ❌ Too detailed | ✅ Right level |
|---|---|
| `Check if file exists with os.path.exists()` | `2: Validate inputs` |
| `POST /repos/{owner}/{repo}/pulls/{number}/reviews` | `4: Post review` |

---

## ↕️ Direction

Always use top-down layout:

```
flowchart TD
```

---

## 🟦 Node shapes

| Shape | Syntax | Use for |
|---|---|---|
| Rectangle | `["..."]` | Standard action step |
| Diamond | `{"..."}` | Decision / branch |
| Hexagon | `{{text}}` | Milestone — key state reached |
| Rounded rect | `([text])` | Terminal — Start, Stop, Return |

---

## ✏️ Node content format

Action steps use a two-line structure:

```
["<b>N: Step name</b>

<i>detail line</i>"]
```

- **Bold title** — step number + name: `<b>1: Identify PR</b>`
  - Step numbers apply to **main-flow action steps only** — branch/conditional nodes, terminals, and decision nodes are not numbered
  - Branch/conditional rectangle nodes (off the main numbered sequence) use the same two-line format but omit the step number: `<b>Truncation warning</b>`
- **Blank line** — required between title and detail; affects rendering in some Mermaid versions
- **Italic detail** — optional, one line: `<i>description or cmd: command</i>`
  - Use **`cmd:` prefix** only when naming an actual CLI command (e.g. `cmd: gh api POST`)
  - Omit `cmd:` for prose descriptions

---

## 🎨 Styling

- Define `classDef milestone` on **every** diagram
- Add `classDef failure` **only** when failure terminal nodes are present — do not define it if unused

```
classDef milestone fill:#2e7d32,stroke:#1b5e20,color:#fff,font-size:18px
classDef failure fill:#c62828,stroke:#b71c1c,color:#fff

class M milestone      %% apply to milestone hexagon nodes
class FAIL failure     %% include only when failure terminals exist
```

---

## 🗂️ Subgraphs

Use subgraphs to group related steps within a phase or logical section:

- Apply when a phase contains **3+ steps** that benefit from visual grouping
- Do not use for single-step phases

```
subgraph INSTALL["Install"]
    direction TB
    A --> B --> C
end
```

---

## 📖 Reference example

`roles/application/ddp/airbyte/README.md` in `pyrc-cac-ans` — an illustrative example demonstrating:

- Subgraphs and milestone nodes
- Failure nodes and rescue branches
- Async task patterns

Treat as a reference, not a dependency.
