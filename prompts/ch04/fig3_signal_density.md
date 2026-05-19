# Figure 4.3: Training Signal Density — BERT vs GPT

**Filename**: `signal_density.png`
**LaTeX label**: `fig:signal-density`
**Caption**: Training signal density comparison: BERT computes loss on 15\% of tokens (sparse), while GPT computes loss on every token (dense). Same data, 6.7$\times$ more gradient signal for GPT.

## Prompt

```
Draw a training signal density comparison between BERT and GPT for a graduate-level
machine learning textbook. Use the course's blue-white visual system.
Landscape orientation, polished editorial style.

LAYOUT:
Two rows, each showing a 20-token sequence with gradient signal visualization.

TOP ROW — BERT (MLM):
- Title: "BERT: Masked Language Modeling"
- 20 token boxes in a horizontal row
- 3 of them (15%) are highlighted in soft orange (#FF9F43) — these produce gradient
- The other 17 are light gray — they provide context but NO gradient signal
- Below: "3 / 20 positions = 15% gradient coverage"
- Small arrows pointing down from ONLY the 3 orange boxes, labeled "∇ loss"
- The gray boxes have NO downward arrows

BOTTOM ROW — GPT (Next-token prediction):
- Title: "GPT: Next-Token Prediction"
- 20 token boxes in a horizontal row
- ALL 19 of them (positions 1-19, predicting positions 2-20) are highlighted
  in Zoom Blue (#2D8CFF) — every position produces gradient
- Show 19 out of 20 blue boxes with downward gradient arrows
- The final token is context-only in this finite example because there is no
  next token inside the displayed sequence
- Below: "19 / 20 positions = ~100% gradient coverage"

CENTER COMPARISON:
- A large annotation between the two rows:
  "Same 20 tokens → BERT: 3 gradients | GPT: 19 gradients"
  "Signal density ratio: ~6.7×"
- An arrow or bracket showing the gap

RIGHT SIDE — SCALING IMPLICATION:
- Small inset or annotation:
  "At 1 trillion tokens:"
  "BERT effective training signal: 150B token-predictions"
  "GPT effective training signal: ~1T token-predictions"
  "The gap compounds at scale"

VISUAL DETAILS:
- Zoom Blue (#2D8CFF) for GPT gradient-producing tokens
- Soft Orange (#FF9F43) for BERT gradient-producing tokens (the 15%)
- Light gray (#E8E8E8) for BERT context-only tokens
- White/ice blue (#FAFCFF) background
- "∇" symbols or small downward arrows for gradient flow
- Bold "6.7×" in the center comparison
- Sans-serif labels in charcoal (#1A1A2E)
```

## Review Checklist

- [ ] BERT row: only 15% of tokens highlighted (orange), rest gray
- [ ] GPT row: nearly all tokens highlighted (blue)
- [ ] Gradient arrows only from highlighted tokens
- [ ] "6.7×" ratio clearly visible and prominent
- [ ] Scaling implication mentioned (compounds at trillion-token scale)
- [ ] Two colors distinguish the models: orange for BERT signal, blue for GPT signal
- [ ] No misleading implication that BERT is "wrong" — just sparser
