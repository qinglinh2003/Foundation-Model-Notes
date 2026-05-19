# Figure 6.4: Loss Spikes and Silent Failures at Scale

**Filename**: `loss_spike.png`
**LaTeX label**: `fig:loss-spike`
**Caption**: Training loss curves at different scales. Left: MiniGPT's smooth, predictable descent (Project 1). Right: a large-model training run showing a loss spike at step ~35K that partially recovers but settles at a higher loss than the pre-spike trajectory (dashed). Silent quality degradation may not be visible from the loss curve alone.

## Prompt

```text
Draw a two-panel loss curve comparison for a graduate-level machine learning
textbook. Use the course's blue-white visual system. Landscape orientation,
polished editorial style.

Purpose:
- The figure should teach that large-model training has failure modes that
  small models never encounter: loss spikes, partial recovery, and silent
  quality degradation.
- The main visual message is: at scale, the most dangerous failures look
  almost normal on the loss curve.

LAYOUT:
Two panels side by side, each showing a training loss (y-axis) vs steps
(x-axis) curve.

LEFT PANEL — MiniGPT (Small Model):
Title: "MiniGPT (3.7M)"

- A single smooth, monotonically decreasing blue curve
- Starts at ~7.6, drops steeply, then gradually flattens to ~3.1
- X-axis: "Steps" from 0 to 10K
- Y-axis: "Training Loss"
- The curve is clean — no spikes, no noise, no drama
- Small annotation: "Smooth, predictable"
- A small green/blue checkmark badge

RIGHT PANEL — Large Model:
Title: "Large LLM (~7B)"

- A blue curve that starts high, descends smoothly for the first ~35K steps
- At step ~35K, a SUDDEN SPIKE upward (loss jumps from ~2.8 to ~4.5)
- After the spike, the curve recovers but settles at ~3.0 instead of
  the ~2.6 it was trending toward
- A dashed blue line showing the "expected trajectory" (what the curve
  would have looked like without the spike) — this dashed line continues
  to ~2.6
- The GAP between the actual curve (~3.0) and the expected trajectory
  (~2.6) is labeled: "Silent quality gap"
- X-axis: "Steps" from 0 to 100K
- Y-axis: "Training Loss"
- The spike region highlighted with a subtle background shading

The ONE orange accent (#FF9F43) is: the loss spike itself (the sharp
upward jump at step ~35K), and the "Silent quality gap" label. This
draws attention to the two key dangers: the spike AND the permanent
quality loss that follows it.

BOTTOM ANNOTATION (spanning both panels):
"At small scale, training is smooth and mistakes are cheap. At large
scale, a single loss spike can permanently degrade final model quality."

STYLE LOCK:
- Match the course's Zoom-inspired blue-white textbook visual system.
- Background: #FAFCFF
- Loss curves: thick #2D8CFF lines
- Expected trajectory dashed line: #2D8CFF dashed
- Axis lines and ticks: #6B7280 steel gray
- Grid: very faint gray dashed
- Orange accent: #FF9F43 ONLY on the spike and "Silent quality gap" label
- Text: #1A1A2E charcoal, sans-serif
- Clean, minimal plot styling — no heavy gridlines or box frames

DO NOT: cartoon style, photorealism, clip art, SaaS dashboard, heavy 3D,
neon, rainbow, coral, teal, purple, green, decorative borders, abstract
background patterns, complex formulas, data points/scatter.
```

## Review Checklist

- [ ] Two panels: MiniGPT (smooth) and Large LLM (spike)
- [ ] Left panel shows clean monotonic descent
- [ ] Right panel shows smooth descent then sudden spike at ~35K
- [ ] Spike recovers but to a HIGHER loss than pre-spike trajectory
- [ ] Dashed line shows expected trajectory without spike
- [ ] "Silent quality gap" labeled between actual and expected curves
- [ ] Orange accent ONLY on spike and quality gap label
- [ ] Different x-axis scales (10K vs 100K) reflecting different training lengths
- [ ] Bottom annotation about small vs large scale failure modes
- [ ] No extra colors beyond blue + white + orange + gray
