# Project 1 Report: Train a MiniGPT from Scratch

**Author:**  
**Date:**

---

## 1. Architecture

- Model configuration (layers, heads, d_model, context length, total parameters)
- Positional encoding choice and justification
- Any deviations from the default config and why

## 2. Tokenizer Analysis

- Vocabulary size and bytes-per-token
- Top-20 most frequent tokens
- At least one documented failure case (numeric splitting, rare word fragmentation, or multilingual inefficiency)
- If you tried multiple vocab sizes: bits-per-byte comparison

## 3. Training

- Final training loss and validation loss
- Loss curve (include figure)
- Learning rate schedule (include figure or annotate on loss curve)
- Did you encounter any of these? If so, how did you diagnose and fix them?
  - NaN loss
  - Loss spike
  - Loss plateau
  - Loss near zero (silent shifted-target bug)
  - Mode collapse (repetitive generation)

## 4. Checkpoint and Resume

- Show that a resumed run's loss curve matches the uninterrupted baseline
- What state did you save? (model, optimizer, scheduler, step, config, RNG?)

## 5. Generation

- At least 3 prompts × 3 temperatures
- Observations: how does temperature affect output quality?
- Include both good and bad examples

## 6. Ablation Experiment

- What did you compare? (e.g., depth vs width, vocab size, PE type, LR schedule)
- Controlled variables (what stayed the same)
- Results (loss curves or final metrics)
- Interpretation: what does the comparison tell you?

## 7. Reflection

- What would you change with 10× compute budget?
- What was the hardest bug to find? How did you find it?
- What concept from Chapters 1-5 was most useful during this project?
