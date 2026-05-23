# Figure 13.6: DPO Training Step Anatomy

**Filename**: `fig_dpo_training_step.png`
**LaTeX label**: `fig:dpo-training-step`
**Caption**: Anatomy of one DPO training step. A preference triple `(x,y_w,y_l)` is scored under both the trainable policy and the frozen reference. DPO compares the policy's winner--loser log-probability gap against the reference gap, scales the margin by beta, and updates only the policy. The figure shows why DPO is supervised in form but still requires careful model bookkeeping.

## Prompt

```text
Draw a DPO training step anatomy diagram for a graduate-level machine
learning textbook. Use a clean blue-white visual system: light blue
background, white cards, thin blue borders, charcoal text, and one soft
orange accent for the trainable update path.

CONCEPT:
One DPO batch contains a prompt, a preferred response, and a rejected
response. Both responses are scored under both the policy model and the
frozen reference model. DPO compares the policy's preference margin to
the reference margin and updates only the policy.

MAIN COMPOSITION:
A wide pipeline with four horizontal bands:
1. input preference triple,
2. model scoring under policy and reference,
3. log-ratio margin computation,
4. DPO loss and policy update.
The layout should feel like a systems anatomy diagram, not a generic
flowchart.

BAND 1 -- INPUT TRIPLE:
At the far left, show one prompt card `x` and two response cards:
- `y_w` chosen / preferred
- `y_l` rejected / dispreferred
Use a small bracket grouping them as `(x, y_w, y_l)`.

BAND 2 -- TWO MODEL ROLES:
In the center, show two model blocks:
- Top: `policy pi_theta` in blue, with a small trainable adapter badge
- Bottom: `reference pi_ref` in gray-blue, with a lock icon
Both winner and loser response cards should feed into both model blocks,
creating four short scoring paths. Keep these paths visually organized
with thin blue lines.

BAND 3 -- LOG-PROBABILITY GAPS:
On the right of the model blocks, show two compact margin cards:
- `policy gap: log pi_theta(y_w) - log pi_theta(y_l)`
- `reference gap: log pi_ref(y_w) - log pi_ref(y_l)`
Then show a subtraction block:
`policy gap - reference gap`
This block should be clear and central.

BAND 4 -- LOSS AND UPDATE:
At the far right, show:
- `beta * margin -> log-sigmoid loss`
- An orange gradient arrow returning only to `policy pi_theta`
- No arrow returning to the reference model
Label the orange arrow "update policy only".

BOTTOM STRIP:
A thin bottom strip with three reminders:
"same data as preferences" -> "extra reference scoring" -> "supervised
loss, policy update"

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF
- Pale blue fills: #E8F4FD
- Locked reference model: muted #DCE7F2
- Orange accent: #FF9F43 only for the update arrow and trainable badge
- Text: #1A1A2E; secondary labels: #6B7280
- Clean sans-serif typography
- Landscape orientation, full-width composition with no empty corners

IMPORTANT:
- Do not show PPO, reward model, or value model; this is DPO only
- Do not imply the reference model is trained
- Do not overcrowd with token-level details
- Keep math snippets short and readable
- Make the four scoring paths clear without visual clutter
```

## Review Checklist

- [ ] Input triple `(x, y_w, y_l)` appears on the left
- [ ] Policy model is trainable; reference model is locked/frozen
- [ ] Both responses are scored under both models
- [ ] Policy gap and reference gap are shown
- [ ] Margin feeds into beta-scaled log-sigmoid loss
- [ ] Orange update arrow returns only to the policy
- [ ] Bottom strip summarizes the workflow
- [ ] No reward model or PPO loop appears
- [ ] Blue-white textbook style, one orange accent
- [ ] Readable at 50% width in PDF

