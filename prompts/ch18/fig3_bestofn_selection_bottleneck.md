# Figure 18.3: Best-of-N and the Selection Bottleneck

**Filename**: `fig_bestofn_selection_bottleneck.png`  
**LaTeX label**: `fig:ch18-bestofn-selection-bottleneck`  
**Caption**: Best-of-N separates candidate availability from selector quality. More samples can make a correct answer appear, but final accuracy depends on whether the selector can identify it.

## Prompt

```text
Create a clear textbook diagram explaining best-of-N candidate generation and the selector bottleneck.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation.

CONCEPT:
Sampling many candidates increases the chance that at least one answer is correct, but final system accuracy depends on the selector/verifier choosing the correct candidate.

MAIN COMPOSITION:
Top row: "Generate N candidates"
Show 12 candidate cards flowing left to right. Most are pale gray with small X marks; three are blue with check marks. Label them "candidate 1 ... candidate N" only sparsely, not all cards.

Middle: a funnel labeled "selector / verifier"
The funnel receives all candidates. Show two possible selector outcomes:
- Good selector: arrow to a blue checked candidate.
- Weak selector: arrow to a gray plausible-looking but wrong candidate.

Bottom row: two small curves:
Left curve labeled "candidate-pool opportunity: pass@k rises with N".
Right curve labeled "selected accuracy: bottlenecked by q".
The selected accuracy curve should plateau below the pass@k curve.

Add a compact formula strip:
"system success ≈ candidate appears × selector chooses it"
Use notation "a_N × q".

STYLE:
- Background #FAFCFF
- Primary blue #2D8CFF for correct candidates and pass@k curve
- Orange #FF9F43 for selector bottleneck / weak selector path
- Pale gray #E5E7EB for wrong candidates
- Text #1A1A2E, annotations #6B7280
- Clean sans-serif typography
- No dashboard styling, no 3D

IMPORTANT:
- The selector bottleneck must be the visual focus.
- Show that more candidates alone does not guarantee better final output.
- Keep formulas large and readable.
```

## Review Checklist

- [ ] Candidate pool includes correct and incorrect candidates.
- [ ] Selector funnel is central.
- [ ] Good and weak selector outcomes are contrasted.
- [ ] pass@k and selected-accuracy curves are distinct.
- [ ] Formula strip is readable.
