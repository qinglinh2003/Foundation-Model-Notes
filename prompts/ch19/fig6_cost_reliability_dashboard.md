# Figure 19.6: Cost Per Useful Task Dashboard

**Filename**: `fig_cost_reliability_dashboard.png`
**LaTeX label**: `fig:ch19-cost-reliability-dashboard`
**Caption**: **Cost per useful task dashboard.** A serving report should connect systems metrics (TTFT, TPOT, throughput, memory) to task metrics (success rate and failure type). The relevant frontier is cost per successful task, not maximum tokens per second alone.

## Prompt

```text
Draw a dashboard-style figure for LLM serving evaluation in a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Show that serving reports must connect hardware/runtime metrics to task success. The key metric is cost per successful task, not tokens per second alone.

MAIN COMPOSITION:
TOP ROW: four metric cards:
1. TTFT: 820 ms
2. TPOT: 38 ms/token
3. Throughput: 2,400 tok/s
4. Peak memory: 67 GB / 80 GB

MIDDLE ROW: task metrics:
- Success rate: 74%
- Tool failures: 9%
- Retrieval misses: 11%
- Final answer errors: 6%
Use tiny bar chart icons in each card.

BOTTOM LEFT: cost equation card:
Request cost = prefill + N × decode + extra calls
Cost per success = request cost / success rate

BOTTOM RIGHT: frontier plot with x-axis "cost per task" and y-axis "success rate". Show three operating points: fast chat, RAG assistant, agent loop. Highlight the balanced point with orange.

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — use only for the balanced operating point
- Text: #1A1A2E (headers), #6B7280 (annotations)
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
Do not make this look like a finance dashboard.
Do not focus only on tokens/sec.
Include both systems metrics and task metrics.
Use concrete numbers, but keep them illustrative.
All text readable at 50% PDF width.
Fill full canvas with organized panels.
```

## Review Checklist

- [ ] TTFT, TPOT, throughput, and memory appear
- [ ] Success rate and failure categories appear
- [ ] Cost per success equation appears
- [ ] Frontier plot has multiple operating points
- [ ] Orange accent only on balanced point
- [ ] Does not over-emphasize tokens/sec
- [ ] Text readable at 50% PDF width
- [ ] Dashboard is dense but organized
