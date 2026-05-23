# Figure 11.6: Self-Instruct Pipeline

**Filename**: `fig_self_instruct.png`
**LaTeX label**: `fig:self-instruct`
**Caption**: The Self-Instruct pipeline. A small seed set of human-written instructions bootstraps a larger synthetic dataset through iterative LLM generation and filtering. Each cycle expands the instruction space, though diversity tends to plateau after several rounds.

## Prompt

```text
Draw a Self-Instruct synthetic data pipeline for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system. LANDSCAPE orientation,
wide and spacious. Match the visual richness of Ch9 "Data Funnel" and Ch10
"Benchmark Decay Cycle": the pipeline should feel iterative and data-rich, not
like plain boxes.

CONCEPT:
"A small seed set bootstraps a large instruction dataset." The visual should show
iterative expansion plus filtering. It should also show the limitation: diversity
plateaus if the model keeps generating similar tasks.

MAIN COMPOSITION:
A circular/spiral pipeline across the center, with five stages:
1. Seed instructions: a small stack of 175 handwritten instruction cards.
2. Generate new instructions: an LLM chip emits many new cards with varied task
   icons (QA, code, summary, math, writing).
3. Generate responses: instruction cards pair with response cards.
4. Filter and deduplicate: a funnel removes duplicates, low-quality cards, and
   near-seed copies.
5. Expanded dataset: a larger curated stack labeled "52K+ examples".

Use arrows to form a loop from expanded dataset back into generation, but make
the second loop lighter to show iteration.

INTERNAL DETAILS:
- In the filter stage, show rejected cards falling out in gray, with tiny labels:
  "duplicate", "too similar", "low quality".
- On the expanded dataset stack, show multiple task colors/patterns, but keep
the palette blue-based.
- Add a small side mini-chart: x-axis "rounds", y-axis "new diversity", curve
 rises early then plateaus. Highlight the plateau dot in soft orange (#FF9F43).
This is the only orange element.

STYLE:
Use primary blue #2D8CFF, pale blue #E8F4FD, border #CFE3F7, charcoal #1A1A2E,
steel gray #6B7280, soft orange #FF9F43 for the plateau warning only. Clean
technical textbook diagram; no dark background, no glossy business style, no
decorative blobs. Text should be sparse and legible.
```

## Review Checklist

- [ ] Pipeline visibly starts from a small seed and ends with a large dataset.
- [ ] Filtering stage removes bad/duplicate examples.
- [ ] Iterative loop is clear.
- [ ] Diversity plateau limitation is visible but not dominant.
