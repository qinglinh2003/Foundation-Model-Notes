# Lab 3: What Holds a GPT Together

## Thesis

A decoder-only Transformer becomes useful only when three things line up:
the objective is correctly shifted, the residual/pre-norm stack makes depth
trainable, and KV cache makes autoregressive inference practical. Lab 3
builds a tiny GPT from a provided scaffold, finds a deliberate objective
bug, then measures what each architectural feature contributes to
correctness, training stability, and inference speed.

Lab 2 removed ingredients from a working model. Lab 3 inverts the method:
start minimal, add structure, observe what each addition fixes.

## The task

Character-level language modeling on Tiny Shakespeare — the same dataset
as Lab 1. This enables direct cross-lab comparison: "Lab 1 used an LSTM
on this data; Lab 3 uses a decoder-only Transformer."

## Experiments at a glance

| #         | What                                | Trainings | Expected headline |
|-----------|-------------------------------------|-----------|-------------------|
| 0         | Shifted-label bug hunt              | 2         | Buggy model has low loss but incoherent generation; fix raises loss but enables real learning |
| 1         | Residual + norm ablation (CENTER)   | 3         | No-residual degrades or destabilizes; post-norm spikes; pre-norm stable |
| 2         | Positional encoding comparison      | 3         | No PE weakens order modeling; learned PE / RoPE restore explicit position |
| 3         | KV cache profiling                  | 0 (reuse) | No-cache: linear time growth; cache: flat |
| Cross-lab | LSTM vs Transformer                 | 0 (reuse) | Qualitative comparison of training dynamics and generation |

Core compute estimate: ~2-3 GPU-hours for all training runs + profiling.
Each individual run is short (5-15 minutes on a single consumer GPU).

## Per-experiment specs

### Experiment 0 — Shifted-Label Bug Hunt

**Corresponds to:** Ch.3 Sec.3.2 (shifted cross-entropy loss).

**Goal:** Diagnose a deliberate off-by-one bug in the loss computation.

**Setup:**

The experiment script compares a deliberately buggy local no-shift loss against
the correct `shifted_ce_loss` implementation in `model.py`:

```python
# buggy: predicts the current token
F.cross_entropy(logits.reshape(-1, V), input_ids.reshape(-1))

# correct: logits[:, t] predicts input_ids[:, t+1]
F.cross_entropy(
    logits[:, :-1].reshape(-1, V),
    input_ids[:, 1:].reshape(-1),
)
```

The buggy version makes the model "predict" the current token instead of
the next token.

- Train buggy model for 500 steps. Note suspiciously low loss; in our pilot
  run it was near zero.
- Generate 200 characters. Output will be incoherent (copying, not predicting).
- Train the fixed model with `shifted_ce_loss`.
- Loss will be higher because the model is solving the real next-token task;
  in our pilot run it was around 2--3 after 500 steps.

**Deliverables:**

- Side-by-side loss curves: buggy vs fixed.
- 200-char generated samples from each.
- One paragraph explaining why "low loss + bad generation" is the diagnostic
  signature of a label alignment bug.

### Experiment 1 — Residual Stream and Normalization (CENTERPIECE)

**Corresponds to:** Ch.3 Sec.3.3 (residual stream) and Sec.3.8 (failure modes).

**Goal:** Demonstrate that the residual stream is the backbone of a
trainable deep Transformer, and that normalization placement matters.

**Setup:**

Three 8-layer models, identical except for architecture:

| Config | Residual? | Norm placement | Expected behavior |
|--------|-----------|----------------|-------------------|
| A      | No        | Pre-norm       | Degraded, unstable, or much slower learning |
| B      | Yes       | Post-norm      | Trains but unstable; occasional loss spikes |
| C      | Yes       | Pre-norm       | Stable training; smooth gradient norms |

Shared hyperparameters:

- d_model=128, 4 heads, FFN inner=512
- Batch 64, seq_len=256
- AdamW, lr=3e-4, weight decay 0.01
- 3000 training steps
- Record: loss and gradient norm at every step

**Deliverables:**

- `grad_norm_comparison.png`: gradient norm vs step, three curves overlaid.
  This is the centerpiece figure of Lab 3.
- `loss_comparison.png`: training loss vs step, three curves.
- Per-config: final validation loss and 200-char generated sample.
- Explicit comparison with Lab 1's RNN vs LSTM gradient norm plot.

**Diagnosis prompt:** The residual stream does for Transformer depth
what cell state does for LSTM time. Where does this analogy hold,
and where does it break?

### Experiment 2 — Positional Encoding

**Corresponds to:** Ch.3 Sec.3.4 (position in decoder-only models).

**Goal:** Verify that without explicit positional information, a decoder-only
Transformer has an incomplete order signal.

**Setup:**

Three 4-layer pre-norm models with residual connections:

| Config | PE type        |
|--------|----------------|
| A      | None           |
| B      | Learned absolute (GPT-2 style) |
| C      | RoPE (optional, if scaffold supports it) |

Same hyperparameters as Exp 1 except 4 layers and 2000 steps.

**Deliverables:**

- Validation loss table for all configs.
- 200-char generated samples from each.
- One sentence on whether the no-PE model's output shows weaker ordering.

**Important:** Do not force a conclusion that "RoPE is better." Short
training on a small model may not show a clear difference. RoPE's
advantage (relative position generalization) manifests at longer contexts.

### Experiment 3 — KV Cache Profiling

**Corresponds to:** Ch.3 Sec.3.6 (autoregressive inference and KV cache).

**Goal:** Visualize the cost structure of autoregressive generation with
and without KV cache.

**Setup:**

Use the pre-norm baseline from Exp 1, config C. Generate 512 tokens twice:

1. **Without KV cache:** Recompute all attention from scratch at every step.
   Record wall-clock time for each generated token.
2. **With KV cache:** Cache K/V from previous steps.
   Record wall-clock time for each generated token.

**Deliverables:**

- `kv_cache_profiling.png`: milliseconds per token vs token position,
  two curves. Without cache should show linear growth; with cache should
  be approximately flat.
- Total generation time for 512 tokens, both modes.
- Optional: memory usage at context lengths 256, 512, 1024, 2048
  using `torch.cuda.memory_allocated()`.

### Cross-Lab Comparison: LSTM vs Transformer

**Corresponds to:** Ch.1 -> Ch.3 narrative arc.

**Goal:** Compare Lab 1's LSTM with Lab 3's Transformer on the same task.

**Setup:**

Use pre-matched configurations:

| | LSTM (Lab 1) | Transformer (Lab 3) |
|---|---|---|
| Layers | 2 | 4 |
| Hidden / d_model | 512 | 256 |
| Approx params | ~5M | ~5M |

Both trained on Tiny Shakespeare with similar total training steps.

**Deliverables:**

- Comparison table: validation loss, tokens/sec, parameter count.
- 200-char generated samples from each.
- One paragraph on qualitative differences.

## Sanity checks

Before trusting any training run, verify:

```bash
python verify.py
```

1. Logits shape is `[B, T, V]` where `V` = vocabulary size.
2. Causal mask works: modifying a future token does not change earlier outputs.
3. Weight tying: `model.embedding.weight is model.lm_head.weight` is True.
4. KV cache consistency: full-sequence and incremental cached forward passes
   produce identical logits in `model.eval()` mode with the same position offsets.

Any failure means a structural bug. Do not run experiments until all pass.

## File structure

```
labs/ch03/
|-- README.md                       this file
|-- data.py                         CharDataset for Tiny Shakespeare (provided)
|-- model.py                        Configurable mini GPT
|-- utils.py                        Training loop, generation, profiling, plotting
|-- verify.py                       4 sanity checks
|-- exp0_shifted_label.py           Bug hunt experiment
|-- exp1_residual_norm.py           Residual + norm ablation (CENTERPIECE)
|-- exp2_positional.py              PE comparison
|-- exp3_kv_cache.py                KV cache profiling
|-- cross_lab_comparison.py         LSTM vs Transformer
```

## What's provided

| File              | Provided                                          | Your task                                                    |
|-------------------|---------------------------------------------------|--------------------------------------------------------------|
| data.py           | CharDataset, train/val split, collate             | Read only unless changing the dataset                        |
| utils.py          | train loop, evaluate, generate, profile_generation, plot helpers | Read what each metric means                   |
| model.py          | Configurable GPT implementation                   | Read the architecture paths tested by each experiment        |
| verify.py         | All four sanity checks                            | Run before experiments                                       |
| exp*.py           | Training loop wrappers, plotting, markdown output | Run, inspect configs, interpret outputs                      |

You may use an AI coding assistant freely. The skill being trained is
not typing PyTorch but designing experiments and interpreting results.

## Experiment Report

Write a 600-800 word report structured around one question:

> What makes a decoder-only Transformer correct, trainable, and fast?

| Section      | Content |
|--------------|---------|
| Question     | What makes a decoder-only Transformer correct, trainable, and fast — and which properties come from architecture vs training objective? |
| Setup        | Model, data, hyperparameters. What was held constant across experiments. |
| Interventions| For each experiment, what was changed and why. |
| Results      | Numbers and figures. The Exp 1 gradient norm plot is the centerpiece — spend the most words here. |
| Diagnosis    | Connect each result to Ch.3 claims. The residual-stream / gradient-highway parallel with Lab 1's LSTM cell state is the linchpin. |
| Next step    | What would you investigate with one more day? |

A strong report:

- Directly compares Lab 1 gradient norm (RNN vs LSTM) with Lab 3
  gradient norm (no-residual vs pre-norm)
- Supports the "cell state ↔ residual stream" parallel with measurements
- Includes at least one surprising result and an honest uncertainty
- Connects the shifted-label bug (Exp 0) to Lab 2's mask bug as
  instances of the same pattern: "low loss does not mean correct model"

## Evaluation rubric

| Weight | Criteria |
|--------|----------|
| 10%    | Setup: model trains correctly; all four sanity checks pass. |
| 15%    | Exp 0: off-by-one bug correctly identified and diagnosed using the buggy-vs-fixed comparison. |
| 30%    | Exp 1 (CENTERPIECE): gradient norm plot shows three regimes. Diagnosis connects residual stream to gradient highway. Explicit Lab 1 comparison. |
| 15%    | Exp 2-3: PE comparison and KV cache profiling are quantitative and honestly interpreted. |
| 20%    | Report: causal reasoning connecting results to Ch.3 theory. Cross-lab comparison included. |
| 10%    | Reproducibility: code, configs, seeds documented. |

## Common pitfalls

- **Not running `verify.py` before experiments.** The most common silent
  bugs (shifted labels, broken causal mask, KV cache mismatch) are exactly
  what `verify` catches.
- **Declaring "RoPE is better" from a 2000-step run.** Short training on
  small models may not distinguish PE strategies. Report what you observed,
  not what you expected.
- **Ignoring the cross-lab comparison.** This is where the Ch.1-to-Ch.3
  narrative closes. A sentence like "the Transformer was faster" is not
  enough — explain _why_ (parallelism, GPU utilization) and whether the
  quality difference matches your expectation.
- **Reporting average ms/token instead of the curve.** Exp 3's whole point
  is the _shape_ of the time-per-token curve, not a single number.

## What's next

A later chapter examines encoder-only architectures (BERT). The same
diagnostic methodology — build, verify, ablate — transfers directly
to understanding why bidirectional attention and masked language modeling
produce different representations than causal next-token prediction.
