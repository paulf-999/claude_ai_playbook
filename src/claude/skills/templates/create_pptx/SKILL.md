---
name: create_pptx
description: Interactively gather deck requirements, propose a slide structure, and produce a .pptx file using python-pptx.
---

Select your agent persona based on the deck type identified in Phase 1:

| Deck type | Persona | Rationale |
|-----------|---------|-----------|
| Executive update, stakeholder comms, retrospective, roadmap | **Project manager** | Outcome-first, business language, narrative arc |
| Technical proposal, training/educational, data insights | **Technical writer** | Structured, evidence-based, precise language |

Adapt your style to the deck type:

| Deck type | Style | Max slides |
|-----------|-------|------------|
| Executive / stakeholder update | Concise, outcome-first, data-driven — one message per slide | 10 |
| Technical proposal | Tradeoff-aware, architecture-focused, detailed | 15 |
| Training / educational | Section-based, step-by-step, includes examples | 20 |
| Retrospective | Narrative arc: context → events → learnings → next actions | 12 |
| Data insights / report | Finding-led, chart placeholders, evidence before conclusion | 15 |
| Strategy / roadmap | Vision → now → next → later, milestone-oriented | 12 |

---

## 🔍 Phase 1 — Gather context

Ask the following questions together in a single message:

1. What type of deck is this? (Executive update, technical proposal, training/educational, retrospective, data insights, strategy/roadmap, or describe your own.)
2. Who is the audience? (e.g. exec leadership, engineering team, external client)
3. What are the 2–3 key messages you want the audience to walk away with?
4. What content, data, or context should the deck include?
5. Any constraints? (e.g. maximum number of slides, presentation time limit)
6. What file name and directory path should the `.pptx` be saved to?

Wait for the user's response before proceeding.

---

## 📐 Phase 2 — Propose slide structure

Based on the deck type and context, propose a slide-by-slide outline:

- List each slide as: `Slide N — <title>: <one sentence describing the message it lands>`
- Apply the style and slide ceiling for the identified deck type
- Group slides into labelled sections where the deck warrants it (e.g. **Problem**, **Solution**, **Next Steps**)
- Always include a title slide (Slide 1) and a closing slide (summary, next steps, or call to action)

Present the outline and ask the user to confirm or adjust before generating the file.

Wait for the user's response before proceeding.

---

## 💻 Phase 3 — Generate the .pptx file

Write a Python script using `python-pptx` to produce the deck. Apply these conventions throughout:

**Format**
- Widescreen 16:9: `prs.slide_width = Inches(13.33)`, `prs.slide_height = Inches(7.5)`
- Slide 1: title slide layout (index `0`) — title and subtitle (author / date)
- All other slides: title + content layout (index `1`)

**Content**
- Bullet text: max 8 words per bullet, max 5 bullets per slide
- Each slide's headline (title) must state the conclusion, not just the topic — e.g. "Costs reduced by 30%" not "Cost analysis"
- Include a `# --- Slide N: <title> ---` comment above each slide block

**Script structure**
```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

# --- Slide 1: <title> ---
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "<deck title>"
slide.placeholders[1].text = "<author> | <date>"

# --- Slide 2: <title> ---
slide = prs.slides.add_slide(prs.slide_layouts[1])
slide.shapes.title.text = "<slide title>"
tf = slide.placeholders[1].text_frame
tf.text = "<first bullet>"
for bullet in ["<second bullet>", "<third bullet>"]:
    p = tf.add_paragraph()
    p.text = bullet

prs.save("<output_path>")
print("Saved to <output_path>")
```

Before running, check that `python-pptx` is available and install it if not:

```bash
pip show python-pptx > /dev/null 2>&1 || pip install python-pptx
```

Execute the script using the Bash tool. Confirm the file path once the script completes successfully.
