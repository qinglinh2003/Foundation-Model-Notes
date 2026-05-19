# Lab 5: Training Pipeline Diagnostics — Report

## Thesis
Training logs can lie. A correct architecture with a broken pipeline produces
numbers that look reasonable but mean the wrong thing.

---

## Experiment 0: Tokenizer and Vocabulary Size Sweep

**Question:** Can we compare raw cross-entropy loss across tokenizers?

**Setup:** Same corpus (Tiny Shakespeare, 1.1MB), same model architecture,
same training budget (1500 steps). Four tokenizers: char (V=65), BPE V=256,
BPE V=1000, BPE V=4000.

**Results:**

| Config   | Vocab | Bytes/Token | Raw CE Loss | Bits-per-Byte |
|----------|------:|------------:|------------:|--------------:|
| char     |    65 |        1.00 |      2.1403 |        3.0877 |
| BPE-256  |   256 |        1.96 |      3.6173 |        2.6640 |
| BPE-1000 |  1000 |        2.79 |      4.3238 |        2.2326 |
| BPE-4000 |  4000 |        3.70 |      5.4542 |        2.1249 |

**Key Insight: Raw loss and bits-per-byte rank in OPPOSITE order.**

A student looking only at raw CE loss would conclude char-level (2.14) is best
and BPE-4000 (5.45) is worst. But normalized to bits-per-byte, BPE-4000 (2.12)
is best and char-level (3.09) is worst.

**Why this happens:** Raw CE loss is per-token, but tokens have different
information content. A char-level token carries ~1 byte of information; a
BPE-4000 token carries ~3.7 bytes. Comparing per-token loss across different
tokenizers is like comparing fuel economy between a car (miles/gallon) and a
truck (miles/gallon) without accounting for payload weight.

**Sample quality confirms bits-per-byte:** BPE-4000 generates coherent phrases
("First Citizen: Master, tell them the body and deserve...") while char-level
generates gibberish ("Now nut the so ham a mart where jup auth").

---

## Experiment 1: Learning-Rate Schedule Ablation (Centerpiece)

**Question:** If loss is decreasing, does that mean the schedule is good enough?

**Setup:** Same model, same char-level tokenizer, same 2000 steps.
Three schedules:
1. too_high: lr=0.1, no warmup, no clipping
2. no_warmup: lr=1e-3, constant, with clipping
3. warmup_cosine: lr=1e-3, 200-step warmup + cosine decay

**Results:**

| Schedule      | Final Val Loss | Sample Quality |
|---------------|---------------:|---------------|
| too_high      |         3.3376 | Near-random character soup |
| no_warmup     |         1.5801 | Coherent but some errors |
| warmup_cosine |         1.6534 | Coherent, similar to no_warmup |

**Key Insight 1: LR 100× too high doesn't NaN — it just silently fails.**

With lr=0.1, loss drops from 4.19 to ~3.3 and plateaus. A naive student might
think "it's learning, just slowly." But the generated text is random character
soup. The model found a low-entropy attractor (predicting common characters)
without learning any structure.

**Key Insight 2: For tiny models with short training, warmup+cosine ≈ constant LR.**

The difference between no_warmup (1.58) and warmup_cosine (1.65) is small and
slightly favors constant LR. This is because cosine decay reduces LR too
aggressively in short runs (2000 steps). The warmup+cosine advantage emerges
at longer training horizons where the "fine-tuning" phase at low LR matters.

**Lesson:** Schedule choice is a function of training budget. Warmup+cosine is
the standard recommendation for production training (100K+ steps), but for
tiny experiments the simpler constant schedule may suffice.

---

## Experiment 2: Checkpoint Resume Ablation

**Question:** Is saving model weights sufficient for resuming training?

**Setup:** Train to step 1000 (Phase 1), then resume to step 2000 with different
checkpoint states:
- uninterrupted: full 2000 steps, no interruption (reference)
- full_resume: restore model + optimizer + scheduler + step
- model_only: restore only model weights
- no_scheduler: restore model + optimizer, but restart scheduler from scratch

**Results:**

| Run            | Final Val Loss | Gap vs Reference |
|----------------|---------------:|-----------------:|
| uninterrupted  |         2.0287 |              0.0 |
| full_resume    |         2.1805 |           +0.152 |
| model_only     |         2.2071 |           +0.178 |
| no_scheduler   |       **1.9139** |        **-0.115** |

**Key Insight 1: model_only resume is worse than full — optimizer state matters.**

The gap between full_resume (2.18) and model_only (2.21) shows that the optimizer's
accumulated momentum and variance estimates have value. Resetting them forces the
optimizer to re-estimate gradient statistics, wasting early resume steps.

**Key Insight 2: no_scheduler "accidentally" beats the reference — the most
dangerous kind of bug.**

Resetting the scheduler gives the model a second warmup phase with fresh high LR.
This effectively grants extra training budget at high learning rate, which for this
short run actually helps. A student might conclude "resetting scheduler is good!"
But this is a coincidence of the short training budget: the reset scheduler will do
warmup + full cosine cycle in the remaining 1000 steps, giving higher average LR
than the original schedule (which was already in its decay phase by step 1000).

**In production this would be a bug:** the model gets an unplanned LR restart,
potentially undoing fine-grained convergence from the first phase. The lesson is:
bugs can improve metrics in ways that don't generalize.

**Key Insight 3: Even full_resume doesn't perfectly match uninterrupted.**

The 0.15 gap between full_resume (2.18) and uninterrupted (2.03) comes from
Phase 1 using a different cosine schedule (1000-step cosine vs 2000-step cosine).
Phase 1's cosine decayed to near-zero by step 1000, so it learned less in later
steps. A true "identical resume" would require using the same total schedule.

---

## Report Questions

**(a) In Exp 0, which metric told the truth?**

Bits-per-byte is the comparable metric. Raw per-token CE loss is misleading
because it doesn't account for token granularity. A model that predicts one
coarse-grained token is solving an easier problem per token but harder per byte.

**(b) In Exp 1, the too_high run showed loss decreasing. Why was it still a failure?**

Because loss decreased from 4.19 to 3.3 by converging to a trivial solution:
predicting common characters without learning structure. The generated samples
confirm this — they're random character soup. A decreasing loss curve is necessary
but not sufficient evidence of learning.

**(c) In Exp 2, the no_scheduler run beat the reference. Is this a good thing?**

No. It's a coincidence of short training. The scheduler reset gave an accidental
LR boost. In longer training, this would waste convergence from Phase 1. The
lesson: metrics can improve for wrong reasons. Always check whether an "improvement"
is robust across training budgets.
