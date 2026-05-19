# Figure 4.5: Pre-train + Fine-tune Paradigm

**Filename**: `pretrain_finetune.png`
**LaTeX label**: `fig:pretrain-finetune`
**Caption**: The pre-train + fine-tune paradigm: one pretrained BERT body serves multiple tasks by swapping lightweight task heads.

## Prompt

```
Draw the pre-train + fine-tune paradigm for a graduate-level machine learning
textbook. Use the course's blue-white visual system. Landscape orientation,
polished editorial style.

LAYOUT:
Two-phase diagram: LEFT = pretraining, RIGHT = fine-tuning with multiple tasks.

LEFT PHASE — PRETRAINING:
- Title: "Phase 1: Pre-train (once, expensive)"
- Large blue rounded rectangle: "BERT Encoder (12 layers)"
- Input at bottom: "Massive unlabeled text (Books, Wikipedia, Web)"
- On top: "MLM Head" box — predicting [MASK] tokens
- Arrow showing loss signal flowing back
- Time/cost annotation: "expensive, done once"

CENTER — TRANSITION:
- Large arrow from left to right
- Label: "Transfer pretrained weights"
- Visual: the blue BERT body stays the same color/shape

RIGHT PHASE — FINE-TUNING (multiple tasks):
- Title: "Phase 2: Fine-tune (per task, cheap)"
- The SAME blue BERT body repeated 3 times (or shown once with 3 branching heads)
- Three task heads in different configurations:

  Task A — SENTIMENT CLASSIFICATION:
  - Small orange (#FF9F43) box on top of [CLS] representation
  - Label: "Linear → 2 classes"
  - Dataset note: "labeled sentiment examples"

  Task B — NAMED ENTITY RECOGNITION:
  - Small orange boxes on top of EACH token representation
  - Label: "Linear → per-token labels"
  - Dataset note: "labeled token spans"

  Task C — QUESTION ANSWERING:
  - Two small orange boxes (start predictor + end predictor)
  - Label: "Linear → start/end span"
  - Dataset note: "labeled answer spans"

KEY ANNOTATIONS:
- The BERT body in all three fine-tuned versions is the SAME blue color
  (same pretrained initialization)
- The task heads are orange — showing they are the ONLY new parameters
- Annotation: "Same body, different heads"
- Bottom note: "Fine-tuning: cheaper, repeated per task"

VISUAL DETAILS:
- Zoom Blue (#2D8CFF) for BERT encoder body (consistent across all instances)
- Soft Orange (#FF9F43) for task-specific heads — the ONLY orange elements
- White/ice blue (#FAFCFF) background
- Dashed line or bracket showing "shared pretrained weights"
- Sans-serif labels in charcoal (#1A1A2E)
- Cost contrast emphasized: "expensive once" vs "cheaper per task"
```

## Review Checklist

- [ ] Two phases clearly separated: pretrain (left) and fine-tune (right)
- [ ] BERT body is the same blue block in both phases
- [ ] Three different task heads shown (classification, NER, QA)
- [ ] Task heads are orange — only new parameters per task
- [ ] Cost contrast visible: expensive pretrain once vs cheaper fine-tune per task
- [ ] "Same body, different heads" principle clear
- [ ] [CLS] used for classification, all tokens for NER, start/end for QA
- [ ] Transfer arrow connecting the two phases
