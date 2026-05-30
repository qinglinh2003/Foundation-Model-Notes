# Figure 22.3: Failure Attribution Tree

**Filename**: `fig_failure_attribution_tree.png`
**LaTeX label**: `fig:ch22-failure-tree`
**Caption**: \textbf{Failure attribution tree.} The goal is not to list every possible bug. It is to find the first layer whose failure made later failures unsurprising.

## Prompt

```text
Draw a wide diagnostic decision tree for a graduate-level machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Show how to localize the first broken layer in a failed model system. The figure should teach that later failures may be symptoms; the audit starts with the earliest layer whose failure made the rest unsurprising.

MAIN COMPOSITION:
Create a left-to-right failure review path with eight stacked layers. Use a central horizontal trace line that flows through the layers, with branch markers for "first broken layer".

LAYERS:
1. MODEL: "could the model solve with oracle evidence?"
Mini-icon: model card with reasoning bubble.
2. CONTEXT: "did evidence retrieval or packing expose the right information?"
Mini-icon: context window with highlighted source.
3. TOOL: "was the right operation available and called correctly?"
Mini-icon: API/tool node with argument schema.
4. WORKFLOW: "did routing, retry, stop, or approval match the task?"
Mini-icon: small workflow graph.
5. STATE: "did scratchpad, trace, and budget remain accurate?"
Mini-icon: state ledger with step counter.
6. VALIDATION: "did tests, verifier, judge, or citation audit catch the error?"
Mini-icon: test panel with pass/fail marks.
7. COST/BUDGET: "did success require unacceptable calls, latency, or money?"
Mini-icon: clock and cost meter.
8. SAFETY: "did permission, sandboxing, injection defense, or data control fail?"
Mini-icon: shield and locked action.

VISUAL LOGIC:
Add a highlighted branch at the Context layer labeled "first broken layer" and show downstream Tool/Workflow/Validation failures as pale secondary symptoms.
Add a bottom note:
"Do not only report that the system failed. Localize the first broken layer."

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — use only on the "first broken layer" marker
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
- Include all eight layers with the exact layer names.
- Make the "first broken layer" idea visually obvious.
- Do not turn this into a dense table; use a decision path with layer cards.
- Keep all labels readable at 50% PDF width.
- Use only one orange accent.
- Avoid product logos, robots, or decorative imagery.
- Fill the full canvas; no empty corners.
```

## Review Checklist

- [ ] Eight layers are present and readable
- [ ] A single "first broken layer" marker is highlighted
- [ ] Downstream failures are visually shown as symptoms
- [ ] Bottom note states the audit principle
- [ ] Orange accent appears only once
- [ ] Text remains readable at 50% PDF width
