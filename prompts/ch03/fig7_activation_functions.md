# Figure 3.7: Activation Function Evolution: ReLU → GELU → SwiGLU

**Filename**: `activation_functions.png`
**LaTeX label**: `fig:activation-functions`
**Caption**: Activation function evolution in Transformer FFNs. \textbf{Left:} ReLU hard-kills all negative inputs, creating dead neurons. \textbf{Center:} GELU softly attenuates negative inputs, reducing dead neurons. \textbf{Right:} SwiGLU adds a learned gate that controls which dimensions activate, at the cost of a third weight matrix. The shaded region in each plot highlights the "dead zone" where the activation outputs zero or near-zero.

## Prompt

```
Draw a three-panel comparison of activation functions for a
machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
The figure should be polished and editorial.

LAYOUT: Three panels side by side, each showing a function plot.

PANEL 1 — "ReLU" (left)
- x-axis: input z, range [-3, 3]
- y-axis: output, range [-1, 3]
- Plot: ReLU(z) = max(0, z)
  - For z < 0: flat at 0 (dead zone)
  - For z > 0: linear with slope 1
- Line color: medium blue (#2563EB), thick (2pt)
- Shade the z < 0 region in light orange (#FFE0C2) and label
  it "dead zone — gradient = 0"
- Title: "ReLU"
- Small annotation: "Hard cutoff at 0"

PANEL 2 — "GELU" (center)
- Same axes as Panel 1
- Plot: GELU(z) ≈ z · Φ(z) where Φ is the standard normal CDF
  - Smooth S-curve transition near 0
  - Slightly negative output for inputs near -1 to -2
  - Linear for large positive z
- Line color: medium blue (#2563EB), thick (2pt)
- Shade a narrow region around z ∈ [-2, 0] in very light
  orange (#FFF0E0) and label "soft attenuation"
- Title: "GELU"
- Small annotation: "Smooth transition — fewer dead neurons"

PANEL 3 — "SwiGLU" (right)
- This panel should show a CONCEPTUAL diagram, not a function
  plot, because SwiGLU involves two inputs
- Show two input paths:
  - Top path: "z · W_gate" → Swish activation → gate signal
  - Bottom path: "z · W_up" → content signal
- An element-wise multiply node (⊙) combines them
- Then "W_down" projects the result back
- Gate path in medium blue, content path in light blue
- The ⊙ node highlighted in orange (#FF9F43)
- Title: "SwiGLU"
- Small annotation: "Learned gate controls which dims activate"

SHARED ANNOTATIONS:
- Below all three panels, a timeline arrow:
  "Transformer (2017) → GPT-2/BERT (2018-19) → LLaMA (2023)"
  with dots marking which activation each era used
- Arrow in light gray, dots in charcoal

VISUAL STYLE:
- Clean axes with minimal tick marks
- Grid lines: very faint gray, only major ticks
- Sans-serif labels in charcoal (#374151)
- White background (#FAFCFF)
- No shadows, no 3D
- Orange accent used only for dead zone shading and SwiGLU gate node
- Polished editorial textbook figure style
```

## Review Checklist

- [ ] Three panels: ReLU, GELU, SwiGLU
- [ ] ReLU shows hard cutoff, GELU shows smooth transition
- [ ] SwiGLU shown as gating diagram (not a simple function plot)
- [ ] Dead zone / attenuation zone visually highlighted
- [ ] Timeline below connects to historical usage
- [ ] Orange accent used sparingly (dead zones + gate node only)
- [ ] All labels readable and mathematically correct
