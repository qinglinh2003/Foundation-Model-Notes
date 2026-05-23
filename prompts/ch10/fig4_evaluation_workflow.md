# Figure 10.5: Project 2 Evaluation Workflow

**Filename**: `fig_evaluation_workflow.png`
**LaTeX label**: `fig:evaluation-workflow`
**Caption**: Project 2 evaluation workflow. The deliverable should connect training-time monitoring, final benchmarks, contamination checks, qualitative inspection, and calibrated reporting. Any missing stage weakens the interpretability of the others.

## Prompt

```text
Draw a Project 2 evaluation workflow for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system. LANDSCAPE
orientation, wide and spacious. Match the visual richness of the book's
best figures — Ch5 "Training Pipeline" multi-row workflow with icons
and curved arrows, Ch6 "Pilot Workflow" staged cards with gate
diamonds and cost bar, Ch9 "Data Funnel" progressive panels with
internal visual elements.

CONCEPT:
"From training loop to evaluation report — every stage matters." This
figure shows the end-to-end evaluation workflow for Project 2. It
should feel like a REAL PIPELINE with concrete artifacts at each stage,
not an abstract flowchart. The reader should be able to use this figure
as a literal checklist.

MAIN COMPOSITION — MULTI-ROW PIPELINE:
The workflow is arranged in TWO ROWS to allow visual breathing room
(like Ch5's Training Pipeline), connected by a curved arrow from the
end of Row 1 to the start of Row 2.

TOP ROW — "DURING TRAINING" (2 stages):
A pale blue background band (#F0F7FF) spans this row with a label
"During Training" on the left edge in primary blue.

STAGE 1 — LOSS MONITORING:
- A large white card with thin blue border and subtle shadow
- Title: "Loss Monitoring" in bold charcoal
- INTERNAL ILLUSTRATION: A mini loss curve — two descending lines
  (one solid for "train", one dashed for "val") on tiny axes. The
  lines should look like real training curves: smooth descent with
  slight noise. Below the curve, show 3-4 tiny domain breakdown bars:
  "web" (long bar), "code" (medium bar), "math" (short bar) — a
  mini stacked visualization of per-domain loss
- Details: "Every 200-500 steps" / "Cross-domain breakdown"
- A small clock icon with "built-in" label

STAGE 2 — CHECKPOINT SAMPLES:
- White card, same style
- Title: "Checkpoint Samples" in bold charcoal
- INTERNAL ILLUSTRATION: A mini text sample display — show 3 small
  white snippet boxes stacked vertically with tiny horizontal lines
  of varying length (representing generated text). The top snippet
  has a green-blue left border (good), the middle is neutral, the
  bottom has a light red-gray left border (problematic). This conveys
  that you look at samples for quality variation.
- Details: "Every 1-2K steps" / "10-20 samples per checkpoint"
- Clock icon: "1-2 hours"

Arrow from Stage 1 → Stage 2: blue arrow with label "save checkpoints"

BOTTOM ROW — "AFTER TRAINING" (3 stages):
A slightly stronger blue background band (#E8F4FD) with label
"After Training" on the left edge.

STAGE 3 — BENCHMARKS:
- White card with blue border
- Title: "Benchmark Suite" in bold charcoal
- INTERNAL ILLUSTRATION: A mini horizontal bar chart showing 4
  benchmark scores. Each bar is a different length:
  "HellaSwag" (longest bar, ~72%)
  "ARC" (medium, ~55%)
  "MMLU subset" (medium, ~45%)
  "+optional: GSM8K" (shortest, ~25%)
  Each bar in primary blue. Below the chart: "5-shot, with 95% CI"
  Show tiny error bars (whiskers) on each bar.
- Clock icon: "2-4 hours"

STAGE 4 — AUDIT & INSPECT:
- White card with blue border
- Title: "Audit & Inspect" in bold charcoal
- INTERNAL ILLUSTRATION: Split into two mini-sections:
  TOP: A tiny CONTAMINATION CHECK panel — show a small document icon
  with a magnifying glass overlay and a checkmark/X. Label: "n-gram
  overlap check"
  BOTTOM: A tiny READING GRID — a 3×3 grid of tiny squares, some
  filled blue (good), some filled light gray (bad), representing
  human-read samples. Label: "Read 50-100 samples"
- Details: "Coherent? On-topic? Factual?"
- Clock icon: "2-3 hours"

STAGE 5 — EVALUATION REPORT:
- LARGER card than the others (visually emphasized as the deliverable)
- Title: "Evaluation Report" in bold charcoal
- Left border: ORANGE (#FF9F43) — the ONLY orange element
- INTERNAL ILLUSTRATION: A mini document/report layout:
  - Tiny "Loss curves" section with a miniature curve icon
  - Tiny "Benchmark table" section with a miniature grid
  - Tiny "Sample gallery" section with 2 small text blocks
  - Tiny "Known limitations" section with a bullet list icon
  These should look like a TABLE OF CONTENTS for the report, drawn
  as small labeled sections in a document frame.
- A small completion checkmark

ARROWS:
- Curved arrow from Stage 2 (end of Row 1) down to Stage 3 (start of Row 2)
- Straight arrows: Stage 3 → Stage 4 → Stage 5
- All arrows in primary blue (#2D8CFF), medium weight
- Arrow from Stage 4 → Stage 5 is THICKER (everything converges here)

FEEDBACK ARROW:
A thin dashed arrow arcing from Stage 5 back up to Stage 1, labeled:
"Mid-training eval may trigger data mix adjustment"
Drawn in steel gray (#6B7280).

TIME BUDGET STRIP (below Row 2):
A thin horizontal bar divided into 5 segments matching the 5 stages:
"built-in | 1-2h | 2-4h | 2-3h | 2-4h"
Right-end total: "~7-13 hours" in bold. This is secondary visual info.

STYLE:
- Background: #FAFCFF
- Row bands: #F0F7FF (during training) and #E8F4FD (after training)
- Cards: white, thin #CFE3F7 borders, subtle shadow
- Primary blue: #2D8CFF
- Orange accent: #FF9F43 ONLY on Stage 5 left border
- Mini-charts inside cards: blue family only
- Text: #1A1A2E for titles, #6B7280 for details
- Clean sans-serif typography, generous margins

IMPORTANT:
- Each stage MUST have an internal illustration, not just text labels
- The mini loss curve, mini bar chart, mini reading grid, and mini
  report layout are what make this figure rich
- Do not use swimlane diagrams or JIRA-board layouts
- Do not use 3D, glow, or gradient fills
- Do not use hardware icons (servers, GPUs)
- Stage 5 must be visibly larger than other stages
```

## Review Checklist

- [ ] Two-row layout: Row 1 (During Training: 2 stages), Row 2 (After Training: 3 stages)
- [ ] Stage 1 has mini loss curve + domain breakdown bars
- [ ] Stage 2 has mini text sample snippets with quality indicators
- [ ] Stage 3 has mini horizontal bar chart with error bars for 4 benchmarks
- [ ] Stage 4 has contamination check panel + reading grid
- [ ] Stage 5 has mini report document layout; LARGER card; orange left border
- [ ] Phase bands: pale blue (during) vs stronger blue (after training)
- [ ] Curved arrow connecting Row 1 → Row 2
- [ ] Dashed feedback arrow from Stage 5 back to Stage 1
- [ ] Time budget strip below with per-stage hours
- [ ] Orange accent only on Stage 5 left border
- [ ] Landscape orientation, matches Training Pipeline / Pilot Workflow quality
- [ ] Readable at 50% width in PDF
