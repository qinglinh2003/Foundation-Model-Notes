# Figure 3.1: Three Transformer Architecture Families

**Filename**: `three_architectures.png`
**LaTeX label**: `fig:three-architectures`
**Caption**: Three architecture families built from the same attention block: encoder-decoder, encoder-only (BERT), and decoder-only (GPT).

## Prompt

```
Draw a side-by-side comparison of three Transformer architecture families for a
graduate-level machine learning textbook. Use the course's blue-white visual system.
Landscape orientation, polished editorial style.

LAYOUT:
Three columns, evenly spaced, each showing one architecture variant.
A shared title row at the top: "Three Transformer Architectures"

COLUMN 1 — ENCODER-DECODER (left):
- Title: "Encoder-Decoder"
- Subtitle: "(Original Transformer, T5)"
- Two vertical stacks side by side:
  - Left stack: 3 blue blocks labeled "Encoder Block" stacked vertically
    - Each block has a small label "Bidirectional Self-Attention" + "FFN"
    - Input at bottom: "Source Input" (e.g., French sentence)
  - Right stack: 3 blue blocks labeled "Decoder Block" stacked vertically
    - Each block has: "Causal Self-Attention" + "Cross-Attention" + "FFN"
    - Input at bottom: "Target Input" (e.g., English sentence)
    - Output at top: "Output Logits"
  - Curved arrows from encoder stack to decoder stack labeled "Cross-Attention"
  - The cross-attention arrows should use soft orange (#FF9F43) — this is the
    orange accent for this figure, showing the extra mechanism decoder-only removes

COLUMN 2 — ENCODER-ONLY (center):
- Title: "Encoder-Only"
- Subtitle: "(BERT)"
- Single vertical stack: 3 blue blocks labeled "Encoder Block"
  - Each block: "Bidirectional Self-Attention" + "FFN"
  - Input at bottom: "Input Tokens"
  - Output at top: "[CLS] Representation"
  - Small annotation: "Bidirectional: every token sees all others"

COLUMN 3 — DECODER-ONLY (right):
- Title: "Decoder-Only"
- Subtitle: "(GPT, LLaMA)"
- Single vertical stack: 3 blue blocks labeled "Decoder Block"
  - Each block: "Causal Self-Attention" + "FFN"
  - Input at bottom: "Input = Prefix"
  - Output at top: "Next-Token Logits"
  - Small annotation: "Causal: each token sees only previous tokens"
  - This column should have a slightly more prominent border or fill
    to indicate it is the focus architecture

VISUAL DETAILS:
- Attention masks visualized as tiny 3x3 matrices inside each block:
  - Bidirectional: full white matrix (all visible)
  - Causal: lower-triangular white, upper-triangular dark
- Clean arrows showing data flow (bottom to top)
- Zoom Blue (#2D8CFF) for all blocks
- Soft Orange (#FF9F43) ONLY for cross-attention arrows in Column 1
- White/ice blue (#FAFCFF) background
- Sans-serif labels in charcoal (#1A1A2E)
```

## Review Checklist

- [ ] Three columns clearly separated
- [ ] Encoder-decoder has TWO stacks with cross-attention arrows between them
- [ ] Encoder-only has ONE stack with bidirectional attention
- [ ] Decoder-only has ONE stack with causal attention
- [ ] Cross-attention arrows are orange (only orange element)
- [ ] Decoder-only column is visually emphasized as the focus
- [ ] Attention mask thumbnails show correct patterns (bidirectional=full, causal=triangular)
- [ ] Labels: BERT for encoder-only, GPT/LLaMA for decoder-only
- [ ] No extra colors beyond blue + white + orange
