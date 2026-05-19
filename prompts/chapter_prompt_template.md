# Chapter Figure Prompt Template

Copy this file into `prompts/chNN/figX_short_name.md` when adding a new figure.

# Figure N.X: Short Descriptive Title

**Filename**: `short_name.png`
**LaTeX label**: `fig:short-name`
**Caption**: One or two sentences explaining the technical point of the figure.
The caption should say what the reader should learn, not merely describe what is
visible.

## Prompt

```text
Draw [specific figure type] for a graduate-level machine learning textbook.
Use the blue-and-white tech style from our session.

Purpose:
- The figure should teach [one precise concept].
- The main visual message is [one sentence].

Required layout:
- [Position and relationship of component 1]
- [Position and relationship of component 2]
- [Position and relationship of component 3]

Required labels:
- "[short label 1]"
- "[short label 2]"
- "[short label 3]"

Connections:
- [Arrow or flow 1]
- [Arrow or flow 2]
- [Arrow or flow 3]

The ONE orange accent (#FF9F43) in this figure is: [describe the single
focal/emphasis element, e.g., a bottleneck, critical path, or key arrow].
Everything else uses the blue palette.

Important constraints:
- Do not add components not listed above.
- Do not use colors outside the blue family except the one orange accent.
- Do not include complex equations inside the image.
- Keep all labels short and readable.
- Prioritize technical correctness over visual appeal.

STYLE LOCK:
- Match the course's Zoom-inspired blue-white textbook visual system.
- Use polished editorial diagram composition, not a rough whiteboard sketch.
- Keep geometry, shadows, spacing, and typography consistent with previous figures
  in the same chapter.

STYLE:
- Background: #FAFCFF (near-white, slight blue tint)
- Primary blocks: #2D8CFF (Zoom Blue)
- Outlines/borders: #0B5CFF (deep blue)
- Light fills/regions: #E8F4FD (ice blue)
- Text: #1A1A2E (charcoal) or white on dark backgrounds
- Secondary text: #6B7280 (steel gray)
- Orange accent: #FF9F43 (soft orange, ONE element only)
- Clean vector-like geometry, rounded rectangles, subtle blue-tinted shadows,
  single-hue blue gradients only, crisp sans-serif labels, generous margins.
- Landscape layout. Modern tech aesthetic (Zoom-inspired).
- Processing blocks are rounded rectangles; tokens are white pill capsules;
  operations are white circles; regions are translucent pale-blue panels.

DO NOT: cartoon style, photorealism, clip art, SaaS dashboard, heavy 3D,
neon, rainbow, coral, teal, purple, green, decorative borders, abstract
background patterns, complex formulas.
```

## Review Checklist

- [ ] The figure teaches exactly one concept
- [ ] Layout matches the prompt
- [ ] Arrow directions are correct
- [ ] Labels are short, readable, and spelled correctly
- [ ] Only blue family + one orange accent — no other colors
- [ ] No extra components or decorative elements were added
- [ ] The figure remains readable at 50% width in the PDF
- [ ] The caption matches the final image
