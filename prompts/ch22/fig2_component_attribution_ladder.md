# Figure 22.2: Component Attribution Ladder

**Filename**: `fig_component_attribution_ladder.png`
**LaTeX label**: `fig:ch22-attribution-ladder`
**Caption**: \textbf{Component attribution ladder.} A full-system score is explained by comparing controlled variants, not by inspecting the final answer alone. Oracle rungs distinguish model limitations from retrieval, tool, and workflow limitations.

## Prompt

```text
Draw a wide ladder-style diagnostic diagram for a graduate-level machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Show that a full model-system score should be explained through controlled variants: base model, oracle evidence, retrieved evidence, citation audit, tools, agent loop, and production constraints. The figure should make ablations, oracle tests, and cost-per-success visible.

MAIN COMPOSITION:
Create a left-to-right ascending ladder with seven large rungs. Each rung should be a labeled platform with a tiny icon, a one-line question, and small metric chips for success, cost, latency, and main failure.

RUNG 1 -- BASE MODEL ONLY:
Icon: single model card.
Question: "What can the model do alone?"
Metric chips: "success low", "cost low", "failure: missing evidence".

RUNG 2 -- + ORACLE EVIDENCE:
Icon: gold-edged evidence card, but use blue palette with one subtle orange checkmark only if this is the single orange accent.
Question: "Can the model use the right evidence?"
Metric chips: "success rises", "cost medium", "failure: edge case".

RUNG 3 -- + RETRIEVED EVIDENCE:
Icon: search index feeding context window.
Question: "Did retrieval expose the evidence?"
Metric chips: "success medium", "failure: retrieval miss".

RUNG 4 -- RAG + CITATION AUDIT:
Icon: claim cards linked to source snippets.
Question: "Are final claims supported?"
Metric chips: "support checked", "failure: citation mismatch".

RUNG 5 -- TOOL WORKFLOW:
Icon: deterministic graph with tool nodes.
Question: "Do typed tools solve the subproblem?"
Metric chips: "cost high", "failure: tool error".

RUNG 6 -- BOUNDED AGENT LOOP:
Icon: observe-act-retry loop with a step counter.
Question: "Do action selection and recovery add value?"
Metric chips: "retries bounded", "failure: drift".

RUNG 7 -- PRODUCTION CONSTRAINTS:
Icon: shield, clock, dollar sign, trace log.
Question: "Does success survive real constraints?"
Metric chips: "cost/success", "latency", "safety", "trace".

RIGHT SIDE:
Add a compact interpretation panel:
"Do not report only the top rung. Report which rung created the gain and what it cost."

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — ONE focal element only, preferably the "oracle evidence" checkmark
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
- The diagram must read as a ladder, not a generic pipeline.
- Include all seven rungs in order.
- Every rung should have internal content; avoid empty boxes.
- Make "cost/success" visible as a metric.
- Keep text readable at 50% PDF width.
- Do not include product logos or benchmark logos.
- Use only one orange accent.
```

## Review Checklist

- [ ] Seven rungs appear in the correct order
- [ ] Oracle evidence and retrieved evidence are visually distinct
- [ ] Cost, latency, and failure attribution are visible
- [ ] Right-side interpretation panel is present
- [ ] Orange accent appears only once
- [ ] Text remains readable at 50% PDF width
