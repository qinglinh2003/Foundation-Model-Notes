# Figure 7.1: Hardware Bandwidth Hierarchy

**Filename**: `bandwidth_hierarchy.png`
**LaTeX label**: `fig:bandwidth-hierarchy`
**Caption**: The memory-to-network bandwidth hierarchy spans four orders of magnitude. Each parallelism strategy maps to the tier whose bandwidth can support its communication pattern.

## Prompt

```text
Create a clean, minimal infographic for a graduate-level ML textbook.
Landscape orientation. Match the visual style of this book exactly:
flat blue-white design, generous white space, simple geometric shapes,
clean sans-serif typography. Light blue background (#EBF5FF or similar).

REFERENCE STYLE: This book uses card-based layouts with rounded blue
boxes, thin lines, small icons, and lots of breathing room. See the
"Scaling Changes the Regime" figure (4 cards with blue cube icons) and
the "BPE Merge Trace" figure (step-by-step boxes with arrows) for the
exact visual language. NO hardware renders, NO 3D, NO glowing effects.

CONCEPT: Show 5 bandwidth tiers as a HORIZONTAL WATERFALL flowing
left to right, where each tier is progressively narrower (slower).

LAYOUT:
5 rounded rectangular cards arranged left to right in a single row.
Each card is slightly narrower than the previous one, creating a
visual "narrowing" that represents decreasing bandwidth.

Card 1 (widest): "SRAM"
  Bandwidth: ~20 TB/s
  Small icon: chip/core icon
  Note: "FlashAttention"

Card 2: "HBM"
  Bandwidth: 2-3 TB/s
  Small icon: memory chip icon
  Note: "Weight reads"

Card 3: "NVLink"
  Bandwidth: 600-900 GB/s
  Small icon: two-GPU connection icon
  Note: "Tensor Parallelism"
  Badge: "Intra-node"

Card 4: "InfiniBand"
  Bandwidth: 50-200 GB/s
  Small icon: cable/network icon
  Note: "Pipeline Parallelism"
  Badge: "Inter-node"

Card 5 (narrowest): "Ethernet"
  Bandwidth: 10-50 GB/s
  Small icon: globe/cloud icon
  Note: "Data Parallelism"

Between each pair of cards, show the bandwidth DROP FACTOR in orange
(#D35400): "~10x", "~5x", "~5x", "~3x". These are the ONLY orange
elements. Use small orange downward arrows or badges.

Below the cards, a single-line annotation:
"Communication-heavy parallelism must stay on the fastest fabric."

COLOR SYSTEM:
- Background: light blue gradient (#EBF5FF to #F5F9FF)
- Cards: white with thin blue (#2D8CFF) borders, rounded corners
- Card interiors: white
- Text: dark charcoal for titles, gray for notes
- Icons: simple blue line icons (like the ones in the Training Pipeline figure)
- Orange (#D35400): ONLY on the drop-factor badges

BEAUTY PRINCIPLES:
- Lots of white space INSIDE and BETWEEN cards
- Cards should feel airy, not packed
- The narrowing card widths should be subtle but noticeable
- Clean, flat, editorial — like an Economist infographic
- No decoration beyond what communicates information

DO NOT: concentric circles, radial layouts, 3D, GPU photos, complex
wiring, neon colors, dark backgrounds, heavy borders
```

## Review Checklist

- [ ] 5 tiers shown left to right
- [ ] Cards narrow progressively (visual metaphor for bandwidth decrease)
- [ ] Bandwidth values correct
- [ ] Orange drop factors between cards (ONLY orange elements)
- [ ] Parallelism mapping shown on each card
- [ ] Matches book's flat blue-white card-based visual language
- [ ] Landscape orientation
- [ ] Clean, spacious, beautiful
