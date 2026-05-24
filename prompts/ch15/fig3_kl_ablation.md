# Figure 15.3: KL Constraint Ablation

**Filename**: `fig_kl_ablation.png`
**LaTeX label**: `fig:kl-ablation`
**Caption**: The KL constraint in action. Without KL: reward model score increases monotonically, but human win rate peaks and then decreases -- classic over-optimization. With appropriate KL: reward model score increases more slowly, but human win rate tracks it. The gap between RM score and human win rate is the measure of reward hacking.

## Prompt

```text
Draw a KL constraint ablation figure for a graduate-level machine
learning textbook. Use a clean blue-white visual system: light blue
background, white panels, thin blue borders, charcoal text, and one
soft orange accent for the problematic divergence.

CONCEPT:
Compare RLHF training with and without a KL constraint to the
reference policy. Without KL, the policy over-optimizes the reward
model: proxy reward rises while actual human preference plateaus or
declines. With KL, progress is slower but reward model score and
human quality stay aligned.

MAIN COMPOSITION:
A side-by-side two-panel comparison with rich internal content.

LEFT PANEL -- "WITHOUT KL (beta = 0)":
Inside the panel:
- A line chart with two curves: "RM score" (solid blue, climbing
  steeply upward) and "human win rate" (dashed blue, rising then
  bending downward after a peak)
- Use the orange accent to shade or highlight the widening gap
  between the two curves after the peak -- this is the visual
  punchline
- Below the chart, show 2-3 small response snippet cards that
  progressively degrade: first card is clean and helpful, second
  is verbose with bullet formatting, third is sycophantic with
  excessive hedging
- Small label: "proxy reward rises, human quality falls"

RIGHT PANEL -- "WITH KL (beta > 0)":
Inside the panel:
- Same two-curve chart, but both curves rise together more slowly
  and stay close to each other throughout training
- A small "elastic tether" icon connecting a blue policy block to
  a gray reference block with a lock icon -- visually representing
  the KL constraint holding the policy near the reference
- Below the chart, show 2-3 response snippet cards that stay
  consistently clean and helpful
- Small label: "controlled drift, aligned improvement"

CENTER DIVIDER:
A thin vertical divider between panels with a compact label:
"KL controls policy drift"

BOTTOM STRIP:
A thin strip below both panels showing three roles of KL with small
icons:
- Shield icon: "reward model regularization"
- Book icon: "capability preservation"
- Tree/branch icon: "output diversity"

STYLE:
- Background: #FAFCFF
- Panels: white with thin #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF for curves and healthy elements
- Pale blue fills: #E8F4FD
- Orange accent: #FF9F43 only for the proxy-human divergence gap
- Frozen reference: light gray #E5E7EB with lock icon
- Text: #1A1A2E; secondary labels: #6B7280
- Clean axes with minimal tick labels; no grid lines
- Landscape orientation

IMPORTANT:
- Do not make the charts look like stock market graphs
- Do not use red or warning triangles
- Do not imply KL eliminates all problems; show it as control, not
  a complete solution
- The orange-shaded divergence gap is the most important visual
  element -- it must be immediately visible
- Keep all labels short and readable at 50% page width
- Response snippet cards should be tiny but suggestive, not text-heavy
```

## Review Checklist

- [ ] Two panels: without KL and with KL
- [ ] Without-KL panel shows diverging RM score vs human win rate
- [ ] Orange accent highlights the proxy-human gap
- [ ] With-KL panel shows aligned curves
- [ ] Elastic tether icon connects policy to reference
- [ ] Response snippets show degradation (left) vs consistency (right)
- [ ] Bottom strip shows three KL roles with icons
- [ ] Center divider label present
- [ ] Blue-white palette, no red or dark backgrounds
- [ ] Readable at 50% width in PDF
