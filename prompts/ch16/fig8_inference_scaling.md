# Figure 16.10: Inference-Time Scaling

**Filename**: `fig_inference_scaling.png`
**LaTeX label**: `fig:inference-scaling`
**Caption**: \textbf{Inference-time scaling for reasoning.} Reasoning models can spend more compute at test time by sampling multiple solutions, voting, ranking with a verifier, or searching over partial reasoning paths. Training-time RL teaches the policy to produce trajectories that make this extra compute useful.

## Prompt

```text
Draw an inference-time scaling diagram for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Show that reasoning models use test-time compute as a third capability axis alongside parameters and training data.

MAIN COMPOSITION:
LEFT: SINGLE SAMPLE
- Prompt enters model, one response exits.
- Small accuracy gauge.

CENTER: PARALLEL SAMPLING
- Same prompt fans out to N responses.
- Majority voting and best-of-N ranking modules.
- Verifier selects or aggregates.
- Orange accent on selected best response.

RIGHT: SEARCH
- Partial reasoning tree with branches.
- PRM/verifier scores intermediate nodes.
- Winning path reaches final answer.

BOTTOM THREE-AXIS STRIP:
- Parameters axis.
- Training/RL data axis.
- Inference compute axis highlighted as "third axis".

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
- Do not imply inference-time scaling is free.
- Include compute cost icons or token counters.
- Keep tree search simple and readable.
- Use one orange selected path only.
- Fill full width with three balanced panels.
- All text readable at 50% PDF width.
```

## Review Checklist

- [ ] Single sample, best-of-N/voting, and search are distinct.
- [ ] Verifier or ranker is visible.
- [ ] Inference compute is shown as the third axis.
- [ ] Compute cost is acknowledged.
- [ ] Only one orange selected path/response.
- [ ] Layout uses full width.
- [ ] Text remains concise.
- [ ] Palette matches blue-white system.
