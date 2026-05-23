# Figure 9.3: Why Deduplication Improves Generalization

**Filename**: `fig_dedup_impact.png`
**LaTeX label**: `fig:dedup-impact`
**Caption**: Deduplication improves generalization, not just efficiency. Left: with duplicates, gradient updates concentrate on memorizing repeated documents, creating narrow optima. Right: after dedup, the same gradient budget is spread across diverse documents, leading to smoother, more generalizable representations.

## Prompt

```text
Draw a deduplication impact visualization for a machine learning
textbook. Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious. Match the visual richness
of the book's best figures — Ch10 "Three-Layer Schema" concentric
rings with progressive visual density, Ch10 "Prompt Sensitivity"
illusion-vs-reality contrast where the right panel reveals what the
left panel hides.

CONCEPT:
"Same compute. Better generalization." Dedup doesn't just save disk
space — it fundamentally changes what the model learns. With
duplicates, gradients memorize; without, they generalize. The figure
should make this FEEL different through visual texture contrast.

MAIN COMPOSITION — TWO-PANEL NARRATIVE:

LEFT PANEL — "Duplicated Corpus" (~45% width):
A large white card with thin blue border and subtle shadow.

UPPER HALF — DOCUMENT GRID:
A 4×4 grid of small rounded document tiles (16 total).
- 10 tiles are the SAME pale blue (#B7D9F2) with a faint repeated
  line pattern inside — these are duplicates. They should have a
  subtle COPY BADGE (tiny "×3" or "×5" in the corner of some tiles)
  showing duplication count.
- 6 tiles are different shades from the blue-teal palette
  (#2D8CFF, #5B7FFF, #00B894, #1A3A5C, #7DBFF0, #B7D9F2)
- The grid should look MONOTONE — overwhelmingly one color.

LOWER HALF — GRADIENT FLOW VISUALIZATION:
Instead of a simple loss landscape, show a GRADIENT FLOW DIAGRAM:
- 8-10 small arrows emanating from a central "∇" gradient symbol
- Most arrows (6-7) point toward the SAME duplicated document group
  (converging to one area) — labeled "memorize"
- Only 2-3 arrows point elsewhere — labeled "explore"
- Below this: a mini loss landscape with 3-4 NARROW SHARP VALLEYS
  (spiky, unstable). A small blue dot trapped in one narrow valley,
  labeled "overfitted"
- The overall feel: concentrated, narrow, stuck

Subtitle: "Gradients concentrate on repeated content" in gray

RIGHT PANEL — "Deduplicated Corpus" (~45% width):
Same size white card.

UPPER HALF — DOCUMENT GRID:
A 4×4 grid where ALL 16 tiles are DIFFERENT colors from the full
blue-teal palette. Each tile has a unique internal pattern (different
line orientations, small shapes). No copy badges.
The grid should look like a RICH MOSAIC — vibrant and diverse.

LOWER HALF — GRADIENT FLOW VISUALIZATION:
- 8-10 arrows emanating from "∇" but now SPREADING OUT evenly across
  the diverse document tiles — no convergence to one area
- Each arrow labeled "learn" in small gray text
- Below: a mini loss landscape with ONE BROAD SMOOTH VALLEY.
  A blue dot sitting comfortably at the bottom, labeled
  "generalizable"
- The overall feel: distributed, broad, stable

Subtitle: "Gradients spread across diverse content" in gray

CENTER CONNECTOR:
A clean horizontal arrow from left panel to right panel.
- Above arrow: "Dedup" in bold charcoal
- Below arrow: "same token count, same compute" in small gray
- The arrow should feel like a TRANSFORMATION, not just a pointer

BOTTOM CALLOUT (spanning both panels):
A centered white card with thin blue border:
"Same compute budget. Better generalization."
"Better generalization" in orange (#FF9F43) — the ONLY orange
element in the entire figure.

STATS ROW (above the callout):
Three small metric badges spanning the width:
- "Duplicates removed: 30-50%" in a small white chip
- "Training loss: ~same" in a small white chip
- "Eval loss: −0.02 to −0.05 nats" in a small chip with orange
  left border (#FF9F43)
These numbers make the abstract concept concrete.

STYLE:
- Background: #FAFCFF
- Panel cards: white with thin #CFE3F7 borders, subtle shadow
- Document tiles: rounded rectangles with thin borders
- Duplicated tiles: same pale blue (#B7D9F2) with copy badges
- Diverse tiles: varied shades from blue-teal-navy palette
- Gradient arrows: thin lines with small arrowheads
- Loss landscapes: conceptual curves, not mathematical axes
- Orange accent: #FF9F43 ONLY on "Better generalization" and
  eval loss chip border
- Text: #1A1A2E for titles, #6B7280 for subtitles
- Clean sans-serif typography, generous spacing

IMPORTANT:
- Do not show actual mathematical loss function plots with axes/ticks
- Do not use photos or realistic document images
- Do not use 3D or glow effects
- The gradient flow diagrams (arrows from ∇) are essential — they
  visually explain WHY dedup helps, not just THAT it helps
- Copy badges on duplicated tiles quantify the problem
- Stats row makes the benefit concrete
```

## Review checklist

- [ ] Two panels: "Duplicated Corpus" vs "Deduplicated Corpus"
- [ ] Left: mostly same-color tiles with copy badges + convergent gradient arrows
- [ ] Right: all different-color tiles + evenly spread gradient arrows
- [ ] Gradient flow from ∇ symbol: concentrated (left) vs distributed (right)
- [ ] Mini loss landscapes: narrow spiky valleys (left) vs one broad valley (right)
- [ ] Arrow labeled "Dedup" + "same token count, same compute" between panels
- [ ] Stats row with concrete numbers (30-50% removed, −0.02 to −0.05 nats)
- [ ] Orange only on "Better generalization" and eval loss chip
- [ ] Blue-teal palette for document tiles
- [ ] Matches ch10 visual richness
