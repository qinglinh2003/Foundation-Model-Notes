# Figure 12.4: NF4 vs. INT4 Quantization

**Filename**: `fig_nf4_quantization.png`
**LaTeX label**: `fig:nf4-quantization`
**Caption**: NF4 vs.\ INT4 quantization. INT4 divides the value range into 16 uniform bins, wasting precision on sparsely populated tails and under-serving the dense center where most weights live. NF4 places its 16 representation values at the quantiles of a standard normal distribution, matching the empirical weight distribution and reducing quantization error. The bottom panel shows that real Transformer weights are approximately normal, validating the NF4 assumption.

## Prompt

```text
Draw an NF4 vs INT4 quantization comparison for a machine learning
textbook. Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious. Match the visual richness
of the book's best figures --- Ch10 "Prompt Sensitivity" side-by-side
illusion-vs-reality contrast, Ch4 "Signal Density" token-level detail,
Ch11 "Chat Template Anatomy" three-tier technical layout.

CONCEPT:
"Match the quantization grid to the weight distribution." Neural
network weights after training are approximately normally distributed.
INT4 uses uniform spacing --- wasting bins on sparse tails and
crowding the dense center. NF4 uses the normal distribution's quantiles
as its 16 representation values --- each bin captures equal probability
mass, minimizing expected quantization error for normally distributed
data. The figure should make this insight feel elegant and inevitable.

MAIN COMPOSITION:
SIDE-BY-SIDE COMPARISON (two panels + evidence):

LEFT PANEL --- "INT4: UNIFORM BINS" (~45% width):
A tall white card with thin blue border.

INSIDE THE CARD:
- Draw a smooth bell curve (normal distribution) in pale blue fill
  (#E8F4FD) with a #2D8CFF outline, centered horizontally
- Below the curve, draw a horizontal number line spanning the same
  range as the curve
- Place 16 evenly spaced tick marks on the number line, each with a
  tiny vertical line extending up to the curve
- HIGHLIGHT THE PROBLEM:
  - In the tail regions (leftmost 3 and rightmost 3 ticks), add
    subtle gray shading between ticks and tiny labels: "sparse ---
    few weights here" in very small #6B7280 text
  - In the center region (middle 4-5 ticks), the gaps between ticks
    are the same width as the tails, but the curve is tall above them.
    Add tiny labels: "crowded --- many weights share few bins"
  - Use subtle gray warning markers on the wasted tail bins to draw
    attention without introducing another accent color
- Below the number line: a small quantization error bar, medium length,
  labeled "higher error"
- Card title at top: "INT4: Uniform Spacing"

RIGHT PANEL --- "NF4: NORMAL QUANTILES" (~45% width):
A tall white card with thin blue border.

INSIDE THE CARD:
- Draw the SAME bell curve shape
- Below the curve, draw a horizontal number line with 16 tick marks,
  but now placed at QUANTILE positions: dense near the center (where
  the curve is tall), sparse in the tails (where the curve is low)
- Each tick represents equal area under the curve between adjacent
  ticks --- show this by lightly shading alternate inter-tick regions
  with alternating pale blue (#E8F4FD) and white, making the
  equal-area property visible
- HIGHLIGHT THE SOLUTION:
  - In the center, ticks are closely packed --- "dense where weights
    concentrate"
  - In the tails, ticks are widely spaced --- "sparse where weights
    are rare"
  - The orange accent (#FF9F43) highlights the CENTRAL CLUSTER of
    ticks (the 4-5 ticks near the mean) --- this is the ONLY orange
    in the figure
- Below the number line: a smaller quantization error bar, visibly
  shorter than the INT4 one, labeled "lower error"
- Card title at top: "NF4: Normal Quantiles"

BOTTOM STRIP --- "WHY NORMAL?" (spanning full width):
A thin white card below both panels containing:
- A small histogram on the left showing actual weight values from a
  Transformer layer --- clearly bell-shaped. Label: "Real Transformer
  weights (one layer)"
- Text on the right: "Transformer weights are approximately normally
  distributed after training. NF4 exploits this structure: 16 quantile
  values → each bin holds equal probability mass → minimum expected
  error for this distribution."
- This strip provides the EVIDENCE that justifies NF4's design

CONNECTING ELEMENT:
Between the two panels at the top, a thin dashed arrow labeled
"same weights, different grid" connecting the two curve tops. This
reinforces that the only difference is where you place the ticks.

STYLE:
- Background: #FAFCFF
- Bell curves: #E8F4FD fill, #2D8CFF outline
- INT4 ticks: #6B7280 (gray, uniform)
- NF4 ticks: #2D8CFF (blue, quantile-spaced)
- Orange accent: #FF9F43 ONLY on central NF4 tick cluster
- Error bars: #6B7280 (INT4, longer) and #2D8CFF (NF4, shorter)
- Cards: white with thin #CFE3F7 borders, subtle shadow
- Histogram in bottom strip: pale blue fill (#E8F4FD)
- Text: #1A1A2E for titles, #6B7280 for annotations
- Clean sans-serif typography, generous spacing

IMPORTANT:
- Do not list the exact 16 NF4 codebook values
- Do not use bar charts instead of bell curves
- Do not use 3D, glow, neon, or gradient fills
- Do not use dark backgrounds
- The two panels MUST be the same height and width for direct visual
  comparison --- this parallel structure is the point
- The equal-area shading in the NF4 panel is the key insight --- make
  it clearly visible
- The error bar comparison should be subtle but noticeable
- Keep the bottom evidence strip compact --- it supports, not dominates
```

## Review Checklist

- [ ] Two side-by-side panels with identical bell curves but different tick placement
- [ ] INT4 ticks evenly spaced; NF4 ticks dense at center, sparse at tails
- [ ] Wasted tail bins in INT4 clearly annotated
- [ ] Equal-area shading between NF4 ticks visible (alternating pale fills)
- [ ] Quantization error bars show INT4 > NF4
- [ ] Bottom strip has real weight histogram as evidence
- [ ] "Same weights, different grid" connecting element
- [ ] Orange accent ONLY on central NF4 tick cluster
- [ ] Panels are identical size for parallel comparison
- [ ] Landscape orientation, matches Prompt Sensitivity quality
- [ ] Readable at 50% width in PDF
