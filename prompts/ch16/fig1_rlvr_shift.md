# Figure 16.1: From Preference Reward to Verifiable Reward

**Filename**: `fig_rlvr_shift.png`
**LaTeX label**: `fig:rlvr-shift`
**Caption**: \textbf{The shift from preference reward to verifiable reward.} RLHF optimizes against a learned reward model trained on human preferences. Reasoning RL often optimizes against a verifier: exact answer matching, unit tests, formal proof checking, or structured process rewards. The verifier does not eliminate specification risk, but it changes the dominant failure mode from learned-proxy extrapolation to verifier design.

## Prompt

```text
Draw a conceptual comparison diagram for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Show the paradigm shift from RLHF preference reward to reasoning RL with verifiable reward. The figure should teach that the key change is the reward source, not merely the optimizer.

MAIN COMPOSITION:
LEFT PANEL: PREFERENCE REWARD
- A policy model generates two response cards.
- Human comparison bubbles feed into a learned reward model card.
- The reward model outputs a scalar score with a small warning label: "learned proxy".
- Include subtle mini artifacts inside the RM card: length bias slider, style preference knob, coverage gaps.

RIGHT PANEL: VERIFIABLE REWARD
- A policy model generates math/code/proof response cards.
- The cards feed into verifier modules: exact answer checker, unit tests, proof checker.
- The verifier outputs pass/fail or numeric correctness.
- Use one orange accent on the verifier output "checked result".

CENTER TRANSITION:
- A large arrow labeled "reward source changes".
- Bottom strip: "dominant risk shifts: proxy extrapolation -> verifier specification".

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
- Do not make the verifier look magical or perfect.
- Do not use red warning colors.
- Keep all labels short and readable.
- Fill the full width; no empty corners.
- Do not include brand logos.
- All text must be legible at 50% PDF width.
```

## Review Checklist

- [ ] Left side clearly shows learned preference reward model.
- [ ] Right side clearly shows verifiers.
- [ ] The central message is reward source, not optimizer.
- [ ] Only one orange focal accent appears.
- [ ] Bottom strip states proxy extrapolation -> verifier specification.
- [ ] No large blank areas.
- [ ] All labels are readable.
- [ ] Style uses blue-white palette.
