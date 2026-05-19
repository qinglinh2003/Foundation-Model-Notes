# Figure 3.5: Shifted Labels for Next-Token Prediction

**Filename**: `shifted_labels.png`
**LaTeX label**: `fig:shifted-labels`
**Caption**: Next-token prediction training: logits at position $t$ are supervised by the token at position $t+1$. The input and target sequences are the same text shifted by one position. The final input token has no target; the first target token has no preceding input logit.

## Prompt

```
Draw a diagram for a machine learning textbook showing how
next-token prediction training aligns inputs with shifted labels.
Use the course's Zoom-inspired blue-white visual system.
The figure should be polished and editorial.

LAYOUT:
- Two horizontal rows of 5 boxes each, aligned vertically
- Top row label (left): "Input tokens"
- Bottom row label (left): "Target labels"

TOP ROW (Input tokens):
- 5 boxes: "The", "cat", "sat", "on", "the"
- Each box has a light blue (#E8F4FD) fill
- Below each box, small gray text: "pos 0", "pos 1", "pos 2", "pos 3", "pos 4"

BOTTOM ROW (Target labels):
- 5 boxes: "cat", "sat", "on", "the", "mat"
- Each box has a slightly different light blue (#D6ECFA) fill
- Below each box, small gray text: "pos 0", "pos 1", "pos 2", "pos 3", "pos 4"

ARROWS:
- Draw diagonal downward arrows from each input box to the
  target box directly below it
- Arrows should be in medium blue (#2563EB)
- Each arrow represents: "logits at this position predict this target"

KEY HIGHLIGHT:
- Use orange (#FF9F43) to highlight the arrow from "on" (input pos 3)
  to "the" (target pos 3), as the featured prediction pair
- Add a small orange annotation: "logits[3] should predict 'the'"

RIGHT-SIDE ANNOTATION:
- A small bracket showing the shift:
  "input[t] → target[t] = input[t+1]"
  in charcoal text

COMMON BUG CALLOUT (optional):
- Small red (muted, not bright) text below the diagram:
  "Bug: if logits[t] predicts input[t] instead of input[t+1],
   the model sees its own answer → suspiciously low loss"

VISUAL STYLE:
- Clean, sans-serif labels in charcoal (#374151)
- White background (#FAFCFF)
- No shadows, no 3D, no heavy gradients
- Grid alignment between rows
- Polished editorial textbook figure style
```

## Review Checklist

- [ ] Input and target rows are clearly labeled
- [ ] Target is input shifted by one position to the left
- [ ] Arrows go from input position to same-index target position (not offset)
- [ ] Orange accent on exactly one arrow pair
- [ ] Position indices are consistent between rows
- [ ] "The cat sat on the" input, "cat sat on the mat" target — shift is correct
- [ ] Bug callout (if included) is visually de-emphasized
