# Figure 6.5: The Pilot Run Discipline

**Filename**: `pilot_workflow.png`
**LaTeX label**: `fig:pilot-workflow`
**Caption**: The staged pilot workflow used in industrial pretraining. Each stage validates a specific aspect of the training recipe before committing more compute. Most failures are caught early when they are cheap to fix.

## Prompt

```text
Draw a staged workflow diagram showing the pilot run discipline for
large-scale LLM training, for a graduate-level machine learning textbook.
Use the course's blue-white visual system. Landscape orientation, polished
editorial style.

Purpose:
- The figure should teach that industrial pretraining is a staged process
  where you validate the recipe at increasing scale before committing the
  full compute budget.
- The main visual message is: catch failures early when they are cheap.

LAYOUT:
A horizontal left-to-right flow with 4 stages connected by arrows.
Each stage is a rounded rectangle card. The cards grow in size from
left to right, visually representing increasing compute commitment.

STAGE 1 — TINY SMOKE RUN:
- Card size: smallest
- Fill: light blue #E8F4FD
- Title: "Tiny Smoke Run"
- Duration: "minutes"
- Scale: "~1% of final"
- Purpose: "Code correctness"
- Validates: "No crashes, loss decreases, shapes correct"
- Icon: a small checkmark

STAGE 2 — SMALL PILOT:
- Card size: slightly larger
- Fill: light blue #E8F4FD
- Title: "Small Pilot"
- Duration: "hours"
- Scale: "~5-10% of final"
- Purpose: "Recipe validation"
- Validates: "LR, warmup, stability, no early divergence"

STAGE 3 — MEDIUM PILOT:
- Card size: larger
- Fill: medium blue #D0E8FF
- Title: "Medium Pilot"
- Duration: "1-2 days"
- Scale: "~20-30% of final"
- Purpose: "Scaling trend"
- Validates: "Loss follows expected curve, throughput stable"

STAGE 4 — FINAL RUN:
- Card size: largest
- Fill: #2D8CFF (Zoom Blue, prominent)
- Title: "Final Run"
- Duration: "days to weeks"
- Scale: "100%"
- Purpose: "Full training"
- Validates: "Target loss, generation quality, eval scores"

ARROWS BETWEEN STAGES:
- Blue arrows connecting Stage 1 -> 2 -> 3 -> 4
- Each arrow has a small "gate" diamond between stages
- Gate labels:
  - Between 1 and 2: "Loss drops?"
  - Between 2 and 3: "Recipe stable?"
  - Between 3 and 4: "Scaling trend OK?"

BELOW THE FLOW — FAILURE PATHS:
- From each gate diamond, a downward arrow (in lighter gray) pointing
  to a small box labeled:
  - "Fix code" (from gate 1)
  - "Adjust recipe" (from gate 2)
  - "Re-evaluate budget" (from gate 3)
- These failure paths loop back to the same or earlier stage

TOP ANNOTATION:
A cost bar running above all 4 stages, showing increasing width:
- Labels: "$" / "$$" / "$$$" / "$$$$"
- The bar gets wider (and slightly darker blue) from left to right
- This visually communicates: catch failures early = save money

The ONE orange accent (#FF9F43) is: the "$$$$" label above the Final
Run stage, emphasizing that mistakes at full scale are the most expensive.

STYLE LOCK:
- Match the course's Zoom-inspired blue-white textbook visual system.
- Background: #FAFCFF
- Cards: rounded rectangles with subtle shadow
- Arrows: #0B5CFF
- Gate diamonds: white fill with #0B5CFF border
- Text: #1A1A2E charcoal, sans-serif
- Secondary text: #6B7280 steel gray
- Orange accent: #FF9F43 ONLY on "$$$$" label
- Clean vector geometry, generous margins, no clutter

DO NOT: cartoon style, photorealism, clip art, SaaS dashboard, heavy 3D,
neon, rainbow, coral, teal, purple, green, decorative borders, abstract
background patterns, complex formulas.
```

## Review Checklist

- [ ] Four stages from left to right: Smoke / Small Pilot / Medium Pilot / Final
- [ ] Cards grow in size left to right
- [ ] Each card shows: title, duration, scale, purpose, validates
- [ ] Gate diamonds between stages with pass/fail conditions
- [ ] Failure paths loop back to earlier stages
- [ ] Cost bar above showing increasing expense
- [ ] Orange accent ONLY on "$$$$" for the final run
- [ ] Visual progression clearly shows "catch failures early"
- [ ] No extra colors beyond blue + white + orange + gray
- [ ] Readable at 50% width in PDF
