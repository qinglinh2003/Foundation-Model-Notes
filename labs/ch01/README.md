# Lab 1: Why Context and Gating Matter

## Overview

This lab verifies the core claims of Chapter 1 through five experiments:

| Experiment | Chapter sections | Core question |
|---|---|---|
| 0. Static Embedding Polysemy Probe | §1.2–1.3 | Does a static word vector collapse multiple word senses? |
| 1. Gradient Pathology | §1.4.1–1.4.3 | Do vanilla RNNs suffer from gradient instability that LSTM/GRU fix? |
| 2. Long-Range Dependency Probe | §1.4.1, §1.4.3 | Can RNN/LSTM/GRU learn dependencies at increasing distances? |
| 3. LSTM vs GRU Efficiency | §1.4.4 | Does GRU achieve similar performance with less compute? |
| 4. Seq2Seq Bottleneck + Attention | §1.5–1.8 | Does a fixed context vector fail on long inputs? Does attention fix it? |

**Schedule:** Experiments 0–3 on Day 2 (~5–6h). Experiment 4 + report on Day 3 (~4–5h).

**Important:** This is a **starter-code lab**. Use an AI coding assistant to generate implementations from the specs below. Your time should go into running experiments, interpreting results, and writing the report—not fighting dataloaders or device placement. The code must be yours to understand and modify, but building it is not the bottleneck.

---

## Experiment 0: Static Embedding Polysemy Probe

### What you need
- Pre-trained GloVe vectors: `glove.6B.100d.txt` ([download](https://nlp.stanford.edu/projects/glove/))
- A script that loads the vectors and computes cosine similarities

### Steps
1. Load `glove.6B.100d.txt` into a dictionary: `word -> numpy array`.
2. Pick 3 polysemous words: `bank`, `cell`, `spring`.
3. For each, find the top-10 nearest neighbors by cosine similarity.
4. Annotate each neighbor: which sense does it belong to?
   - `bank`: financial (money, credit, loan) vs. geographic (river, shore, stream)
   - `cell`: biology (membrane, organism) vs. prison (jail, inmate) vs. phone (mobile, battery)
   - `spring`: season (summer, autumn) vs. water (fountain, creek) vs. mechanical (coil, bounce)
5. Run the analogy test: find the closest word to `king - man + woman`. Is it `queen`?

### What to look for
Do nearest neighbors mix senses? If `bank` neighbors are mostly financial, try other polysemous words or a different embedding. The key question is whether *any* single vector can cleanly represent a word with multiple distinct meanings.

### Deliverable
A table: for each polysemous word, top-10 neighbors with sense annotations.

---

## Experiments 1–3: Character-Level Language Model

### Baseline Specification

Build a character-level language model that supports **RNN, LSTM, and GRU** (switchable via config/flag). Use the same codebase for all three.

#### Data
- Source: Tiny Shakespeare (~1.1 MB) or any plain-text file, 1–5 MB
- Split: 90% train / 10% validation, split by contiguous chunks (not random)
- Preprocessing: character-level vocabulary (no tokenizer)

#### Model
- Architectures: vanilla RNN (`nn.RNN`), LSTM (`nn.LSTM`), GRU (`nn.GRU`)
- Layers: 1
- Hidden size: 256
- Input: learned character embedding (dim 64)
- Output: linear projection to vocab size, cross-entropy loss

#### Training
- Optimizer: Adam, lr=1e-3
- Batch size: 64
- Sequence length (truncated BPTT): 128
- Gradient clipping: max norm 5.0
- Epochs: 10–20 (until validation loss plateaus)
- **Critical:** detach hidden state between BPTT segments:
  ```python
  hidden = tuple(x.detach() for x in hidden)  # LSTM
  hidden = hidden.detach()  # RNN, GRU
  ```

#### Logging
- Record at every step: loss, gradient norm (before clipping)
- Save to CSV, TensorBoard, or W&B

#### Expected Performance
- Validation PPL: roughly 3–8 (character-level)
- Training: 5–30 min on a single GPU
- RNN may be unstable at longer sequence lengths

### Sanity Checks (do these before any experiment)

1. **Hidden-state detach:** GPU memory and step time should remain constant across batches. If either grows, the computation graph is leaking.

2. **Loss alignment:** Feed `"hello"`. The loss at position 0 should correspond to predicting `'e'` from `'h'`, position 1 should predict `'l'` from `'e'`, etc.

3. **Gradient logging:** Plot gradient norms for a few hundred steps. Values should not be all zeros or NaN. Typical range: 0.1–10 before clipping.

---

## Experiment 1: Gradient Pathology

### Normal run
Train RNN, LSTM, GRU with identical hyperparameters (as specified above). Record gradient norms.

**Plot:** gradient norm vs. training step, three curves on one axes.

### Stress run
Change config:
- Sequence length: 256
- Learning rate: 3e-3
- Gradient clipping: **disabled**
- Run for 500 steps only

Record for each model:
- Did loss become NaN?
- Did gradient norm spike above 1000?
- Was training stable?

**If RNN does not explode:** increase learning rate or sequence length until you find its breaking point. The goal is to characterize *where* the stability boundary lies, not just to confirm a predetermined result. If LSTM also becomes unstable, note the conditions and compare thresholds.

**Deliverable:** Gradient norm plot (normal run) + one table summarizing stress run outcomes.

---

## Experiment 2: Long-Range Dependency Probe

### Synthetic Delayed-Memory Task

Generate sequences of the form:

```
[MARKER] a [NOISE x N] [QUERY] -> a
```

Where:
- Vocabulary: 10 random tokens + special tokens `[MARKER]`, `[QUERY]`, `[PAD]`
- `a` is a random token from the vocabulary (the "signal")
- Noise tokens are random (not `a`, not special tokens)
- N (dependency distance) varies: **8, 32, 128, 256**

#### Model
- Same RNN/LSTM/GRU architecture as the char LM, but:
  - Input: integer token IDs → embedding (dim 32)
  - Output: predict the signal class after `[QUERY]` (single classification; class IDs 0--9)
  - Hidden size: 128
  - Train with cross-entropy on the query position only

#### Training
- Generate 10,000 training sequences, 1,000 test sequences per distance
- **Train separate models for each distance** (isolates dependency length from mixed-difficulty effects)
- Train until convergence or 50 epochs
- Record test accuracy for each model × distance

**Deliverable:** One figure: accuracy (y-axis) vs. dependency distance (x-axis), three curves (RNN, LSTM, GRU).

### What to look for
- At what distance does each model's accuracy start to degrade? Is there a sharp cliff or a gradual decline?
- If results do not match predictions (e.g., RNN succeeds at N=128), investigate: is the hidden size large enough to memorize? Is the noise vocabulary too small? Adjust and rerun.
- **Optional extension:** train on mixed distances and test generalization to N=512 (never seen during training).

---

## Experiment 3: LSTM vs GRU Efficiency

Collect from your Experiment 1 and 2 runs:

| Metric | LSTM | GRU | RNN |
|---|---|---|---|
| Parameter count | | | |
| Training speed (tokens/sec) | | | |
| Final validation PPL (char LM) | | | |
| Accuracy at N=128 (delayed memory) | | | |

### How to compute parameter count
```python
sum(p.numel() for p in model.parameters())
```

GRU should have ~25% fewer parameters than LSTM at the same hidden size (3 gates vs. 4 gate-like operations).

### Optional: parameter-matched comparison
Train GRU with hidden_size=295 (so total params ≈ LSTM with hidden_size=256). Compare convergence speed and final metric.

### Quick generation check
Generate 200 characters from trained LSTM and GRU at temperature=1.0. Qualitatively: is one noticeably better?

**Deliverable:** One comparison table. One sentence on whether "similar results with less overhead" holds on these tasks.

---

## Experiment 4: Seq2Seq Bottleneck and Attention

### Task: Sequence Reversal

Input: `a b c d` → Output: `d c b a`

This task maximally exposes the bottleneck: the first output token depends on the *last* input token, so all source information must pass through the context vector.

### Data
- Vocabulary: 26 lowercase letters
- Input lengths: **10, 30, 50, 100**
- Generate 10,000 training pairs and 1,000 test pairs per length
- No padding needed if you process lengths separately; otherwise pad and mask

### Models

#### Model A: Seq2Seq without attention
- Encoder: 1-layer LSTM, hidden_size=128
- Context: final encoder hidden state only
- Decoder: 1-layer LSTM, initialized with context
- Teacher forcing during training

```
encoder output = final hidden state
decoder initial state = encoder final state
decoder generates one token at a time
```

#### Model B: Seq2Seq with Bahdanau attention
- Same encoder and decoder as Model A
- Add attention: at each decoder step, compute alignment scores over all encoder hidden states, take weighted sum as context vector, concatenate with decoder input

```python
# Bahdanau attention (additive)
score = V @ tanh(W1 @ decoder_hidden + W2 @ encoder_states)
alpha = softmax(score)
context = alpha @ encoder_states
```

### Training
- Optimizer: Adam, lr=1e-3
- Batch size: 64
- Train until convergence or 100 epochs per length
- Metric: exact sequence match accuracy on test set

### Plots

1. **Accuracy vs. input length:** two curves (no attention, with attention) on one axes.
2. **Attention heatmap:** for one test example at L=30, plot the attention weight matrix $[\alpha_{t,s}]$ where t=decoder step, s=encoder position. Use `matplotlib.pyplot.imshow`.

### What to look for
- Without attention: at what length does accuracy start to collapse? Is the degradation gradual or sudden?
- With attention: does it maintain high accuracy at L=100? If not, check training budget—attention models may need more epochs to converge on longer sequences.
- Attention heatmap: does the pattern resemble an anti-diagonal? If it is noisy, the model may need more training, or the attention mechanism may have a bug. A clean anti-diagonal is a strong signal that attention learned the correct alignment.

**Deliverable:** Accuracy vs. length plot + one attention heatmap + one paragraph connecting results to §1.5 bottleneck discussion.

---

## File Structure and Starter Code

All scaffold files are provided. Sections marked `# TODO: YOUR CODE HERE`
require your implementation. Everything else (data loading, plotting, logging,
training utilities) is ready to use.

```
labs/ch01/
├── README.md                # this file
│
│   ── PROVIDED (do not modify unless noted) ──
├── data.py                  # ✅ all datasets: CharDataset, DelayedMemoryData, ReversalData
├── utils.py                 # ✅ logging, plotting, training helpers
│
│   ── IMPLEMENT TODO BLOCKS ──
├── model.py                 # 🔧 CharLM, DelayedMemoryClassifier, Seq2Seq (Encoder/Decoder/Attention)
├── exp0_polysemy.py         # 🔧 analogy function + sense annotations
├── exp1_gradient.py         # 🔧 stress test training loop
├── exp2_distance.py         # 🔧 probe training loop
├── exp3_efficiency.py       # 🔧 metric collection and comparison table
├── exp4_seq2seq.py          # 🔧 Seq2Seq training loop + interpretation
│
│   ── YOUR OUTPUT ──
├── figures/                 # save your plots here
│   ├── gradient_norm_normal.png
│   ├── gradient_norm_stress.png
│   ├── distance_probe.png
│   ├── accuracy_vs_length.png
│   └── attention_heatmap.png
├── results/                 # JSON results from exp2, exp4
└── report.md                # your experiment report
```

### What's provided vs. what you implement

| File | Provided | You implement |
|------|----------|---------------|
| `data.py` | All 3 datasets, collate functions, data loading | Nothing — fully provided |
| `utils.py` | MetricLogger, gradient norm, all 4 plot functions, CharLM train/eval/generate | Nothing — fully provided |
| `model.py` | Class structure, `__init__` signatures, forward signatures, helper methods | RNN/LSTM/GRU layer creation, hidden-state detach, attention layers, attention scoring, decoder forward step |
| `exp0_polysemy.py` | GloVe loading, nearest-neighbor search, main script | Analogy vector arithmetic, sense annotations |
| `exp1_gradient.py` | Normal training run (complete), plotting, summary | Stress test training loop (no clipping) |
| `exp2_distance.py` | Data setup, evaluation function, plotting, summary | Training loop for delayed-memory probe |
| `exp3_efficiency.py` | Parameter counting, log loading | Metric collection, comparison table |
| `exp4_seq2seq.py` | Data setup, evaluation, attention extraction, plotting | Training loop, interpretation |

### Getting started

```bash
# 1. Download data
wget https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt \
     -O tiny_shakespeare.txt

# 2. Download GloVe (for Experiment 0)
wget https://nlp.stanford.edu/data/glove.6B.zip && unzip glove.6B.zip

# 3. Fill in the TODO blocks in model.py first — all experiments depend on it

# 4. Run experiments in order
python exp0_polysemy.py --glove_path glove.6B.100d.txt
python exp1_gradient.py --data_path tiny_shakespeare.txt
python exp2_distance.py
python exp3_efficiency.py
python exp4_seq2seq.py
```

## Experiment Report

Write a 500–700 word report structured as:

**Question:** Which architectural change most directly addressed which failure mode?

**Evidence:** Summarize your key quantitative results from all five experiments. Use numbers, not vague impressions.

**Diagnosis:** Connect each result to the theory from Chapter 1:
- Why did RNN gradients behave differently from LSTM/GRU? (→ gradient highway, §1.4.3)
- Why did RNN fail at long dependency distances? (→ vanishing gradient, §1.4.1)
- Why did GRU approach LSTM performance with fewer parameters? (→ merged gates, §1.4.4)
- Why did the no-attention Seq2Seq fail on long inputs? (→ bottleneck, §1.5)
- Why did the attention heatmap show an anti-diagonal? (→ alignment, §1.6)

**Trade-offs:** What did GRU save compared with LSTM? What did attention fix that gating alone could not?

**Next step:** What would you investigate with one more day?

## Evaluation Rubric

| Weight | Criteria |
|---|---|
| 15% | Setup: models train correctly, sanity checks pass |
| 20% | Experiments 1–2: gradient and dependency results are measured carefully and used to analyze RNN limitations vs. LSTM/GRU |
| 15% | Experiment 3: efficiency comparison with quantitative data and honest interpretation |
| 20% | Experiment 4: bottleneck demonstrated; attention heatmap correctly interpreted |
| 20% | Report: causal reasoning connecting experimental results to chapter theory |
| 10% | Reproducibility: code, configs, and instructions sufficient for replication |
