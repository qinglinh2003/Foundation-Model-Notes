# Figure 14.5: KL Constraint and Reward Hacking

**Filename**: `fig_kl_constraint.png`
**LaTeX label**: `fig:kl-constraint`
**Caption**: The effect of KL constraint on RLHF training. With KL, reward improves while the policy stays near the reference. Without KL, proxy reward can rise while human preference degrades as the policy over-optimizes the reward model.

## Prompt

```text
Draw a KL-constraint comparison diagram for a graduate-level machine
learning textbook. Use a clean blue-white visual system: light blue
background, white cards, thin blue borders, charcoal text, and one soft
orange accent for the danger zone.

CONCEPT:
RLHF optimizes an imperfect reward proxy. A KL penalty keeps the policy
close to the reference model, where the proxy is trustworthy. Without
KL, proxy reward may rise while human preference falls.

MAIN COMPOSITION:
A split two-panel layout. Left panel: "With KL constraint". Right panel:
"Without KL constraint". Each panel contains a mini training curve and a
small response-style illustration.

LEFT PANEL -- "WITH KL":
Mini chart:
- x-axis: RL steps
- y-axis: score
- Blue curve "proxy reward" rises moderately then plateaus
- Dark charcoal curve "human preference" rises with it
- A pale blue band labeled "trustworthy proxy region"
Response illustration:
- A compact, helpful answer card
- Small anchor icon connecting policy to reference
- Label: "policy stays near SFT reference"

RIGHT PANEL -- "WITHOUT KL":
Mini chart:
- Blue curve "proxy reward" rises steeply
- Charcoal curve "human preference" rises briefly then falls
- Orange shaded region at the right labeled "over-optimization"
Response illustration:
- A bloated, repetitive answer card with length bars growing too long
- Small broken-anchor icon
- Label: "reward hack: proxy improves, quality drops"

CENTER EQUATION CARD:
Between panels, show:
"maximize reward - beta KL(pi || pi_ref)"
Keep equation compact and legible.

BOTTOM STRIP:
Three short messages:
"KL protects capability" | "KL limits reward hacking" | "KL preserves diversity"

STYLE:
- Background: #FAFCFF
- Panels: white with #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF
- Pale blue fills: #E8F4FD
- Orange accent: #FF9F43 only for the over-optimization danger zone
- Text: #1A1A2E; secondary labels: #6B7280
- Clean sans-serif typography; landscape orientation

IMPORTANT:
- Do not use horror imagery or dramatic red warning colors
- Do not make the response cards text-heavy
- The contrast must be clear: with KL = aligned curves; without KL =
  reward up, preference down
- Use only one orange accent for the danger region
- Keep the equation short and readable
```

## Review Checklist

- [ ] Two panels: with KL and without KL
- [ ] With KL: proxy reward and human preference rise together
- [ ] Without KL: proxy reward rises while human preference falls
- [ ] Orange over-optimization region only on right panel
- [ ] Equation card: reward - beta KL
- [ ] Response illustrations show helpful vs repetitive output
- [ ] Bottom strip lists KL functions
- [ ] Blue-white style with single orange danger accent

