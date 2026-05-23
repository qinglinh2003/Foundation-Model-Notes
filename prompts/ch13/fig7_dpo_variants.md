# Figure 13.7: DPO Variant Landscape

**Filename**: `fig_dpo_variants.png`
**LaTeX label**: `fig:dpo-variants`
**Caption**: Representative DPO variants modify different assumptions. DPO sits at the center: paired preferences, a frozen reference, and a log-sigmoid margin loss. IPO changes the loss geometry, KTO changes the data format to unpaired good/bad labels, and ORPO merges SFT and preference learning into one objective. SimPO removes the reference model and length-normalizes the implicit reward. The right variant depends on what kind of data and stability problem you actually have.

## Prompt

```text
Draw a DPO variant landscape diagram for a graduate-level machine
learning textbook. Use a clean blue-white visual system: light blue
background, white cards, thin blue borders, charcoal text, and one soft
orange accent for the default DPO method.

CONCEPT:
DPO is the default preference-optimization method, but variants change
specific assumptions: IPO changes the loss geometry, SimPO removes the
reference model and length-normalizes the reward, KTO changes the data
format, and ORPO merges SFT with preference learning. The figure should
help students see what each variant changes, not memorize names.

MAIN COMPOSITION:
A central DPO card with four surrounding variant cards arranged like a
map. Use short connector lines from DPO to each variant. Each card must
contain a small internal mini-visual that shows the change.

CENTER CARD -- "DPO: DEFAULT":
Place DPO in the center with a subtle orange outline or badge. Inside:
- paired data icon: winner card vs loser card
- frozen reference model icon
- log-sigmoid margin mini-curve
Short note: "paired preferences + reference model"

TOP LEFT CARD -- "IPO":
Inside the IPO card:
- show a sigmoid curve that flattens on easy pairs
- next to it, show a squared-margin target line
- short note: "changes loss geometry"
The visual should communicate less saturation / target margin.

TOP RIGHT CARD -- "SimPO":
Inside the SimPO card:
- show the reference model icon removed or faded out
- show a length-normalized log-probability bar
- short note: "reference-free + length-normalized"
Make clear that SimPO changes both the reference requirement and the
reward normalization.

MIDDLE RIGHT CARD -- "KTO":
Inside the KTO card:
- show individual response cards labeled good and bad, not paired
- show two separate thumbs-style labels, but avoid cartoonish hands
- short note: "uses unpaired labels"
Do not imply there is a winner-loser pair.

BOTTOM CARD -- "ORPO":
Inside the ORPO card:
- show two streams merging: SFT loss + preference odds term
- one combined objective card
- short note: "combines SFT + preference"
Make clear that ORPO removes the separate DPO stage.

BOTTOM DECISION STRIP:
A full-width strip with five short recommendations:
"DPO: default" | "IPO: noisy margins" | "SimPO: no reference" |
"KTO: only good/bad labels" | "ORPO: single-stage training"

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF
- Pale blue fills: #E8F4FD
- Orange accent: #FF9F43 only for the central DPO default badge
- Text: #1A1A2E; secondary labels: #6B7280
- Clean sans-serif typography
- Landscape orientation, balanced, no empty corners

IMPORTANT:
- Do not make this a crowded literature survey
- Do not add extra methods beyond DPO, IPO, SimPO, KTO, ORPO
- Keep each card's text to one short phrase
- Use mini-visuals to show the change each method makes
- Avoid red/green status colors; use blue-white plus one orange accent
```

## Review Checklist

- [ ] Central DPO card has the only orange default badge
- [ ] IPO card shows changed loss geometry
- [ ] SimPO card shows reference-free, length-normalized reward
- [ ] KTO card shows unpaired good/bad labels
- [ ] ORPO card shows SFT and preference streams merging
- [ ] Bottom strip gives five short recommendations
- [ ] No extra variants are included
- [ ] Blue-white textbook style, no dark background
- [ ] Text remains short and legible
- [ ] Readable at 50% width in PDF
