# Figure 23.2: Local Detail Versus Global Representation

**Filename**: `fig_local_detail_global_representation.png`
**LaTeX label**: `fig:ch23-local-detail-global-representation`
**Caption**: \textbf{Local detail versus global representation.} Patch-level or multiscale features can preserve small objects, attributes, and spatial relations. A pooled representation may preserve the scene gist while discarding the local evidence needed for grounding.

## Prompt

```text
Draw a wide comparison diagram for a graduate-level machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Compare local patch-level visual features with a pooled global image representation. Teach that a representation can preserve scene gist while losing the small local evidence needed to answer a grounding question.

MAIN COMPOSITION:
Split the canvas into three horizontal zones: input image on the left, local-feature path across the top right, global-pooled path across the bottom right. Use the same table-scene image in both paths for comparison.

LEFT -- INPUT IMAGE:
Show a dining-table scene with a small cup on the left, a central plate, and background table texture. Add the user question in a small callout: "What color is the small cup on the left?"

TOP PATH -- LOCAL FEATURES:
Show a patch grid or multiscale feature map preserving regions. Include three zoomed mini-crops: "small cup", "cup color", and "left-of plate". Represent local tokens as a small grid of blue squares with one orange square marking the cup region. Add short labels:
- "attributes"
- "boundaries"
- "spatial relations"

BOTTOM PATH -- GLOBAL REPRESENTATION:
Show the full image collapsing through a pooling funnel into one large capsule labeled "global gist". Inside the capsule include tiny icons for "table scene", "cups", "indoor", but omit the cup color. Add a small warning label: "local detail may be pooled away".

RIGHT -- OUTCOME COMPARISON:
Add two compact answer panels:
Top local path: "Evidence recoverable: cup color"
Bottom global path: "Gist preserved: table setting"

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — use only on the small cup token / local crop
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
- Do not make this look like a generic classification diagram; emphasize local grounding.
- Do not use paragraphs of text; use compact labels.
- Keep the local and global paths visually distinct and parallel.
- Make the small cup visibly peripheral and easy to identify.
- Use one orange accent only on the small-cup evidence.
- Fill the full canvas with the comparison paths and outcome panels.
- All text must be readable at 50% PDF width.
- Avoid implying global representations are bad; show they are useful for gist but weak for local detail.
```

## Review Checklist

- [ ] The input image includes a small cup on the left
- [ ] A local-feature path preserves cup color or cup region evidence
- [ ] A global-pooled path preserves scene gist but loses local detail
- [ ] The figure includes the question about the small cup
- [ ] Orange accent appears only on the local cup evidence
- [ ] The contrast is about local grounding, not generic classification
- [ ] Text labels are short and readable
- [ ] No dark background, gradients, product logos, or 3D effects
