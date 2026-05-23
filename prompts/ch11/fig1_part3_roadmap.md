# Figure 11.1: Part III Roadmap

**Filename**: `fig_part3_roadmap.png`
**LaTeX label**: `fig:part3-roadmap`
**Caption**: Part III roadmap. The post-training pipeline transforms a pretrained language model into a useful product through progressively richer training signals. Instruction tuning and PEFT use demonstrations; preference learning uses pairwise comparisons; RLHF and reasoning RL use reward signals. RL foundations supports the reward-based chapters.

## Prompt

```text
Draw a Part III roadmap for a machine learning textbook. Use the course's
Zoom-inspired blue-white visual system. LANDSCAPE orientation, wide and
spacious. Match the visual richness of the book's best figures: Ch10
"Three-Layer Schema" with rich internal details, Ch9 "Data Funnel" with a
clear left-to-right transformation, and Ch5 "Training Pipeline" with compact
technical mini-illustrations inside each block.

CONCEPT:
"From pretrained model to useful product." The figure should be the visual
spine for Part III. It is not a generic flowchart; it is a post-training map
where each chapter introduces a new signal type or engineering lever.

MAIN COMPOSITION:
A left-to-right pipeline across the center:
Pretrained LM -> Instruction Tuning -> PEFT -> Preference Learning / DPO ->
RLHF -> Reasoning RL -> Frontiers.

Each stage is a rounded white card with thin blue border (#CFE3F7), subtle
shadow, and a small internal visual:
- Pretrained LM: a dense blue token stream entering a model chip
- Instruction Tuning (Ch.11): instruction-response card pairs, assistant tokens
  highlighted
- PEFT (Ch.12): a frozen large model block with tiny adapter modules attached
- Preference Learning / DPO (Ch.13): two response cards labeled chosen/rejected
  with a check mark on chosen
- RLHF (Ch.15): reward model scalar head feeding policy update arrows
- Reasoning RL (Ch.16): math/code verifier with pass/fail signals
- Frontiers (Ch.17): open research map with question markers

IMPORTANT STRUCTURE:
Chapter 14 is NOT a pipeline stage. Put it as a side module below RLHF and
Reasoning RL: "Ch.14 RL vocabulary" with arrows feeding upward into Ch.15 and
Ch.16. The visual message: Ch.14 is background machinery, not a product-training
stage.

SIGNAL BANDS:
Below the main pipeline, draw three horizontal bands:
- Demonstrations: under Ch.11 and Ch.12
- Preferences: under Ch.13 and Ch.15
- Verifiable rewards: under Ch.16
Use pale blue fills for bands. The only orange (#FF9F43) should highlight the
transition label "richer training signals" above the pipeline.

STYLE:
Use primary blue #2D8CFF, pale blue #E8F4FD, light border #CFE3F7, charcoal
text #1A1A2E, steel gray #6B7280, soft orange #FF9F43 for one accent only.
Clean textbook diagram, not a business slide. No gradients, no dark background,
no decorative blobs. Text must be short and legible.
```

## Review Checklist

- [ ] Ch.14 appears as a support module, not a pipeline stage.
- [ ] Each chapter card has a concrete mini-visual, not only text.
- [ ] Only one orange accent is used.
- [ ] The figure reads clearly at textbook width.
