# Figure 1.7: Sequential vs Parallel Computation

**Filename**: `sequential_vs_parallel.png`
**LaTeX label**: `fig:seq-vs-parallel`
**Caption**: The fundamental computational difference between recurrent and attention-based architectures. \emph{Left:} an RNN must process tokens sequentially --- each hidden state depends on the previous one, creating a serial chain of $T$ steps that cannot be parallelized across time. \emph{Right:} a Transformer layer updates all positions in parallel while attention connects each position to its allowed context under the attention mask.

## Prompt

```
Draw a side-by-side comparison diagram for a machine learning textbook showing
why Transformers replaced RNNs. Use the course's Zoom-inspired blue-white
visual system. The figure should be polished and editorial, not a rough
whiteboard sketch.

OVERALL LAYOUT:
- Landscape orientation, generous whitespace
- Two panels side by side
- Left panel: "Recurrent (Sequential)" — shows the RNN bottleneck
- Right panel: "Attention (Parallel)" — shows the Transformer advantage
- A vertical divider between panels, thin, in #E8F4FD
- Each panel has a title at the top in bold charcoal (#1A1A2E)

LEFT PANEL — RECURRENT (SEQUENTIAL):
- Background: very subtle pale blue (#F0F7FF) rounded panel
- Four input tokens at the bottom: x_1, x_2, x_3, x_4 in white pill shapes
  with #2D8CFF border
- Four hidden state nodes above them: h_1, h_2, h_3, h_4 in #2D8CFF
  rounded rectangles
- Vertical arrows from each x_t up to h_t (input feeding)
- CRITICAL: horizontal arrows forming a CHAIN: h_1 → h_2 → h_3 → h_4
- These horizontal chain arrows should be in #FF9F43 (soft orange) — this is
  the ONE orange accent, highlighting the sequential dependency bottleneck
- Each orange arrow has a small clock/wait icon or a "wait" annotation to
  emphasize that h_2 cannot start until h_1 finishes
- Below the panel, annotation in steel gray (#6B7280):
  "T serial steps — each state waits for the previous one"
- Optional: a subtle "time →" label along the bottom

RIGHT PANEL — ATTENTION (PARALLEL, MASKED FOR LANGUAGE MODELING):
- Background: very subtle pale blue (#F0F7FF) rounded panel
- Same four input tokens at the bottom: x_1, x_2, x_3, x_4 in white pills
- Four representation nodes above them: z_1, z_2, z_3, z_4 in #2D8CFF
  rounded rectangles
- Between the input row and the representation row, draw CAUSAL ATTENTION CONNECTIONS:
  - z_1 connects only to x_1
  - z_2 connects to x_1 and x_2
  - z_3 connects to x_1, x_2, and x_3
  - z_4 connects to x_1, x_2, x_3, and x_4
  - These lines should be in varying opacity of #0B5CFF (deep blue)
  - This creates a triangular masked-attention web: no position attends to future tokens
- The key visual message: ALL z_i are computed SIMULTANEOUSLY
- Add small parallel-processing indicators: maybe "= 1 step" annotation
  or show all four z nodes updating at the same time (e.g., a bracket
  grouping them with "parallel")
- Below the panel, annotation in steel gray:
  "1 parallel step — all positions updated simultaneously"

VISUAL CONTRAST:
- Left panel should feel constrained, bottlenecked (the orange chain dominates)
- Right panel should feel open, connected, fast (the blue web is the hero)
- The contrast should be immediately obvious at a glance

ARROWS AND LINES:
- RNN recurrent chain: #FF9F43 (orange), solid, medium weight, pointed heads
- RNN input arrows: #6B7280 (steel gray), thinner
- Attention connections: #0B5CFF (deep blue), varying opacity
- Input arrows in right panel: #6B7280 (steel gray)

STYLE:
- Background: #FAFCFF
- Very subtle blue-tinted shadows on nodes
- Only non-blue color: the orange sequential chain arrows in the left panel
- Clean, modern, Zoom-like tech aesthetic
- Match the same rounded geometry, line weights, typography, margins, and subtle
  shadows used by the other Chapter 1 figures
```

## Review Checklist

- [ ] Two panels clearly labeled: "Recurrent (Sequential)" and "Attention (Parallel)"
- [ ] Left panel: h_1 → h_2 → h_3 → h_4 chain is clearly SEQUENTIAL with orange arrows
- [ ] Right panel: each z_i connects only to its allowed prefix tokens under a causal mask
- [ ] Right panel: all z_i nodes are visually simultaneous (not chained)
- [ ] Orange color ONLY on the sequential chain arrows — nothing else is orange
- [ ] Visual contrast is immediately obvious: left feels constrained, right feels open
- [ ] Labels are crisp, short, correctly spelled
- [ ] Style matches other Ch1 figures (same blue palette, rounded geometry, shadows)
- [ ] No extra colors (no coral, teal, purple, green)
