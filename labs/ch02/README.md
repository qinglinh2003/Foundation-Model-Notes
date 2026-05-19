# Lab 2: Attention Is Not All You Need

## Thesis

A vanilla Transformer block has five structural ingredients:

1. Scaled dot-product attention (with proper $\sqrt{d_k}$ scaling)
2. Causal masking (for autoregressive generation)
3. Multi-head projection
4. Positional encoding
5. Per-token feed-forward sub-layer wrapped in residual connections

Lab 2 puts a working vanilla model on a real NLP task, then removes
one structural ingredient at a time and measures the damage. The
overall lesson, named after Dong et al. (2021), is that **attention
by itself is structurally insufficient**: each of the other four
ingredients is load-bearing and Ch.2's claims about them are
measurable.

## The task

English morphological inflection, from the UniMorph dataset.

```
Input:  <PAST>    walk          ->  Output: walked
Input:  <PAST>    try           ->  Output: tried           (phonological)
Input:  <GERUND>  make          ->  Output: making          (phonological)
Input:  <PLURAL>  city          ->  Output: cities          (phonological)
Input:  <3SG>     go            ->  Output: goes
Input:  <PAST>    go            ->  Output: went            (irregular)
Input:  <PLURAL>  child         ->  Output: children        (irregular)
```

This is the same task Faruqui et al.\ (2016) tackled with an LSTM
encoder-decoder. Lab 1 you built the LSTM family. Lab 2 trains a
vanilla Transformer and pulls each module out to see what breaks.

## Experiments at a glance

| #     | Ingredient ablated         | Trainings | Expected headline |
|-------|----------------------------|-----------|-------------------|
| 0     | none (vanilla baseline)    | 1         | Overall acc > 95% on regular forms |
| 1     | decoder causal mask        | 1         | Train loss looks perfect, greedy decode collapses |
| 2     | FFN and/or residual        | 4 + diagnostic | Pure SAN collapses (rank metric); +FFN alone insufficient; +residual recovers regulars but fails irregulars |
| 3     | positional encoding        | 4         | Removing decoder PE breaks output length; removing encoder PE hurts phonological cases |
| 4     | head count + visualization | 3 + plots | Diminishing returns past h=4; visible head specialization in cross-attn |
| Stretch | sqrt(d_k); wug test; length generalization | 0 (reuse Exp 0 checkpoint) | softmax saturation; productivity probe; pos extrapolation |

Core compute estimate: ~1-2 GPU-hours for all twelve training runs +
diagnostic measurements. Each individual run is short (8-12 minutes
on a single consumer GPU).

## Per-experiment specs

### Experiment 0 -- Vanilla baseline

**Corresponds to:** Chapter 2 in full.

**Goal:** Train the unmodified encoder-decoder Transformer to
convergence. This is the ceiling for every later experiment.

**Setup:**

- Encoder-decoder Transformer, 2 enc + 2 dec layers, d_model=128,
  4 heads, FFN inner dim=512, pre-norm, sinusoidal PE.
- AdamW, lr=3e-4, weight decay 0.01.
- Batch 64, ~20 epochs on 76k filtered UniMorph pairs.
- Hybrid train/val/test split: regular lemmas split by lemma (test
  rule generalization); irregular pairs split by (lemma, tag) (test
  in-context memorization).

**Deliverables:**

- Training-loss curve.
- Per-tag x per-category accuracy table (a 3x4 grid: pure_regular /
  phonological / irregular x PAST / GERUND / 3SG / PLURAL).
- 25 qualitative samples from validation.
- Saved checkpoint, reused by Exp 4 visualization and Exp Stretch.

```bash
python exp0_baseline.py
```

### Experiment 1 -- Causal mask ablation

**Corresponds to:** Ch.2 Sec.2.3 (Masking).

**Goal:** Show that a missing decoder causal mask produces a
suspiciously low training loss and a useless inference model.

**Setup:** Train two models identically except for the
`use_causal_mask` flag.

**Deliverables:**

- Side-by-side accuracy table: vanilla vs.\ broken.
- Sample predictions showing the broken model's gibberish.
- Combined training-loss plot.

**Diagnosis prompt:** Why does the unmasked model achieve near-zero
training loss without learning anything generalizable? Connect to
Ch.2 Sec.2.3.3 (Implementation Pitfalls).

```bash
python exp1_mask.py
```

### Experiment 2 -- FFN and residual ablation (centerpiece)

**Corresponds to:** Ch.2 Sec.2.6 (Transformer Block) and the Failure
Modes box on "Self-attention is all you need" being half-right.

**Goal:** Two complementary measurements demonstrate the same point.

Part A (no training):

- Stack 24 encoder blocks for each of four configurations.
- Forward a random batch.
- Measure Dong-2021 relative residual and mean off-diagonal cosine
  similarity at every layer.
- Plot 4 curves on log-y axes.

Part B (training):

- Train the full encoder-decoder Transformer for each of
  {pure_SAN, +residual, +FFN, +both} on the inflection task.
- Report per-category accuracy.

**Expected qualitative result:**

- Part A: pure_SAN cosine -> 1.0 within 2 layers (doubly exponential
  collapse); residual alone stays low; FFN alone collapses; both
  stays low.
- Part B: pure_SAN < 10% on everything; +residual reaches ~70%
  on pure_regular but ~10% on phonological/irregular; +FFN alone
  trains very poorly because tokens are uniform; +both = vanilla.

**Deliverables:**

- `diagnostic_cosine.png`, `diagnostic_residual.png`,
  `diagnostic.csv`.
- Per-config trained accuracy tables.
- `results.md` with the synthesis.

```bash
python exp2_rank_collapse.py
```

### Experiment 3 -- Positional encoding ablation

**Corresponds to:** Ch.2 Sec.2.5 (Positional Information).

**Goal:** Verify that PE is necessary by removing it from encoder,
decoder, both. Each variant breaks a different class of inflection.

**Configurations:**

```
enc_PE  dec_PE   what breaks
------  ------   -------------------------------------------
 on      on     vanilla
 off     on     encoder cannot distinguish lemma char positions
 on      off    decoder cannot count output characters
 off     off    fully permutation-invariant Seq2Seq
```

**Deliverables:** four trained models, per-config accuracy, the same
3x4 category x tag table per config.

```bash
python exp3_positional.py
```

### Experiment 4 -- Multi-head ablation + visualization

**Corresponds to:** Ch.2 Sec.2.4 (Multi-Head Attention) and the
Failure Modes note on "more heads are not always better".

**Goal:** Train h in {1, 4, 8} with d_model held at 128. Compare
accuracy. Then visualize cross-attention from the trained h=4 model
on a handful of validation examples spanning different (tag,
category) cells.

**Deliverables:**

- Accuracy table by head count.
- Cross-attention heatmap files
  `cross_attn_<idx>_<tag>_<category>.png`, one per chosen example,
  each a 4-head grid.

**Interpretive prompt:** Look for at least one head with a near-
diagonal pattern (lemma copy), one head fixating on the TAG token
(paradigm control), and one head focusing on the lemma's final
character(s) for phonological cases.

```bash
python exp4_heads.py
```

### Experiment Stretch -- three probes that reuse Exp 0

**Corresponds to:** Ch.2 Sec.2.2.3 (sqrt(d_k) scaling), and forward
links to Ch.5 (tokenization) / Ch.19 (long context).

S1. **sqrt(d_k) scaling**: Sample random Q, K for d_k in {8, 32, 128,
512}; measure mean softmax entropy with and without the 1/sqrt(d_k)
factor. Plot.

S2. **Wug test**: Run the trained vanilla model on Berko (1958) and
extended pseudo-words. Productivity is the diagnostic: a model that
truly learned rules generalizes; a model that memorized fails.

S3. **Length generalization**: Slice val accuracy by lemma length.
Sinusoidal PE permits extrapolation; do the inflection rules
transfer to lengths the optimizer never saw?

```bash
python exp_stretch.py   # requires exp0_baseline checkpoint
```

## Sanity checks

Before trusting any training run, run

```bash
python verify.py
```

This executes four standalone tests that pin down properties of the
Transformer implementation:

1. Attention row sums equal 1.0 (correct softmax).
2. Decoder output at position t does not depend on `dec_in[t+1:]`
   (causal mask works).
3. Without positional encoding, encoder output permutes with the
   input (attention is permutation-equivariant).
4. With positional encoding, the same permutation produces a
   measurably different output (PE breaks the symmetry).

Any failure here means a structural bug; do not run the experiments
until all four pass.

## File structure

```
labs/ch02/
|-- README.md                       this file
|-- data/
|   |-- prepare_data.py             one-time filter / balance / patch script
|   |-- unimorph_eng_raw.tsv        raw UniMorph data, 10 MB
|   |-- unimorph_eng_filtered.tsv   76k balanced pairs across 4 tags
|   |-- wug_test.tsv                Berko 1958 + extensions, 44 pseudo-words
|-- data.py                         Dataset, Vocab, hybrid split
|-- model.py                        5 components + Seq2SeqTransformer
|-- utils.py                        classify_form, training/eval, rank metrics
|-- verify.py                       4 sanity checks
|-- exp0_baseline.py                vanilla training
|-- exp1_mask.py                    causal mask ablation
|-- exp2_rank_collapse.py           FFN/residual ablation (CORE)
|-- exp3_positional.py              PE ablation
|-- exp4_heads.py                   multi-head ablation + visualization
|-- exp_stretch.py                  3 stretch probes
|-- answers/                        reference outputs (mirror of student's expected outputs)
|   |-- exp0_baseline/
|   |-- exp1_mask/
|   |-- exp2_rank_collapse/
|   |-- exp3_positional/
|   |-- exp4_heads/
|   |-- exp_stretch/
|   |-- report.md                   the synthesis write-up (Core deliverable)
```

## What's provided vs.\ what you implement

| File              | Provided                                          | You implement                                                |
|-------------------|---------------------------------------------------|--------------------------------------------------------------|
| data.py           | Vocab, MorphInflectionDataset, hybrid split, Wug loader | Nothing -- fully provided                                |
| utils.py          | classify_form, MetricLogger, train/eval, rank metrics, plot helpers | Nothing -- fully provided                |
| model.py          | Encoder/Decoder assembly, Seq2SeqTransformer, FFN | The 5 core mechanisms (TODO 1-5 below)                       |
| verify.py         | All four sanity checks (read these to learn what to test) | Nothing -- but you should run it before every experiment |
| exp\*.py          | Training loop wrappers, plotting, markdown output | Nothing -- but you should read what each script measures and how |

The five TODOs in `model.py`, each tied to one Ch.2 section:

| # | What                                  | Ch.2 section |
|---|---------------------------------------|--------------|
| 1 | `ScaledDotProductAttention.forward`   | 2.2 (Scaled Dot-Product Attention) |
| 2 | `make_causal_mask`                    | 2.3.1 (Causal Mask)                |
| 3 | `MultiHeadAttention.forward` (reshape) | 2.4 (Multi-Head Attention)        |
| 4 | `SinusoidalPositionalEncoding`        | 2.5.2 (Sinusoidal Positional Encoding) |
| 5 | `TransformerBlock.forward` (pre-norm wiring + ablation flags) | 2.6 (Transformer Block) |

You may use an AI coding assistant freely. The skill being trained is
not typing PyTorch but designing experiments and interpreting them.

## Getting started

```bash
# 1. (one-time, only if you do not have the filtered TSV yet)
cd data
curl -sL https://raw.githubusercontent.com/unimorph/eng/master/eng \
    -o unimorph_eng_raw.tsv
python prepare_data.py
cd ..

# 2. Sanity check before training anything
python verify.py

# 3. Smoke test on 1 epoch to confirm the pipeline runs end-to-end
python exp0_baseline.py --epochs 1

# 4. Run the experiments in order
python exp0_baseline.py
python exp1_mask.py
python exp2_rank_collapse.py
python exp3_positional.py
python exp4_heads.py
python exp_stretch.py
```

Each `expN.py` produces an `answers/expN_*/results.md` markdown
report; the synthesis report `answers/report.md` is the Core
deliverable that ties them together.

## Experiment Report

Write a 600-800 word report following the six-section template:

| Section      | Content |
|--------------|---------|
| Question     | What did this lab set out to demonstrate? (One sentence, in your own words.) |
| Setup        | Data, model, hyperparameters in two-three sentences. |
| Interventions| For each of the five experiments, name what was removed/changed and why. |
| Results      | The headline numbers, in tables. Use the per-category accuracy grid. |
| Diagnosis    | Connect each result to the corresponding Ch.2 claim. The Exp 2 rank-collapse + accuracy-stair pair is the linchpin -- spend the most words there. |
| Next step    | If you had one more day, what would you investigate? |

A strong report includes at least one result that surprised you and an
honest acknowledgment of any experiment whose interpretation you are
uncertain about. If you caught a bug in your implementation, briefly
describe how `verify.py` (or a different sanity check) flagged it.

## Evaluation rubric

| Weight | Criteria |
|--------|----------|
| 15%    | Setup: all models train; sanity checks pass; deterministic with the same seed. |
| 25%    | Exp 2 (FFN/residual): both the diagnostic figures and the trained accuracy matrix are produced. Diagnosis explicitly links rank collapse to FFN/residual's distinct roles. |
| 20%    | Exp 1, 3, 4: ablations executed cleanly. Comparisons are quantitative, not vague. |
| 10%    | Cross-attention visualization (Exp 4) includes a written interpretation of at least one head's behavior. |
| 20%    | Synthesis report: causal reasoning connecting results to Ch.2 theory. Includes one surprise and one uncertainty. |
| 10%    | Reproducibility: code, configs, seeds documented; another student could re-run and get similar numbers. |

## Common pitfalls

- **Forgetting to call `verify.py` after editing `model.py`.** The
  most common silent bugs (mask, padding) are exactly what `verify`
  catches.
- **Reporting overall accuracy only.** Exp 2's whole point lives in
  the per-category breakdown. An "85% overall" can hide complete
  failure on irregulars.
- **Training too short.** If Exp 0 baseline lands below 90% on
  pure_regular, your training budget is too small; increase
  `--epochs`. All later experiments inherit this floor.
- **Hand-engineering tokenization.** Stay at the character level
  (already provided). Subword issues belong to Ch.5.

## What's next

Chapter 3 picks up on architectural decisions that this lab kept
fixed: depth, width, normalization placement, the choice between
encoder-decoder (Vaswani) and decoder-only (GPT). The same
ablation methodology you used here transfers directly to those
decisions.
