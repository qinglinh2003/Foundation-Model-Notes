# Figure 8.1: The Compute Allocation Hyperbola

**Filename**: `fig_compute_hyperbola.png`
**LaTeX label**: `fig:compute-hyperbola`
**Caption**: Every point on the hyperbola $N \times D = C/6$ uses the same compute budget. Scaling laws identify which point yields the lowest loss. Historical models reveal how the field's answer to this question has shifted.

## Prompt

```text
Draw a compute-allocation trade-off landscape for a machine learning
textbook. Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious. Match the visual richness
of the book's best figures — Ch10 "Three-Layer Schema" concentric
rings with internal illustrations, Ch9 "Data Funnel" progressive
panels with mini-visualizations inside each stage.

CONCEPT:
"Where you sit on the hyperbola defines your model." This is not
just a scatter plot — it is a LANDSCAPE that tells the story of how
the field learned to allocate compute. Each model is a character in
the story, with its own visual identity.

MAIN COMPOSITION:
A wide log-log plot area occupying the center 70% of the figure,
with generous annotation space around it.

PLOT AREA:
- White background with a very faint blue grid (#E8F4FD)
- X-axis: "Model Size N (parameters)" — log scale, 100M to 1T
- Y-axis: "Training Data D (tokens)" — log scale, 10B to 100T
- The constant-compute frontier: a smooth, medium-weight blue
  diagonal (#2D8CFF) labeled "N × D = C (fixed compute)"

THE KEY INNOVATION — EACH MODEL DOT IS A MINI-VIGNETTE:
Instead of plain dots, each model is a small WHITE CARD (~40×30px feel)
with a thin blue border, positioned at the correct log-log coordinates.
Inside each card:

Card 1 — GPT-3 (2020):
  Position: N=175B, D=300B (BELOW the line)
  Inside: tiny icon of a large box (big model) next to a small data
  stream (little data). Bold "175B / 300B"
  Below card: "over-modeled" in steel gray
  Card border: light blue (#7EC8E3)
  A thin downward arrow from the frontier line to this card, showing
  how far it falls below the optimum

Card 2 — Chinchilla (2022):
  Position: N=70B, D=1.4T (ON the line)
  Inside: two equal-sized boxes (balanced N and D). Bold "70B / 1.4T"
  Below card: "compute-optimal" in primary blue
  Card border: primary blue (#2D8CFF), slightly thicker — the hero
  A small checkmark icon inside the card

Card 3 — LLaMA-2 7B (2023):
  Position: N=7B, D=2T (ABOVE the line)
  Inside: tiny box + large data stream. Bold "7B / 2T"
  Below card: "over-trained 14×" in steel gray
  Card border: light blue

Card 4 — LLaMA-3 8B (2024):
  Position: N=8B, D=15T (FAR ABOVE the line)
  Inside: tiny box + massive data stream (overflowing the card edge).
  Bold "8B / 15T"
  Below card: "over-trained 94×" in steel gray
  Card border: light blue

Card 5 — Project 2 (student):
  Position: N≈1B, D≈18B
  Inside: a small star icon. Bold "~1B / ~18B"
  Below card: "your budget" in orange (#FF9F43)
  Card border: orange (#FF9F43) — the ONLY orange element
  This card should be slightly larger with a subtle glow/shadow

NARRATIVE ARROW:
A thin curved arrow connecting GPT-3 → Chinchilla → LLaMA-2 → LLaMA-3,
tracing the field's historical trajectory. Along this arrow, tiny
year labels: "2020" → "2022" → "2023" → "2024". The arrow tells the
story: the field moved from over-modeling to optimal to deliberate
over-training.

ZONE ANNOTATIONS:
- Below the frontier line: a pale blue wash with label
  "Over-modeled zone: too many params for data"
- Above the frontier line: a pale blue wash (slightly different shade)
  with label "Over-trained zone: more data than compute-optimal"
- The zones should be very subtle, not distracting

BOTTOM CALLOUT:
A white card spanning the width, thin blue border:
"same compute, better allocation → lower loss"
A thin arrow from GPT-3's card to Chinchilla's card echoing this.

STYLE:
- Background: #FAFCFF
- Plot area: white with #E8F4FD grid lines
- Primary blue: #2D8CFF
- Orange accent: #FF9F43 (ONLY on Project 2 card)
- Text: #1A1A2E (charcoal), #6B7280 (steel gray for annotations)
- Clean sans-serif labels, generous margins
- Model cards give depth and narrative — not just dots on a chart

IMPORTANT:
- Do not use plain colored dots — use mini-vignette cards
- Do not use 3D effects, gradient fills, neon
- Do not add more than one orange element
- The narrative arrow connecting models chronologically is essential
- Log-log axes must be clearly labeled
```

## Review Checklist

- [ ] Log-log axes with clear labels (Model Size N / Training Data D)
- [ ] Smooth blue diagonal line labeled "N × D = C"
- [ ] 5 mini-vignette cards (not plain dots) at correct positions
- [ ] Each card has internal illustration (model/data size icons)
- [ ] GPT-3 below line, Chinchilla on line, LLaMA above line
- [ ] Narrative arrow tracing 2020→2024 historical trajectory
- [ ] Project 2 in orange — the ONLY orange element
- [ ] Zone annotations (over-modeled / over-trained) as subtle washes
- [ ] Readable at 50% width in PDF
