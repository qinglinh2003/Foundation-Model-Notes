# Figure 5.4: Training Pipeline

**Filename**: `training_pipeline.png`
**LaTeX label**: `fig:training-pipeline`
**Caption**: The training pipeline from raw text to gradient update. Each stage is a contract: tokenize, chunk into context windows, shift targets, batch, forward pass, cross-entropy loss, backward pass, clip gradients, optimizer step, scheduler step, validate periodically, checkpoint.

## Prompt

```
Draw the complete MiniGPT training pipeline as a circular/loop diagram for a
graduate-level machine learning textbook. Use the course's blue-white visual system.
Landscape orientation, polished editorial style.

THIS IS THE MOST IMPORTANT FIGURE IN CHAPTER 5. It should function as a visual
index that students reference while implementing Project 1.

LAYOUT:
A flowing pipeline diagram that shows the COMPLETE path from raw text to a trained
model. The pipeline forms a loop (since training iterates). Use a combination of
left-to-right flow for the main data path and a return loop for iteration.

MAIN DATA PATH (left to right, top row):

Stage 1: RAW TEXT
- Icon: a document/text block
- Label: "Raw Text"
- Small note: "corpus"

Stage 2: TOKENIZE
- Icon: processing block
- Label: "Tokenize (BPE)"
- Small note: "§5.2-5.3"
- Output arrow labeled "token IDs"

Stage 3: CHUNK + SHIFT
- Icon: processing block
- Label: "Chunk & Shift"
- Small note: "§5.4"
- Show a small visual: input [t0,t1,t2,t3] / target [t1,t2,t3,t4]
- Output arrow labeled "training examples"

Stage 4: BATCH
- Icon: stack of examples
- Label: "Batch (B×T)"
- Output arrow labeled "batch tensor"

COMPUTATION PATH (middle row, left to right):

Stage 5: FORWARD PASS
- Icon: neural network block (representing the GPT model)
- Label: "Forward Pass"
- Small note: "logits"

Stage 6: CROSS-ENTROPY LOSS
- Icon: loss computation node
- Label: "CE Loss"
- Small note: "§5.5"
- Show the compact formula: "-Σ log p(target)"

Stage 7: BACKWARD PASS
- Icon: gradient flow block
- Label: "Backward"
- Small note: "gradients"

UPDATE PATH (bottom row or return path):

Stage 8: CLIP GRADIENTS
- Icon: scissors/limit symbol
- Label: "Clip (norm ≤ 1.0)"

Stage 9: OPTIMIZER STEP
- Icon: AdamW block
- Label: "AdamW Step"
- Small note: "§5.6"

Stage 10: SCHEDULER STEP
- Icon: curve/schedule symbol
- Label: "LR Schedule"
- Small note: "warmup + cosine"

Stage 11: ZERO GRAD
- Icon: reset symbol
- Label: "Zero Grad"

PERIODIC BRANCHES (below the main loop):

Branch A: VALIDATE
- Dashed arrow from after forward pass
- Label: "Validate (every N steps)"
- Small note: "§5.8"

Branch B: CHECKPOINT
- Dashed arrow from after optimizer step
- Label: "Checkpoint"
- Small note: "model + optimizer + scheduler + step"
- Small note: "§5.8"

LOOP ARROW:
- A large return arrow from "Zero Grad" back to "Batch" showing iteration
- Label on the return arrow: "next batch"

VISUAL DETAILS:
- Processing blocks: rounded rectangles with blue fill (#2D8CFF), white text
- Data labels on arrows: steel gray text
- Section references (§5.x): small italic gray text below each block
- The orange accent: put it on the LOSS node — it's the central feedback signal
- Background: white (#FAFCFF) with very subtle ice-blue region panels
  grouping related stages (data prep / computation / update)
- Arrows: deep blue (#0B5CFF) for main flow, gray dashed for periodic branches
- The loop should feel like a cycle, not just a linear pipeline
- Add only FOUR small failure callouts, not one on every stage:
  - Tokenize: "wrong IDs = garbage"
  - Chunk & Shift: "no shift = silent bug"
  - Clip: "no clip = gradient spike"
  - Zero Grad: "no zero = unintended accumulation"
- Keep failure callouts short and secondary; the main stage labels must remain readable.
- The figure should be self-contained: a student implementing Project 1 can
  look at this figure and check off each stage of their code
```

## Review Checklist

- [ ] Complete pipeline from raw text to gradient update
- [ ] Loop structure visible (not just linear)
- [ ] All 11 stages present and labeled
- [ ] Section references (§5.x) link to chapter content
- [ ] Validate and Checkpoint shown as periodic branches
- [ ] Orange accent on the loss node ONLY
- [ ] Exactly four small "what goes wrong" annotations on critical stages
- [ ] Data flow arrows labeled with what flows between stages
- [ ] Clean enough to read at 50% width in PDF
- [ ] No extra colors beyond blue + white + orange + gray
