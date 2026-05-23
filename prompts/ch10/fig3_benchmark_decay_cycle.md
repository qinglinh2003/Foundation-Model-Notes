# Figure 10.4: Benchmark Decay Under Goodhart Pressure

**Filename**: `fig_benchmark_decay_cycle.png`
**LaTeX label**: `fig:benchmark-decay-cycle`
**Caption**: A benchmark starts as a useful measurement instrument, becomes an optimization target, saturates, and is eventually replaced by harder or fresher tasks. The cycle does not make benchmarks useless; it makes benchmark age and protocol history part of the interpretation.

## Prompt

```text
Draw a benchmark decay cycle diagram for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system. LANDSCAPE
orientation, wide and spacious. Match the visual richness of the book's
best figures — Ch7 "DDP to FSDP" four-column progression with internal
state diagrams, Ch6 "Scale Gap" visual-metaphor cards, Ch5 "Training
Pipeline" multi-row workflow with icons.

CONCEPT:
"The Goodhart Cycle." Benchmarks follow a predictable life cycle:
Release → Optimization → Saturation → Replacement. The visual must
convey both the CYCLICAL nature and the DECAY of signal quality.
Each stage should have a rich internal illustration — not just a text
label, but a visual mini-story showing what happens to the benchmark
at that stage.

MAIN COMPOSITION:
Four large STAGE CARDS arranged horizontally, connected by heavy blue
arrows. Each card is a white rounded rectangle (~200px tall) with thin
blue border and subtle shadow. The cards share the same height but the
internal illustrations visually "degrade" from left to right.

Above the four cards, a horizontal SIGNAL QUALITY BAR running the
full width. Build it from 5 adjacent rectangular segments that step
from saturated blue (#2D8CFF) on the left to pale gray-blue (#E0E7EF)
on the right. Do not use a smooth gradient. Labels: left end "High
signal quality" / right end "Signal exhausted".

CARD 1 — RELEASE:
- Title: "1. Release" in bold charcoal
- INTERNAL ILLUSTRATION: Draw a mini scatter plot inside the card.
  Show 5-6 colored dots (different blues representing different models)
  spread along a diagonal — models are well-separated, scores vary
  meaningfully. The dots should look like a real evaluation result where
  ranking is clear.
- Below the mini-plot: "Models score low; ranking reflects real ability"
- A small "year 0" tag in the bottom-right corner
- Fill: very pale blue (#F0F7FF)

CARD 2 — OPTIMIZATION:
- Title: "2. Optimization" in bold charcoal
- INTERNAL ILLUSTRATION: The same mini scatter plot, but now the dots
  have shifted UPWARD and COMPRESSED together. The gap between them is
  smaller. Add 2-3 tiny upward arrows pushing the dots, suggesting
  optimization pressure. Add tiny labels near some arrows: "train on
  test", "format tuning"
- Below: "Labs optimize against the benchmark"
- A small "~1 year" tag
- Fill: slightly stronger blue (#E8F4FD)

CARD 3 — SATURATION:
- Title: "3. Saturation" in bold charcoal
- INTERNAL ILLUSTRATION: The dots are now CLUSTERED AT THE TOP of the
  mini-plot, all above 90%. They overlap, forming a tight indistinguishable
  blob near the ceiling. A thin dashed line marks "ceiling" at the top.
  The dots should feel like a traffic jam — no separation, no information.
- Below: "Scores >90 %; differences are noise"
- A small "~2 years" tag
- Fill: stronger blue (#D8EAF8)

CARD 4 — REPLACEMENT:
- Title: "4. Replacement" in bold charcoal
- INTERNAL ILLUSTRATION: The old saturated blob is shown faded out
  (ghosted, dashed outlines, very light gray). Below or overlaid, a
  NEW scatter plot appears with fresh dots spread out along a diagonal
  again — a new benchmark with clean separation. This is drawn in
  primary blue, full opacity. A small label: "new benchmark"
- Below: "GPQA, MMLU-Pro, LiveBench, ..."
- A small "~3 years" tag
- Fill: white
- Card border: orange (#FF9F43) — the ONLY orange-bordered card

CONNECTING ARROWS:
Heavy smooth arrows (#2D8CFF) between cards 1→2→3→4. The arrows should
be substantial (not thin lines) to convey inevitability.

RETURN ARROW:
A wide graceful curved arrow looping from Card 4 underneath back to
Card 1. Drawn in steel gray (#6B7280), dashed style. Label on the
curve: "Cycle restarts" in small gray text.

TIMELINE BAR (below the cards, very small):
A thin horizontal timeline with concrete examples:
"SQuAD (2016) → SuperGLUE (2019) → MMLU (2020) → GPQA (2024)"
Each name sits above a small dot on the timeline. This makes the
abstract cycle feel real and grounded.

BOTTOM CALLOUT:
A white card with thin blue border below the timeline:
"When a measure becomes a target, it ceases to be a good measure."
"— Goodhart's Law"
The word "target" in orange (#FF9F43) — the only orange text accent.

STYLE:
- Background: #FAFCFF
- Cards: white or pale blue, thin #CFE3F7 borders, subtle shadow
- Primary blue: #2D8CFF
- Orange accent: #FF9F43 ONLY on Card 4 border + "target" in callout
- Mini scatter plot dots: various blues (#2D8CFF, #7DBFF0, #B7D9F2)
- Text: #1A1A2E for titles, #6B7280 for annotations
- Clean sans-serif typography, generous margins

IMPORTANT:
- Each card MUST have a mini scatter plot illustration, not just text
- The scatter plots must show a visible DEGRADATION of signal from
  Card 1 (spread out) to Card 3 (clustered at ceiling)
- Do not use a literal circular cycle layout
- Do not use emoji, clip art, or trophy icons
- Do not use 3D, glow, neon, or gradient fills on cards
- Do not make it look like a generic process slide
```

## Review Checklist

- [ ] Four horizontal cards: Release, Optimization, Saturation, Replacement
- [ ] Each card has a MINI SCATTER PLOT showing signal degradation
- [ ] Card 1: dots spread (good signal) → Card 3: dots clustered at ceiling (no signal)
- [ ] Card 4: ghosted old plot + fresh new plot
- [ ] Signal quality segmented bar above cards (blue → gray-blue)
- [ ] Heavy connecting arrows + dashed return arrow completing cycle
- [ ] Timeline with real benchmarks: SQuAD → SuperGLUE → MMLU → GPQA
- [ ] Card 4 has orange border; "target" is orange in Goodhart callout
- [ ] Year tags on each card (year 0, ~1yr, ~2yr, ~3yr)
- [ ] Landscape orientation, matches DDP-to-FSDP / Scale Gap quality
- [ ] Readable at 50% width in PDF
