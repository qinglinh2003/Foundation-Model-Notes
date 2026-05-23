# Figure 12.3: Intrinsic Dimension of Fine-Tuning

**Filename**: `fig_intrinsic_dimension.png`
**LaTeX label**: `fig:intrinsic-dimension`
**Caption**: The intrinsic dimension of fine-tuning. Left: the full parameter space is vast, but pretraining has already placed the model near a good region. Center: the fine-tuning update lives in a surprisingly small subspace---classic intrinsic-dimension experiments show that much smaller projected spaces can recover much of full fine-tuning quality. Right: LoRA parameterizes this subspace explicitly as a learned low-rank factorization. This is the mathematical echo of Chapter~11's LIMA observation: fine-tuning redirects, it does not rebuild.

## Prompt

```text
Draw an intrinsic dimension diagram for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system. LANDSCAPE
orientation, wide and spacious. Match the visual richness of the book's
best figures --- Ch10 "Three-Layer Schema" concentric rings with
progressive detail, Ch7 "Bandwidth Hierarchy" layered structure, Ch9
"Data Funnel" narrative left-to-right transformation.

CONCEPT:
"Fine-tuning lives in a tiny subspace." This is the chapter's
conceptual soul --- the mathematical explanation for why LoRA works.
The figure tells a THREE-PANEL progressive zoom story: vast parameter
space → tiny intrinsic subspace → LoRA's parameterization of that
subspace. It should deliver the same kind of "oh" moment as Ch10's
three-layer schema.

MAIN COMPOSITION:
THREE-PANEL PROGRESSIVE ZOOM:
Three panels arranged left to right, connected by zoom-arrow brackets.
Each panel is a rounded white card with thin blue border. The panels
get progressively SMALLER in depicted space but RICHER in detail ---
this inversion is the visual storytelling device.

PANEL 1 --- "FULL PARAMETER SPACE" (leftmost):
A large, mostly featureless contour landscape:
- Draw a bird's-eye contour map (topographic style) in very pale blue
  (#E8F4FD) with subtle contour lines in #CFE3F7
- The landscape is vast and mostly flat --- most directions are
  irrelevant for fine-tuning
- A single small dot in primary blue (#2D8CFF) labeled "pretrained
  model" sits in a good region (near a valley/basin)
- Around the dot, a tiny highlighted rectangular region outlined in
  dashed blue --- this is where we zoom next
- Label at top: "Full Parameter Space"
- Annotation at bottom: "Most directions do not matter for fine-tuning"
- The overall feel should be VAST and mostly EMPTY

PANEL 2 --- "INTRINSIC SUBSPACE" (center):
A zoomed-in view of the highlighted region from Panel 1:
- Now the contour lines are visible and meaningful --- a clear valley
  or basin with concentric contour lines
- The pretrained model dot appears again at the edge of the valley
- A short curved path in soft orange (#FF9F43) traces the fine-tuning
  trajectory from the pretrained point to the fine-tuned point at the
  valley floor --- this is the ONLY orange element
- The path is short and direct --- fine-tuning is a small redirect
- Two thin coordinate axes labeled "intrinsic dim 1" and "intrinsic
  dim 2" to show this is a low-dimensional slice
- Label at top: "Intrinsic Subspace"
- Annotation: "d_intrinsic surprisingly small"
- A small callout card below: "Aghajanyan et al. (2020): much smaller
  projected subspaces can recover most full-FT quality in classic
  experiments"

PANEL 3 --- "LoRA's PARAMETERIZATION" (rightmost):
The same valley from Panel 2, but now with LoRA's coordinate system:
- The two axes are now labeled "B columns" and "A rows"
- The same orange fine-tuning path is shown
- Small matrix icons at each axis end: a thin tall block labeled "B"
  on the vertical axis, a thin wide block labeled "A" on the horizontal
- A badge at the top: "rank r = number of axes"
- Label at top: "LoRA Coordinates"
- Annotation: "Learned low-rank basis replaces random projection"

ZOOM CONNECTORS:
Between Panel 1 and Panel 2: thin dashed bracket lines from the
highlighted region to Panel 2's borders, suggesting a zoom operation.
Between Panel 2 and Panel 3: similar bracket lines but shorter,
suggesting a re-parameterization (same space, different coordinates).

BOTTOM BANNER:
A wide white card with thin blue border spanning full width below
all three panels. Contains the conceptual bridge to Ch.11:
Left side: "Ch.11 (behavioral): SFT surfaces existing capability,
it does not teach new knowledge"
Right side: "Ch.12 (mathematical): the update lives in a subspace
far smaller than the full parameter space"
Center divider: a small "=" or "same insight" badge connecting the two.

STYLE:
- Background: #FAFCFF
- Panel backgrounds: white with thin #CFE3F7 borders, subtle shadow
- Contour lines: #CFE3F7 (Panel 1, faint), #B7D9F2 (Panel 2, visible)
- Pretrained dot: #2D8CFF
- Fine-tuning path: #FF9F43 (orange) --- the ONLY orange element
- Matrix icons: #2D8CFF (B) and #E8F4FD (A)
- Text: #1A1A2E for labels, #6B7280 for annotations
- Clean sans-serif typography, generous spacing between panels
- Progressive detail: Panel 1 is sparse, Panel 2 is moderate,
  Panel 3 has the most structure

IMPORTANT:
- Do not use 3D surface plots or wireframe meshes
- Do not use neural network diagrams
- Do not use scatter plots of training runs
- Do not make the three panels equal in visual density --- Panel 1
  must feel vast/empty, Panel 3 must feel structured/labeled
- The zoom progression is the key visual device --- it must read
  naturally left to right
- Do not crowd the bottom banner with too much text
- The orange fine-tuning path should be short and direct, not
  winding or complex
```

## Review Checklist

- [ ] Three-panel progressive zoom: vast space → intrinsic subspace → LoRA axes
- [ ] Panel 1 feels vast and mostly empty with a single pretrained dot
- [ ] Panel 2 shows clear valley/basin with contour lines
- [ ] Orange fine-tuning path visible in Panels 2 and 3 (only orange element)
- [ ] Panel 3 relabels axes as B columns / A rows with matrix icons
- [ ] Zoom connectors link panels visually
- [ ] Bottom banner bridges Ch.11 behavioral → Ch.12 mathematical insight
- [ ] Aghajanyan citation callout in Panel 2
- [ ] Progressive visual density: sparse → moderate → structured
- [ ] "rank r = number of axes" badge in Panel 3
- [ ] Landscape orientation, matches Three-Layer Schema quality
- [ ] Readable at 50% width in PDF
