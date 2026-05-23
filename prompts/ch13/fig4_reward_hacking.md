# Figure 13.2: Reward Hacking

**Filename**: `fig_reward_hacking.png`
**LaTeX label**: `fig:reward-hacking`
**Caption**: Reward hacking. As the policy optimizes against the reward model, RM reward increases monotonically (blue curve), but true human preference (orange curve) peaks and then declines. The gap between the two curves is the over-optimization region---the policy has learned to exploit the RM's blind spots rather than genuinely improve. The KL constraint limits how far the policy can drift from the reference, keeping it in the region where RM reward and human preference are correlated.

## Prompt

```text
Draw a reward hacking and over-optimization diagram for a graduate-level
machine learning textbook. Use a clean blue-white visual system:
light blue background, white panels, thin blue borders, charcoal text,
and one soft orange accent for the failure region.

CONCEPT:
Optimizing a reward model too hard can improve the proxy score while
making humans like the model less. The figure should show the divergence
between proxy reward and true human preference, with KL control keeping
training in the useful region.

MAIN COMPOSITION:
A large central chart fills about 70% of the canvas width. A right-side
diagnostic panel fills the remaining 30%. Use a bottom annotation strip
for the practical lesson.

CENTRAL CHART:
Axes:
- x-axis: "optimization strength / training steps"
- y-axis: "score"
Curves:
- Blue curve: "reward model score" rises steadily and then plateaus
- Orange curve: "human preference" rises at first, peaks, then declines
The orange curve is the only orange element.

REGIONS:
Divide the x-axis into three softly shaded vertical bands:
1. "Under-optimized": both scores low
2. "Useful optimization": both scores improve together
3. "Over-optimization": RM score rises while human preference falls
The over-optimization band should have a light orange tint.

KL CONTROL:
Place a vertical dashed blue line near the peak of the human preference
curve labeled "KL constraint / early stopping". The line should indicate
where training should stop before reward hacking dominates.

RIGHT DIAGNOSTIC PANEL:
Create three stacked mini-cards:
1. "Proxy improves": small gauge moving upward
2. "Behavior degrades": response bubble becomes verbose or generic
3. "Human raters disagree": two small rater icons with warning symbol
Keep these as simple blue line illustrations.

BOTTOM STRIP:
One-sentence lesson in a white strip:
"A reward model is a proxy. Optimize it enough to improve behavior,
not so much that the policy learns its blind spots."

STYLE:
- Background: #FAFCFF
- Main chart panel: white with thin #CFE3F7 border
- Blue curve and labels: #2D8CFF
- Orange curve and over-optimization band: #FF9F43
- Grid lines: very light #E8F4FD
- Text: #1A1A2E; secondary text: #6B7280
- Clean sans-serif typography
- Landscape orientation, chart-first layout

IMPORTANT:
- Do not use red alert styling; keep the failure region soft orange
- Do not make the chart mathematically busy
- Do not use 3D plots or glossy effects
- The two curves must clearly separate in the over-optimization region
- The KL stopping line must be visually connected to the useful region
```

## Review Checklist

- [ ] Central chart with RM reward increasing and human preference peaking
- [ ] Over-optimization region clearly shaded
- [ ] Dashed KL / early stopping line before collapse
- [ ] Right diagnostic panel with three mini-cards
- [ ] Bottom lesson strip
- [ ] Orange used only for human preference curve and failure region
- [ ] Readable at 50% width in PDF

