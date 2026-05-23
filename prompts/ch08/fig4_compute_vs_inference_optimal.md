# Figure 8.4: Compute-Optimal vs Inference-Optimal

**Filename**: `fig_overtraining.png`
**LaTeX label**: `fig:overtraining`
**Caption**: Chinchilla optimizes training compute alone. Production models optimize lifetime cost --- training plus billions of inference calls. The result: every major production model massively over-trains relative to the Chinchilla optimum.

## Prompt

```text
Draw a compute-optimal vs inference-optimal comparison for a machine
learning textbook. Use the course's Zoom-inspired blue-white visual
system. LANDSCAPE orientation, wide and spacious. Match the visual
richness of the book's best figures — Ch10 "Goodhart Cycle" four-panel
narrative with mini-charts inside each card, Ch10 "Evaluation Workflow"
multi-stage pipeline with internal illustrations.

CONCEPT:
"Optimize for deployment, not training." The industry has moved
beyond Chinchilla: production models deliberately over-train (use far
more data than compute-optimal) because a smaller, over-trained model
is cheaper to serve billions of inference calls. The figure should
tell this as a COST STORY — training cost goes up, but inference cost
goes way down, and inference dominates lifetime cost.

MAIN COMPOSITION — TWO-ZONE LAYOUT:

LEFT ZONE — THE BAR CHART (~55% width):
A horizontal bar chart showing 5 models, but each bar is NOT a plain
colored rectangle. Instead, each bar is a COMPOUND VISUAL:

EACH BAR HAS INTERNAL STRUCTURE:
The bar is divided into two segments:
- LEFT segment (blue): represents the Chinchilla-optimal data amount
  (always the same length, the 1× baseline)
- RIGHT segment (progressively longer): represents the EXTRA data
  beyond optimal

Model Bars (top to bottom):

Bar 1 — GPT-3 (2020):
  Total: 0.09× (UNDER-trained)
  The bar extends LEFT from the baseline — it didn't even reach optimal
  Color: pale blue (#B7D9F2)
  Right annotation: "1:1.7 — under-trained"
  Mini icon: a large model box with a tiny data trickle

Bar 2 — Chinchilla (2022):
  Total: 1× (baseline)
  A VERTICAL REFERENCE LINE here labeled "Chinchilla optimal"
  Color: primary blue (#2D8CFF)
  Right annotation: "1:20 — compute-optimal"
  Mini icon: two balanced boxes

Bar 3 — LLaMA-2 7B (2023):
  Total: 14×
  Bar extends well past baseline
  Color: slate blue (#5B7FFF)
  Right annotation: "1:286"
  Mini icon: small model + large data stream

Bar 4 — Mistral 7B (2023):
  Total: 57×
  Much longer bar
  Color: slate blue (#5B7FFF)
  Right annotation: "1:1143"

Bar 5 — LLaMA-3 8B (2024):
  Total: 94×
  Longest bar, nearly reaching edge
  Color: slate blue (#5B7FFF)
  Right annotation: "1:1875"
  Mini icon: tiny model + massive overflowing data stream

X-axis: log scale, "Over-training factor (× Chinchilla-optimal)" 0.1× to 100×
Left bracket: "2020: scale the model"
Right bracket: "2023+: scale the data"

RIGHT ZONE — THE COST EXPLANATION (~40% width):
A vertical COST BREAKDOWN panel that explains WHY over-training is rational.
This is the "detective evidence" — three stacked mini-visualizations:

Panel A — "Training Cost":
  A small bar or area chart showing training cost increasing with
  over-training. The bar grows modestly from 1× to ~3×.
  Label: "Training cost: +2-3×"
  Color: primary blue

Panel B — "Inference Cost per Query":
  A small bar showing inference cost DECREASING as the model gets
  smaller (smaller model = cheaper per query).
  A downward arrow from "70B" to "7B" labeled "10× fewer params"
  Label: "Cost per query: −10×"
  Color: primary blue

Panel C — "Lifetime Cost" (the punchline):
  A simple equation visual:
  "Training (once)" + "Inference (billions)" = "Lifetime Cost"
  The inference box is MUCH LARGER than the training box, making it
  visually obvious that inference dominates.
  Below: "Over-training pays for itself after ~1B queries"
  The "pays for itself" text in orange (#FF9F43) — the ONLY orange
  element.

BOTTOM CALLOUT (spanning full width):
A white card with thin blue border:
"A smaller model on more data costs more to train — but saves on
every one of the billions of inference calls."

STYLE:
- Background: #FAFCFF
- Plot area: white
- Primary blue: #2D8CFF (Chinchilla bar + reference line)
- Secondary blue: #5B7FFF (production model bars)
- Light blue: #7EC8E3 (GPT-3 under-trained bar)
- Orange accent: #FF9F43 (ONLY on "pays for itself" in Panel C)
- Text: #1A1A2E (charcoal), #6B7280 (steel gray for annotations)
- Clean sans-serif labels, generous margins
- Bars have internal structure, not plain colored rectangles

IMPORTANT:
- Do not use 3D bars, gradient fills, neon
- Do not use vertical bar chart (horizontal bars)
- The right-side cost explanation panels are essential — they explain
  the WHY, not just the WHAT
- Mini model/data icons inside or next to bars add richness
- Log-scale X-axis with clear grid lines
```

## Review Checklist

- [ ] 5 horizontal bars: GPT-3, Chinchilla, LLaMA-2, Mistral, LLaMA-3
- [ ] Each bar has internal structure (baseline segment + extra segment)
- [ ] Mini model/data icons next to key bars
- [ ] Vertical reference line at 1× labeled "Chinchilla optimal"
- [ ] Right zone: three cost explanation panels (Training / Inference / Lifetime)
- [ ] Lifetime cost panel shows inference dominating training
- [ ] Orange accent ONLY on "pays for itself"
- [ ] Era brackets: "2020: scale the model" vs "2023+: scale the data"
- [ ] Bars show progression: 0.09× → 1× → 14× → 57× → 94×
- [ ] Readable at 50% width in PDF
