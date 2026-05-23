# Figure 13.3: DPO Derivation

**Filename**: `fig_dpo_derivation.png`
**LaTeX label**: `fig:dpo-derivation`
**Caption**: The DPO derivation in three steps. Left: the KL-constrained objective has a closed-form optimal policy. Center: rearranging gives the reward as a function of the policy-to-reference ratio, plus a prompt-dependent constant. Right: substituting into Bradley-Terry cancels the prompt-dependent constant, yielding a supervised loss on preference pairs. The reward model and RL loop are eliminated entirely.

## Prompt

```text
Draw a DPO derivation diagram for a graduate-level machine learning
textbook. Use a clean blue-white visual system: light blue background,
white cards, thin blue borders, charcoal text, and one soft orange
accent for the cancellation step.

CONCEPT:
DPO looks mysterious until the algebra is visualized. The figure should
show three steps: KL-constrained objective -> reward as policy/reference
log-ratio -> Bradley-Terry cancellation -> supervised DPO loss.

MAIN COMPOSITION:
Three large equation cards arranged left to right, connected by arrows.
Each card contains a compact equation plus an internal visual metaphor.
The rightmost card should visibly remove the reward model and RL loop.

CARD 1 -- "1. KL-CONSTRAINED OBJECTIVE":
Equation, simplified and legible:
"maximize reward - beta * KL(policy || reference)"
Mini-visual:
- A policy model block trying to move toward a reward star
- A reference model block acting like an anchor
- A blue elastic tether between policy and reference labeled "KL"
Small note: "high reward, limited drift"

CARD 2 -- "2. SOLVE FOR REWARD":
Equation, compact:
"r(x,y) = beta log[pi(y|x) / pi_ref(y|x)] + beta log Z(x)"
Mini-visual:
- Two probability bars: policy probability and reference probability
- A ratio gauge comparing them
- A small constant tile labeled "log Z(x)"
Small note: "reward becomes a log-ratio"

CARD 3 -- "3. SUBSTITUTE INTO BRADLEY-TERRY":
Equation, compact:
"P(y_w > y_l) = sigma(beta[log-ratio_w - log-ratio_l])"
Mini-visual:
- Winner and loser response cards entering a sigmoid
- The "log Z(x)" tiles from winner and loser crossing out
- The cross-out/cancellation should be soft orange (#FF9F43), the only
  orange element
Small note: "partition function cancels"

BOTTOM RESULT BAND:
A wide white band under the three cards:
Left side: "Removed: reward model + PPO loop"
Right side: "Kept: preference pairs + policy/reference log-probs"
Center badge: "DPO loss"

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders, subtle shadow
- Primary blue: #2D8CFF
- Pale blue fills: #E8F4FD
- Orange accent: #FF9F43 only for crossing out log Z(x)
- Text: #1A1A2E; secondary labels: #6B7280
- Equations should be short, large, and readable
- Landscape orientation with generous spacing

IMPORTANT:
- Do not place long derivations inside the image
- Do not include dense LaTeX notation beyond the three compact equations
- Do not use a blackboard aesthetic
- The cancellation of log Z(x) must be visually obvious
- The final result must read as supervised preference learning, not RL
```

## Review Checklist

- [ ] Three equation cards: objective, reward log-ratio, BT substitution
- [ ] Card 1 shows policy anchored to reference by KL
- [ ] Card 2 shows policy/reference probability ratio
- [ ] Card 3 visibly cancels log Z(x)
- [ ] Bottom result band contrasts removed vs kept machinery
- [ ] Orange used only for cancellation
- [ ] Equations readable and not overcrowded
- [ ] Readable at 50% width in PDF

