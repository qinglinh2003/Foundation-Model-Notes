# Figure 16.9: Reasoning Data Infrastructure Loop

**Filename**: `fig_reasoning_data_loop.png`
**LaTeX label**: `fig:reasoning-data-loop`
**Caption**: \textbf{Reasoning data infrastructure.} A reasoning-RL system is a loop: generate candidate problems or solutions, verify outputs, filter or score trajectories, update the policy, and refresh the curriculum. The algorithm is only as good as the task distribution and verifier pipeline.

## Prompt

```text
Draw a systems loop diagram for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Show that reasoning RL depends on data infrastructure: task difficulty, verifier engineering, filtering, policy update, and curriculum refresh.

MAIN COMPOSITION:
CIRCULAR LOOP WITH FIVE STATIONS:
1. Problem bank / curriculum: easy, medium, hard cards.
2. Policy samples solutions: multiple response cards.
3. Verifier scores outputs: answer checker and unit tests.
4. Filter / score trajectories: pass/fail and partial credit bins.
5. Update policy and refresh curriculum: model card feeding back to problem bank.

INTERNAL DETAILS:
- Include a small difficulty meter showing the useful frontier: not all-pass, not all-fail.
- Include a verifier checklist: parse, normalize, test, timeout.
- Orange accent on the "mixed rewards = useful signal" zone.

BOTTOM BANNER:
- "Verifier engineering is data cleaning for RLVR."

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
- Do not make a generic MLOps diagram.
- The difficulty frontier must be visible.
- Keep station labels short.
- Use icons and mini-cards, not paragraphs.
- Fill the full width.
- All text readable at 50% PDF width.
```

## Review Checklist

- [ ] Five-station loop is clear.
- [ ] Difficulty frontier is visible.
- [ ] Verifier engineering details appear.
- [ ] Mixed rewards are highlighted with one orange accent.
- [ ] Bottom banner states the lesson.
- [ ] No generic cloud/server imagery dominates.
- [ ] Text remains readable.
- [ ] Canvas is full and balanced.
