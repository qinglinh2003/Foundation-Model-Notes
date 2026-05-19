# Figure 1.1: RNN Unrolled Computation Graph

**Filename**: `rnn_unrolled.png`
**LaTeX label**: `fig:rnn-unrolled`
**Caption**: An unrolled recurrent neural network across four time steps. Each hidden state $h_t$ receives input from the current token $x_t$ and the previous hidden state $h_{t-1}$, producing output $y_t$. The sequential dependency $h_1 \to h_2 \to h_3 \to h_4$ prevents parallel computation.

## Prompt

```
Draw an unrolled recurrent neural network across 4 time steps for a machine
learning textbook. Use the course's Zoom-inspired blue-white visual system.
The figure should be polished and editorial, not a rough whiteboard sketch.

LAYOUT (left to right, three horizontal rows):

Bottom row — INPUTS:
- Four nodes labeled x_1, x_2, x_3, x_4
- Style: small rounded capsules, white fill, thin #0B5CFF border

Middle row — HIDDEN STATES (focal element):
- Four nodes labeled h_1, h_2, h_3, h_4
- Style: larger rounded rectangles filled with #2D8CFF (Zoom Blue),
  subtle lighter-to-darker blue gradient, very soft blue-tinted shadow
- White text labels inside each node
- Put "tanh" in small white text in the lower-right corner of each node
- On the far left, one dashed-outline node labeled "h_0" in light gray (#F3F4F6
  fill, #6B7280 dashed border), with a thin dashed arrow into h_1

Top row — OUTPUTS:
- Four nodes labeled y_1, y_2, y_3, y_4
- Style: small rounded capsules matching the input style

ARROWS:
- Vertical arrows from each x_t up to corresponding h_t: thin #6B7280 (steel gray)
- Vertical arrows from each h_t up to corresponding y_t: thin #6B7280
- Horizontal recurrent arrows h_1 → h_2 → h_3 → h_4: THICKER, #FF9F43 (soft
  orange), with clean triangular heads. This is the ONE orange accent element
  in the figure — it highlights the sequential dependency.
- Arrow from h_0 to h_1: dashed, light gray

BACKGROUND AND ANNOTATIONS:
- A translucent ice blue region (#E8F4FD, no visible border) behind the entire
  hidden state row, with generous padding
- Above the orange recurrent arrows, a compact annotation in #6B7280:
  "sequential — cannot parallelize"
- A subtle horizontal arrow at the very bottom labeled "Time →" in small
  #6B7280 text

STYLE:
- Background: #FAFCFF. All outlines: #0B5CFF or #6B7280.
- Hidden state blocks: #2D8CFF with subtle shadow.
- Only color outside the blue family: the orange recurrent arrows.
- Clean, modern, Zoom-like tech aesthetic. Not a cartoon, not a whiteboard sketch.
- Match the same node shapes, arrow weights, typography, margins, and subtle
  shadows used by the other Chapter 1 figures.
```

## Review Checklist

- [ ] Exactly 4 time steps shown
- [ ] h_0 is dashed/gray, all others are solid blue
- [ ] Recurrent arrows are orange (#FF9F43), thicker than other arrows
- [ ] All other elements are blue/white/gray — no other colors
- [ ] Arrows go left-to-right for recurrence, bottom-to-top for input/output
- [ ] "tanh" is inside hidden state nodes
- [ ] Overall feel: clean tech blue-white, not colorful/decorative
