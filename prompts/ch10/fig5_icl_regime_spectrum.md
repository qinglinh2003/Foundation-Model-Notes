# Figure 10.3: ICL Regime Spectrum

**Filename**: `fig_icl_regime_spectrum.png`
**LaTeX label**: `fig:icl-regime-spectrum`
**Caption**: In-context learning evaluation spans three regimes. Zero-shot relies on instruction alone and is simple but ambiguous; few-shot (3--8 demonstrations) is the standard protocol for Project~2 and balances informativeness with manageable degrees of freedom; many-shot (100+) requires long-context infrastructure and introduces dual-use concerns. The protocol choice is itself an experimental variable.

## Prompt

```text
Draw an ICL regime spectrum for a machine learning textbook. Use the
course's Zoom-inspired blue-white visual system. LANDSCAPE orientation,
wide and spacious. Match the visual richness of the book's best
figures — Ch4 "Signal Density" token-level visualization with colored
blocks, Ch3 "KV Cache" two-panel comparison with internal state
diagrams, Ch4 "BERT vs JEPA" side-by-side with architectural detail.

CONCEPT:
"Three ICL regimes — three evaluation protocols, not three tricks."
This figure shows zero-shot, few-shot, and many-shot as CONCRETE
PROMPT CONSTRUCTIONS, not abstract labels. The reader should see
what each prompt actually looks like, and feel the increasing
complexity (degrees of freedom) from left to right.

MAIN COMPOSITION — THREE PROMPT CONSTRUCTION PANELS:
Three tall cards arranged horizontally. Each card shows the ACTUAL
STRUCTURE of a prompt in that regime, drawn as a vertical stack of
colored token blocks (like Ch4's Signal Density figure). The cards
grow in visual complexity from left to right.

CARD 1 (left) — ZERO-SHOT:
- Title: "Zero-shot" in bold charcoal
- Card fill: very pale blue (#F0F7FF), thin #CFE3F7 border
- INTERNAL ILLUSTRATION — A vertical prompt construction:
  - A single white block labeled "System instruction" at the top,
    with 2-3 tiny horizontal lines inside (representing instruction text)
  - A thin blue divider line
  - A block labeled "Test question" in primary blue (#2D8CFF)
  - That's it — the prompt is visually SHORT and SPARSE
  - The empty space below should feel intentional — there's nothing
    else to configure
- Below the card: "1 degree of freedom: template wording"
- Small annotation: "Simple but ambiguous"

CARD 2 (center) — FEW-SHOT (K = 3-8):
- Title: "Few-shot (K = 3–8)" in bold charcoal
- Card border: orange (#FF9F43) — the ONLY orange-bordered card
- Card fill: white
- INTERNAL ILLUSTRATION — A taller vertical prompt construction:
  - "System instruction" block at top (same as Card 1)
  - Blue divider
  - THREE EXAMPLE BLOCKS stacked vertically, each slightly different:
    - "Example 1" — a small Q/A pair shown as two nested rectangles
      (light blue question block + white answer block)
    - "Example 2" — same structure
    - "Example 3" — same structure
    Each example pair has a tiny number badge ("1", "2", "3") on the left
  - A small "..." indicating more examples could be added
  - Blue divider
  - "Test question" block in primary blue
  - The prompt is TALLER and RICHER than Card 1

  To the RIGHT of the example stack, draw 3 small ANNOTATION ARROWS
  pointing to different aspects, each labeling a degree of freedom:
  - Arrow to the examples: "which examples?"
  - Arrow to the ordering: "what order?"
  - Arrow to the count: "how many?"
  These arrows in steel gray, small text.

- Below the card: "4+ degrees of freedom: template + K + selection + order"
- Subtitle: "Project 2 recommended" in orange (#FF9F43)

CARD 3 (right) — MANY-SHOT (K = 100+):
- Title: "Many-shot (K = 100–1000)" in bold charcoal
- Card fill: very pale blue (#F0F7FF)
- Card border: DASHED #CFE3F7 (indicating "optional, not required")
- INTERNAL ILLUSTRATION — A very tall vertical prompt construction:
  - "System instruction" block at top
  - Blue divider
  - MANY example blocks, but shown as a compressed/scrolling list:
    - First 3 example blocks drawn normally
    - Then a visual COMPRESSION: many thin lines getting progressively
      shorter and more faded, suggesting 100+ examples. Use a "..."
      and a small count: "×100-1000"
  - Blue divider
  - "Test question" block in primary blue
  - The prompt is VERY TALL, and the compression visual should make
    the scale feel impractical for a small model

  A small WARNING tag inside the card: "Requires long context" in
  steel gray with a tiny caution triangle.
  Another small tag: "Dual-use risk" in steel gray.

- Below the card: "5+ degrees of freedom: template + K + selection + order + context budget"
- Small annotation: "Not required for 900M project"

BOTTOM AXIS (spanning all three cards):
A thin horizontal bar below all three cards:
- Left end: "Fewer protocol degrees of freedom"
- Right end: "More protocol degrees of freedom"
- The bar is divided into 5 small adjacent segments that step from
  pale blue (#CFE3F7) to primary blue (#2D8CFF). Do not use a smooth
  gradient.
- Small upward tick marks at each card position

TOP COMPARISON BAR (small, above the cards):
A thin comparison strip showing rough score variance introduced by each:
- Zero-shot: "±2–3 pp (template only)"
- Few-shot: "±5–10 pp (template + examples)"
- Many-shot: "±15+ pp (all variables)"
This connects to the prompt sensitivity figure and makes the
increasing-variance message concrete.

STYLE:
- Background: #FAFCFF
- Cards: white or pale blue, thin #CFE3F7 borders, subtle shadow
- Primary blue: #2D8CFF
- Example blocks: light blue (#B7D9F2) for questions, white for answers
- Orange accent: #FF9F43 ONLY on Card 2 border + "Project 2 recommended"
- Dashed border on Card 3 only
- Text: #1A1A2E for titles, #6B7280 for annotations
- Clean sans-serif typography, generous margins

IMPORTANT:
- Each card must show a CONCRETE PROMPT STRUCTURE with colored blocks,
  not just text labels in a box
- The visual height of the prompt construction must increase left to right
- Do not draw neural network internals or attention mechanisms
- Do not use icons of brains, robots, or chat bubbles
- Do not use 3D, glow, or gradient fills
- Keep it as an evaluation protocol comparison showing what the
  prompts actually look like
```

## Review Checklist

- [ ] Three cards showing actual prompt constructions as colored block stacks
- [ ] Card 1 (Zero-shot): instruction + question only — visually SHORT
- [ ] Card 2 (Few-shot): instruction + 3 example pairs + question — MEDIUM, with annotation arrows labeling degrees of freedom
- [ ] Card 3 (Many-shot): instruction + compressed 100+ examples + question — TALL, with warning tags
- [ ] Prompt constructions use colored blocks (light blue Q, white A) like token visualizations
- [ ] Card 2 has orange border + "Project 2 recommended" orange subtitle
- [ ] Card 3 has dashed border + "Not required" annotation
- [ ] Bottom axis: fewer → more degrees of freedom
- [ ] Top comparison bar showing approximate variance per regime
- [ ] Orange accent only on Card 2
- [ ] Landscape orientation, matches Signal Density / BERT vs JEPA quality
- [ ] Readable at 50% width in PDF
