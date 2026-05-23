# Figure 13.3: Bradley-Terry Model

**Filename**: `fig_bradley_terry.png`
**LaTeX label**: `fig:bradley-terry`
**Caption**: The Bradley-Terry model turns reward gaps into preference probabilities. Two candidate responses receive latent reward scores. Their difference passes through a sigmoid: small gaps produce uncertain preferences near 50--50, while large gaps saturate toward near-certain preference. Reward model training learns scores that make the observed comparisons likely.

## Prompt

```text
Draw a Bradley-Terry preference model diagram for a graduate-level
machine learning textbook. Use a clean blue-white visual system: light
blue background, white cards, thin blue borders, charcoal text, and one
soft orange accent for the central sigmoid transformation.

CONCEPT:
Bradley-Terry converts a pair of latent reward scores into a preference
probability. The figure should make the equation intuitive: response
scores are compared, the reward difference passes through a sigmoid,
and the result is the probability that the winner is preferred.

MAIN COMPOSITION:
A wide left-to-right computation diagram with three stages:
1. two response cards with hidden reward scores,
2. reward difference and sigmoid transformation,
3. output preference probability plus two small examples showing small
   versus large reward gaps.

STAGE 1 -- RESPONSE CARDS:
On the left, show a prompt card:
"Prompt x: Write a concise summary"
Below it, show two stacked response cards:
- `y_w` winner card with a small latent reward gauge `r(x,y_w)=2.0`
- `y_l` loser card with a small latent reward gauge `r(x,y_l)=0.5`
The gauges should look like small blue meters, not literal thermometers.

STAGE 2 -- DIFFERENCE INTO SIGMOID:
In the center, draw a compact equation block:
`Delta r = r_w - r_l = 1.5`
An arrow flows into an S-shaped sigmoid curve. Put the equation
`sigma(Delta r)` near the curve. Use the single orange accent on the
point on the sigmoid curve corresponding to Delta r = 1.5.

STAGE 3 -- PROBABILITY OUTPUT:
On the right, show a probability card:
`P(y_w > y_l | x) = 0.82`
Below it, show two mini-cases:
- "Small gap" with two close reward gauges and probability near 0.5
- "Large gap" with separated reward gauges and probability near 1.0
The mini-cases should be small visual insets, not big extra panels.

BOTTOM STRIP:
A thin bottom strip with the lesson:
"BT learns latent rewards from observed comparisons, not from absolute
quality labels."

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF
- Pale blue fills: #E8F4FD
- Orange accent: #FF9F43 only for the sigmoid point and probability
  highlight
- Text: #1A1A2E; secondary labels: #6B7280
- Clean sans-serif typography
- Landscape orientation, spacious but information-rich

IMPORTANT:
- Do not overfill the figure with equations
- Do not draw a generic neural network here; this is the statistical
  preference model, not the reward model architecture
- Keep the sigmoid curve central and legible
- Use `>` instead of ornate symbols if needed for readability
- Keep all numbers limited to the example in the chapter
```

## Review Checklist

- [ ] Prompt and two response cards are visible
- [ ] Reward scores `2.0` and `0.5` are shown as latent gauges
- [ ] Difference `Delta r = 1.5` feeds into a sigmoid curve
- [ ] Output probability `0.82` is visible
- [ ] Small-gap and large-gap mini-cases appear
- [ ] Bottom strip states that rewards are inferred from comparisons
- [ ] Orange accent only marks the central sigmoid/probability insight
- [ ] Blue-white textbook style, no dark background
- [ ] Readable at 50% width in PDF

