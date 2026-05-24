# Figure 17.2: Three Regimes of RL Effect

**Filename**: `fig_rl_effect_regimes.png`
**LaTeX label**: `fig:rl-effect-regimes`
**Caption**: Three regimes of RL effect. In sharpening, RL reallocates probability mass toward already-sampled good trajectories. In composition, RL makes existing subskills cooperate reliably in one trajectory. In discovery, RL finds genuinely new strategies outside the base model's accessible support. Current LLM RLVR has strong evidence for sharpening, some evidence for composition, and weak evidence for discovery.

## Prompt

```text
Draw a three-regime conceptual taxonomy for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
The figure classifies RL effects into sharpening, composition, and discovery. It should show that current LLM RLVR mostly sits in regimes 1-2, with discovery still uncertain.

MAIN COMPOSITION:
THREE HORIZONTAL PANELS:
Panel 1: "Regime 1 — Sharpening". Show many existing paths from a base model distribution. After RL, probability mass thickens around one already-existing successful path. Include label: "increase probability of known good paths".

Panel 2: "Regime 2 — Composition". Show separate small skill tiles (verify, decompose, algebra, summarize) connected into one chain after RL. Include label: "make existing subskills cooperate".

Panel 3: "Regime 3 — Discovery". Show a dashed path leaving the visible base-model support boundary into a new strategy region with a question mark. Include label: "find strategies outside accessible support".

TOP INDICATOR:
Above panels, place a thin arrow labeled "stronger claim as you move right". Add a small orange marker spanning panel 1 and lightly touching panel 2 labeled "current LLM RLVR evidence mostly here".

BOTTOM NOTE:
Full-width note: "The question is not whether RL improves scores; it is which regime explains the improvement."

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — use only for the "current evidence" marker
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
- Do not make discovery look impossible; make it uncertain.
- Use dashed boundary and question mark only in the discovery panel.
- Keep all three panels equal width.
- Include internal visual details in every panel, not just text boxes.
- All text must be readable at 50% PDF width.
```

## Review Checklist

- [ ] Three panels are clearly labeled sharpening, composition, discovery.
- [ ] Regime 1 shows probability mass reallocation.
- [ ] Regime 2 shows subskill chaining.
- [ ] Regime 3 shows a new path beyond support with uncertainty.
- [ ] Orange marker indicates current evidence mostly in regimes 1-2.
- [ ] Bottom note asks which regime explains improvement.
- [ ] Layout uses full width.
- [ ] No decorative gradients or dark background.
