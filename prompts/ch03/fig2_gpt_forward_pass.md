# Figure 3.2: GPT Forward Pass

**Filename**: `gpt_forward_pass.png`
**LaTeX label**: `fig:gpt-forward`
**Caption**: The GPT forward pass from token ids to next-token logits, traced on a running example.

## Prompt

```
Draw a complete GPT forward pass diagram for a graduate-level machine learning
textbook. Use the course's blue-white visual system. Landscape orientation,
polished editorial style.

LAYOUT:
Data flows from LEFT to RIGHT (input on left, output on right).
The diagram traces a concrete example: the input string "The cat sat on"
with token ids (464, 3797, 3332, 319).

STAGE 1 — TOKEN IDS (leftmost):
- Four small white rounded rectangles stacked vertically, each containing:
  "The" (464), "cat" (3797), "sat" (3332), "on" (319)
- Label above: "Token IDs"

STAGE 2 — EMBEDDING TABLE:
- A tall blue rectangle labeled "Embedding Table"
- Annotation: "E ∈ R^{50257 x 768}"
- Arrows from token IDs into the embedding table
- Output: four horizontal bars representing 768-dim vectors
- Below the output, a small "+" symbol and a box labeled "PE" (Positional Encoding)
- After addition: label "4 x 768 matrix"

STAGE 3 — DECODER BLOCKS:
- A tall rounded blue rectangle (or stack of smaller blocks) labeled:
  "x 12 Decoder Blocks"
- Inside, show one expanded block with:
  - "LN" → "Causal MHA" → "+" (residual)
  - "LN" → "FFN" → "+" (residual)
- The residual connections shown as bypass arrows
- Annotation: "Shape preserved: 4 x 768"

STAGE 4 — FINAL LAYER NORM:
- Small blue rectangle labeled "LayerNorm"

STAGE 5 — LM HEAD:
- Blue rectangle labeled "LM Head (E^T)"
- Annotation: "768 → 50,257"
- A dashed arrow connecting back to the Embedding Table in Stage 2,
  labeled "Weight Tying" — this is the orange accent element (#FF9F43)

STAGE 6 — OUTPUT (rightmost):
- A probability distribution visualization:
  - A short bar chart or softmax output showing a few candidate tokens
  - "the" with high bar, "a" with medium bar, "mat" with smaller bar
  - Label: "P(next token | prefix)"

VISUAL STYLE:
- Clean left-to-right flow with thin blue arrows
- The weight tying dashed arrow is the ONE orange element
- Shape annotations at each stage (4x768, etc.)
- Zoom Blue (#2D8CFF) for all processing blocks
- White background (#FAFCFF)
- Sans-serif charcoal labels
- The running example tokens should be clearly visible throughout
```

## Review Checklist

- [ ] Data flows left to right: Token IDs → Embedding → Blocks → LN → LM Head → Logits
- [ ] Token IDs show actual numbers (464, 3797, 3332, 319)
- [ ] Embedding table shows dimension: 50257 x 768
- [ ] PE is added (not concatenated) to embeddings
- [ ] Decoder block shows pre-norm structure: LN before MHA and FFN
- [ ] Residual connections visible as bypass arrows
- [ ] LM head shows E^T (weight tying)
- [ ] Weight tying arrow is dashed and orange
- [ ] Output shows probability distribution, not raw logits
- [ ] Shape preserved through blocks: 4 x 768
