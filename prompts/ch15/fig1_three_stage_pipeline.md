# Figure 15.1: Three-Stage RLHF Pipeline

**Filename**: `fig_three_stage_pipeline.png`
**LaTeX label**: `fig:three-stage-pipeline`
**Caption**: The three-stage RLHF pipeline. Stage 1: supervised fine-tuning on human demonstrations. Stage 2: reward model training on human preference pairs. Stage 3: PPO optimization of the policy against the frozen reward model, with a KL penalty to the SFT checkpoint. Each stage produces a model that feeds into the next.

## Prompt

```text
Draw a three-stage RLHF pipeline diagram for a graduate-level machine
learning textbook. Use a clean blue-white visual system: light blue
background, white cards, thin blue borders, charcoal text, and one
soft orange accent for the key training signal.

CONCEPT:
RLHF transforms a pretrained language model in three stages. Each
stage uses a different supervision signal: demonstrations, pairwise
comparisons, then scalar rewards with KL control. The figure must
make the signal progression and model flow visible.

MAIN COMPOSITION:
A wide horizontal layout with three large stage cards arranged left
to right, connected by thick blue arrows. Each card is a white
rounded panel with rich internal mini-visuals, not just text labels.

STAGE 1 -- "SFT":
Inside the card:
- A pretrained model block (gray, unlabeled) at left receiving a
  small stack of instruction-response pair cards
- A blue gradient arrow pointing to a "SFT policy" model block
- Small annotation: "13K demonstrations" near the pair cards
- A tiny teacher/pencil icon beside the demonstration cards

STAGE 2 -- "REWARD MODEL":
Inside the card:
- Two response cards side by side labeled A and B, with a checkmark
  on A and a muted mark on B
- A transformer block with a small scalar-head gauge outputting two
  scores: r(A) > r(B)
- A mini sigmoid curve icon representing Bradley-Terry
- Small annotation: "33K comparisons" near the response pairs

STAGE 3 -- "PPO":
Inside the card:
- The SFT policy generating response strips (token by token)
- A frozen reward model (gray, lock icon) scoring each response
- A frozen reference policy (gray, lock icon) providing KL signal
- A trainable policy block (blue) with a gradient update arrow
- Use the single orange accent on the PPO update arrow only
- Small annotation: "31K prompts" near the prompt batch

BOTTOM STRIP:
A thin white strip across the bottom with three signal labels and
small icons:
"demonstrations (human writer)" -> "preferences (pairwise judge)" ->
"rewards + KL (policy optimizer)"

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF
- Pale blue fills: #E8F4FD
- Frozen modules: light gray #E5E7EB with lock icon
- Orange accent: #FF9F43 only for the PPO update arrow
- Text: #1A1A2E; secondary labels: #6B7280
- Clean sans-serif typography; landscape orientation

IMPORTANT:
- Do not use dark backgrounds, neon colors, 3D effects, or gradients
- Do not make this a generic flowchart with empty boxes; each stage
  needs internal visual content showing what happens inside
- Do not use red or warning colors
- Keep all text short and readable at 50% page width
- Frozen models must have lock icons; trainable models must look
  visually distinct (blue vs gray)
- All arrows flow left to right except the PPO feedback loop
```

## Review Checklist

- [ ] Three stages: SFT, Reward Model, PPO
- [ ] SFT card shows demonstration pairs and produces SFT policy
- [ ] RM card shows pairwise comparison with sigmoid/scalar head
- [ ] PPO card shows four models: policy (trainable), reference (frozen), reward (frozen), value
- [ ] Frozen models have lock icons, trainable models are blue
- [ ] Orange accent appears only on the PPO update arrow
- [ ] Bottom strip shows signal progression with icons
- [ ] InstructGPT-scale annotations visible (13K, 33K, 31K)
- [ ] Blue-white palette, no dark backgrounds or red
- [ ] Readable at 50% width in PDF
