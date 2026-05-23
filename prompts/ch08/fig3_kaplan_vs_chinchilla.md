# Figure 8.3: Kaplan vs Chinchilla — Two Answers to the Same Question

**Filename**: `fig_kaplan_chinchilla.png`
**LaTeX label**: `fig:kaplan-chinchilla`
**Caption**: Kaplan (2020) and Chinchilla (2022) gave opposite answers to the same question: how should model size and data scale with compute? The difference was not in the math but in the measurement protocol --- particularly the learning-rate schedule.

## Prompt

```text
Draw a Kaplan-vs-Chinchilla comparison for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system. LANDSCAPE
orientation, wide and spacious. Match the visual richness of the book's
best figures — Ch10 "Three-Layer Schema" concentric rings with rich
internal illustrations, Ch10 "Goodhart Cycle" four-panel narrative
with mini-charts inside each card.

CONCEPT:
"Same question. Opposite answers. The difference was measurement."
This is a forensic comparison — not just two cards side by side, but
a DETECTIVE STORY showing why two careful teams got opposite results.
The visual punchline is in the bottom panel: a tiny methodological
detail (learning rate schedule) changed everything.

MAIN COMPOSITION — THREE-ROW LAYOUT:

TOP ROW — THE QUESTION (10% height):
A centered white banner with thin blue border:
"How should N and D scale with compute C?"
Clean, bold, centered. This is the shared starting point.

MIDDLE ROW — TWO ANSWER CARDS (55% height):
Two large white cards side by side with a bold "VS" divider between them.

LEFT CARD — "Kaplan et al. (2020)":
- Title: "Kaplan (2020)" in primary blue, bold
- Subtitle: "Scale the model faster"
- INTERNAL VISUAL — ALLOCATION DIAGRAM:
  A horizontal split bar showing N vs D allocation:
  73% of the bar is solid blue (#2D8CFF) labeled "Model N"
  27% is light blue (#B7D9F2) labeled "Data D"
  The imbalance should be VISUALLY DRAMATIC
- Key formulas in clean type: "N* ∝ C^0.73" / "D* ∝ C^0.27"
- INTERNAL VISUAL — MINI MODEL ICON:
  A tall narrow rectangle (big model) next to a thin data stream
  (little data) — visual metaphor for the recommendation
- Result: "→ GPT-3: 175B params, 300B tokens" with "N:D ≈ 1:1.7"
- INTERNAL VISUAL — MINI TRAINING CURVE:
  A tiny loss curve that plateaus EARLY and levels off — showing
  that under Kaplan's protocol, small models appeared to converge
  quickly (because the LR wasn't decayed properly)

RIGHT CARD — "Hoffmann et al. (2022)":
- Title: "Chinchilla (2022)" in primary blue, bold
- Subtitle: "Scale both equally"
- INTERNAL VISUAL — ALLOCATION DIAGRAM:
  A horizontal split bar: 50% blue + 50% slate blue (#5B7FFF)
  Perfectly balanced — the visual contrast with the left card's
  73/27 split should be immediately striking
- Key formulas: "N* ∝ C^0.50" / "D* ∝ C^0.50"
- INTERNAL VISUAL — MINI MODEL ICON:
  Two equal-sized boxes side by side — balanced N and D
- Result: "→ Chinchilla: 70B params, 1.4T tokens" with "N:D ≈ 1:20"
- INTERNAL VISUAL — MINI TRAINING CURVE:
  A tiny loss curve that keeps descending longer — cosine decay
  lets the model keep learning, so small models looked worse under
  Kaplan but better under Chinchilla

BOTTOM ROW — THE DETECTIVE EVIDENCE (30% height):
A wide panel with thin blue border, divided into three columns:

Column A — "The Methodological Difference":
  Two mini learning-rate schedule diagrams stacked vertically:
  Top: "Kaplan LR" — a flat line that drops sharply at the end
  (fixed schedule, early stopping). Gray line.
  Bottom: "Chinchilla LR" — a smooth cosine curve that decays
  gradually to near zero. Blue line.
  A small arrow between them labeled "This changed everything"

Column B — "The Effect on Small Models":
  Two mini loss curves stacked vertically:
  Top: "Under Kaplan protocol" — small model appears to plateau
  early → conclusion: "small models converge fast, make them bigger"
  Bottom: "Under Chinchilla protocol" — same small model keeps
  improving → conclusion: "small models need more data"

Column C — "The Lesson" (orange accent):
  A white card with orange (#FF9F43) left border:
  "Scaling exponents depend on training protocol, not just architecture."
  This is the ONLY orange element in the figure.
  Below: "Measurement matters as much as math."

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders, subtle shadow
- Primary blue: #2D8CFF
- Secondary blue: #5B7FFF (for D segment in allocation bars)
- Light blue: #B7D9F2
- Orange accent: #FF9F43 (ONLY on the lesson card border in Column C)
- Text: #1A1A2E (charcoal), #6B7280 (steel gray for notes)
- Clean sans-serif labels, generous spacing
- Mini training curves and LR schedules should be simple, clean lines

IMPORTANT:
- Do not use 3D pie charts or gradient fills
- Do not use photorealism or neon
- The mini training curves and LR schedules in the bottom panel are
  essential — they show WHY the answers differed, not just THAT they
  differed
- The allocation bars must make the 73/27 vs 50/50 contrast dramatic
```

## Review Checklist

- [ ] Three-row layout: question → two answer cards → detective evidence
- [ ] Left card shows 73/27 split with internal allocation bar and mini icons
- [ ] Right card shows 50/50 split with balanced internal visuals
- [ ] Both cards have mini training curves showing different convergence behavior
- [ ] Bottom panel Column A: LR schedule comparison (fixed vs cosine)
- [ ] Bottom panel Column B: effect on small model loss curves
- [ ] Bottom panel Column C: lesson callout with orange border
- [ ] Only orange element is the lesson card border
- [ ] VS divider between the two main cards
- [ ] Readable at 50% width in PDF
