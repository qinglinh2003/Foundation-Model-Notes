# Figure 4.2: Masked Language Modeling Training Flow

**Filename**: `mlm_training.png`
**LaTeX label**: `fig:mlm-training`
**Caption**: The MLM training procedure: 15\% of tokens are selected, corrupted via the 80/10/10 strategy, and the model predicts the originals only at masked positions.

## Prompt

```
Draw the Masked Language Modeling (MLM) training procedure for a graduate-level
machine learning textbook. Use the course's blue-white visual system.
Landscape orientation, polished editorial style.

LAYOUT:
A vertical flow diagram showing how one training example is processed.

ROW 1 — ORIGINAL INPUT:
- A 12-token sentence in token boxes:
  "The curious cat sat quietly on the old mat near the window"
- All boxes in light blue, clean and even

ROW 2 — SELECTION (15% chosen):
- Arrow down labeled "Select 15% of positions"
- Same sentence but 2 positions are highlighted (roughly 15% of 12 tokens):
  "cat" and "old"
- Highlighted positions have a dashed orange border indicating
  "selected for corruption"

ROW 3 — CORRUPTION (80/10/10):
- Three branches from each selected position showing the 80/10/10 rule:
  - Token "cat": replaced with [MASK] — labeled "80%: [MASK]"
  - Token "old": replaced with random word "green" — labeled "10%: random"
  - Show a ghost/faded third option: "10%: keep original" with a small note
- The corrupted sequence shown in full:
  "The curious [MASK] sat quietly on the green mat near the window"
- [MASK] token in soft orange (#FF9F43) — this is the figure's orange accent
- Random replacement "green" in a lighter orange tint

ROW 4 — TRANSFORMER:
- A blue rounded box labeled "BERT Encoder (12 layers)"
- Input arrows from corrupted sequence going in
- Output arrows coming out to ROW 5

ROW 5 — PREDICTION + LOSS:
- Output representations shown as boxes
- Prediction heads ONLY at positions 2 and 5 (where corruption happened)
- Token "cat": prediction "cat" with checkmark ✓
- Token "old": prediction "old" with checkmark ✓
- Other positions: grayed out, labeled "No loss computed here"
- Loss arrows only from positions 2 and 5

ANNOTATIONS:
- Right side: "Loss on 15% of tokens only"
- Right side: "Other 85% provide context but no gradient"
- Bottom: "Train/test mismatch: [MASK] appears in training but not at inference"

VISUAL DETAILS:
- Zoom Blue (#2D8CFF) for all standard elements
- Soft Orange (#FF9F43) ONLY for [MASK] tokens and the 80/10/10 labels
- White/ice blue (#FAFCFF) background
- Grayed-out positions use light gray (#E0E0E0)
- Sans-serif labels in charcoal (#1A1A2E)
- Clean arrows with consistent weight
```

## Review Checklist

- [ ] Flow is top-to-bottom: original → selection → corruption → model → prediction
- [ ] 80/10/10 rule clearly shown with three options
- [ ] [MASK] tokens are orange (only orange element besides 80/10/10 labels)
- [ ] Loss computed ONLY at masked positions — other positions grayed out
- [ ] Annotation about train/test mismatch included
- [ ] "15% of tokens" stated explicitly
- [ ] No extra colors beyond blue + white + orange + gray
