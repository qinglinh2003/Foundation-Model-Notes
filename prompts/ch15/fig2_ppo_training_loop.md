# Figure 15.2: PPO Training Loop for RLHF

**Filename**: `fig_ppo_training_loop.png`
**LaTeX label**: `fig:ppo-training-loop`
**Caption**: The PPO training loop for RLHF. Each iteration: (1) sample a batch of prompts, (2) generate responses from the current policy, (3) score with the frozen reward model and compute per-token KL penalties, (4) estimate advantages using GAE, (5) update the policy with the clipped PPO objective, (6) update the value model. The reference policy remains frozen throughout.

## Prompt

```text
Draw a PPO training loop diagram for a graduate-level machine
learning textbook. Use a clean blue-white visual system: light blue
background, white cards, thin blue borders, charcoal text, and one
soft orange accent for the trainable update path.

CONCEPT:
One RLHF PPO iteration for a language model involves six steps in a
loop: sample prompts, generate responses, score with reward model,
compute KL penalties, estimate advantages, and update policy. The
figure should show this as a clockwise loop with four distinct
model blocks (two frozen, two trainable).

MAIN COMPOSITION:
A circular loop layout around a central "policy update" hub. Six
numbered steps arranged clockwise, each as a compact white card with
internal mini-visuals.

STEP 1 -- "SAMPLE PROMPTS":
A small stack of prompt cards drawn from a prompt dataset icon.

STEP 2 -- "GENERATE RESPONSES":
A blue policy model block emitting several response strips, shown
token by token with small colored squares representing tokens.

STEP 3 -- "SCORE RESPONSES":
A frozen gray reward model block (lock icon) outputting one scalar
score per response. Show a small gauge or meter beside each response
strip. Also show a frozen gray reference model computing per-token
KL values alongside the policy's tokens.

STEP 4 -- "COMPUTE ADVANTAGES":
A trainable value model block outputting a token-level advantage
curve. Show a mini line chart of advantages across the token
sequence: mostly near zero, with a spike at the final token where
the terminal reward arrives.

STEP 5 -- "PPO UPDATE":
A clipped objective block with the orange accent on the gradient
arrow updating the policy. Show the clipping visually: a small
[1-epsilon, 1+epsilon] bracket icon.

STEP 6 -- "VALUE UPDATE":
The value model receiving the actual returns and updating. Show a
small MSE loss icon.

TOKEN TIMELINE:
Below the main loop, add a compact token-level timeline for one
response: most tokens show only KL penalty (small blue ticks); the
final token shows terminal RM score plus KL (blue tick + orange
marker). Label: "reward = terminal RM score - per-token KL".

MODEL LEGEND:
A small legend in one corner:
- Blue block = trainable (policy, value model)
- Gray block with lock = frozen (reward model, reference policy)

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
- Do not draw a generic RL loop; include LLM-specific token details
- Do not use red or warning colors
- Do not use gradients, glows, 3D effects, or decorative elements
- Make frozen vs trainable modules visually obvious (gray+lock vs blue)
- Keep the loop readable clockwise with clear step numbers
- All text must be short and legible at textbook figure size
```

## Review Checklist

- [ ] Six numbered PPO iteration steps visible in clockwise loop
- [ ] Four model blocks present: policy, value (trainable/blue), reward, reference (frozen/gray+lock)
- [ ] Step 3 shows both reward scoring and KL computation
- [ ] Step 5 has the orange accent on the PPO update
- [ ] Token timeline shows terminal reward + per-token KL
- [ ] Model legend distinguishes trainable vs frozen
- [ ] Clipping bracket visible in PPO update step
- [ ] Blue-white palette, no dark backgrounds or red
- [ ] Readable at 50% width in PDF
