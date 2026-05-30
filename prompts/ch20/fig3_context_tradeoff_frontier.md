# Figure 20.3: Long Context, RAG, Caching, and Hybrid Tradeoffs

**Filename**: `fig_context_tradeoff_frontier.png`
**LaTeX label**: `fig:ch20-context-tradeoff-frontier`
**Caption**: Long context, RAG, caching, and hybrid tradeoffs. Different context paths occupy different regions of the cost, latency, coverage, and auditability space. Routing chooses an operating point for a particular query, not a universal winner.

## Prompt

```text
Draw a context-system tradeoff map for a graduate-level machine learning
textbook. Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Long context, RAG, caching, and hybrid systems are operating points in a
tradeoff space. The lesson is not that one method wins universally; routing
chooses a path based on evidence coverage, latency, cost, and auditability.

MAIN COMPOSITION:
Use a two-panel layout. The left panel should be a labeled technical map with
visible axes, operating points, and only two short callouts. The right panel
should be a large routing card with generous row height; it must be readable
when printed, not a dense table.

LEFT PANEL -- "OPERATING MAP":
Draw a clean 2D map, not a single universal frontier curve.
x-axis: "cost / latency"
y-axis: "evidence coverage"
Place four large visual operating points:
- "direct: 1K prompt" in the low-cost / low-coverage corner
- "cache: stable corpus" in the low-latency / medium-coverage region
- "RAG: top-k evidence" in medium-cost / high-auditability region
- "long context: 128K--1M tokens" in higher-cost / high-coverage region
Add "hybrid: retrieve + long reader" as the orange-accent point between RAG and
long context.
Use faint blue contour bands rather than a hard winner curve.
Add only this callout near the long-context point:
"high coverage, high KV cost".
Add only this callout near the RAG point:
"auditable, can miss evidence".

RIGHT PANEL -- "ROUTING CARD":
Show a large decision card with three rows and three columns:
"query", "route", "risk".
Use only three rows:
- "quick fact" -> "direct" -> "unsupported"
- "fresh evidence" -> "RAG" -> "miss"
- "cross-document" -> "hybrid" -> "cost"
Use path icons beside the route names. Make this card visually prominent and
larger than the metric gauges.

BOTTOM MINI-BAR:
Show four simple gauges with labels only:
"coverage", "latency", "cost", "audit".
Add the bottom takeaway:
"routing chooses an operating point, not a universal winner".

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 only for the hybrid operating point
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
- Do not imply there is one universal best method.
- Do not draw a business analytics dashboard.
- Do not add real benchmark claims; the token counts are illustrative labels.
- Include the routing card text and the two callouts; do not add more callouts.
- Keep the visual focus on operating points and routing, with enough labels to
  teach the tradeoff.
- All labels readable at 50% PDF width.
- Fill the full landscape canvas.
```

## Review Checklist

- [ ] Map includes direct, cache, RAG, long context, and hybrid
- [ ] Operating points include 1K prompt, 128K--1M tokens, top-k evidence, and retrieve + long reader
- [ ] Hybrid is the only orange-accent operating point
- [ ] Axes are cost/latency and evidence coverage
- [ ] Right routing card has only three rows and is visually large
- [ ] Four gauges show coverage, latency, cost, and audit with labels
- [ ] Bottom takeaway sentence is present
- [ ] Figure does not imply a universal winner
- [ ] Text readable at 50% width in PDF
