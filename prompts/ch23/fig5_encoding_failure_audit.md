# Figure 23.5: Encoding Failure Audit

**Filename**: `fig_encoding_failure_audit.png`
**LaTeX label**: `fig:ch23-encoding-failure-audit`
**Caption**: \textbf{Encoding failure audit.} Many VLM symptoms can originate before language generation: small objects disappear, attributes blur, boundaries mix, spatial precision weakens, local details are pooled away, salience bias dominates, or resolution mismatch changes the representation.

## Prompt

```text
Draw a wide failure-taxonomy diagram for a graduate-level machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Show that many VLM errors can originate at the visual encoding layer before language generation. The figure should help readers audit whether the visual evidence survived tokenization.

MAIN COMPOSITION:
Place a central horizontal pipeline across the top:
"Original image" -> "resize + patch" -> "visual encoder" -> "visual tokens" -> "LLM answer"
Put a large question under the visual-token stage:
"Did the evidence survive tokenization?"

FAILURE TAXONOMY GRID:
Below the pipeline, create seven compact cards in a 4-over-3 grid. Each card has a mini-illustration, a symptom label, and a diagnostic tag.

CARD 1 -- SMALL OBJECT LOST:
Mini-illustration: tiny cup shrinking below one patch.
Symptom: "misses small object"
Diagnostic: "crop oracle / higher resolution"

CARD 2 -- ATTRIBUTE LOST:
Mini-illustration: colored cup becoming gray or blurred.
Symptom: "gets color wrong"
Diagnostic: "local crop / attribute probe"

CARD 3 -- BOUNDARY MIXED:
Mini-illustration: one patch straddling cup and table.
Symptom: "object boundary ambiguous"
Diagnostic: "smaller patches / segmentation cue"

CARD 4 -- SPATIAL PRECISION WEAK:
Mini-illustration: left and right arrows fading over patch grid.
Symptom: "confuses left/right"
Diagnostic: "spatial crop / shuffle test"

CARD 5 -- POOLED AWAY:
Mini-illustration: many local tokens collapsing into one global gist token.
Symptom: "answers from scene gist"
Diagnostic: "local token probe"

CARD 6 -- SALIENCE BIAS:
Mini-illustration: central plate large and bright, small left cup dim.
Symptom: "ignores peripheral detail"
Diagnostic: "crop contrast / remove distractor"

CARD 7 -- RESOLUTION MISMATCH:
Mini-illustration: 14 x 14 position grid stretched to 28 x 28 with warped coordinates.
Symptom: "scale or position changes"
Diagnostic: "resolution ablation"

BOTTOM STRIP:
Add a thin summary banner:
"Before blaming reasoning, test whether the needed visual evidence was encoded."
Use the single orange accent on the word "encoded" or a small warning marker beside it.

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — use only in the bottom summary banner
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
- Do not draw a generic error checklist; every card must include a mini-illustration.
- Keep the pipeline visible but secondary to the failure taxonomy.
- Include all seven failure modes listed above.
- Make diagnostic tags short and readable.
- Use one orange accent only in the bottom strip.
- Fill the full canvas with the pipeline, card grid, and summary banner.
- All text must be readable at 50% PDF width.
- Do not include product logos, robots, or photorealistic screenshots.
```

## Review Checklist

- [ ] The top pipeline includes original image, patching, encoder, visual tokens, and answer
- [ ] The central audit question asks whether evidence survived tokenization
- [ ] Seven failure cards are present
- [ ] Each card includes a mini-illustration, symptom, and diagnostic
- [ ] Small-object, attribute, boundary, spatial, pooling, salience, and resolution failures are all included
- [ ] Bottom strip states the pre-reasoning audit lesson
- [ ] Orange accent appears only once
- [ ] Text remains readable at 50% PDF width
