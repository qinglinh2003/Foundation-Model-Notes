# Figure 13.1: Preference Learning Pipeline

**Filename**: `fig_preference_pipeline.png`
**LaTeX label**: `fig:preference-pipeline`
**Caption**: The preference learning pipeline. From raw pairwise judgments to model update. Human or AI annotators compare response pairs (Part A). The Bradley-Terry model converts these comparisons into a scalar reward signal, which can train a reward model (Part B). DPO bypasses the reward model entirely, learning directly from preference pairs via a supervised loss (Part C). The three parts of this chapter follow this pipeline from left to right.

## Prompt

```text
Draw a preference learning pipeline diagram for a graduate-level
machine learning textbook. Use a clean blue-white visual system:
light blue background, white cards, thin blue borders, charcoal text,
and one soft orange accent for the central insight.

CONCEPT:
Preference learning turns a simple comparison ("Response A is better
than Response B") into a model update. The figure should show the
chapter's three-part structure: preference data, reward modeling, and
DPO as the supervised shortcut.

MAIN COMPOSITION:
A wide horizontal pipeline with three large stages arranged left to
right. Each stage is a rounded white card with internal mini-visuals,
not just text. Use arrows between stages. The DPO branch should bypass
the reward model stage with a clean curved orange arrow.

STAGE 1 -- "PART A: PREFERENCE DATA":
Inside the card, show:
- A prompt card at the top: "Explain backpropagation simply"
- Two response cards below it labeled "A" and "B"
- A small annotator panel on the side with two possible icons: human
  rater and AI judge
- A checkmark beside Response A and a muted mark beside Response B
- Output label: "(x, y_w, y_l)"
Keep the text short and legible.

STAGE 2 -- "PART B: REWARD MODELING":
Inside the card, show:
- The pair (winner/loser) entering a small Bradley-Terry block
- A sigmoid curve mini-plot labeled "P(A > B)"
- A transformer-like block with a scalar head outputting two scores:
  r(x, A) and r(x, B)
- The scalar head should look like a small gauge or dial, not a large
  separate model
Output label: "reward model r_phi(x,y)"

STAGE 3 -- "PART C: DPO":
Inside the card, show:
- Two model blocks: policy pi_theta and frozen reference pi_ref
- Winner and loser responses scored under both models
- A compact loss card: "log ratio margin -> DPO loss"
- A gradient arrow updating only the policy

BYPASS ARROW:
Draw a soft orange curved arrow from Stage 1 directly to Stage 3,
passing under Stage 2. Label it "DPO: skip RM + RL loop". This is the
only orange element in the figure. It should be visually clear but not
overpower the main pipeline.

BOTTOM STRIP:
A thin white strip across the bottom with three short phrases:
"Compare responses" -> "Infer quality" -> "Update policy"

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF
- Pale blue fills: #E8F4FD
- Orange accent: #FF9F43 only for the DPO bypass arrow
- Text: #1A1A2E; secondary labels: #6B7280
- Use clean sans-serif typography
- Landscape orientation, spacious, high information density but readable

IMPORTANT:
- Do not use dark backgrounds, neon colors, 3D effects, or decorative
  gradients
- Do not make this a generic flowchart with empty boxes
- Every stage must contain mini-visuals that show what happens inside
- Keep all text short; avoid paragraphs inside the figure
- The DPO bypass should clearly communicate "same data, simpler route"
```

## Review Checklist

- [ ] Three large stages: Preference Data, Reward Modeling, DPO
- [ ] Stage 1 shows prompt + two responses + human/AI judge + winner
- [ ] Stage 2 shows Bradley-Terry sigmoid and scalar reward model
- [ ] Stage 3 shows policy/reference log-ratio loss and policy update
- [ ] Orange bypass arrow from data directly to DPO
- [ ] Bottom strip: Compare responses -> Infer quality -> Update policy
- [ ] Blue-white style with only one orange accent
- [ ] Readable at 50% width in PDF

