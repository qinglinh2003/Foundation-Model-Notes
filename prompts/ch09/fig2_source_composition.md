# Figure 9.2: Pretraining Data Source Composition

**Filename**: `fig_source_composition.png`
**LaTeX label**: `fig:source-composition`
**Caption**: A typical pretraining data mixture. Web crawl dominates by volume, but curated sources are deliberately upweighted to develop specific capabilities. The rightmost bar shows a typical training mixture after upweighting.

## Prompt

```text
Draw a data source composition comparison for a machine learning
textbook. Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious. Match the visual richness
of the book's best figures — Ch10 "Prompt Sensitivity" dual-panel
with illusion-vs-reality contrast, Ch10 "Three-Layer Schema" with
rich internal illustrations inside each layer.

CONCEPT:
"Natural vs Curated." The internet is ~95% generic web crawl. But
the best training mixtures deliberately upweight small, high-quality
sources by 10-25×. The figure must make this DRAMATIC REBALANCING
instantly visible: one bar is a monotone wall, the other is a
rich mosaic.

MAIN COMPOSITION — THREE-COLUMN LAYOUT:

LEFT COLUMN — "Natural Proportion" (~30% width):
A tall vertical stacked bar in a white card with thin blue border.
- Title: "Natural Proportion" in charcoal, subtitle: "(by raw token count)"
- The bar is ALMOST ENTIRELY ONE COLOR: web crawl at ~95%.
  Use a pale blue (#B7D9F2) for the web segment.
- The remaining sources are barely visible slivers at the bottom:
  Code ~3%, Wikipedia ~0.5%, Books ~0.3%, Math/Science ~0.2%
- KEY ENRICHMENT: Inside the massive web segment, show a faint
  repeated watermark pattern of tiny text lines — suggesting the
  monotony of web text. Same content, over and over.
- Each sliver gets a tiny right-aligned label with source name and %
- The VISUAL MESSAGE: this bar is boringly monochrome

CENTER COLUMN — "The Transformation" (~25% width):
Instead of simple arrows, show a REWEIGHTING MECHANISM:
- A vertical stack of 5 small MULTIPLIER BADGES, one per source,
  aligned between the two bars:
  - Web: "×0.68" (downweighted) — in steel gray, small
  - Code: "×4.0" (upweighted) — in primary blue, medium
  - Wikipedia: "×10" (heavily upweighted) — in teal (#00B894), large
  - Books: "×16.7" (heavily upweighted) — in navy (#1A3A5C), large
  - Math: "×25" (massively upweighted) — in orange (#FF9F43), largest
    badge with a subtle glow. This is the ONLY orange element.
- Thin curved arrows connect each left bar segment to the
  corresponding right bar segment, passing through the multiplier
  badge. The arrows should fan out gracefully.
- Below the badges: "Deliberate upweighting" in steel gray

RIGHT COLUMN — "Typical Training Mix" (~30% width):
A tall vertical stacked bar in a white card, same height as left bar.
- Title: "Typical Training Mix" in charcoal
- Subtitle: "(after deliberate upweighting)"
- Now the bar is VISIBLY DIVERSE:
  Web (filtered CC): ~65% — primary blue (#2D8CFF)
  Code: ~12% — slate blue (#5B7FFF)
  Wikipedia: ~5% — teal (#00B894)
  Books: ~5% — deep navy (#1A3A5C)
  Math/Science: ~5% — the ONLY segment with orange left-border (#FF9F43)
  Other/Synthetic: ~8% — warm gray (#9CA3AF)
- KEY ENRICHMENT: Inside each segment, show tiny CONTENT PREVIEWS:
  - Web segment: 2-3 faint horizontal lines (generic text)
  - Code segment: a tiny code bracket icon "{ }"
  - Wikipedia segment: a tiny encyclopedia icon
  - Books segment: a tiny book spine
  - Math segment: a tiny "∑" or "∫" symbol
  These icons make each segment's content type instantly recognizable.
- Each segment gets a right-aligned label with source name and %

BOTTOM CALLOUT (spanning full width):
A centered white card with thin blue border:
"Upweighting high-quality sources costs zero extra compute
but measurably improves target capabilities."
"zero" in orange (#FF9F43).

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders, subtle shadow
- Bar segments: distinct colors from the blue-teal-navy palette
- Orange accent: #FF9F43 ONLY on Math "×25" badge, Math segment
  border, and the word "zero"
- Text: #1A1A2E for titles, #6B7280 for annotations
- Clean sans-serif typography
- Thin white gaps between bar segments for readability
- Generous margins and spacing

IMPORTANT:
- Do not use pie charts
- Do not use 3D, gradient fills, or glow effects
- Do not use more than 6 source categories
- Do not make the figure feel like a matplotlib screenshot
- The center column's multiplier badges are essential — they
  quantify the transformation, not just show arrows
- Content preview icons inside right bar segments add richness
```

## Review checklist

- [ ] Two tall stacked bars: Natural (left) vs Training Mix (right)
- [ ] Left bar: web dominates at ~95%, visually monotone
- [ ] Right bar: visibly diverse with 6 distinguishable segments
- [ ] Center column: multiplier badges (×0.68 to ×25) with curved arrows
- [ ] Math "×25" badge in orange — the largest and most prominent
- [ ] Content preview icons inside right bar segments (code brackets, book spine, etc.)
- [ ] Faint watermark pattern inside left bar's web segment
- [ ] Orange accent limited to Math badge, Math border, and "zero"
- [ ] Landscape orientation
- [ ] Matches the visual richness of ch10 figures
