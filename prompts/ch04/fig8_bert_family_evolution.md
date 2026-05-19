# Figure 4.8: BERT Family Evolution

**Filename**: `bert_family_evolution.png`
**LaTeX label**: `fig:bert-family`
**Caption**: The BERT family tree: each successor addressed a specific limitation while preserving the core bidirectional encoder architecture.

## Prompt

```
Draw an evolution/family tree of BERT-style models for a graduate-level
machine learning textbook. Use the course's blue-white visual system.
Landscape orientation, polished editorial style.

LAYOUT:
A horizontal timeline/tree showing BERT's descendants, flowing left to right.
Each model is a node with its key contribution annotated.

TIMELINE (left to right):

NODE 1 — BERT (2018):
- Largest node, positioned at left
- Label: "BERT"
- Subtitle: "MLM + NSP"
- Key traits: "Bidirectional, 110M/340M params, max 512 tokens"
- This is the root/trunk

BRANCH A (top) — ROBERTA (2019):
- Branches from BERT
- Label: "RoBERTa"
- Key fix: "Remove NSP, dynamic masking, more data, longer training"
- Annotation: "Same architecture, better recipe"
- Small icon or note: "Training improvements only"

BRANCH B (middle) — DEBERTA (2020):
- Branches from BERT
- Label: "DeBERTa"
- Key fix: "Disentangled attention (separate content + position)"
- Annotation: "Architectural improvement"
- Show a small inset: content vector + position vector instead of summed

BRANCH C (bottom-left) — SENTENCE-BERT (2019):
- Branches from BERT
- Label: "Sentence-BERT"
- Key fix: "Siamese/contrastive training for sentence embeddings"
- Annotation: "New training objective for retrieval"

BRANCH D (far right) — MODERN EMBEDDINGS (2023-24):
- Continuation from Sentence-BERT direction
- Label: "BGE / E5 / GTE"
- Key fix: "Large-scale contrastive + instruction-aware training"
- Annotation: "Production embedding models"

ANNOTATIONS:
- A timeline bar at the bottom: 2018 → 2019 → 2020 → ... → 2024
- Above the tree: "What stayed constant: bidirectional Transformer encoder"
- Below the tree: "What changed: training recipe, objectives, scale"

COLOR CODING:
- Each branch has a subtle color variation to distinguish:
  - Training recipe improvements: lighter blue
  - Architectural improvements: medium blue
  - Objective/application changes: blue with orange accent

HIGHLIGHT:
- The orange accent (#FF9F43) should be on the annotation
  "What changed" or on arrows showing key improvements —
  pick ONE element to highlight. Suggestion: highlight the
  "Remove NSP" annotation on RoBERTa, as it's the most
  impactful single lesson (NSP was actively harmful)

VISUAL DETAILS:
- Zoom Blue (#2D8CFF) for all model nodes
- Soft Orange (#FF9F43) for the single highlighted lesson
- White/ice blue (#FAFCFF) background
- Clean connecting lines (not arrows — this is a family tree)
- Each node: rounded rectangle with model name prominent
- Timeline bar at bottom for temporal orientation
- Sans-serif labels in charcoal (#1A1A2E)
```

## Review Checklist

- [ ] BERT as root node with clear branching to successors
- [ ] RoBERTa: training recipe fix (remove NSP, dynamic masking)
- [ ] DeBERTa: architectural fix (disentangled attention)
- [ ] Sentence-BERT: objective/application fix (contrastive for embeddings)
- [ ] BGE/E5/GTE: modern production continuation
- [ ] Timeline bar providing temporal orientation
- [ ] "What stayed constant" vs "What changed" annotations
- [ ] Orange accent on ONE key lesson (suggest: "Remove NSP")
- [ ] Overall message: same core architecture, incremental improvements
