# Lab 4 Report: Same Block, Different Capability

## Report Question

> Chapter 4 claims that BERT won representations while GPT won generation.
> Does your Lab 4 data support this claim? Where exactly does the
> bidirectional advantage appear, and where does it not?

## Answer

### The Surprise: SST-2 Shows No Gap

The frozen-probe experiment (Exp 1) on SST-2 sentiment classification produced an unexpected result:

| Encoder | SST-2 Accuracy |
|---------|---------------|
| Static embeddings (no context) | 70.4% |
| DistilGPT2 (causal context) | 81.3% |
| DistilBERT (bidirectional context) | 81.1% |

BERT and GPT are essentially tied on sentence-level classification. Fine-tuning (Exp 3) confirms: DistilBERT 87.0% vs DistilGPT2 87.4% — still no meaningful gap.

This initially seems to contradict "BERT is better for understanding." But it doesn't — it reveals that the claim needs qualification.

### The Key Finding: NER Reveals the Real Gap

Experiment 2 (NER token classification on CoNLL-2003) shows where the bidirectional advantage actually lives:

| Task type | DistilBERT | DistilGPT2 | Gap |
|-----------|-----------|-----------|-----|
| Sentence-level (SST-2) | 81.1% | 81.3% | ~0 |
| **Token-level (NER F1)** | **90.3%** | **68.5%** | **+21.8 pp** |

The gap is **21.8 percentage points** on entity F1 — a crushing difference. And it appears specifically on entity boundary detection (B- labels), where GPT's causal mask prevents tokens from seeing the words that follow them:

| Label | DistilBERT F1 | DistilGPT2 F1 | Gap |
|-------|:---:|:---:|:---:|
| B-ORG | 90.6% | 46.0% | +44.6 |
| B-MISC | 89.0% | 50.0% | +39.0 |
| B-PER | 99.0% | 78.0% | +21.0 |

GPT cannot recognize "New" as the start of "New York Times" because it hasn't seen "York Times" yet.

### The Generation Flip

Experiment 4 completes the picture by showing the other side:

- **GPT** generates fluent, multi-sentence continuations from any prompt
- **BERT** can only fill [MASK] tokens — one word at a time, with no coherent generation capability
- Iterative mask filling is an awkward workaround, not a real generation interface

### The Polysemy Closure

Experiment 0 closes the loop from Lab 1: static embeddings assign identical vectors to "bank" regardless of context (cosine = 1.0). BERT's contextual embeddings produce distinct representations per sense (cosine = 0.49-0.69). The problem Lab 1 identified is solved by bidirectional attention.

## Synthesis

| Dimension | BERT wins | GPT wins | Tied |
|-----------|-----------|----------|------|
| Sentence classification | | | ✓ (both ~81-87%) |
| Token-level NER | ✓ (90.3% F1) | | |
| Entity boundary detection | ✓ (+40pp on B-ORG) | | |
| Text generation | | ✓ | |
| Polysemy resolution | ✓ | (not tested, same arch) | |

### The Precise Claim

Lab 4 refines Ch4's thesis from "BERT wins understanding, GPT wins generation" to a more precise statement:

> **BERT wins when every token must independently encode full-context information. GPT wins when the task requires sequential generation. On sentence-level aggregation, they are equivalent.**

This precision matters because it explains:
- Why BERT remains load-bearing infrastructure for NER, retrieval, and reranking (token-level tasks)
- Why GPT replaced BERT for chat, writing, and instruction following (generation tasks)
- Why GPT can also do classification well (sentence-level tasks don't need bidirectional context)

### The Architecture-Objective Design Space

Together with Lab 3, Lab 4 maps out how one Transformer block produces different machines:

| Config | Mask | Objective | Best at |
|--------|------|-----------|---------|
| GPT (Ch3) | Causal | Next-token prediction | Generation, sentence-level tasks |
| BERT (Ch4) | Bidirectional | Masked LM | Token-level understanding, retrieval |
| JEPA (Ch4 §4.9) | Non-causal/masked | Latent-space prediction | World modeling (emerging) |

**Meta-lesson:** Capability is not determined by the Transformer block alone. It emerges from the interaction of architecture, mask, and training objective. This is the central lesson of Part I.

## Connection to Previous Labs

- **Lab 1 Exp 0 → Lab 4 Exp 0:** Static embedding polysemy limitation → BERT solves it. Loop closed.
- **Lab 3 (residual/norm) → Lab 4 (mask type):** Lab 3 asked "what makes a GPT trainable?" Lab 4 asks "what makes representations good for understanding vs generation?" Both answers are about architectural constraints.
- **Unified lesson across 4 labs:** The simplest version of each component doesn't work. Careful engineering of mask, residual stream, position encoding, and training objective is what produces useful models.
