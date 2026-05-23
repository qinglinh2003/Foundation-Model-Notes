# Figure 10.1: Three-Layer Evaluation Schema

**Filename**: `fig_three_layer_schema.png`
**LaTeX label**: `fig:three-layer-schema`
**Caption**: Three-layer evaluation schema. Loss-based evaluation is mathematically precise but weakly tied to capability; benchmarks are scalable capability proxies but fragile under contamination, saturation, and prompt choices; behavioral evaluation is closest to real use but noisy and expensive. Responsible evaluation triangulates across all three.

## Prompt

```text
Draw a three-layer evaluation schema for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system. LANDSCAPE
orientation, wide and spacious. Match the visual quality of the book's
best figures — Ch7 "Bandwidth Hierarchy" concentric rings, Ch9 "Data
Funnel" progressive panels, Ch4 "Signal Density" token-level detail.

CONCEPT:
"Three layers of evaluation, three kinds of evidence." The figure is
the chapter's organizing framework. Three evaluation layers are
arranged as concentric rings — Loss at the core (most precise, narrowest),
Benchmarks in the middle ring, Behavioral on the outer ring (closest
to real use, widest). The visual should instantly convey a TRADE-OFF
between precision (inner) and validity (outer).

MAIN COMPOSITION — CONCENTRIC RINGS:
Three concentric rounded rectangles (not perfect circles — use softly
rounded stadium shapes) centered in the figure. Each ring is a distinct
band with generous width. The innermost is tight and geometric, the
outermost is wide and textured.

CORE RING — LOSS-BASED (Layer 1):
- A small, crisp, highly geometric core in primary blue (#2D8CFF)
- Inside: a tiny clean loss curve descending left-to-right (sharp,
  smooth, mathematical-looking line). Next to it, three small metric
  capsules in white: "Loss (nats)" / "Perplexity" / "BPB"
- The overall feel is SURGICAL and PRECISE — clean lines, no fuzz
- Small label pinned to the left edge: "Layer 1: Loss-Based"
- Tag on right: "Precise but blind to capability"

MIDDLE RING — BENCHMARKS (Layer 2):
- A wider band in medium blue (#B7D9F2) wrapping around the core
- Inside this band, scatter 6-8 small white BENCHMARK CHIPS arranged
  around the ring like satellite items. Each chip is a tiny rounded
  rectangle with a benchmark name:
  "MMLU" / "HellaSwag" / "ARC" / "GSM8K" / "HumanEval" / "TruthfulQA"
  Some chips have tiny bar-chart icons next to them (1-2 bars, abstract)
- Between the chips, add subtle small WARNING MARKERS — tiny triangles
  or caution symbols near 2-3 chips, labeled in very small gray text:
  "contamination?" / "saturated" / "prompt-sensitive"
  This conveys that benchmarks are useful but fragile.
- Label pinned to the left: "Layer 2: Benchmarks"
- Tag on right: "Scalable but fragile"

OUTER RING — BEHAVIORAL (Layer 3):
- The widest band in pale blue (#E8F4FD), wrapping around everything
- Inside: a richer, more textured visual. Show:
  - A tiny abstract CHAT TRANSCRIPT snippet (3-4 short horizontal lines
    of varying length, like a conversation)
  - A tiny RUBRIC CARD (a small checklist with 3 checked items)
  - A tiny HUMAN SILHOUETTE next to an "LLM" label with a double arrow
    between them (judge setup)
  - These elements are scattered around the band, giving it visual
    richness and organic texture compared to the geometric core
- Label pinned to the left: "Layer 3: Behavioral"
- Tag on right: "Valid but noisy and expensive"

AXIS ANNOTATIONS:
- A thin arrow running from the core outward to the left, labeled
  "← Higher precision" in small charcoal text
- A thin arrow running from the core outward to the right, labeled
  "Higher validity →" in small charcoal text
- These arrows should be subtle, not dominant

BOTTOM CALLOUT:
A wide white card below the rings with thin blue border (#CFE3F7):
"Responsible evaluation triangulates across all three layers."
The word "triangulates" in orange (#FF9F43) — the ONLY orange element
in the entire figure. Small triangulation lines drawn from the callout
to each of the three rings (thin dashed lines), visually connecting
the advice to the structure.

STYLE:
- Background: #FAFCFF
- Core: #2D8CFF (crisp, geometric)
- Middle ring: #B7D9F2 (moderate complexity)
- Outer ring: #E8F4FD (rich, textured)
- Benchmark chips: white with thin #CFE3F7 borders
- Orange accent: #FF9F43 ONLY on "triangulates"
- Text: #1A1A2E for labels, #6B7280 for annotations
- Clean sans-serif typography, generous spacing
- Progressive visual density from core (clean) to outer (rich) — this
  is the KEY visual storytelling device

IMPORTANT:
- Do not use a Venn diagram or pie chart
- Do not use a pyramid or triangle shape
- Do not use literal microscope, checkmark, or people icons
- Do not use 3D, glow, neon, or gradient fills
- Do not crowd text — let the concentric structure speak
- The three rings must have VISIBLY different internal textures
```

## Review Checklist

- [ ] Three concentric rounded rings: Loss (core), Benchmarks (middle), Behavioral (outer)
- [ ] Core is geometric and precise; outer is rich and textured
- [ ] Benchmark chips scattered in middle ring with warning markers
- [ ] Behavioral ring has chat transcript, rubric card, judge setup visuals
- [ ] Loss curve inside the core ring
- [ ] Precision ← → Validity axis annotations
- [ ] Triangulation dashed lines from callout to each ring
- [ ] Orange only on "triangulates" in bottom callout
- [ ] Landscape orientation, matches Bandwidth Hierarchy / Data Funnel quality
- [ ] Readable at 50% width in PDF
