# Figure 16.4: DAPO Fixes Vanilla GRPO Failure Modes

**Filename**: `fig_dapo_failure_modes.png`
**LaTeX label**: `fig:dapo-failure-modes`
**Caption**: \textbf{DAPO as targeted repairs to vanilla GRPO.} Each column pairs a vanilla GRPO failure mode (top) with the DAPO component that addresses it (bottom). Left to right: symmetric clipping suppresses entropy $\to$ Clip-Higher uses asymmetric bounds; homogeneous groups produce zero gradient $\to$ Dynamic Sampling filters them out; per-sample length normalization biases gradients $\to$ Token-Level Loss normalizes across all tokens; hard truncation creates reward noise $\to$ Overlong Reward Shaping replaces the cliff with a ramp.

## Prompt

```text
Draw a high-information algorithm diagram for a graduate-level machine
learning textbook. Clean blue-white technical style with one orange
accent. LANDSCAPE orientation, wide and spacious.

CONCEPT:
Four failure modes of vanilla GRPO in reasoning RL, each paired with the
DAPO component that fixes it. The visual should teach a failure-mode
taxonomy: each DAPO component is a targeted repair, not a random trick.

MAIN COMPOSITION:
Four equal-width columns filling the canvas edge to edge. Each column
has two vertically stacked cards separated by a thin downward arrow.

COLUMN 1 — ENTROPY COLLAPSE -> CLIP-HIGHER
Top card (failure mode, pale blue fill):
- Header: "Entropy Collapse"
- Mini line chart: policy entropy curve dropping sharply over training
  steps, ending near zero.
- One-line label: "symmetric clipping suppresses exploration"
Bottom card (DAPO fix, white fill with thin orange left border):
- Header: "Clip-Higher"
- Small ratio-axis diagram showing asymmetric clipping bounds:
  lower bound at 1-0.2, upper bound at 1+0.28. The upper band is
  visibly wider than the lower band.
- One-line label: "widen upper bound so probability increases flow"

COLUMN 2 — ZERO-GRADIENT GROUPS -> DYNAMIC SAMPLING
Top card:
- Header: "Zero-Gradient Groups"
- Four small response chips all showing reward = 1 (or all = 0).
  A variance meter reads zero. Gradient arrow fades to nothing.
- Label: "all-pass or all-fail groups carry no signal"
Bottom card (orange left border):
- Header: "Dynamic Sampling"
- Larger pool of response chips; a filter selects only groups with
  mixed rewards [1, 0, 1, 0]. Gradient arrow is strong blue.
- Label: "oversample until group has non-zero variance"

COLUMN 3 — LENGTH BIAS -> TOKEN-LEVEL LOSS
Top card:
- Header: "Length Bias"
- Two response bars: short (20 tokens) and long (200 tokens).
  A 1/|y| icon shrinks the long bar's gradient contribution.
- Label: "per-sample normalization dilutes long responses"
Bottom card (orange left border):
- Header: "Token-Level Loss"
- All tokens from all responses pooled into one sum, divided by
  total token count. Both bars contribute proportionally.
- Label: "normalize by total tokens across the group"

COLUMN 4 — OVERLONG TRUNCATION -> REWARD SHAPING
Top card:
- Header: "Overlong Truncation"
- Token strip hitting a vertical wall at max_length. A muted gray
  warning icon at the wall. Reward = noisy near the boundary.
- Label: "hard cutoff creates reward noise near max length"
Bottom card (orange left border):
- Header: "Overlong Reward Shaping"
- Token strip approaching max_length with a smooth downward ramp
  (soft penalty curve) instead of a wall.
- Label: "replace cliff with gradual penalty ramp"

CONNECTING ELEMENTS:
- A thin orange horizontal bar across the bottom of all four fix cards,
  labeled "DAPO: four targeted repairs".
- No bottom banner below this bar — the bar IS the takeaway.

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills for top cards: #E8F4FD
- White fills for bottom cards with thin #FF9F43 left border
- Orange accent: #FF9F43 — only for left borders and bottom bar
- Text: #1A1A2E for headers, #6B7280 for labels
- Clean sans-serif typography
- Flat vector, no gradients, no dark background, no 3D, no glow

IMPORTANT:
- Do not use red or green anywhere. Blue-white-orange only.
- Do not include equations — use iconic/diagrammatic representations.
- Do not imply DAPO is permanently the best method.
- Each column must be self-contained and readable independently.
- Keep all text short — headers max 3 words, labels max 8 words.
- Fill the full canvas; four columns should have equal spacing.
```

## Review Checklist

- [ ] Four columns are clearly separated and equally spaced.
- [ ] Each column pairs one failure mode (top) with one DAPO fix (bottom).
- [ ] Entropy Collapse card has a declining entropy mini-chart.
- [ ] Clip-Higher card shows asymmetric bounds (upper wider than lower).
- [ ] Zero-Gradient card shows all-same rewards with zero variance.
- [ ] Dynamic Sampling card shows filtering to mixed-reward groups.
- [ ] Length Bias card shows 1/|y| dilution on long responses.
- [ ] Token-Level Loss card shows pooled total-token normalization.
- [ ] Overlong card shows hard wall; Reward Shaping card shows soft ramp.
- [ ] Orange is used only for fix-card left borders and the bottom bar.
- [ ] No red, no green, no equations.
- [ ] All text readable at 50% PDF width.
