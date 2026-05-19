# Figure 1.5: GRU Cell Diagram

**Filename**: `gru_cell.png`
**LaTeX label**: `fig:gru-cell`
**Caption**: Internal structure of a GRU cell. Unlike the LSTM, the GRU has no separate cell state---the hidden state $\mathbf{h}_t$ serves as both memory and output. The update gate $\mathbf{z}_t$ merges the roles of the LSTM's forget and input gates, while the reset gate $\mathbf{r}_t$ controls how much past state enters the candidate computation.

## Prompt

```
Draw a technically precise GRU (Gated Recurrent Unit) cell diagram for a
machine learning textbook. Use the course's Zoom-inspired blue-white visual
system. The figure should be polished and editorial, not a rough whiteboard
sketch.

OVERALL LAYOUT:
- Landscape orientation, generous whitespace
- Inputs enter from the left: h_{t-1} (previous hidden state) and x_t
  (current input), shown as merging arrows at bottom-left
- Output h_t exits to the right
- The diagram should clearly show that there is NO separate cell state
  (unlike the LSTM) — only one hidden state flowing through

KEY STRUCTURAL DIFFERENCE FROM LSTM:
- The GRU has NO cell state highway at the top. Instead, the hidden state
  itself is the only state, updated via a linear interpolation controlled
  by the update gate.
- The final equation is: h_t = (1 - z_t) * h_{t-1} + z_t * h_tilde
- This interpolation should be the visual centerpiece: show h_{t-1} and h_tilde
  being mixed by z_t, with a clear "interpolation" structure

TWO GATES (use different SHADES OF BLUE to distinguish):

1. RESET GATE (left):
   - Rounded rectangle labeled "σ" with subtitle "reset"
   - Fill: #0B5CFF (deep blue), white text
   - Produces r_t
   - r_t multiplies (⊗) h_{t-1} BEFORE it enters the candidate computation
   - This means: reset gate controls how much old state is visible when
     computing the new candidate

2. UPDATE GATE (right):
   - Rounded rectangle labeled "σ" with subtitle "update"
   - Fill: #2D8CFF (Zoom Blue), white text
   - Produces z_t
   - z_t controls the interpolation between h_{t-1} and h_tilde
   - Show this as: (1 - z_t) path from h_{t-1} and z_t path from h_tilde,
     merging at an ADD node (⊕) to produce h_t

CANDIDATE STATE:
- A tanh box labeled "tanh" with subtitle "candidate"
- Fill: #E8F4FD (ice blue), dark text
- Takes "[r_t * h_{t-1}, x_t]" as input
- Produces h_tilde
- Use the plain label "h_tilde" in the image if the model struggles with
  h-tilde notation; exact math notation can be handled in the caption

THE INTERPOLATION (hero element, use orange accent):
- The final mixing of h_{t-1} and h_tilde should be visually prominent
- Use #FF9F43 (soft orange) for the interpolation region or the mixing
  arrows/node to highlight this as the key mechanism
- Show clearly: when z_t ≈ 0, output ≈ h_{t-1} (copy old state);
  when z_t ≈ 1, output ≈ h_tilde (use new candidate)
- This is the ONE orange accent in the figure

OPERATION NODES:
- Multiply nodes: white circles with "×" inside, thin #0B5CFF outline,
  very subtle shadow
- Add/interpolation node: white circle with "+" inside, same style
- "1 - z_t" node: small box or annotation showing the complement

SIGNAL LABELS:
- Every signal line labeled: h_{t-1}, h_t, x_t, z_t, r_t, h_tilde
- Also label the (1 - z_t) path explicitly
- Labels in #1A1A2E charcoal, crisp sans-serif
- Keep labels short and readable. Prefer "h_tilde" over ornate math typography
  if the generated text becomes unclear.

ARROWS:
- All arrows: #0B5CFF (deep blue) or #6B7280 (steel gray for secondary paths)
- Smooth, medium weight, clean pointed heads
- Input concatenation [x_t, h_{t-1}] shown as merging arrows

STYLE:
- Background: #FAFCFF
- Very subtle blue-tinted shadows on gate boxes
- Only non-blue color: the orange interpolation highlight
- Clean, modern, Zoom-like tech aesthetic
- Match the same rounded geometry, line weights, typography, margins, and
  subtle shadows used by the LSTM cell diagram (Figure 1.2)
```

## Review Checklist

- [ ] NO cell state highway at the top (this is NOT an LSTM)
- [ ] Only TWO gates: reset and update (not three)
- [ ] Both gates in different shades of blue (deep blue and Zoom blue)
- [ ] Reset gate multiplies h_{t-1} BEFORE it enters the tanh candidate box
- [ ] Update gate controls the interpolation between h_{t-1} and h_tilde
- [ ] The interpolation h_t = (1-z_t)·h_{t-1} + z_t·h_tilde is visually clear
- [ ] Orange accent is on the interpolation mechanism (not on a gate)
- [ ] All signal labels present: h_{t-1}, h_t, x_t, z_t, r_t, h_tilde, (1-z_t)
- [ ] No separate cell state c_t visible anywhere
- [ ] Visual style matches the LSTM cell diagram (same palette, geometry, shadows)
