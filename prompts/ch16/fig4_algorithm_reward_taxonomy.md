# Figure 16.5: Algorithm by Reward Source

**Filename**: `fig_algorithm_reward_taxonomy.png`
**LaTeX label**: `fig:algorithm-reward-taxonomy`
**Caption**: \textbf{Reasoning RL is an algorithm--reward design space.} The reward source can be a human preference model, an AI preference model, an exact verifier, a unit-test suite, a process reward model, or a self-generated signal. The optimizer can be PPO, GRPO, rejection sampling, iterative DPO, or self-training. The 2024--2026 shift is not a single algorithm; it is the pairing of scalable reward sources with iterative optimization.

## Prompt

```text
Draw a two-axis taxonomy diagram for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Show that reasoning RL is not one method. It is a design space crossing reward sources with optimization algorithms.

MAIN COMPOSITION:
MATRIX LAYOUT:
- Horizontal axis: reward source.
  Columns: preference RM, AI judge, exact verifier, unit tests, process RM, self-signal.
- Vertical axis: optimizer.
  Rows: PPO, GRPO, rejection sampling, iterative DPO, self-training.
- Use pale blue cells with small icons.

HIGHLIGHTED PATH:
- One orange path highlights "exact verifier + GRPO" as the chapter's main case study.
- Other cells are visible but muted.

MINI LEGEND:
- Critic required icon.
- Gradient update icon.
- Inference-only icon.
- Data-filtering icon.

BOTTOM BANNER:
- "The shift is scalable reward + iterative optimization, not one algorithm."

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
- Do not make every cell equally prominent.
- Do not use long paragraphs inside cells.
- Do not imply GRPO is the whole field.
- Keep axes readable.
- Fill the full canvas.
- All text readable at 50% PDF width.
```

## Review Checklist

- [ ] Two axes are clear.
- [ ] GRPO + verifier is highlighted.
- [ ] Other methods remain visible.
- [ ] Legend explains icons.
- [ ] Bottom banner states the core lesson.
- [ ] Only one orange path/focal element.
- [ ] No dense paragraphs.
- [ ] Canvas has no empty corners.
