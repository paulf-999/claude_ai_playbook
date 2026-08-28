# 🎨 Mermaid Advanced Techniques

## 📋 Contents

- [🟦 Node shapes](#-node-shapes)
- [✏️ Node content format](#-node-content-format)
- [🎨 Styling](#-styling)
- [🗂️ Subgraphs](#-subgraphs)
- [📖 Reference example](#-reference-example)

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
