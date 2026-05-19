# Lab 4: Same Block, Different Capability

## Thesis

A bidirectional encoder and a causal decoder, built from the same
Transformer block, excel at fundamentally different tasks — and this
difference is measurable, not just theoretical.

Lab 2 removed ingredients from a working model. Lab 3 built one up
from scratch. Lab 4 uses a different method: **controlled comparison**.
Same data, same probe, same budget — only variable is the encoder type.

## The tasks

Lab 4 uses two task granularities to make the comparison precise:

- SST-2 sentence classification for Exp 1 and Exp 3.
- CoNLL-2003 token-level NER for Exp 2.

Exp 0 is a polysemy cosine sanity check. Exp 4 contrasts free-form
generation with mask filling.

## Models

- **DistilBERT** (`distilbert-base-uncased`, ~66M params)
- **DistilGPT2** (`distilgpt2`, ~82M params)
- Parameter counts are close enough for fair comparison.

## Experiments at a glance

| #         | What                                | Key evidence |
|-----------|-------------------------------------|-------------|
| 0         | Polysemy sanity check               | Static cosine ≈ 1.0 across senses; BERT cosine drops |
| 1         | Frozen SST-2 probe                  | BERT ≈ GPT on sentence-level classification |
| 2         | NER token classification (CENTERPIECE) | BERT >> GPT when each token needs right context |
| 3         | Fine-tune SST-2 comparison          | Fine-tuning preserves SST-2 parity |
| 4         | Generation flip                     | GPT generates fluently; BERT can only fill [MASK] |

## Per-experiment specs

### Experiment 0 — Polysemy Sanity Check

**Corresponds to:** Ch.4 Sec.4.2, closes loop from Lab 1 Exp 0.

**Goal:** Show that BERT's contextual embeddings distinguish word senses
that static embeddings cannot.

**Setup:**
- Words: "bank" (financial/river), "bat" (sports/animal), "light" (illumination/weight/mood)
- For each word, extract embeddings from DistilBERT in different-sense sentences
- Compare cosine similarity: static (token embedding layer only) vs contextual (last hidden layer)

**Deliverables:**
- Cosine similarity table: static vs contextual for each word pair
- One paragraph connecting to Lab 1 Exp 0

### Experiment 1 — Frozen SST-2 Probe

**Corresponds to:** Ch.4 Sec.4.2, 4.6.

**Goal:** Measure how much task-relevant information different encoders
capture, using a frozen-encoder + linear-probe protocol.

**Setup:**
- Dataset: SST-2, 5000 train / 872 val
- Three encoders (all frozen):
  - A: Static embeddings (mean of token embeddings, no transformer layers)
  - B: DistilGPT2 last-token hidden state
  - C: DistilBERT [CLS] hidden state
- Probe: single linear layer → 2 classes, trained for 10 epochs

**Deliverables:**
- Bar chart: accuracy for A, B, C
- Interpretation of why BERT and GPT are nearly tied on sentence-level
  classification: GPT's last token has already seen the whole sentence.

### Experiment 2 — NER Token Classification (CENTERPIECE)

**Corresponds to:** Ch.4 Sec.4.2, 4.6.

**Goal:** Show where bidirectional context creates a real advantage:
token-level understanding, where each token representation may need
words to its right.

**Setup:**
- Dataset: CoNLL-2003 NER subset
- Models: DistilBERT vs DistilGPT2
- Task: token-level entity tagging
- Metric: entity-level F1

**Deliverables:**
- Bar chart: entity F1 for BERT vs GPT
- Per-label breakdown, with special attention to B- labels where entity
  boundaries require right context

### Experiment 3 — Fine-tune SST-2 Comparison

**Corresponds to:** Ch.4 Sec.4.5 (pre-train + fine-tune).

**Goal:** Check whether full fine-tuning changes the sentence-level
result from Exp 1.

**Setup:**
- Full fine-tune DistilBERT (3 epochs, lr=2e-5)
- Full fine-tune DistilGPT2 (3 epochs, lr=2e-5, use last-token pooling)
- Same SST-2 train/val split

**Deliverables:**
- Bar chart: fine-tuned accuracy for both models
- Compare gap vs Exp 1 frozen gap and Exp 2 token-level gap

### Experiment 4 — Generation Flip

**Corresponds to:** Ch.4 Sec.4.6 (why BERT lost the frontier role).

**Goal:** Show that GPT can generate while BERT cannot — the other
half of the capability tradeoff.

**Setup:**
- GPT: autoregressive generation from prompts (50 tokens, temperature=0.8)
- BERT: [MASK] filling (top-5 predictions per mask position)
- BERT: iterative mask filling attempt (awkward multi-step "generation")
- No training required

**Deliverables:**
- Side-by-side outputs
- Qualitative observation: GPT is fluent; BERT is limited to single-token fill

## File structure

```
labs/ch04/
├── README.md              # This file
├── data.py                # SST-2 loader + polysemy examples
├── utils.py               # Probe, training, evaluation, plotting
├── exp0_polysemy.py       # Exp 0: static vs contextual polysemy
├── exp1_frozen_probe.py   # Exp 1: frozen SST-2 probe
├── exp2_ner_probe.py      # Exp 2: NER token classification
├── exp3_finetune.py       # Exp 3: fine-tune SST-2 comparison
├── exp4_generation.py     # Exp 4: generation flip
├── logs/                  # Training CSV logs (auto-created)
├── plots/                 # Experiment plots (auto-created)
└── answers/               # Results and report (after running)
```

## Dependencies

```bash
pip install transformers datasets torch
```

## Running

```bash
cd labs/ch04
python exp0_polysemy.py
python exp1_frozen_probe.py
python exp2_ner_probe.py
python exp3_finetune.py
python exp4_generation.py
```

## Rubric

| Component | Weight | Criteria |
|-----------|--------|----------|
| Exp 0: Polysemy | 10% | Cosine table shows static ≈ 1.0, contextual < 1.0 across senses |
| Exp 1: SST-2 frozen probe | 20% | BERT ≈ GPT result is reported and explained |
| Exp 2: NER token probe | 25% | BERT's entity-F1 advantage is reported and tied to bidirectional context |
| Exp 3: SST-2 fine-tune | 15% | Fine-tune result is compared with Exp 1 and Exp 2 |
| Exp 4: Generation | 10% | Side-by-side outputs; architectural explanation of why BERT can't generate |
| Report | 25% | Answers the report question with evidence from all experiments |

## Report question

> Chapter 4 claims that BERT won representations while GPT won generation.
> Does your Lab 4 data support this claim? Specifically: (a) why does
> SST-2 show little gap between BERT and GPT? (b) why does token-level
> NER show a large gap? (c) does fine-tuning change the sentence-level
> conclusion? (d) can BERT generate coherent text? What architectural
> property prevents it?

## Common pitfalls

1. **GPT padding**: DistilGPT2 has no pad token by default. Set
   `tokenizer.pad_token = tokenizer.eos_token` before tokenizing.

2. **GPT pooling**: Use last non-pad token, not first token. GPT's causal
   attention means the last token has the most context.

3. **Frozen vs fine-tune**: Make sure encoder parameters are truly frozen
   in Exp 1 (no gradients through the model). In Exp 3, both model and
   head parameters must be updated.

4. **BERT [CLS] vs mean pooling**: Exp 1 uses [CLS]. This is BERT's
   designed sentence representation. Mean pooling is an alternative
   (explored by Sentence-BERT) but not the default.
