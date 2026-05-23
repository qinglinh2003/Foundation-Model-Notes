# Figure 14.1: Three Training Signals

**Filename**: `fig_signal_comparison.png`
**LaTeX label**: `fig:signal-comparison`
**Caption**: Three training paradigms, three signal types. SFT uses demonstrations, DPO uses pairwise preferences, and RL uses scalar rewards. As supervision becomes less prescriptive, the model gains more room to discover strategies, but optimization becomes harder.

## Prompt

```text
Draw a training-signal comparison diagram for a graduate-level machine
learning textbook. Use a clean blue-white visual system: light blue
background, white cards, thin blue borders, charcoal text, and one
soft orange accent for the main transition.

CONCEPT:
SFT, DPO, and RL differ by the type of supervision they provide. SFT
prescribes the answer, DPO ranks two answers, and RL scores the final
outcome. The figure should show increasing freedom and increasing
optimization difficulty from left to right.

MAIN COMPOSITION:
A wide horizontal three-card comparison. Each card is a white panel
with rich internal mini-visuals, not just labels. Arrange left to right:
"SFT: demonstrate", "DPO: compare", "RL: reward". Use a thin orange
arrow across the bottom labeled "less prescriptive signal -> more
discovery, harder optimization".

CARD 1 -- "SFT: DEMONSTRATION":
Inside the card:
- A prompt card at top: "Solve this problem"
- A single target response card below, with a teacher pencil icon
- A blue gradient arrow from target response to model update
- Small label: "learn to imitate y*"

CARD 2 -- "DPO: PREFERENCE":
Inside the card:
- Same prompt card
- Two response cards side by side labeled A and B
- A checkmark on A and muted mark on B
- Two small model blocks: policy and reference
- Small label: "learn relative preference"

CARD 3 -- "RL: REWARD":
Inside the card:
- Same prompt card
- A model generating three possible response paths
- A verifier or reward meter at the end of each path
- Scores: 1, 0, 1 or "pass/fail"
- Small label: "learn from outcome"

TOP AXIS:
Add a subtle axis above the cards:
"Signal type: target response -> pairwise ranking -> scalar reward"

BOTTOM AXIS:
Add a second axis below the cards:
"Model freedom: low -> medium -> high"

STYLE:
- Background: #FAFCFF
- Cards: white with #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF
- Pale blue fills: #E8F4FD
- Orange accent: #FF9F43 only for the bottom discovery arrow
- Text: #1A1A2E; secondary labels: #6B7280
- Clean sans-serif typography; landscape orientation

IMPORTANT:
- Do not use dark backgrounds, neon colors, or decorative gradients
- Do not make this a generic table; each card needs mini-visuals
- Keep all text short and readable
- Use only one orange accent, the bottom progression arrow
- The three paradigms must be visually parallel and easy to compare
```

## Review Checklist

- [ ] Three cards: SFT, DPO, RL
- [ ] SFT card shows one target demonstration
- [ ] DPO card shows pairwise winner/loser
- [ ] RL card shows generated paths scored by a verifier/reward meter
- [ ] Top axis: target -> ranking -> reward
- [ ] Bottom orange arrow: more discovery / harder optimization
- [ ] Blue-white style, single orange accent
- [ ] Readable at 50% width in PDF

