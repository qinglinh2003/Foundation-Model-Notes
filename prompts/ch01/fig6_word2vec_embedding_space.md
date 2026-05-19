# Figure 1.6: Word2Vec Static Embedding Space

**Filename**: `word2vec_embedding_space.png`
**LaTeX label**: `fig:word2vec-space`
**Caption**: A stylized 2D projection of a Word2Vec embedding space. \emph{Left:} semantic clusters and the classic analogy parallelogram show that distances and directions encode meaning. \emph{Right:} the word \texttt{bank} appears as a single point regardless of context, illustrating the polysemy limitation that contextual models such as ELMo address.

## Prompt

```
Draw a two-panel figure for a machine learning textbook illustrating Word2Vec's
static embedding space. Use the course's Zoom-inspired blue-white visual system.
The figure should be polished and editorial, not a rough whiteboard sketch.

OVERALL LAYOUT:
- Landscape orientation, generous whitespace
- Two panels side by side, separated by a thin vertical divider line in #E8F4FD
- Left panel occupies roughly 60% of the width, right panel 40%
- Pale blue (#F0F7FF) background for each panel, #FAFCFF for the overall background

LEFT PANEL — EMBEDDING GEOMETRY:
- Title above panel in charcoal (#1A1A2E): "Embedding Space"
- A 2D scatter plot showing word dots in a continuous space
- Three visible semantic clusters, each in a translucent light blue (#E8F4FD)
  rounded region:
  1. Animals cluster: "cat", "dog", "fish" — bottom left area
  2. Countries cluster: "France", "Germany", "Japan" — top left area
  3. Royalty/gender cluster: "king", "queen", "man", "woman" — center right area
- Each word is a small filled circle in #2D8CFF (Zoom Blue) with its label
  in charcoal (#1A1A2E) next to it
- ANALOGY PARALLELOGRAM (the hero element):
  - Draw a dashed parallelogram connecting king, queen, man, woman
  - The parallelogram lines are #0B5CFF (deep blue), dashed
  - The arrow from "man" to "king" and from "woman" to "queen" are labeled
    "royalty" in steel gray (#6B7280)
  - The arrow from "man" to "woman" and from "king" to "queen" are labeled
    "gender" in steel gray
  - This demonstrates: king - man + woman ≈ queen
- Below the parallelogram, a small annotation in steel gray:
  "king − man + woman ≈ queen"

RIGHT PANEL — STATIC LIMITATION (polysemy problem):
- Title above panel in charcoal: "One Vector Per Word"
- Show three different contexts at the top, each in a rounded white pill
  with blue border:
  1. "river bank"
  2. "investment bank"
  3. "central bank"
- From each context pill, draw a downward arrow converging to ONE single
  point labeled "v_bank"
- The single point v_bank is drawn in #FF9F43 (soft orange) — this is the
  ONE orange accent in the figure, highlighting the problem
- Below v_bank, a small annotation in steel gray:
  "same vector regardless of context"
- The visual message: all three different senses of "bank" collapse into
  one fixed point — this is the limitation

ARROWS AND LINES:
- Parallelogram edges: dashed #0B5CFF
- Context-to-vector arrows: solid #6B7280 (steel gray), converging
- All arrows: smooth, medium weight, clean pointed heads

STYLE:
- Background: #FAFCFF
- Very subtle blue-tinted shadows on cluster regions
- Only non-blue color: the orange v_bank point in the right panel
- Clean, modern, Zoom-like tech aesthetic
- Match the same rounded geometry, line weights, typography, margins, and subtle
  shadows used by the other Chapter 1 figures
```

## Review Checklist

- [ ] Two panels clearly separated: embedding geometry (left) and polysemy limitation (right)
- [ ] Three semantic clusters visible with translucent blue backgrounds
- [ ] Analogy parallelogram connects king, queen, man, woman with dashed lines
- [ ] "king - man + woman ≈ queen" annotation present
- [ ] Three different "bank" contexts all point to ONE single v_bank point
- [ ] v_bank is the ONLY orange element in the entire figure
- [ ] No other warm colors (no coral, teal, purple, green)
- [ ] Labels are crisp, short, and correctly spelled
- [ ] Style matches other Ch1 figures (same blue palette, rounded geometry, shadows)
