# Figure 16.7: Process vs Outcome Rewards

**Filename**: `fig_process_vs_outcome.png`
**LaTeX label**: `fig:process-vs-outcome`
**Caption**: \textbf{Outcome rewards vs process rewards.} Outcome rewards score only the final response: correct answer, passed tests, accepted proof. Process rewards score intermediate reasoning steps, providing denser credit assignment but requiring more supervision and introducing another learned proxy.

## Prompt

```text
Draw a split-panel reasoning reward diagram for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Compare outcome reward with process reward. Outcome reward is scalable but sparse; process reward gives denser credit assignment but requires step-level supervision.

MAIN COMPOSITION:
LEFT PANEL: OUTCOME REWARD
- A multi-step solution scroll with steps faded.
- Only the final answer box is scored.
- Verifier stamp at the end: pass/fail.
- Annotation: "cheap, scalable, sparse".

RIGHT PANEL: PROCESS REWARD
- Same multi-step solution scroll.
- Each step has a small score badge: +, +, -, +.
- A process reward model evaluates intermediate steps.
- Annotation: "dense feedback, higher supervision cost".

CENTER COMPARISON STRIP:
- Credit assignment gauge: low on left, high on right.
- Proxy risk gauge: lower for exact outcome, higher for learned process model.
- Use one orange accent on the step where process reward catches an error.

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — ONE focal element only
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
- Do not use long chain-of-thought text; use abstract step cards.
- Do not imply process reward is always better.
- Keep both panels balanced.
- Make the sparse vs dense contrast obvious.
- Fill full width.
- All text readable at 50% PDF width.
```

## Review Checklist

- [ ] Outcome reward scores only final answer.
- [ ] Process reward scores intermediate steps.
- [ ] Tradeoff between scalability and credit assignment is visible.
- [ ] One orange accent catches an intermediate error.
- [ ] No real chain-of-thought text is needed.
- [ ] Balanced two-panel layout.
- [ ] Labels are concise.
- [ ] Palette matches blue-white system.
