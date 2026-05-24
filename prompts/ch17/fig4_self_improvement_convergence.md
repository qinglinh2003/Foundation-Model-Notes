# Figure 17.4: Self-Improvement Convergence or Collapse

**Filename**: `fig_self_improvement_convergence.png`
**LaTeX label**: `fig:self-improvement-convergence`
**Caption**: Self-improvement can converge or collapse. Iterative loops generate, judge, filter, and train. They improve when the judge remains calibrated and the filtered data expands useful behavior. They collapse when repeated filtering narrows support, amplifies judge errors, or creates self-confirming artifacts.

## Prompt

```text
Draw a self-improvement loop with two possible outcomes for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
The figure shows that iterative self-improvement is not automatically good: it can converge when feedback is calibrated, or collapse when repeated filtering narrows support.

MAIN COMPOSITION:
CENTER LOOP:
Create a circular four-step loop: Generate candidates → Judge / verify → Filter selected data → Train next model. Use blue arrows around a central model icon labeled M_t to M_{t+1}. Add tiny candidate cards around "Generate", score meters around "Judge", funnel icon around "Filter", and adapter/gradient icon around "Train".

RIGHT BRANCH: CONVERGENCE
From the loop, arrow to a blue "Converges" panel. Show held-out score rising, diversity stable, errors shrinking. Labels: "independent judge", "fresh difficulty", "diversity audit".

LEFT BRANCH: COLLAPSE
From the loop, arrow to an orange-accent "Collapse / narrowing" panel. Show score rising but diversity falling, repeated error icon, judge drift meter. Labels: "self-confirming judge", "mode narrowing", "error amplification".

BOTTOM STRIP:
"The key question is not whether iteration works, but when the loop remains calibrated."

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — use only in collapse panel warning elements
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
- The loop must be central and visually dominant.
- Both convergence and collapse branches must be balanced.
- Do not use red; use orange sparingly for warning.
- Include metrics curves inside the outcome panels.
- All text readable at 50% PDF width.
```

## Review Checklist

- [ ] Generate-judge-filter-train loop is clear.
- [ ] Convergence branch shows score up and diversity stable.
- [ ] Collapse branch shows score up but diversity down or errors repeat.
- [ ] Calibration question appears in bottom strip.
- [ ] Orange is limited to collapse warnings.
- [ ] No empty corners.
- [ ] Text labels are readable.
- [ ] Figure does not look like a generic business process diagram.
