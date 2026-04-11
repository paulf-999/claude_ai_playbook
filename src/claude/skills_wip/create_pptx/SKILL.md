---
name: create_pptx
description: Interactively gather deck requirements, propose a slide structure, and produce a .pptx file using python-pptx with style presets and Phosphor Icons support.
version: 0.1.0
maturity: draft
tags:
  criticality: could
  status: wip
  tested: false
tools: Bash, Read
---

## Scope gate

This skill is at **draft** maturity. Claude behaviour is constrained accordingly:

| Maturity | Allowed |
|---|---|
| draft | Happy path only. Log gaps as TODOs, do not solve them. No refactoring. |
| tactical | Main path + light error handling. No gold-plating. |
| strategic | Full coverage, edge cases, documentation, evals expected. |

---

Base directory for this skill: ~/.claude/skills/create_pptx

Select your agent persona based on the deck type identified in Phase 1:

| Deck type | Persona |
|---|---|
| Executive update, stakeholder comms, retrospective, roadmap | **Project manager** |
| Technical proposal, training/educational, data insights | **Technical writer** |

| Deck type | Max slides |
|---|---|
| Executive / stakeholder | 10 |
| Technical proposal | 15 |
| Training / educational | 20 |
| Retrospective | 12 |
| Data insights / report | 15 |
| Strategy / roadmap | 12 |

---

## Phase 1 — Gather context

Ask the following in a single message:

1. What type of deck is this?
2. Who is the audience?
3. What are the 2–3 key messages the audience should walk away with?
4. What content, data, or context should the deck include? (Paste text, share Confluence URLs, or describe.)
5. Any constraints? (slide limit, time limit)
6. What file name and directory path should the `.pptx` be saved to?
7. Which style preset?

| Style | Use case |
|---|---|
| `formal` | Compliance, regulatory, conservative audiences |
| `soft` | KT sessions, training, learning contexts |
| `executive` | C-suite, board, steering groups |
| `dark` | Conference talks, tech demos, external presentations |
| `data_report` | Analytics, metrics reviews, data findings |
| `workshop` | Facilitation, brainstorming, interactive sessions |
| `narrative` | Pitches, change comms, persuasion |
| `minimal` | Design-led, editorial, letting content breathe |

8. Do any slides need icons? If yes, which slides and what concept should each icon represent? (Icons are sourced from Phosphor Icons — clean black stroke, transparent background.)
9. Is a live demo planned at any point in the session?

Wait for the user's response before proceeding.

---

## Phase 1b — Load style spec

Read `~/.claude/skills/create_pptx/styles/{chosen_style}.md` using the Read tool. Note all parameters before proceeding.

---

## Phase 2 — Propose slide structure

Propose a slide-by-slide outline:

- Format: `Slide N — <title>: <one sentence describing the message it lands>`
- Always include: Slide 1 (title slide) and a closing slide (next steps or questions)
- Always include: Slide 2 (agenda)
- If a live demo is planned: place the demo slide at **Slide 3**, immediately after the agenda
- Apply the max_bullets and slide ceiling for the deck type
- Slide titles must be **short** — aim to fit on a single line. State the conclusion, not just the topic.

Present the outline and wait for the user to confirm or adjust before proceeding.

---

## Phase 3 — Generate the .pptx file

### Font and dependency check

Before generating, check and install dependencies:

```bash
pip show python-pptx > /dev/null 2>&1 || pip install python-pptx
pip show cairosvg > /dev/null 2>&1 || pip install cairosvg
```

**Note on fonts:** Both `Georgia` (title) and `Inter` (body) must be installed on the Windows system. Georgia is a Windows system font. Inter is free and available at https://rsms.me/inter/ — install before opening the generated file in PowerPoint.

### Python script structure

```python
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from lxml import etree
import urllib.request, tempfile, os

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)
```

### Style parameters

Set these constants at the top of the script from the style spec:

```python
TITLE_FONT        = "Georgia"
BODY_FONT         = "Inter"
TITLE_SIZE        = Pt(36)           # from style spec
BODY_SIZE         = Pt(20)           # from style spec
TITLE_COLOUR      = RGBColor(...)    # from style spec
BODY_COLOUR       = RGBColor(0x2F, 0x2F, 0x2F)
BG_COLOUR         = RGBColor(0xFF, 0xFF, 0xFF)  # override for dark style
HEADER_BAR        = False            # True for formal style only
HEADER_BAR_COLOUR = None             # Set for formal style
ACCENT_COLOUR     = RGBColor(...)    # from style spec
REF_SIZE          = Pt(14)
REF_COLOUR        = TITLE_COLOUR     # reference links use title colour
```

### Helper functions

Include these in every generated script:

```python
def set_background(slide):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = BG_COLOUR


def add_header_bar(slide):
    """Formal style only — coloured rectangle behind title placeholder."""
    if not HEADER_BAR:
        return
    bar = slide.shapes.add_shape(1, 0, 0, prs.slide_width, Inches(1.3))
    bar.fill.solid()
    bar.fill.fore_color.rgb = HEADER_BAR_COLOUR
    bar.line.fill.background()
    sp = bar._element
    sp.getparent().remove(sp)
    slide.shapes._spTree.insert(2, sp)


def style_heading(shape, centered=False):
    """Style the title placeholder. Centered for title slide only."""
    for para in shape.text_frame.paragraphs:
        para.alignment = PP_ALIGN.CENTER if centered else PP_ALIGN.LEFT
        for run in para.runs:
            run.font.name      = TITLE_FONT
            run.font.size      = TITLE_SIZE
            run.font.bold      = True
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if HEADER_BAR else TITLE_COLOUR


def add_bullet(tf, text, first=False):
    """Append a styled bullet to a text frame."""
    p           = tf.paragraphs[0] if first else tf.add_paragraph()
    p.text      = text
    p.alignment = PP_ALIGN.LEFT
    for run in p.runs:
        run.font.name      = BODY_FONT
        run.font.size      = BODY_SIZE
        run.font.color.rgb = BODY_COLOUR


def add_ref_link(slide, tf, label, url):
    """Append a hyperlinked reference line to the text frame."""
    p           = tf.add_paragraph()
    p.alignment = PP_ALIGN.LEFT
    run         = p.add_run()
    run.text    = f"Ref: {label}"
    run.font.name      = BODY_FONT
    run.font.size      = REF_SIZE
    run.font.color.rgb = REF_COLOUR
    run.font.underline = True
    rId   = slide.part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    rPr   = run._r.get_or_add_rPr()
    hlink = etree.SubElement(rPr, qn("a:hlinkClick"))
    hlink.set(qn("r:id"), rId)


def new_content_slide(title_text):
    """Create a standard content slide (layout 1) with background and styled heading."""
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    set_background(slide)
    add_header_bar(slide)
    slide.shapes.title.text = title_text
    style_heading(slide.shapes.title)
    return slide, slide.placeholders[1].text_frame
```

### Icon helper

If any slides require icons, include this function:

```python
def get_icon_png(icon_name, tmp_dir, dark=False):
    """Download Phosphor icon SVG and convert to PNG."""
    import cairosvg
    url      = f"https://raw.githubusercontent.com/phosphor-icons/core/main/assets/regular/{icon_name}.svg"
    svg_path = os.path.join(tmp_dir, f"{icon_name}.svg")
    png_path = os.path.join(tmp_dir, f"{icon_name}.png")
    urllib.request.urlretrieve(url, svg_path)
    if dark:
        svg = open(svg_path).read().replace('#000000', '#FFFFFF').replace('currentColor', '#FFFFFF')
        open(svg_path, 'w').write(svg)
    cairosvg.svg2png(url=f"file://{svg_path}", write_to=png_path, output_width=72, output_height=72)
    return png_path

# Usage: add icon to slide (top-right corner)
# with tempfile.TemporaryDirectory() as tmp:
#     icon = get_icon_png("shield", tmp, dark=HEADER_BAR or bool(BG_COLOUR))
#     slide.shapes.add_picture(icon, Inches(11.5), Inches(0.3), Inches(0.9), Inches(0.9))
```

### Slide construction rules

**Title slide (layout index 0):**
```python
slide = prs.slides.add_slide(prs.slide_layouts[0])
set_background(slide)
slide.shapes.title.text = "<deck title>"
style_heading(slide.shapes.title, centered=True)   # centered on title slide only
sub = slide.placeholders[1]
sub.text = "<author>  |  <date>"
for para in sub.text_frame.paragraphs:
    para.alignment = PP_ALIGN.CENTER
    for run in para.runs:
        run.font.name = BODY_FONT
        run.font.size = Pt(20)
```

**All other slides (layout index 1):** use `new_content_slide()`, which sets heading to left-aligned.

**Agenda slide:** always number agenda items — `"1.  Item"`, `"2.  Item"`, etc.

**Content rules:**
- Headings: short — aim to fit on one line; state the conclusion, not the topic
- Body text: always `PP_ALIGN.LEFT`
- Max bullets per slide: as specified in style spec
- Max 8 words per bullet
- When source material is provided (Confluence pages, docs, URLs): use 2–3 bullets of supporting context + `add_ref_link()` pointing to the source — do not recreate the full content
- When URLs are available, always embed as clickable hyperlinks using `add_ref_link()`
- Include `# --- Slide N: title ---` comment above each slide block

### Save

```python
prs.save("<output_path>")
print("Saved to <output_path>")
```

Execute the script using the Bash tool. Confirm the file path once complete.
