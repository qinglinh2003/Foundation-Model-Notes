# Figure 9.4: Mixing Experiment — Different Recipes, Different Outcomes

**Filename**: `fig_mixing_experiment.png`
**LaTeX label**: `fig:mixing-experiment`
**Caption**: Three candidate mixtures trained on the same compute budget with the same model architecture. The diverse mixture (with code and math) achieves lower loss on held-out evaluation, despite using fewer web tokens. Data mixing is a zero-cost lever for improving model capability.

## Prompt

```text
Draw a data mixing experiment visualization for a machine learning
textbook. Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious. Match the visual richness
of the book's best figures — Ch10 "Evaluation Workflow" multi-stage
pipeline with internal illustrations, Ch10 "ICL Spectrum" three-card
comparison with concrete prompt structures inside each card.

CONCEPT:
"Same model. Same compute. Different data. Different capability."
This is the chapter's climax visual — it proves that data recipe is
a FREE LEVER for improving models. The figure must make the reader
feel the divergence: identical starting conditions, but one recipe
wins decisively.

MAIN COMPOSITION — TWO-ZONE LAYOUT:

LEFT ZONE — RECIPE CARDS (~35% width):
Three white cards stacked vertically with generous spacing.
Each card is a mini-infographic, not just a label.

Card A — "Baseline" (top):
- Title: "Baseline" in charcoal, bold
- Tag: "web only" in small gray badge
- INTERNAL VISUAL — MIXTURE BAR:
  A horizontal stacked bar (~80% card width):
  100% solid primary blue (#2D8CFF)
- INTERNAL VISUAL — SAMPLE CONTENT PREVIEW:
  Below the bar, a tiny 2-line text snippet in light gray showing
  what web-only data looks like: generic prose lines
  (just abstract horizontal lines of varying length, like text)
- Label: "100% FineWeb-Edu"

Card B — "Diverse" (middle) — THE WINNER:
- Title: "Diverse" in charcoal, bold
- Tag: "★ winner" in a small orange badge (#FF9F43)
- INTERNAL VISUAL — MIXTURE BAR:
  70% primary blue (#2D8CFF) + 15% slate blue (#5B7FFF) + 15% orange (#FF9F43)
  The orange segment represents Math — the ONLY orange in the bar
- INTERNAL VISUAL — SAMPLE CONTENT PREVIEWS:
  Three tiny snippets stacked: prose lines + code bracket "{ }" +
  math symbol "∫dx". Shows the three types of content.
- Label: "70% FineWeb + 15% Code + 15% Math"
- This card has a slightly thicker border or subtle highlight to
  mark it as the winner

Card C — "Balanced" (bottom):
- Title: "Balanced" in charcoal, bold
- Tag: "diverse but diluted" in small gray badge
- INTERNAL VISUAL — MIXTURE BAR:
  60% primary blue + 20% teal (#00B894) + 10% slate blue + 10% orange
- INTERNAL VISUAL — SAMPLE CONTENT PREVIEWS:
  Four tiny snippets: prose + mixed corpus lines + code + math
- Label: "60% FineWeb + 20% SlimPajama + 10% Code + 10% Math"

CONNECTOR LINES:
Three thin lines from each card extending rightward into the chart,
color-coded to match each recipe's dominant color. The lines should
enter the chart area smoothly, like tributaries feeding into a river.

RIGHT ZONE — LOSS CURVE CHART (~60% width):
A clean line chart in a white card with thin blue border.

CHART FRAME:
- White background, very faint blue grid (#F0F6FF)
- X-axis: "Training Steps" (0 to 1,000)
- Y-axis: "Validation Loss (nats/token)" — range ~3.2 to 3.8
- Clean axis labels, thin lines, no heavy borders

THREE CURVES:
All start together at ~3.75, then diverge after ~step 200:
- Baseline: solid primary blue (#2D8CFF), descends to ~3.45
- Diverse: dashed slate blue (#5B7FFF), descends MORE steeply to ~3.35
- Balanced: dotted teal (#00B894), descends to ~3.40

KEY ENRICHMENT — DIVERGENCE ZONE:
At the point where curves begin diverging (~step 200), add a subtle
vertical gray dashed line labeled "divergence begins". A tiny
annotation: "same model, same FLOPs — only the data differs"

KEY ENRICHMENT — ENDPOINT ANNOTATIONS:
At step 1000, each curve ends with a small white ENDPOINT CARD:
- Baseline card: "3.45 nats"
- Diverse card: "3.35 nats" with a small star icon
- Balanced card: "3.40 nats"

VERTICAL BRACKET at step 1000:
A thin bracket spanning Baseline (3.45) to Diverse (3.35):
"Δ = 0.10 nats" in orange (#FF9F43)
Below: "≈ free performance from data alone" in small orange text
This is the KEY INSIGHT annotation.

BOTTOM CALLOUT (spanning full width):
A centered white card with thin blue border:
"Data mixing is the highest-leverage, lowest-cost decision in Project 2."
"highest-leverage" in orange (#FF9F43) — the single accent word.

HORIZONTAL LEGEND below the chart:
— solid blue line: "Baseline (web only)"
— dashed slate line: "Diverse (web + code + math)"
— dotted teal line: "Balanced (web + mixed)"

STYLE:
- Background: #FAFCFF
- Recipe cards: white, thin #CFE3F7 borders, subtle shadow
- Chart area: white, thin #CFE3F7 border, light #F0F6FF grid
- Line colors: #2D8CFF (baseline), #5B7FFF (diverse), #00B894 (balanced)
- Orange accent: #FF9F43 on Math segments, "★ winner" badge,
  "Δ = 0.10 nats" bracket, "free performance" text, and
  "highest-leverage" in callout
- Text: #1A1A2E for main text, #6B7280 for secondary
- Clean sans-serif throughout
- Lines should look editorial, not auto-generated

IMPORTANT:
- Do not make curves noisy/jagged (smooth, clean lines only)
- Do not add error bars, confidence bands, or scatter points
- Do not use more than 3 curves
- Do not use rainbow or gradient fills
- Do not make it look like a WandB or TensorBoard screenshot
- Sample content previews inside recipe cards are essential
- Endpoint cards at step 1000 make the exact numbers readable
- Divergence zone annotation makes the story clear
```

## Review checklist

- [ ] Three recipe cards with mixture bars AND sample content previews
- [ ] Card B marked as "★ winner" with orange badge
- [ ] Clean line chart with 3 smooth curves starting together, diverging at ~step 200
- [ ] Diverse mixture achieves lowest final loss (3.35 vs 3.45)
- [ ] Divergence zone annotation at ~step 200
- [ ] Endpoint cards at step 1000 with exact loss values
- [ ] Vertical bracket showing Δ = 0.10 nats in orange
- [ ] "Free performance from data alone" orange annotation
- [ ] Connector lines from cards to chart
- [ ] Bottom callout: "highest-leverage" in orange
- [ ] Landscape orientation
- [ ] Matches ch10 visual richness
