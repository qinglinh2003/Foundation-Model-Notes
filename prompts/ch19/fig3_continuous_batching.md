# Figure 19.3: Static vs Continuous Batching

**Filename**: `fig_continuous_batching.png`
**LaTeX label**: `fig:ch19-continuous-batching`
**Caption**: **Static versus continuous batching.** Static batching holds a group until completion, wasting slots as sequences finish at different lengths. Continuous batching updates the active set at each decode step, admitting new requests and removing completed ones.

## Prompt

```text
Draw a side-by-side batching diagram for LLM serving in a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Compare static batching and continuous batching for variable-length autoregressive generation. The key lesson is that decode proceeds step by step, so the scheduler can remove finished requests and admit new ones between iterations.

MAIN COMPOSITION:
LEFT HALF titled "Static batching":
Show a time grid with 4 request lanes. Requests A, B, C, D start together. A and C finish early, but their lanes become pale empty padding slots while B continues long. Label wasted slots "idle padding".

RIGHT HALF titled "Continuous batching":
Show a time grid with decode iteration columns. Requests A, B, C start; A finishes and request D enters; C finishes and request E enters. Active lanes stay mostly filled. Label "remove finished" and "admit new request".

CENTER DIVIDER: a vertical comparison strip:
Static: simple, but wastes slots under variable lengths
Continuous: better utilization, more scheduler complexity

BOTTOM MINI-METRICS:
GPU utilization, TTFT queueing, throughput, variable output lengths.

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — use only on wasted idle padding in static batching
- Text: #1A1A2E (headers), #6B7280 (annotations)
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
Do not make this a data training batch figure.
Show decode iterations, not epochs or steps of SGD.
Make variable output lengths obvious.
Make continuous admission and removal visually clear.
All text readable at 50% PDF width.
Fill the full landscape width.
```

## Review Checklist

- [ ] Static and continuous batching are side by side
- [ ] Finished requests create wasted slots only in static batching
- [ ] Continuous batching admits new requests mid-stream
- [ ] Decode iterations are clearly labeled
- [ ] Orange accent only marks wasted padding
- [ ] No training terminology
- [ ] Text readable at 50% PDF width
- [ ] Figure uses full width
