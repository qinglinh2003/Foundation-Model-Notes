# Figure 6.1: The Scale Gap

**Filename**: `scale_gap.png`
**LaTeX label**: `fig:scale-gap`
**Caption**: From MiniGPT to frontier LLMs: training time, memory footprint, and cost of a single mistake grow by orders of magnitude, while the core Transformer block remains the same.

## Prompt

```text
Draw a scale comparison infographic for a graduate-level machine learning textbook.
Use the course's blue-white visual system. Landscape orientation, polished
editorial style.

Purpose:
- The figure should teach that scaling a Transformer changes the engineering
  regime, not the architecture.
- The main visual message is: the same building block operates at wildly
  different scales, and the cost of mistakes grows with it.

LAYOUT:
Four columns, left to right, each representing a model scale.
Each column is a vertical card with consistent layout.

COLUMN 1 — MiniGPT (Project 1):
- Icon: a single small blue cube
- Title: "MiniGPT"
- Params: "3.7 M"
- Training time: "5 minutes"
- GPU memory: "< 100 MB"
- Mistake cost: "5 min rerun"
- Small badge: "Project 1"

COLUMN 2 — Small LLM:
- Icon: a small stack of ~4 blue cubes
- Title: "Small LLM"
- Params: "300 M"
- Training time: "1–2 days"
- GPU memory: "~8 GB"
- Mistake cost: "hours"
- Small badge: "Project 2"

COLUMN 3 — Medium LLM:
- Icon: a larger stack of ~12 blue cubes
- Title: "Medium LLM"
- Params: "7 B"
- Training time: "weeks"
- GPU memory: "~140 GB"
- Mistake cost: "days + $$"

COLUMN 4 — Frontier LLM:
- Icon: a tall tower of many blue cubes, visually much larger
- Title: "Frontier LLM"
- Params: "70 B+"
- Training time: "months"
- GPU memory: "> 1 TB"
- Mistake cost: "$$$$"

BOTTOM ANNOTATION (spanning all four columns):
Left side: a thin horizontal blue bar connecting all four columns
Right side: text reading "Same Transformer block. Different engineering regime."

VISUAL EMPHASIS:
- The cube icons should clearly grow in size left to right, making the
  scale difference immediately visible
- The ONE orange accent (#FF9F43) is on the "Mistake cost" row of Column 4
  ("$$$$"), highlighting that mistakes at frontier scale are extremely expensive
- All other elements use the blue palette

STYLE LOCK:
- Match the course's Zoom-inspired blue-white textbook visual system.
- Background: #FAFCFF
- Primary blocks: #2D8CFF
- Outlines: #0B5CFF
- Light fills: #E8F4FD
- Text: #1A1A2E (charcoal)
- Secondary text: #6B7280 (steel gray)
- Orange accent: #FF9F43 (ONE element only — the frontier mistake cost)
- Clean vector-like geometry, rounded rectangles, sans-serif labels,
  generous margins.
- Landscape layout. Modern tech aesthetic.

DO NOT: cartoon style, photorealism, clip art, SaaS dashboard, heavy 3D,
neon, rainbow, coral, teal, purple, green, decorative borders, abstract
background patterns, complex formulas.
```

## Review Checklist

- [ ] Four columns: MiniGPT / 300M / 7B / 70B+
- [ ] Cube icons clearly grow in size left to right
- [ ] Each column shows: params, training time, GPU memory, mistake cost
- [ ] Project 1 and Project 2 badges on first two columns
- [ ] Bottom annotation: "Same Transformer block. Different engineering regime."
- [ ] Orange accent ONLY on frontier mistake cost
- [ ] No extra colors beyond blue + white + orange + gray
- [ ] Readable at 50% width in PDF
