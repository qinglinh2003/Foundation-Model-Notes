# Figure 20.2: RAG Pipeline with Attribution

**Filename**: `fig_rag_attribution_pipeline.png`
**LaTeX label**: `fig:ch20-rag-attribution-pipeline`
**Caption**: RAG as access, selection, and attribution. Retrieval finds candidate evidence, reranking and packing decide what enters the prompt, generation produces the answer, and citation checking asks whether each claim is supported by the cited source.

## Prompt

```text
Draw a retrieval-augmented generation pipeline for a graduate-level machine
learning textbook. Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
RAG is not just vector search. It has three system layers: access to candidate
evidence, selection of what enters the prompt, and attribution that checks
whether answer claims are supported by cited sources.

MAIN COMPOSITION:
A wide horizontal pipeline with three large stage cards connected left to right.
Each stage card should contain rich internal mini-visuals plus direct labels and
small counts. Match the information density of earlier chapter figures: clear
stage headers, short annotations, numeric examples, and a bottom formula/lesson
strip.

STAGE 1 -- "ACCESS":
Inside the card:
- A corpus shelf with many small document tiles
- A query embedding dot and a sparse keyword tag entering the shelf
- A small set of retrieved evidence cards coming out
- Use two tiny search icons to imply dense + sparse retrieval without writing
  long explanations
Add these labels inside the stage:
"dense + sparse search"
"500K-token corpus"
"100 candidates"

STAGE 2 -- "SELECTION":
Inside the card:
- Candidate evidence cards enter a reranker sorter
- The top few cards become a neat prompt pack
- Low-value cards fall into a muted side tray
- Show a small packing gauge labeled "context budget"
Add these labels inside the stage:
"rerank"
"100 -> 8 passages"
"pack into 6K tokens"

STAGE 3 -- "ATTRIBUTION":
Inside the card:
- A model produces an answer card with three short claim lines:
  "Claim A", "Claim B", "Claim C"
- Thin blue citation threads connect each claim line back to source cards
- One citation thread is checked by a small verifier lens
- Use the single orange accent on the verifier lens, not on every citation
Add these labels inside the stage:
"cite"
"audit support"
"claim -> source"

BOTTOM STRIP:
Show the three-layer lesson as compact icon labels plus one formula-like line:
"find evidence" -> "choose evidence" -> "support claims"
"RAG quality = retrieval recall × selection quality × faithfulness"

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Muted discarded cards: #E5E7EB
- Orange accent: #FF9F43 only for the citation verifier lens
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
- Do not draw a generic vector database product diagram.
- Do not include logos, cloud icons, SQL tables, or dashboard widgets.
- The attribution threads must visibly connect answer claims back to sources.
- Keep labels short, but include all required labels and numeric counts.
- Use direct labels as part of the diagram, not just icons.
- The figure should be visually denser than a simple flowchart but still clean.
- All text readable at 50% PDF width.
```

## Review Checklist

- [ ] Three stages: Access, Selection, Attribution
- [ ] Stage labels and counts appear: 500K-token corpus, 100 candidates, 100 -> 8 passages, 6K tokens
- [ ] Access stage shows corpus and retrieved evidence cards
- [ ] Selection stage shows reranking, discarded cards, and context budget
- [ ] Attribution stage shows answer claims connected to source cards
- [ ] Orange accent appears only on the verifier lens
- [ ] Bottom strip states find, choose, support and includes the RAG quality line
- [ ] No vector database product imagery
- [ ] Text readable at 50% width in PDF
