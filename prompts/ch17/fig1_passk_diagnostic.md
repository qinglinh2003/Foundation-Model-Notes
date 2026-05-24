# Figure 17.1: The Pass@k Diagnostic

**Filename**: `fig_passk_diagnostic.png`
**LaTeX label**: `fig:passk-diagnostic`
**Caption**: The pass@k diagnostic. Low-k accuracy measures user-facing single-attempt performance. High-k accuracy probes the breadth of the model's accessible solution space. If RL improves pass@1 but the base model catches up at large k, the evidence points toward sampling efficiency and support narrowing, not an expanded capability boundary.

## Prompt

```text
Draw a pass@k diagnostic chart for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
The figure teaches that pass@1 and high-k pass rates measure different kinds of capability. RL can improve low-k success while the base model retains broader high-k solution support.

MAIN COMPOSITION:
LEFT PANEL: PASS@K CURVES
Create a clean line chart with x-axis labeled k = 1, 4, 16, 64, 256, 1024 and y-axis labeled pass@k. Draw two curves: Base Model in medium blue starts low at k=1 then climbs steadily and crosses near high k; RL-Tuned Model in orange starts high at k=1 but plateaus slightly lower. Mark the crossover near k=256 with a small callout: "base catches up at large k".

RIGHT PANEL: TWO DEFINITIONS OF CAPABILITY
Two stacked definition cards. Top card: "User-facing capability" with a single sample icon and label "pass@1 / low-k success". Bottom card: "Distributional capability" with a fan of many sampled paths and label "high-k support / solution breadth". Use small path icons: successful paths with blue check marks, failed paths in pale gray.

BOTTOM STRIP: INTERPRETATION
Full-width banner: "RL may improve sampling efficiency without expanding the capability boundary." Include a small probability-mass icon: orange mass concentrated on one good path, blue mass spread across many paths.

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — use only for the RL curve and crossover callout
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
- Do not make the chart look like a business dashboard.
- Do not include tiny unreadable axis labels.
- Do not imply RL is bad; show two valid capability definitions.
- Keep the orange accent limited to the RL-tuned curve and one callout.
- Fill the full canvas; no empty right side.
- All text must be readable at 50% PDF width.
```

## Review Checklist

- [ ] X-axis contains k = 1 through 1024.
- [ ] Base curve catches up or crosses at large k.
- [ ] RL curve wins clearly at low k.
- [ ] Two capability definitions are visually distinct.
- [ ] Bottom interpretation banner is present.
- [ ] Orange is used only for the RL curve/callout.
- [ ] No empty corners.
- [ ] All labels are readable.
