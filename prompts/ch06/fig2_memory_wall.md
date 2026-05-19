# Figure 6.2: The Memory Wall — Training State Breakdown

**Filename**: `memory_wall.png`
**LaTeX label**: `fig:memory-wall`
**Caption**: Training memory breakdown by component for six model sizes under bf16 mixed-precision training. Optimizer states (Adam m and v in fp32) dominate at every scale. Horizontal reference lines show the VRAM of mainstream and frontier GPUs, from RTX 4090 (24\,GB) through H200 (141\,GB), B200 (192\,GB), and B300 / Blackwell Ultra (288\,GB). At 7B parameters the training state exceeds an H100 but fits an H200; at 13B it exceeds an H200 but fits within the Blackwell generation; at 70B no single GPU suffices.

## Prompt

```text
Draw a stacked bar chart showing GPU memory breakdown for training
at different model scales, for a graduate-level machine learning textbook.
Use the course's blue-white visual system. Landscape orientation, polished
editorial style.

Purpose:
- The figure should teach that training memory is dominated by optimizer
  states (not model weights), and that beyond ~1B parameters, no single
  GPU can hold the full training state.
- The main visual message is: the memory wall is what makes distributed
  training necessary.
- Secondary message: GPU memory generations matter. A model that is
  impossible on an H100 can become single-GPU feasible on H200/B200/B300,
  but 70B-class training still requires sharding across many GPUs.

LAYOUT:
A horizontal bar chart with 6 bars (one per model scale), stacked by
memory component. Each bar grows left to right. Use a LOG-SCALE x-axis
(base 10) so that all 6 bars are visible — linear scale would make the
small models invisible next to 70B.

BAR 1 — MiniGPT (3.7M, fp32):
- Total: ~0.2 GB
- Components stacked:
  - Parameters (0.015 GB) — dark blue #0B5CFF
  - Gradients (0.015 GB) — medium blue #2D8CFF
  - Adam m (0.015 GB) — light blue #5BA8FF
  - Adam v (0.015 GB) — pale blue #A3D0FF
  - Activations (~0.1 GB) — ice blue #E8F4FD

BAR 2 — 300M (bf16 mixed-precision):
- Total: ~7 GB
- Components stacked:
  - Parameters bf16 (0.6 GB) — dark blue
  - Gradients bf16 (0.6 GB) — medium blue
  - Adam m fp32 (1.2 GB) — light blue
  - Adam v fp32 (1.2 GB) — pale blue
  - Activations (~3 GB) — ice blue

BAR 3 — 1B (bf16 mixed-precision):
- Total: ~20 GB
- Components stacked:
  - Parameters bf16 (2 GB) — dark blue
  - Gradients bf16 (2 GB) — medium blue
  - Adam m fp32 (4 GB) — light blue
  - Adam v fp32 (4 GB) — pale blue
  - Activations (~8 GB) — ice blue

BAR 4 — 7B (bf16 mixed-precision):
- Total: ~128 GB
- Components stacked:
  - Parameters bf16 (14 GB) — dark blue
  - Gradients bf16 (14 GB) — medium blue
  - Adam m fp32 (28 GB) — light blue
  - Adam v fp32 (28 GB) — pale blue
  - Activations (~44 GB) — ice blue

BAR 5 — 13B (bf16 mixed-precision):
- Total: ~238 GB
- Components stacked:
  - Parameters bf16 (26 GB) — dark blue
  - Gradients bf16 (26 GB) — medium blue
  - Adam m fp32 (52 GB) — light blue
  - Adam v fp32 (52 GB) — pale blue
  - Activations (~82 GB) — ice blue

BAR 6 — 70B (bf16 mixed-precision):
- Total: ~1270 GB (1.27 TB)
- Components stacked (same color scheme, much longer bar):
  - Parameters bf16 (140 GB) — dark blue
  - Gradients bf16 (140 GB) — medium blue
  - Adam m fp32 (280 GB) — light blue
  - Adam v fp32 (280 GB) — pale blue
  - Activations (~430 GB) — ice blue

GPU CAPACITY REFERENCE LINES (vertical dashed lines):
- 24 GB — labeled "RTX 4090 (24 GB)" — gray dashed, thin
- 40 GB — labeled "A100-40GB" — gray dashed, thin
- 48 GB — labeled "A40 (48 GB)" — gray dashed, thin
- 80 GB — labeled "A100-80GB / H100 (80 GB)" — gray dashed, medium thickness
- 141 GB — labeled "H200 (141 GB)" — gray dashed, medium thickness
- 192 GB — labeled "B200 (192 GB)" — gray dashed, slightly thicker
- 288 GB — labeled "B300 / Blackwell Ultra (288 GB)" — gray dashed, thickest

These lines create visual "walls" that the bars crash into. Six GPU
reference levels spanning from consumer (24 GB) to frontier datacenter
(288 GB) show how each generation pushes the memory wall further out
— but even the biggest single-GPU reference cannot hold a 70B training state.

VISUAL EMPHASIS:
- The 300M bar fits within the 24 GB line — trainable on a single
  consumer GPU.
- The 1B bar sits just under the RTX 4090 24 GB line — possible but
  tight once real framework overhead is included.
- The 7B bar (~128 GB) blows past H100 (80 GB) but fits within
  H200 (141 GB) — showing that H200's extra HBM3e memory was
  specifically designed for this regime.
- The 13B bar (~238 GB) exceeds H200 and B200, but fits within
  B300 / Blackwell Ultra (288 GB) — the frontier single-GPU boundary.
- The 70B bar (~1.27 TB) extends far beyond ALL single-GPU lines
  — clearly needs a multi-GPU cluster regardless of hardware generation.

The ONE orange accent (#FF9F43) is: the portion of the 7B bar that
extends BEYOND the 80 GB H100 line but stays within the H200 line.
This visually shows that H100 cannot hold 7B training, but H200 can
— illustrating how GPU memory evolution tracks model size growth.

LEGEND:
A horizontal legend below the chart:
- Dark blue: Parameters (bf16)
- Medium blue: Gradients (bf16)
- Light blue: Adam m (fp32)
- Pale blue: Adam v (fp32)
- Ice blue: Activations (estimated)

BOTTOM ANNOTATION (centered, smaller text):
"Mixed-precision training: weights and gradients in bf16, optimizer states
in fp32. Adam m/v alone consume 8 bytes per parameter; persistent training
state is about 12 bytes per parameter before activations."

RIGHT-SIDE ANNOTATION (next to 70B bar):
"~1.27 TB — requires sharding across dozens of GPUs"

STYLE LOCK:
- Match the course's Zoom-inspired blue-white textbook visual system.
- Background: #FAFCFF
- Use the 5-shade blue progression described above for stacking
- Text: #1A1A2E (charcoal)
- Secondary text / axis labels: #6B7280 (steel gray)
- GPU reference lines: #9CA3AF (light gray) dashed
- Orange accent: #FF9F43 (ONLY on the overflow portion of the 7B bar)
- Clean vector geometry, sans-serif labels, generous margins.
- Landscape layout. Modern tech aesthetic.
- Y-axis labels: model names and param counts.
- X-axis: "Training Memory (GB)" with LOG SCALE (base 10), tick marks
  at 0.1, 1, 10, 100, 1000 GB.

DO NOT: cartoon style, photorealism, clip art, SaaS dashboard, heavy 3D,
neon, rainbow, coral, teal, purple, green, decorative borders, abstract
background patterns, complex formulas, pie charts, linear scale.
```

## Review Checklist

- [ ] Six horizontal stacked bars: MiniGPT / 300M / 1B / 7B / 13B / 70B
- [ ] Five components per bar with consistent 5-shade blue color coding
- [ ] Log-scale x-axis so all bars are visible
- [ ] Seven GPU capacity reference lines: 24GB, 40GB, 48GB, 80GB, 141GB, 192GB, 288GB
- [ ] GPU labels clearly readable (RTX 4090, A100-40GB, A40, A100-80/H100, H200, B200, B300)
- [ ] 7B bar exceeds H100 80GB but fits within H200 141GB
- [ ] 13B bar exceeds H200 141GB and B200 192GB but fits within B300 288GB
- [ ] Orange accent on the 7B bar portion between H100 (80GB) and H200 (141GB)
- [ ] 70B bar extends far right with "~1.27 TB" annotation
- [ ] Legend shows all five components with correct colors
- [ ] Bottom annotation about mixed-precision memory breakdown
- [ ] Bars are proportionally sized on log scale
- [ ] MiniGPT bar is small but still visible (log scale helps)
- [ ] No extra colors beyond blue shades + orange + gray
