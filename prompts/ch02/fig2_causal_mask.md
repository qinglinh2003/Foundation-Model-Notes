# Figure 2.2: Causal Mask Matrix

**Filename**: `causal_mask.png`
**LaTeX label**: `fig:causal-mask`
**Caption**: Causal (autoregressive) mask for a 4-token sequence. White cells indicate allowed attention (token $i$ can attend to tokens $\leq i$); dark cells indicate blocked attention ($-\infty$ before softmax). Each row's visible positions expand as we move down the sequence.

## Prompt

```
Draw a causal attention mask matrix for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
The figure should be polished and editorial.

LAYOUT:
- A 4×4 grid/matrix, clearly drawn with visible cell borders
- Column headers (top): x_1, x_2, x_3, x_4 — labeled "Keys (attending TO)"
- Row headers (left): x_1, x_2, x_3, x_4 — labeled "Queries (attending FROM)"

CELL VALUES AND COLORS:
- Row x_1: [✓, ✗, ✗, ✗]
- Row x_2: [✓, ✓, ✗, ✗]
- Row x_3: [✓, ✓, ✓, ✗]
- Row x_4: [✓, ✓, ✓, ✓]

Where:
- ✓ cells (lower triangle including diagonal): white or very light blue (#E8F4FD)
  fill, with "0" written inside in charcoal text
- ✗ cells (upper triangle): dark navy (#0B5CFF) or charcoal fill, with "−∞"
  written inside in white text

The result should be a clear lower-triangular pattern.

ANNOTATIONS:
- Below the matrix, add a small legend:
  - White/light cell: "allowed (score unchanged)"
  - Dark cell: "blocked (score → −∞ before softmax)"
- On the right side, draw a small orange (#FF9F43) annotation arrow pointing
  to the diagonal, labeled "each token sees only itself and the past"

VISUAL STYLE:
- Clean grid lines in medium gray (#6B7280)
- Cell borders clearly visible
- Token labels in sans-serif charcoal
- White or very pale blue (#FAFCFF) background
- The lower-triangular pattern should be the immediate visual takeaway
- No shadows, no heavy gradients, no 3D
- Polished editorial textbook figure style
```

## Review Checklist

- [ ] Matrix is 4×4 with correct lower-triangular pattern
- [ ] Diagonal is INCLUDED in allowed cells (each token can attend to itself)
- [ ] Blocked cells show −∞, not 0
- [ ] Allowed cells show 0, not 1
- [ ] Column = Keys, Row = Queries (not reversed)
- [ ] Orange accent used only for the diagonal annotation
- [ ] Labels are readable and correctly spelled
