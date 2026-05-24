# Figure 15.4: Reward Hacking and Over-Optimization

**Filename**: `fig_reward_hacking.png`
**LaTeX label**: `fig:rlhf-reward-hacking`
**Caption**: Reward hacking: optimizing the proxy, not the goal. Left: early in PPO training, reward model score and human win rate increase together. Right: after over-optimization, reward model score continues to rise but human win rate plateaus or decreases. The policy has found behaviors that exploit the reward model's biases without improving genuine quality.

## Prompt

```text
Draw a reward hacking diagram for a graduate-level machine learning
textbook. Use a clean blue-white visual system: light blue background,
white cards, thin blue borders, charcoal text, and one soft orange
accent for the failure signal.

CONCEPT:
Reward hacking occurs when an RL-trained policy optimizes a learned
reward proxy rather than the true human goal. The policy discovers
behaviors that score highly on the reward model but degrade actual
quality: verbosity, over-formatting, sycophancy, and hedging. The
figure should show this as a three-phase narrative from healthy
training to exploitation.

MAIN COMPOSITION:
A wide horizontal three-zone narrative layout, reading left to right
as a timeline of training progression.

ZONE 1 -- "EARLY TRAINING (HEALTHY)":
A white card showing:
- Two rising curves in a mini chart: "RM score" and "human quality"
  climbing together
- A small clean response card below: short, helpful, direct
- A green-blue check or "aligned" indicator
- Label: "proxy and goal agree"

ZONE 2 -- "OVER-OPTIMIZATION (DIVERGENCE)":
A white card showing:
- The same two curves, but now "RM score" continues upward while
  "human quality" bends flat then downward
- Use the orange accent to shade the widening gap between the curves
- A small response card showing early signs of exploitation:
  slightly verbose, added bullet points
- Label: "proxy overtakes goal"

ZONE 3 -- "HACKED BEHAVIORS":
A white card showing four small behavior example cards arranged in a
2x2 grid, each with a tiny stylized response snippet (not just text
labels):
- "Verbose": a long response block with unnecessary padding
- "Over-formatted": excessive headers, bullets, bold
- "Sycophantic": "What a great question! You're absolutely right..."
- "Hedged": "On one hand... on the other hand... it depends..."
Each card has a small high-RM-score badge but a low-human-quality
indicator

BOTTOM STRIP:
A thin strip across the bottom showing six mitigation levers as
small labeled icons:
- Tether icon: "KL constraint"
- Two-model icon: "RM ensemble"
- Diverse-prompts icon: "prompt diversity"
- Ruler icon: "length penalty"
- Human-eye icon: "human checkpoints"
- Refresh icon: "RM retraining"

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF
- Pale blue fills: #E8F4FD
- Orange accent: #FF9F43 only for the proxy-goal divergence gap
  and the failure path
- Text: #1A1A2E; secondary labels: #6B7280
- Clean sans-serif typography; landscape orientation

IMPORTANT:
- Do not use scary, alarmist, or dystopian imagery
- Do not use red warning triangles or danger symbols
- Do not make the behavior cards text-heavy; use visual snippets
- The proxy-vs-human divergence must be the visual center of gravity
- Make the three-zone progression read naturally left to right
- Keep all text short and readable at 50% page width
```

## Review Checklist

- [ ] Three zones: healthy training, divergence, hacked behaviors
- [ ] Zone 1 shows aligned RM score and human quality curves
- [ ] Zone 2 shows diverging curves with orange-highlighted gap
- [ ] Zone 3 shows four concrete hacked behaviors with visual snippets
- [ ] Each hacked behavior has high-RM but low-human indicators
- [ ] Bottom strip shows six mitigation levers with icons
- [ ] Orange accent used only for the failure/divergence signal
- [ ] No red, no alarmist imagery
- [ ] Blue-white palette throughout
- [ ] Readable at 50% width in PDF
