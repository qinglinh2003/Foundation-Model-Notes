# Figure 18.4: Self-Consistency Pipeline

**Filename**: `fig_self_consistency_pipeline.png`  
**LaTeX label**: `fig:ch18-self-consistency-pipeline`  
**Caption**: Self-consistency turns one prompt into a small reasoning ensemble. Multiple sampled traces produce final answers; aggregation uses answer agreement as a weak selection signal.

## Prompt

```text
Draw a self-consistency pipeline for chain-of-thought reasoning.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, spacious and readable.

CONCEPT:
Self-consistency samples multiple reasoning traces, extracts final answers, and chooses the answer with strongest agreement.

MAIN COMPOSITION:
Left: one prompt card labeled "Question".
From it, branch into 6 reasoning trace cards arranged in two rows.
Each trace card should show a short abstract step pattern, not real math:
"path A: decompose → solve → answer 42"
"path B: equation → simplify → answer 42"
"path C: shortcut → answer 41"
Do not use too much text; use icons and short labels.

Middle-right: "Answer extraction"
Show final answer chips: 42, 42, 42, 41, 42, 43.

Right: "Vote / cluster"
Show a tally where 42 wins with 4 votes, 41 and 43 have 1 each.
Final output card: "selected answer: 42".

Bottom warning strip:
"Agreement is evidence, not proof: correlated mistakes can still win."

STYLE:
- Background #FAFCFF
- Primary blue #2D8CFF for winning traces/answer
- Pale blue #E8F4FD for trace cards
- Gray #D1D5DB for losing alternatives
- Orange #FF9F43 only for warning strip
- Text #1A1A2E, annotations #6B7280
- Clean sans-serif typography
- No dark background, no glow, no 3D

IMPORTANT:
- Make the many-traces-to-one-answer flow visually obvious.
- Do not show long chain-of-thought text.
- Warning about correlated errors must be visible.
- All text must remain readable at PDF size.
```

## Review Checklist

- [ ] One prompt branches into multiple traces.
- [ ] Final answers are extracted and tallied.
- [ ] Winning answer is selected by agreement.
- [ ] Correlated-error warning is present.
