# Figure 4.6: BERT in the Modern RAG Pipeline

**Filename**: `rag_pipeline.png`
**LaTeX label**: `fig:rag-pipeline`
**Caption**: A modern RAG pipeline: encoder models (BERT-style) handle retrieval and reranking; a decoder model (GPT-style) generates the final answer. The user sees GPT; the system depends on BERT.

## Prompt

```
Draw a modern RAG (Retrieval-Augmented Generation) pipeline for a graduate-level
machine learning textbook. Use the course's blue-white visual system.
Landscape orientation, polished editorial style.

LAYOUT:
A horizontal flow diagram showing a query moving through three stages.

STAGE 1 — RETRIEVAL (Bi-Encoder):
- Title: "Stage 1: Retrieve"
- Subtitle: "Bi-Encoder (BERT-style)"
- Show:
  - Query box: "What causes auroras?" → encoded by "Query Encoder" (blue)
  - Document database icon with "1M documents pre-encoded"
  - ANN (Approximate Nearest Neighbor) search connecting them
  - Output: "Top-100 candidates"
- Speed annotation: "~10ms, scalable to billions"
- The encoder boxes are Zoom Blue (#2D8CFF)

STAGE 2 — RERANKING (Cross-Encoder):
- Title: "Stage 2: Rerank"
- Subtitle: "Cross-Encoder (BERT-style)"
- Show:
  - Input: each (query, document) pair concatenated as
    "[CLS] query [SEP] document [SEP]"
  - A BERT cross-encoder scoring each pair
  - Output: "Top-5 reranked"
- Speed annotation: "~100ms for 100 pairs"
- The cross-encoder box is Zoom Blue

STAGE 3 — GENERATION (GPT):
- Title: "Stage 3: Generate"
- Subtitle: "Decoder-only (GPT-style)"
- Show:
  - Input: "Query + Top-5 documents as context"
  - A GPT model generating the answer
  - Output: "Auroras are caused by charged particles from the solar wind..."
- Speed annotation: "~1-3s for full answer"
- The GPT box should be a slightly different shade or have a
  distinct visual treatment to show it's a different model type

BOTTOM ANNOTATION:
- A bracket under Stages 1-2: "BERT-style encoders: invisible infrastructure"
  in Zoom Blue
- A bracket under Stage 3: "GPT-style decoder: user-facing interface"
- Center annotation in soft orange (#FF9F43):
  "The user sees GPT. The system depends on encoder models."

FLOW ARROWS:
- Large horizontal arrows between stages
- Each arrow labeled with what passes through:
  Stage 1→2: "100 candidates"
  Stage 2→3: "5 documents + query"

VISUAL DETAILS:
- Zoom Blue (#2D8CFF) for all encoder/BERT components
- Slightly different blue or a subtle border distinction for GPT component
- Soft Orange (#FF9F43) for the bottom annotation text only
- White/ice blue (#FAFCFF) background
- Database icon for document store
- Clean flow arrows with consistent weight
- Sans-serif labels in charcoal (#1A1A2E)
```

## Review Checklist

- [ ] Three stages clearly separated: Retrieve → Rerank → Generate
- [ ] Stages 1-2 labeled as "BERT-style" encoder models
- [ ] Stage 3 labeled as "GPT-style" decoder model
- [ ] Bi-encoder vs cross-encoder distinction clear
- [ ] Speed annotations show cost at each stage
- [ ] Bottom annotation: "user sees GPT, system depends on encoder models"
- [ ] Orange accent used only for the key insight annotation
- [ ] Data flow arrows show what passes between stages (100→5→answer)
