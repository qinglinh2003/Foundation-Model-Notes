# Figure 5.5: Learning Rate Schedules

**Filename**: `lr_schedule.png`
**LaTeX label**: `fig:lr-schedule`
**Caption**: Learning rate schedules for Transformer training. Left: constant learning rate — often unstable for Transformers. Center: warmup + constant — linear ramp from zero prevents early instability. Right: warmup + cosine decay — the standard recipe.

## Prompt

```
Draw a three-panel learning rate schedule comparison for a graduate-level machine
learning textbook. Use the course's blue-white visual system. Landscape orientation,
polished editorial style.

LAYOUT:
Three panels side by side, each showing a learning rate (y-axis) vs training steps
(x-axis) curve. All three share the same axis scale for direct comparison.

LEFT PANEL — CONSTANT LR:
- Title: "Constant"
- A flat horizontal line at η_max from step 0 to the end
- Below the curve: a small annotation in orange "Often unstable for Transformers"
- An orange lightning bolt or warning icon at the beginning (early training danger)
- Shaded region near the start labeled "danger zone: noisy gradients"

CENTER PANEL — WARMUP + CONSTANT:
- Title: "Warmup + Constant"
- A linear ramp from 0 to η_max over the first ~10% of steps
- Then flat at η_max for the rest
- The warmup region has a light blue shading
- Annotation on the ramp: "Linear warmup"
- Small note: "Prevents early instability"

RIGHT PANEL — WARMUP + COSINE DECAY:
- Title: "Warmup + Cosine Decay"
- Linear ramp from 0 to η_max over first ~10% of steps
- Then smooth cosine curve descending from η_max to η_min (~0.1 × η_max)
- The warmup region has light blue shading
- The cosine decay region has a very subtle gradient fill
- Annotations:
  - On ramp: "Warmup"
  - On peak: "η_max"
  - On the cosine portion: "Cosine decay"
  - At the end: "η_min"
- A blue "Standard" badge on this panel to indicate it is the recommended
  approach
- This panel should feel slightly emphasized (like the "Goldilocks" panel in Fig 5.1)

AXIS LABELS:
- Y-axis: "Learning Rate (η)" — same scale across all three
- X-axis: "Training Steps" — same scale across all three
- Mark "η_max" and "η_min" on the y-axis of the right panel
- Mark "t_warmup" on the x-axis where warmup ends

VISUAL DETAILS:
- Curves: thick blue (#2D8CFF) lines, smooth
- Background: white (#FAFCFF)
- Axis lines and ticks: steel gray (#6B7280)
- Grid: very faint gray dashed lines
- The orange accent: ONLY on the "danger zone" annotation in the left panel
- The right panel's "Standard" badge should be a subtle blue highlight
- Each panel is a clean mini-plot with consistent styling
- Sans-serif labels
- The three panels should be the same height and width
- At the bottom, a single annotation spanning all three:
  "Why warmup? Early gradients are noisy. Large steps on noisy estimates = catastrophe."
```

## Review Checklist

- [ ] Three panels: Constant / Warmup+Constant / Warmup+Cosine
- [ ] Same axis scale across all three for direct comparison
- [ ] Constant shows flat line with "danger" annotation
- [ ] Warmup shows linear ramp followed by flat
- [ ] Cosine shows linear ramp + smooth cosine decay curve
- [ ] η_max and η_min labeled on y-axis
- [ ] t_warmup labeled on x-axis
- [ ] Right panel emphasized as the "standard" approach
- [ ] Orange accent ONLY on the "danger zone" in left panel
- [ ] Bottom annotation explains the "why" of warmup
- [ ] No extra colors beyond blue + white + orange + gray
