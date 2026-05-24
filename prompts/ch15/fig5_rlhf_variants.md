# Figure 15.5: RLHF Variants

**Filename**: `fig_rlhf_variants.png`
**LaTeX label**: `fig:rlhf-variants`
**Caption**: Three RLHF variants. Each variant modifies a different component of the InstructGPT pipeline. Constitutional AI replaces human preference annotation with AI self-critique. Llama 2 adds rejection sampling between SFT and PPO and iteratively retrains the reward model. RLAIF scales feedback by combining human and AI annotation.

## Prompt

```text
Draw an RLHF variants comparison figure for a graduate-level machine
learning textbook. Use a clean blue-white visual system: light blue
background, white cards, thin blue borders, charcoal text, and one
soft orange accent for the modified pipeline components.

CONCEPT:
Three major RLHF variants each modify a different component of the
standard InstructGPT pipeline (SFT -> RM -> PPO). Constitutional AI
changes the preference data source. Llama 2 changes the training
loop structure. RLAIF changes the feedback scaling. The figure
should show a central baseline and three variant cards that each
highlight what they change.

MAIN COMPOSITION:
A central baseline pipeline card at the top with three variant cards
arranged below it, connected by thin blue arrows pointing to the
component each variant modifies.

BASELINE PIPELINE (TOP):
A compact horizontal pipeline strip: "SFT -> Reward Model -> PPO"
with three connected blocks. This is the anchor that all variants
reference.

VARIANT CARD 1 -- "CONSTITUTIONAL AI":
A white card showing:
- A small constitution document icon (list of principles)
- A self-critique loop: model response -> model critique based on
  principles -> model revision -> revised response
- The orange accent on the "preference annotation" component,
  showing it is replaced by AI self-critique
- Key change label: "human annotation -> AI self-critique"

VARIANT CARD 2 -- "LLAMA 2-STYLE ITERATION":
A white card showing:
- A rejection sampling stage between SFT and PPO: generate N
  responses, score with RM, keep best
- A feedback loop arrow from current policy outputs back to RM
  retraining
- The orange accent on the iterative loop arrow
- Key change label: "single pass -> iterative RM retraining"

VARIANT CARD 3 -- "RLAIF / HYBRID FEEDBACK":
A white card showing:
- Two annotation sources side by side: a human rater icon for
  high-stakes categories (safety, harm) and an AI judge icon for
  scalable volume (style, helpfulness)
- Both feeding into a shared reward dataset
- The orange accent on the AI judge contribution
- Key change label: "human-only -> human + AI feedback"

LINKING ARROWS:
Thin blue arrows from each variant card pointing to the specific
baseline component it modifies. Each arrow is labeled with what
changes.

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF
- Pale blue fills: #E8F4FD
- Orange accent: #FF9F43 only for the modified component in each
  variant
- Text: #1A1A2E; secondary labels: #6B7280
- Clean sans-serif typography; landscape orientation

IMPORTANT:
- Do not imply these variants are mutually exclusive; they can be
  combined
- Do not use brand logos or company names in the visual
- Do not crowd the cards with paragraphs; use icons and short labels
- Each variant must clearly show which pipeline component it changes
- Keep all text readable at 50% page width
```

## Review Checklist

- [ ] Baseline pipeline (SFT -> RM -> PPO) visible at top
- [ ] Three variant cards below, each modifying a different component
- [ ] Constitutional AI shows self-critique loop with principles
- [ ] Llama 2 shows rejection sampling and RM retraining loop
- [ ] RLAIF shows human + AI feedback sources
- [ ] Orange accent marks the modified component in each variant
- [ ] Linking arrows connect variants to baseline components
- [ ] Key change labels are concise and readable
- [ ] Blue-white palette, no dark backgrounds or red
- [ ] Readable at 50% width in PDF
