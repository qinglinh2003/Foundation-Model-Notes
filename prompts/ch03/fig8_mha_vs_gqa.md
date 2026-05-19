# Figure 3.8: MHA vs GQA vs MQA — Head Sharing Patterns

**Filename**: `mha_vs_gqa.png`
**LaTeX label**: `fig:mha-gqa`
**Caption**: Head sharing patterns in multi-head attention variants. \textbf{Left:} Standard MHA---each query head has its own K/V head. \textbf{Center:} GQA (Grouped Query Attention)---groups of query heads share K/V heads, reducing KV cache by a factor of $h / n_\text{kv}$. \textbf{Right:} MQA (Multi-Query Attention)---all query heads share a single K/V head, minimizing cache but potentially reducing quality.

## Prompt

```
Draw a three-panel comparison of attention head sharing patterns
for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
The figure should be polished and editorial.

LAYOUT: Three panels side by side.

PANEL 1 — "MHA (Multi-Head Attention)" (left)
- Show 8 query heads (Q1..Q8) as blue circles in a row at the top
- Show 8 KV heads (KV1..KV8) as blue circles in a row at the bottom
- Draw one-to-one arrows from each Q head to its corresponding KV head
- All circles in medium blue (#2563EB)
- Title: "MHA"
- Below: "8 Q heads, 8 KV heads"
- Below that: "KV cache: 8 × T × d_k"

PANEL 2 — "GQA (Grouped Query Attention)" (center)
- Show 8 query heads (Q1..Q8) as blue circles in a row at the top
- Show 2 KV heads (KV1, KV2) as slightly larger circles at the bottom
- Draw arrows: Q1-Q4 all point to KV1, Q5-Q8 all point to KV2
- Group brackets above Q1-Q4 and Q5-Q8
- KV heads in slightly darker blue (#1D4ED8) to show they are shared
- Title: "GQA"
- Below: "8 Q heads, 2 KV heads"
- Below that: "KV cache: 2 × T × d_k (4× smaller)"
- Highlight the "4× smaller" in orange (#FF9F43)

PANEL 3 — "MQA (Multi-Query Attention)" (right)
- Show 8 query heads (Q1..Q8) as blue circles in a row at the top
- Show 1 KV head (KV1) as a single larger circle at the bottom center
- Draw arrows: all 8 Q heads point to KV1
- KV head in dark blue (#1E3A8A)
- Title: "MQA"
- Below: "8 Q heads, 1 KV head"
- Below that: "KV cache: 1 × T × d_k (8× smaller)"

BOTTOM ANNOTATION (spanning all panels):
- A horizontal arrow from left to right:
  "More KV heads ← → Fewer KV heads"
- Below: "Quality ← → Inference memory savings"
- This shows the tradeoff axis

VISUAL STYLE:
- Clean circles with thin borders
- Arrows in light gray, clean lines
- Sans-serif labels in charcoal (#374151)
- White background (#FAFCFF)
- No shadows, no 3D, no heavy gradients
- Orange accent ONLY on the "4× smaller" text in GQA panel
- Polished editorial textbook figure style
```

## Review Checklist

- [ ] Three panels: MHA, GQA, MQA — in that order
- [ ] MHA: 1-to-1 mapping between Q and KV heads
- [ ] GQA: many-to-one mapping (groups of Q heads share KV heads)
- [ ] MQA: all-to-one mapping (all Q heads share 1 KV head)
- [ ] Cache size annotations are correct (proportional to KV head count)
- [ ] Orange accent on GQA's memory savings only
- [ ] Tradeoff axis annotation at the bottom
- [ ] All labels readable and correctly spelled
