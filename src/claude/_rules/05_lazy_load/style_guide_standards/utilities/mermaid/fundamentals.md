# 🔀 Mermaid Fundamentals

[Mermaid](https://mermaid.js.org) is a Markdown-native diagramming language that renders flowcharts, sequence diagrams, and more directly in GitHub — no external tooling required.

## 📋 Contents

- [✅ When to use](#-when-to-use)
- [📍 Placement](#-placement)
- [📐 Diagram level](#-diagram-level)
- [↕️ Direction](#-direction)

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
