# Figure 2.1: Scaled Dot-Product Attention

**Filename**: `scaled_dot_product_attention.png`
**LaTeX label**: `fig:sdpa`
**Caption**: Scaled dot-product attention computation. Queries and keys interact through matrix multiplication and scaling to produce attention weights, which are applied to values to produce context-aware output representations.

## Prompt

```
Draw a technically precise computation flow diagram of scaled dot-product attention
for a machine learning textbook. Use the course's Zoom-inspired blue-white visual system.
The figure should be polished and editorial, not a rough whiteboard sketch.

OVERALL LAYOUT:
- Landscape orientation, generous whitespace
- Data flows from BOTTOM to TOP (inputs at bottom, output at top)
- Three input matrices at the bottom: Q (queries), K (keys), V (values)
- One output matrix at the top: Attention(Q, K, V)

COMPUTATION FLOW (bottom to top):

1. INPUTS (bottom row, three rounded rectangles side by side):
   - Left: "Q" in Zoom Blue (#2D8CFF) fill
   - Center: "K^T" in Zoom Blue (#2D8CFF) fill (note the transpose)
   - Right: "V" in Zoom Blue (#2D8CFF) fill

2. FIRST OPERATION (Q × K^T):
   - Q and K^T arrows converge into a "MatMul" operation node (circle or rounded square)
   - Label the operation node "MatMul"
   - Output arrow goes up

3. SCALE:
   - A rounded rectangle labeled "Scale" with annotation "÷ √d_k" next to it
   - Use slightly different shade or border to distinguish from MatMul

4. MASK (optional path):
   - A rounded rectangle labeled "Mask"
   - Use soft orange (#FF9F43) outline — this is the ONE orange accent element
   - Small annotation: "−∞ for forbidden positions"
   - This is the visual focal point showing where masking happens

5. SOFTMAX:
   - A rounded rectangle labeled "Softmax"
   - Annotation: "per row"

6. SECOND MATMUL:
   - The softmax output and V arrows converge into another "MatMul" node
   - Output goes up to the final result

7. OUTPUT (top):
   - Rounded rectangle labeled "Attention(Q, K, V)"
   - Slightly larger than input boxes

ARROWS:
- Thin, clean arrows connecting each stage
- Use Zoom Blue (#2D8CFF) for main data flow arrows
- Use charcoal (#1A1A2E) for labels

VISUAL STYLE:
- Each operation node should be a clean rounded rectangle or circle
- Consistent spacing between stages
- The mask step should visually stand out with its orange accent
- White or very pale blue (#FAFCFF) background
- Sans-serif labels in charcoal
- No shadows, no heavy gradients, no 3D effects
- Subtle depth cues are OK (very light drop shadow on boxes)
- Should look like a polished figure from a modern AI textbook
```

## Review Checklist

- [ ] Data flows bottom to top: Q, K^T, V → MatMul → Scale → Mask → Softmax → MatMul → Output
- [ ] K is transposed (K^T), not K
- [ ] Scale shows ÷ √d_k, not × √d_k
- [ ] Mask step is present and uses orange accent
- [ ] Mask annotation says −∞, not 0
- [ ] Softmax annotation says "per row"
- [ ] V enters at the second MatMul, not the first
- [ ] All labels readable and correctly spelled
