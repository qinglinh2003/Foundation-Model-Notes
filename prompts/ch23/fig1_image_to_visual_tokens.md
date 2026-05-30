# Figure 23.1: From Image to Visual Tokens

**Filename**: `fig_image_to_visual_tokens.png`
**LaTeX label**: `fig:ch23-image-to-visual-tokens`
**Caption**: \textbf{From image to visual tokens.} A patch-based encoder resizes the image, divides it into spatial patches, linearly projects each patch into a vector, adds position information, and processes the resulting sequence with Transformer blocks.

## Prompt

```text
Draw a wide pipeline diagram for a graduate-level machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Show how a still image becomes a finite sequence of visual tokens before it reaches a Transformer encoder. The figure should make clear that the model does not see raw pixels directly; it sees patched, embedded, position-marked vectors.

MAIN COMPOSITION:
Create a left-to-right pipeline with six stages connected by thin blue arrows. Fill the full canvas width.

STAGE 1 -- INPUT IMAGE:
Show a simple dining-table scene as a clean flat illustration: table surface, plate, fruit bowl, and a small cup near the left edge. Put a tiny label "I: H x W x C" beneath it.

STAGE 2 -- RESIZE:
Show the same image inside a smaller frame labeled "resize to model input". Add a subtle ruler icon and a note "detail may shrink".

STAGE 3 -- PATCH GRID:
Overlay a visible 4 x 4 patch grid on the image. Highlight one left-edge patch that contains the small cup mixed with table texture. Label: "P x P patches".

STAGE 4 -- FLATTEN + PROJECT:
Show several patch tiles becoming short vertical vectors, then passing through a small linear projection box labeled "linear projection to d_v". Include tiny vector bars, not equations only.

STAGE 5 -- POSITION:
Show token vectors receiving small coordinate tags such as "(row 1, col 2)" and "(row 3, col 4)". Label: "add positional information".

STAGE 6 -- TRANSFORMER ENCODER:
Show a compact stack of Transformer blocks consuming an ordered row of blue token capsules labeled v1, v2, v3, ... vN.

BOTTOM STRIP:
Add a thin summary banner spanning the bottom:
"Image pixels become a budgeted sequence of visual tokens."

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — use only on the one highlighted patch containing the small cup
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
- Do not draw a photorealistic image; use clean textbook-style flat illustration.
- Do not use product logos, robot mascots, camera brands, or UI screenshots.
- Keep text labels short and readable at 50% PDF width.
- Use exactly one orange focal element: the highlighted small-cup patch.
- Make the arrows show a clear left-to-right sequence.
- Include internal visual detail in every stage; avoid plain empty boxes.
- Fill the full width with no large empty corners.
- Do not imply the patch token is a word token; keep it spatial and vector-like.
```

## Review Checklist

- [ ] Six stages are visible: input, resize, patch grid, project, position, Transformer
- [ ] The small cup appears near the left edge of the input image
- [ ] One patch containing the cup is highlighted in orange
- [ ] Visual tokens are shown as vectors or capsules, not as words
- [ ] Positional information appears explicitly
- [ ] Bottom strip states the budgeted-token lesson
- [ ] All labels are readable at 50% PDF width
- [ ] No product logos, mascots, gradients, dark background, or 3D effects
