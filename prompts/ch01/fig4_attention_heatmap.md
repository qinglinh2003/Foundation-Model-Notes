# Figure 1.4: Attention Alignment Heatmap

**Filename**: `attention_alignment.png`
**LaTeX label**: `fig:attention-heatmap`
**Caption**: Attention alignment weights for an English-to-French translation example. The non-diagonal pattern reveals that attention learns word reordering: ``chat'' attends to ``cat'' and ``noir'' attends to ``black,'' reflecting the adjective-noun order difference between English and French.

## Prompt

```
Draw a publication-quality attention alignment heatmap for an English-to-French
translation example. Use the course's Zoom-inspired blue-white visual system.
This should look like an elegant research-paper figure with precise data.

GRID SPECIFICATION:
- 3 columns (x-axis): source tokens "the", "black", "cat"
- 3 rows (y-axis): target tokens "le", "chat", "noir"
- X-axis label at top: "Source (English)" in #6B7280
- Y-axis label on left: "Target (French)" in #6B7280

CELL VALUES (attention weights — display the number inside each cell):
- Row "le":    0.85,  0.05,  0.10
- Row "chat":  0.05,  0.10,  0.85
- Row "noir":  0.05,  0.85,  0.10

COLOR SCALE (blue monochrome — matches our palette):
- 0.0: near-white (#F0F7FF)
- 0.25: ice blue (#E8F4FD)
- 0.50: medium blue (#5BA3FF)
- 0.75: Zoom Blue (#2D8CFF)
- 1.0: deep blue (#0B5CFF)
The gradient should be smooth and high contrast within the blue family.

CELL STYLING:
- Thin white borders (1-2px) between cells for a clean grid
- Numbers in white bold text on dark blue cells (≥0.50)
- Numbers in #1A1A2E charcoal text on light cells (<0.50)
- Cells may have very slightly rounded corners

COLOR BAR:
- Vertical color bar on the right side
- Labeled "Attention Weight α" in #6B7280
- Smooth blue gradient from #F0F7FF to #0B5CFF
- Tick marks at 0.0, 0.25, 0.50, 0.75, 1.00
- Thin #0B5CFF border

ANNOTATIONS (the ONE orange accent):
- Add thin dashed lines or subtle curved arrows OUTSIDE the heatmap grid
  connecting the non-diagonal alignments:
  - "chat" → "cat" with a small #FF9F43 label "word reordering"
  - "noir" → "black" with a small #FF9F43 arrow
- These orange annotations should be subtle and must not obstruct the grid
- They are the only non-blue colored elements in the figure

TYPOGRAPHY:
- Token labels: clean sans-serif, slightly larger than cell numbers
- Axis labels: smaller semibold, #6B7280
- No title inside the image

OVERALL:
- Background: #FAFCFF
- Very subtle blue-tinted shadow behind the heatmap panel
- Generous whitespace around grid and color bar
- The non-diagonal pattern should be immediately obvious at a glance
- Clean, modern, Zoom-like tech aesthetic
- Match the same typography, margins, blue palette, and subtle depth used by the
  other Chapter 1 figures.

IMPORTANT:
- Do not invent additional numbers.
- Do not swap axes.
- Do not replace the matrix with an abstract illustration.
```

## Review Checklist

- [ ] 3×3 grid with correct labels on correct axes
- [ ] Numbers inside cells match specification exactly
- [ ] Color gradient is all-blue (light blue → deep blue), no other hue
- [ ] "chat" row has highest weight on "cat" column (not "chat")
- [ ] "noir" row has highest weight on "black" column
- [ ] "le" row has highest weight on "the" column
- [ ] Color bar present with blue gradient and "Attention Weight α" label
- [ ] Only non-blue elements: the orange annotation arrows/labels
- [ ] Overall palette: blue-white + single orange accent
