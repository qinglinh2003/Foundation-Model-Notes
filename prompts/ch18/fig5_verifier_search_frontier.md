# Figure 18.5: Verifier-Guided Search and the Cost-Reliability Frontier

**Filename**: `fig_verifier_search_frontier.png`  
**LaTeX label**: `fig:ch18-verifier-search-frontier`  
**Caption**: Verifier-guided search and the cost--reliability frontier. Flat best-of-N spends compute on complete candidates; process-guided search spends compute adaptively on partial traces. Both must be judged by reliability gained per unit of latency and cost.

## Prompt

```text
Create a textbook figure connecting verifier-guided search to the cost-reliability frontier.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation.

CONCEPT:
Inference-time scaling methods improve reliability by spending compute, but gains must be evaluated against latency and cost. Flat best-of-N and process-guided search spend compute differently.

MAIN COMPOSITION:
Use two coordinated panels.

LEFT PANEL: "Two ways to spend compute"
Top subpanel: Flat best-of-N.
Show many complete candidate paths generated in parallel, then a verifier scoring completed answers.
Bottom subpanel: Process-guided search.
Show a branching reasoning tree where a verifier prunes weak partial branches and expands promising branches.
Use blue check marks on promising branches and gray X marks on pruned branches.

RIGHT PANEL: "Cost--reliability frontier"
Draw a clean 2D curve.
x-axis: "runtime cost / latency"
y-axis: "task reliability"
Plot three labeled points:
"single sample" low cost / lower reliability
"best-of-N" medium-high cost / higher reliability
"guided search" higher cost / potentially higher reliability
Show diminishing returns by flattening the curve.
Add a small orange callout: "choose operating point by product need".

STYLE:
- Background #FAFCFF
- Primary blue #2D8CFF
- Pale blue #E8F4FD
- Gray #D1D5DB for pruned/failed paths
- Orange #FF9F43 only for the operating-point callout
- Text #1A1A2E, annotations #6B7280
- Clean sans-serif typography
- No business-dashboard look, no gradients, no dark background

IMPORTANT:
- The left panel must contrast complete-candidate reranking vs partial-trace search.
- The right panel must clearly show diminishing returns.
- Do not include external tools, APIs, browsers, calculators, or code execution; this is model-internal search.
- All labels must be readable at PDF size.
```

## Review Checklist

- [ ] Flat best-of-N and process-guided search are visually distinct.
- [ ] Cost-reliability frontier has labeled operating points.
- [ ] Diminishing returns are visible.
- [ ] No external tool-use imagery appears.
