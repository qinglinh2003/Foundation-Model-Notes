# Figure 20.4: Compression and Memory Hierarchy

**Filename**: `fig_compression_memory_hierarchy.png`
**LaTeX label**: `fig:ch20-compression-memory-hierarchy`
**Caption**: Compression and memory hierarchy. Raw documents can be segmented, retrieved, summarized, packed into working context, or written to persistent memory. Each upward step saves tokens but increases the risk of information loss.

## Prompt

```text
Draw a compression-and-memory hierarchy diagram for a graduate-level machine
learning textbook. Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Context compression saves tokens by moving information through increasingly
compact representations, but each step can drop details. Persistent memory is
not the same as the current working context.

MAIN COMPOSITION:
Create a large vertical hourglass in the center, surrounded by memory panels.
The hourglass should be the visual anchor. Use concrete token counts on each
layer so the reader sees compression as a quantitative budget tradeoff, similar
to the memory and cost figures in Chapter 19.

TOP WIDE LAYER -- "RAW EVIDENCE":
Show many full document pages, experiment logs, and chat transcript cards
spread across the top. They should look abundant and detailed.
Label this layer:
"raw evidence: 50 pages / 60K tokens".

MIDDLE NARROW LAYERS:
Layer 1: "chunks: 200 chunks" -- document pages split into smaller cards.
Layer 2: "retrieved: 12 passages" -- a selected subset of cards moves inward.
Layer 3: "summary: 3 short notes" -- many cards collapse into a shorter note strip.
Use the single orange accent on one tiny lost-detail card falling out of the
hourglass, labeled "lost detail".

BOTTOM LAYER -- "WORKING CONTEXT":
Show a clean model context window receiving a compact evidence pack.
Inside the window, show only a few source cards and a summary strip.
Label the window:
"working context: 4K tokens".

SIDE MEMORY PANELS:
Left side: "episodic memory" with small event cards on a timeline.
Right side: "semantic memory" with only three stable fact cards in a neat file
drawer. Do not add more examples or tiny notes inside these cards.
Both side panels connect back to the working context with thin blue arrows.
Add one small label below the side panels:
"persistent memory is retrieved, not always visible".

BOTTOM STRIP:
Add a thin lesson strip with one compact equation-like line:
"60K raw -> 4K working context"
"fewer tokens" -> "more abstraction" -> "higher loss risk".

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 only for the lost-detail card
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
- Do not make the figure a plain stack of boxes.
- The hourglass metaphor must be visually obvious.
- Do not include agent scratchpads, plans, or tool loops.
- Keep labels short and readable, but include the required token counts.
- Make persistent memory visually separate from working context.
- Keep semantic memory sparse: only three visible cards, large enough to read.
- Fill the full canvas with balanced side panels.
```

## Review Checklist

- [ ] Hourglass hierarchy is the central visual anchor
- [ ] Token-count labels appear: 60K raw, 200 chunks, 12 passages, 3 notes, 4K context
- [ ] Raw evidence, chunks, retrieved evidence, summary, and working context appear
- [ ] Episodic and semantic memory are side panels, not agent scratchpads
- [ ] Lost detail is the only orange-accent element
- [ ] Bottom strip shows 60K raw -> 4K working context and the loss-risk lesson
- [ ] No tool or agent loop imagery
- [ ] Text readable at 50% width in PDF
