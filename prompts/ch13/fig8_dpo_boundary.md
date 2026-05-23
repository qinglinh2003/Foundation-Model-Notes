# Figure 13.4: DPO Capability Boundary

**Filename**: `fig_dpo_boundary.png`
**LaTeX label**: `fig:dpo-boundary`
**Caption**: The DPO capability boundary. Left: tasks where DPO excels---helpfulness, format, tone, safety---all involve holistic comparative judgments. Right: tasks where DPO struggles---math reasoning, code correctness, sustained planning---all require dense or outcome-based reward signals. The boundary is not sharp: many tasks fall in between, and the right method depends on the specific quality gap.

## Prompt

```text
Draw a DPO capability boundary diagram for a graduate-level machine
learning textbook. Use a clean blue-white visual system: light blue
background, white cards, thin blue borders, charcoal text, and one soft
orange accent for the boundary zone.

CONCEPT:
DPO is excellent for holistic preference improvements, but it is not
the right tool for every post-training problem. The figure should show
a spectrum from "comparative judgment is enough" to "verifiable or dense
reward needed."

MAIN COMPOSITION:
A wide two-zone landscape. Left zone: "DPO works well". Right zone:
"Needs stronger reward signal". Between them: a soft orange transition
band labeled "boundary depends on the gap". Use task cards with internal
mini-icons in each zone.

LEFT ZONE -- "DPO WORKS WELL":
Four task cards arranged in a 2x2 grid:
1. Helpfulness: response bubble with organized bullet list
2. Format compliance: checklist / JSON braces icon
3. Tone and style: slider from terse to warm
4. Safety/refusal calibration: shield icon with balanced response bubble
Each card has a small pairwise comparison icon: A vs B with a checkmark.
Label: "holistic comparison"

RIGHT ZONE -- "NEEDS STRONGER SIGNAL":
Four task cards arranged in a 2x2 grid:
1. Multi-step math: equation steps with a final boxed answer
2. Code correctness: terminal test result / unit tests
3. Long-horizon planning: timeline with dependencies
4. Formal verification: proof/checkmark document
Each card has a verifier icon: test, answer key, or process signal.
Label: "outcome / process reward"

BOUNDARY BAND:
Vertical soft orange band between the zones. It should not be a hard
wall. Use a translucent gradient-free pale orange fill or dotted orange
texture. Label: "mixed cases". Place two small example cards inside:
- "concise reasoning explanation"
- "tool-use answer with style constraints"
These show that some tasks sit between DPO and RL-style methods.

TOP AXIS:
A horizontal arrow across the top:
"Holistic preference" -> "Dense / verifiable reward"
Use blue arrow line, with the boundary point marked in orange.

BOTTOM STRIP:
One-sentence rule:
"Use DPO when humans can reliably compare whole responses; use RL or
verifiers when correctness depends on intermediate steps or outcomes."

STYLE:
- Background: #FAFCFF
- Zone panels: white with thin #CFE3F7 borders
- Task cards: white with pale blue headers
- Primary blue: #2D8CFF
- Boundary accent: #FF9F43 only
- Text: #1A1A2E; secondary text: #6B7280
- Use simple schematic icons, not detailed illustrations
- Landscape orientation, balanced left/right density

IMPORTANT:
- Do not imply DPO is bad or obsolete
- Do not make the boundary a hard vertical wall
- Do not use red for failure; use soft orange for the transition zone
- Keep task card text short and readable
- The left/right distinction must be understandable at a glance
```

## Review Checklist

- [ ] Left zone shows DPO-suitable holistic tasks
- [ ] Right zone shows tasks needing verifier/dense rewards
- [ ] Soft orange boundary band with mixed cases
- [ ] Top axis: holistic preference -> dense/verifiable reward
- [ ] Bottom rule-of-thumb strip
- [ ] No hard wall or red failure styling
- [ ] Blue-white style with one orange boundary accent
- [ ] Readable at 50% width in PDF

