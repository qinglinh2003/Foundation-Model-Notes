# Figure 8.2: Power-Law Loss Curves

**Filename**: `fig_power_law_curves.png`
**LaTeX label**: `fig:power-law-curves`
**Caption**: Loss decreases as a power law with both model size and data. On log-log axes, each relationship is a straight line whose slope is the scaling exponent. Diminishing returns are baked in: each 10$\times$ increase in compute yields a roughly constant drop in loss.

## Prompt

```text
Draw a power-law scaling visualization for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system. LANDSCAPE
orientation, wide and spacious. Match the visual richness of the book's
best figures — Ch10 "Prompt Sensitivity" dual-panel with internal
dot-cloud detail, Ch10 "Goodhart Cycle" four-panel with mini scatter
plots inside each card.

CONCEPT:
"Straight lines on log-log axes are the fingerprint of power laws."
This figure should make the reader FEEL diminishing returns — not just
read about them. The key insight: each 10× compute buys the same
fixed drop in loss, forever.

MAIN COMPOSITION — THREE-ZONE LAYOUT:

LEFT PANEL — "Loss vs Model Size" (~35% width):
A clean log-log chart in a white card with thin blue border.
- X-axis: "Parameters N" (log scale, 10M to 100B)
- Y-axis: "Cross-entropy Loss L" (log scale, ~2.0 to 4.0)
- A straight blue line (#2D8CFF) sloping down, with 6-8 small data
  dots scattered near it showing empirical measurements
- Slope annotation: "α ≈ 0.34" in a small white badge
- A dashed horizontal line near the bottom: "E ≈ 1.69" labeled
  "irreducible loss (data entropy)"
- KEY ENRICHMENT: At three points along the line (small model, medium,
  large), add tiny SAMPLE OUTPUT SNIPPETS — 2-line text previews
  showing quality progression:
  - At 100M: garbled text snippet in a small gray box (barely coherent)
  - At 10B: readable but generic snippet
  - At 100B: fluent, specific snippet
  These snippets make the abstract loss numbers CONCRETE.

RIGHT PANEL — "Loss vs Training Data" (~35% width):
Same layout as left panel.
- X-axis: "Tokens D" (log scale, 1B to 10T)
- Y-axis: same scale as left
- Straight blue line with dots, slope "β ≈ 0.28"
- Same dashed entropy floor
- KEY ENRICHMENT: Instead of sample outputs, show EPOCH MARKERS
  along the line — small tags at key positions:
  "1 epoch" / "4 epochs" / "16 epochs"
  This connects data scaling to the practical concept of epochs.

CENTER BRIDGE — "The Diminishing Returns Staircase" (~30% width):
Between the two panels, a vertical STAIRCASE DIAGRAM that visualizes
the diminishing returns directly:
- A series of 4 descending steps, each representing a 10× compute increase
- Each step is a small white card showing:
  Step 1: "10× compute" → "−0.11 nats"
  Step 2: "100× compute" → "−0.22 nats total"
  Step 3: "1000× compute" → "−0.33 nats total"
  Step 4: "10000× compute" → "−0.44 nats total"
- The step HEIGHT is the same each time — that's the visual point
  (constant drop per 10× — power law)
- The step WIDTH grows each time — showing the growing COST per step
- Orange accent (#FF9F43): highlight the "−0.11 nats" per step
  annotation — the ONLY orange element. This is the key practical
  number for napkin estimation.

BOTTOM EQUATION (spanning full width):
A white card centered below:
"L(N, D) = E + A/N^α + B/D^β"
Clean mathematical typography. Label: "Chinchilla functional form"

STYLE:
- Background: #FAFCFF
- Panel cards: white with thin #CFE3F7 borders
- Plot area: white with very faint #F0F4FF grid lines
- Primary blue: #2D8CFF for lines and dots
- Dashed entropy floor: #6B7280 (steel gray)
- Orange accent: #FF9F43 (ONLY on the staircase "−0.11 nats" labels)
- Text: #1A1A2E (charcoal), #6B7280 (steel gray for annotations)
- Clean sans-serif labels, generous margins
- Both panels same height and Y-axis scale

IMPORTANT:
- Do not use plain dual-panel without the center staircase bridge
- Do not use 3D effects, gradient fills, neon
- Do not use multiple colored lines in a single panel
- The sample output snippets in the left panel are essential — they
  make abstract loss numbers concrete
- The staircase must show EQUAL height steps (constant gain) with
  INCREASING width steps (growing cost)
```

## Review Checklist

- [ ] Two log-log panels: Loss vs N (left) and Loss vs D (right)
- [ ] Center staircase showing diminishing returns visually
- [ ] Left panel has sample output quality snippets at three model sizes
- [ ] Right panel has epoch markers along the line
- [ ] Slopes labeled: α ≈ 0.34 and β ≈ 0.28
- [ ] Dashed entropy floor at E ≈ 1.69
- [ ] Staircase steps: equal height (constant gain), increasing width (growing cost)
- [ ] Orange accent ONLY on "−0.11 nats" staircase annotations
- [ ] Bottom equation: L(N,D) = E + A/N^α + B/D^β
- [ ] Readable at 50% width in PDF
