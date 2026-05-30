# Figure 20.1: Context Paths for One Query

**Filename**: `fig_context_paths.png`
**LaTeX label**: `fig:ch20-context-paths`
**Caption**: Context routing for one query. A context system can answer directly, read a long prompt, retrieve evidence, reuse cached context, compress history, or route to a hybrid path. The chapter's central question is not which path is universally best, but which path fits the task, cost budget, and evidence risk.

## Prompt

```text
Draw a context-routing diagram for a graduate-level machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
One user query can follow different context paths before the model answers:
direct answer, long-context reading, retrieval, cached context, compression,
or a hybrid path. The figure should feel like a systems routing map, not a
generic flowchart.

MAIN COMPOSITION:
A wide left-to-right routing map with three visual zones. The figure should
look like an explanatory systems diagram, not a sparse icon poster. Use direct
text labels inside the lanes the way earlier chapter figures label TTFT, TPOT,
pass@k, and KV cache.

LEFT ZONE -- "USER QUERY":
Show a clean question card entering the system. Put a short realistic query
inside the card:
"What changed since last meeting?"
Add only two small icons beside it: a clock and a document. Do not add extra
text tags under the query.

CENTER ZONE -- "CONTEXT ROUTER":
Show a large blue routing switchboard panel with five output lanes. The router
should look like a technical substrate: input port, branching traces, and small
decision knobs. Use the single orange accent on the active routing switch.
Inside the router, add three compact decision labels:
"coverage?", "latency?", "citation?"

FIVE ROUTING LANES:
Arrange five lanes from top to bottom, each with a concrete mini-visual:
1. "direct answer" -- a short thin lane from query to model, with a lightning
   icon.
2. "long-context read" -- a long document scroll feeding a wide context window
   labeled "128K--1M tokens".
3. "RAG retrieval" -- document shards pulled from a corpus shelf by a magnifier,
   labeled "top-k evidence".
4. "cached context" -- a memory-page stack reused through a cache chip.
5. "compress history" -- many cards squeezed through a funnel into a summary
   strip, labeled "10K -> 2K tokens".

RIGHT ZONE -- "MODEL ANSWER":
Show all lanes entering a single model context window, then one answer card.
The long-read and retrieve lanes should braid briefly before the model to
suggest a hybrid path, but do not add a separate large "hybrid" box.
Inside the final context window, add only three short slot labels:
"evidence", "history", "citations". On the answer card, show two claim lines
and one citation bracket without extra micro-text.

BOTTOM STRIP:
A thin comparison strip with four compact metric cards. Each card has a label
and a tiny visual meter:
"coverage", "latency", "cost", "auditability".
Add the takeaway sentence in the strip:
"route context by task, budget, and evidence risk".

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 only for the active routing switch
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
- Do not make this a hub-and-spoke icon poster.
- Do not use product logos, browser windows, agents, tools, or code execution.
- Keep the five lanes visually distinct through mini-visuals plus short direct
  labels.
- Include only the concrete labels and numbers listed above; do not add extra
  per-lane explanatory phrases.
- Use no paragraphs inside the image. Prefer larger route labels over small
  annotations.
- All labels must be readable at 50% PDF width.
- Fill the full landscape canvas with no empty corners.
```

## Review Checklist

- [ ] Query, router, five context paths, model, and answer are present
- [ ] Each path has a concrete mini-visual, not just a text label
- [ ] Lane labels include direct answer, long-context read, RAG retrieval, cached context, and compress history
- [ ] Concrete text appears: 128K--1M tokens, top-k evidence, 10K -> 2K tokens
- [ ] There are no tiny per-route explanation labels beyond the required labels
- [ ] Long-read and retrieval paths can combine into a hybrid path
- [ ] Bottom strip shows coverage, latency, cost, auditability, and the takeaway sentence
- [ ] Orange accent appears only on the active routing switch
- [ ] No agent/tool/browser imagery
- [ ] Text readable at 50% width in PDF
- [ ] Figure uses the full landscape canvas
