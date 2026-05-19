# Figure 1.2: LSTM Cell Diagram

**Filename**: `lstm_cell.png`
**LaTeX label**: `fig:lstm-cell`
**Caption**: Internal structure of an LSTM cell. The cell state $c_t$ flows along the top ``highway,'' modulated by three gates: the forget gate $f_t$ selectively erases, the input gate $i_t$ selectively writes, and the output gate $o_t$ controls what is exposed as the hidden state $h_t$.

## Prompt

```
Draw a technically precise LSTM cell diagram for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system. The figure should be
polished and editorial, not a rough whiteboard sketch.

OVERALL LAYOUT:
- Landscape orientation, generous whitespace
- The cell state "highway" runs horizontally across the TOP, from c_{t-1}
  on the left to c_t on the right
- Inputs (x_t and h_{t-1}) enter from the bottom-left
- Output h_t exits to the right

CELL STATE HIGHWAY (the hero element):
- Draw as a wide, prominent horizontal band in #FF9F43 (soft orange) —
  this is the ONE orange accent in the figure, representing the memory path
- Label "c_{t-1}" on the left entry and "c_t" on the right exit
- This should be the most visually striking element

THREE GATES (use different SHADES OF BLUE to distinguish):

1. FORGET GATE (leftmost on the highway):
   - Rounded rectangle labeled "σ" with subtitle "forget"
   - Fill: #0B5CFF (deep blue), white text
   - Produces f_t
   - Connects to a multiply node (⊗) on the cell state highway

2. INPUT GATE (middle):
   - Rounded rectangle labeled "σ" with subtitle "input"
   - Fill: #2D8CFF (Zoom Blue), white text
   - Paired with a tanh candidate box (fill: #E8F4FD ice blue, dark text,
     labeled "tanh") that produces candidate c̃_t
   - Their outputs multiply (⊗), then feed into an ADD node (⊕) on the highway

3. OUTPUT GATE (rightmost):
   - Rounded rectangle labeled "σ" with subtitle "output"
   - Fill: #5BA3FF (lighter blue), white text
   - A tanh is applied to c_t, then multiplied (⊗) by o_t to produce h_t

The three gates are ALL BLUE but distinguishable by shade:
deep blue → medium blue → lighter blue (left to right).

OPERATION NODES:
- Multiply nodes (⊗): white circles with "×" inside, thin #0B5CFF outline,
  very subtle shadow
- Add node (⊕): white circle with "+" inside, same style

SIGNAL LABELS:
- Every signal line labeled: c_{t-1}, c_t, h_{t-1}, h_t, x_t, f_t, i_t, o_t, c̃_t
- Labels in #1A1A2E charcoal, crisp sans-serif

ARROWS:
- All arrows: #0B5CFF (deep blue) or #6B7280 (steel gray for secondary paths)
- Smooth, medium weight, clean pointed heads
- Input concatenation [x_t, h_{t-1}] shown as merging arrows at bottom-left

STYLE:
- Background: #FAFCFF
- Very subtle blue-tinted shadows on gate boxes
- Only non-blue color: the orange cell state highway
- Clean, modern, Zoom-like tech aesthetic
- Match the same rounded geometry, line weights, typography, margins, and subtle
  shadows used by the other Chapter 1 figures.
```

## Review Checklist

- [ ] Cell state flows LEFT to RIGHT at the top as a prominent orange highway
- [ ] Three gates present, ALL in different shades of blue (no coral/purple/teal)
- [ ] Forget gate MULTIPLIES c_{t-1} (not adds)
- [ ] Input gate output and candidate are multiplied, then ADDED to cell state
- [ ] Output gate multiplies tanh(c_t) to produce h_t
- [ ] All signal labels are present and correct
- [ ] Only orange element is the cell state highway — everything else is blue/white/gray
