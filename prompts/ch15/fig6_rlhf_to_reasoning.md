# Figure 15.6: From RLHF to Reasoning RL

**Filename**: `fig_rlhf_to_reasoning.png`
**LaTeX label**: `fig:rlhf-to-reasoning`
**Caption**: From RLHF to reasoning RL. The machinery taught in this chapter carries directly into reasoning RL. What changes is the reward source: from a learned human-preference proxy to a verifiable task signal. This change reduces learned-reward over-optimization but does not remove all specification risk.

## Prompt

```text
Draw a conceptual bridge diagram for a graduate-level machine
learning textbook. Use a clean blue-white visual system: light blue
background, white panels, thin blue borders, charcoal text, and one
soft orange accent for the central transition.

CONCEPT:
The policy-optimization machinery of RLHF (policy sampling, reward
scoring, KL constraint, iterative updates) carries directly into
reasoning RL. What changes is the reward source: from a learned
human-preference proxy to a verifiable task signal (math correctness,
code tests, proof checkers). The figure should show shared machinery
and changed reward source as a clear bridge.

MAIN COMPOSITION:
A left-to-right two-panel bridge layout with a central transition
arrow connecting them.

LEFT PANEL -- "CLASSICAL RLHF (THIS CHAPTER)":
A white card showing:
- A policy model generating responses
- A learned reward model (with a small "proxy" warning badge)
  scoring responses
- A KL tether to reference policy
- PPO update loop
- Small icons for: preference pairs as input, human annotator
- Below the internals, a small caveat strip: "proxy can be hacked"

RIGHT PANEL -- "REASONING RL (NEXT CHAPTER)":
A white card showing:
- A policy model generating reasoning traces (show a chain-of-thought
  strip with intermediate steps)
- Verifiable reward sources as three small stacked cards:
  - Calculator icon: "math answer checker"
  - Terminal icon: "code unit tests"
  - Proof icon: "formal verification"
- Same KL tether and policy update loop as left panel
- Below the internals, a small caveat strip: "less proxy hacking,
  still specification risk"

CENTER TRANSITION:
A prominent soft-orange horizontal arrow connecting the two panels,
labeled "reward source changes". Below the arrow, a compact list of
what stays the same:
- "policy sampling" (check icon)
- "reward scoring" (check icon)
- "KL / reference control" (check icon)
- "iterative updates" (check icon)

BOTTOM STRIP:
A thin contrast strip across the bottom with two rows:
Row 1: "RLHF: learned proxy | human preference | reward hacking risk"
Row 2: "Reasoning RL: verifier | task correctness | specification risk"

STYLE:
- Background: #FAFCFF
- Panels: white with thin #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF
- Pale blue fills: #E8F4FD
- Orange accent: #FF9F43 only for the center transition arrow
- Frozen/reference elements: light gray #E5E7EB
- Text: #1A1A2E; secondary labels: #6B7280
- Clean sans-serif typography; landscape orientation

IMPORTANT:
- Do not imply reasoning RL completely solves reward hacking; show
  reduced but not eliminated risk
- Do not make reasoning RL look unrelated to RLHF; emphasize the
  shared machinery as the visual throughline
- Do not use red or warning colors
- Keep the transition arrow as the visual center of gravity
- The caveats must be readable but visually secondary to the main
  bridge narrative
- Keep all text short and readable at 50% page width
```

## Review Checklist

- [ ] Two panels: classical RLHF and reasoning RL
- [ ] RLHF panel shows learned reward model with proxy warning
- [ ] Reasoning RL panel shows verifiable rewards (math, code, proofs)
- [ ] Both panels share KL tether and policy update loop
- [ ] Orange transition arrow is the visual centerpiece
- [ ] Shared machinery listed below the transition arrow
- [ ] Bottom strip contrasts reward sources and risk types
- [ ] Caveat strips present in both panels
- [ ] Blue-white palette, no red or dark backgrounds
- [ ] Readable at 50% width in PDF
