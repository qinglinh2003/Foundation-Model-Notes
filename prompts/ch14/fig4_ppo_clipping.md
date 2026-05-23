# Figure 14.4: PPO Clipping

**Filename**: `fig_ppo_clipping.png`
**LaTeX label**: `fig:ppo-clipping`
**Caption**: PPO's clipping mechanism. For positive and negative advantages, the objective flattens outside the interval [1-epsilon, 1+epsilon], creating a trust-region-like update without second-order optimization.

## Prompt

```text
Draw a PPO clipping diagram for a graduate-level machine learning
textbook. Use a clean blue-white visual system: light blue background,
white cards, thin blue borders, charcoal text, and one soft orange
accent for the trust region.

CONCEPT:
PPO prevents the new policy from moving too far from the old policy by
clipping the probability ratio rho. The figure should make the flat
clipped regions visually obvious for both positive and negative
advantages.

MAIN COMPOSITION:
A two-panel plot layout. Left panel: positive advantage. Right panel:
negative advantage. Each panel is a clean line chart with rho on the
x-axis and surrogate objective on the y-axis.

LEFT PANEL -- "POSITIVE ADVANTAGE":
- Draw dashed blue line for unclipped objective increasing linearly
- Draw solid blue line for clipped objective: increases until rho =
  1 + epsilon, then becomes flat
- Shade the trust region [1-epsilon, 1+epsilon] in pale orange
- Add marker at rho = 1.3, epsilon = 0.2 with label "clipped"
- Small annotation: "do not over-reinforce good action"

RIGHT PANEL -- "NEGATIVE ADVANTAGE":
- Draw dashed blue line for unclipped objective decreasing linearly
- Draw solid blue line for clipped objective: decreases until rho =
  1 - epsilon, then becomes flat
- Same pale orange trust region shading
- Add marker at rho = 0.7, epsilon = 0.2 with label "clipped"
- Small annotation: "do not over-suppress bad action"

CENTER EXPLANATION:
Between panels, show a compact formula card:
"rho = pi_theta / pi_old"
"clip rho to [1-epsilon, 1+epsilon]"

BOTTOM STRIP:
Three short steps:
"sample with old policy" -> "compute ratio rho" -> "clip update if too far"

STYLE:
- Background: #FAFCFF
- Panels: white with #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF
- Pale blue fills: #E8F4FD
- Orange accent: #FF9F43 only for trust-region shading and clipped markers
- Text: #1A1A2E; secondary labels: #6B7280
- Use clean mathematical axes, not decorative 3D plots

IMPORTANT:
- Do not use red/green finance chart styling
- Do not crowd the plots with dense tick marks
- The flat clipped regions must be obvious
- The trust region [1-epsilon, 1+epsilon] must be highlighted in both panels
- Keep equations short and legible
```

## Review Checklist

- [ ] Two panels: positive advantage and negative advantage
- [ ] Dashed unclipped line and solid clipped line in each panel
- [ ] Shaded trust region [1-epsilon, 1+epsilon]
- [ ] Markers show clipped examples
- [ ] Formula card defines rho and clipping interval
- [ ] Bottom strip shows PPO update logic
- [ ] Blue-white style with soft orange trust-region accent
- [ ] Readable at 50% width in PDF

