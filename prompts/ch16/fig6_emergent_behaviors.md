# Figure 16.8: Emergent Reasoning Behaviors

**Filename**: `fig_emergent_behaviors.png`
**LaTeX label**: `fig:emergent-behaviors`
**Caption**: \textbf{Reasoning behaviors reinforced by verifier reward.} Longer deliberation, self-checking, backtracking, and edge-case testing can emerge because they correlate with verifier success. R1-Zero is the anchor case: response length and reflection-like phrases increased during RL training without supervised reasoning traces as the main source.

## Prompt

```text
Draw a behavior-emergence diagram for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Show how verifier reward can reinforce reasoning behaviors without explicitly labeling each behavior, using R1-Zero as the concrete training-log anchor.

MAIN COMPOSITION:
CENTRAL TRAJECTORY:
- A response trajectory flows left to right through reasoning tokens.
- Four behavior callouts branch from the trajectory: longer deliberation, self-checking, backtracking, edge-case testing.

BEHAVIOR MINI-VISUALS:
- Longer deliberation: token length meter increasing only on hard tasks.
- Self-checking: small checklist over an equation.
- Backtracking: curved arrow returning to an earlier plan.
- Edge-case testing: code function tested on boundary inputs.

R1-ZERO TRAINING LOG PANEL:
- Add a compact right-side mini chart labeled "R1-Zero training signal".
- Chart 1: average response length rises over training steps.
- Chart 2: reflection marker frequency rises ("wait", "check", "reconsider") as tiny tick marks, not full text paragraphs.
- Add a small note: "behavior emerged from verifier reward, not direct labels".

REWARD CONNECTION:
- All branches converge to a verifier pass badge.
- Orange accent on "trajectory succeeds" badge.
- Add a small warning: "correlation, not direct labels".

BOTTOM STRIP:
- "RL reinforces successful trajectories; behaviors are discovered when they help."

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
- Do not imply the behaviors are manually labeled.
- Do not imply R1-Zero is the production R1 recipe; this is the RL-only case study.
- Do not use anthropomorphic brain imagery.
- Keep behavior icons simple and concrete.
- Use abstract token strips instead of full text.
- Fill the canvas with no empty corners.
- All text readable at 50% PDF width.
```

## Review Checklist

- [ ] Four behaviors are clearly shown.
- [ ] R1-Zero mini training-log panel shows length and reflection markers.
- [ ] Verifier success connects to trajectory reward.
- [ ] It is clear behaviors are reinforced indirectly.
- [ ] One orange success badge only.
- [ ] No anthropomorphic imagery.
- [ ] Token trajectory is readable.
- [ ] Bottom strip states the lesson.
- [ ] Canvas is filled.
