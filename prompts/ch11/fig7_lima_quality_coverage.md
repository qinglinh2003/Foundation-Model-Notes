# Figure 11.7: The LIMA Quality--Coverage Trade-Off

**Filename**: `fig_lima_quality_coverage.png`
**LaTeX label**: `fig:lima-quality-coverage`
**Caption**: The LIMA quality--coverage trade-off. Small, carefully curated datasets can strongly redirect capable base models, but coverage becomes the limiting factor as task diversity grows. The practical question is not quality versus scale; it is how much curated coverage the model needs at its capability level.

## Prompt

```text
Draw a quality-versus-coverage landscape for instruction tuning datasets in a
machine learning textbook. Use the course's Zoom-inspired blue-white visual
system. LANDSCAPE orientation, wide and spacious. Match the visual richness of
Ch8 "Compute Hyperbola" and Ch10 "Benchmark Decay Cycle": dense but readable
internal annotations, concrete dataset markers, and a visual trade-off rather
than a plain chart.

CONCEPT:
"LIMA is not quality instead of scale; it is quality under a coverage constraint."
The figure should visualize why 1K excellent examples can work surprisingly well
for a capable base model, but broader task coverage still matters.

MAIN COMPOSITION:
A large two-axis landscape:
- x-axis: "curated coverage" from narrow to broad
- y-axis: "demonstration quality" from noisy to excellent

Place four dataset bubbles:
- LIMA: high quality, narrow coverage, labeled "1K curated"
- Alpaca: medium quality, broader coverage, labeled "52K synthetic"
- FLAN-style templates: broad coverage, lower/medium quality, labeled
  "template scale"
- Tulu-style mixture: broad coverage, high filtered quality, labeled
  "mixed + filtered"

VISUAL STRUCTURE:
Add two translucent regions:
1. Upper-left region: "surface existing capability" with a small 65B base-model
   chip behind the LIMA bubble.
2. Upper-right region: "robust assistant coverage" with many task icons: chat,
   code, math, writing, multilingual, safety.

Add a diagonal "quality frontier" curve across the plot. Use soft orange
(#FF9F43) only to highlight the tension label:
"quality alone is not coverage."

BOTTOM STRIP:
Add a small strip comparing model scale:
"larger base model -> less coverage needed to surface behavior"
"smaller base model -> more coverage needed to teach behavior"
Use small model chips of different sizes, not big text.

STYLE:
Use primary blue #2D8CFF, pale blue #E8F4FD, border #CFE3F7, charcoal #1A1A2E,
steel gray #6B7280, and soft orange #FF9F43 for one focal accent only. Clean
technical textbook diagram, not a marketing infographic. No dark background, no
decorative blobs, no gradients. Keep labels concise and legible.
```

## Review Checklist

- [ ] LIMA is high-quality but narrow, not shown as universally sufficient.
- [ ] Coverage is visually tied to task diversity.
- [ ] Model scale caveat is visible.
- [ ] Orange is used once for the central trade-off message.

