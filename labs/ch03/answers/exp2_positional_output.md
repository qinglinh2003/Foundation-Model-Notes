# Experiment 2: Positional Encoding

> Question: How much positional information does a causal decoder-only model need? Does the causal mask already provide implicit position, or is explicit PE structurally necessary?

## Setup

Three GPTs (6 layers, d_model=128, 4 heads, ~800K-830K params), trained for 2000 steps. The only difference is positional encoding type:
- A: No PE at all (causal mask provides the only position signal)
- B: Learned absolute PE (one embedding per position, up to 512)
- C: RoPE (rotary position embedding applied to Q/K)

## Results

| Config | Val Loss | Params |
|--------|----------|--------|
| A: No PE         | 2.08 | 797,056 |
| B: Learned PE    | 1.77 | 829,824 |
| C: RoPE          | **1.55** | 797,056 |

![Loss curves](figures/exp2_loss_comparison.png)
*No-PE (A) converges to a higher floor. RoPE (C) reaches the lowest loss.*

## Generated Samples

**Config A (no PE):**
```
ROMEO:
Thou be sencious by his a'elf:
And tell speace, thou not let to shalt to of so.

FRIAR S:
Melsecion, them who can the curp to'er would that pre
```

**Config C (RoPE):**
```
ROMEO:
'Tis in sdeep do! ' to your shame.

Nurse:
No, Romeo.

LUCIO:
Good no fellow. This commiary of speak wament speak,
Which you out.

HENRY LO:
Th
```

## Observations

1. **No PE is not catastrophic.** Val loss 2.08 is substantially better than random (4.17). The causal mask provides implicit order: position t sees t tokens, position t+1 sees t+1 tokens. This counting difference gives a partial position signal, consistent with Haviv et al. (2022) who showed decoder-only models can learn position from mask structure alone.

2. **But explicit PE clearly helps.** The gap from 2.08 to 1.77 (learned) and 1.55 (RoPE) is large. Character-level language modeling requires knowing *exactly* where you are in a word/sentence structure. The causal mask's implicit position is too coarse for this.

3. **RoPE outperforms learned PE even at 256 tokens.** This is notable because RoPE's theoretical advantage (relative position generalization, extrapolation beyond training length) shouldn't matter much at 256 tokens where both methods see all positions during training. The likely explanation: RoPE's inductive bias (attention decays with distance by default) matches natural language statistics better than a purely learned positional structure.

## Diagnosis

Positional encoding is **structurally necessary for strong performance** but not for basic learning. A causal decoder-only model without PE can still learn *something* — it knows "how many tokens came before me" from the mask shape. But it cannot learn the fine-grained positional structure needed for language: word boundaries, clause positions, dialogue formatting.

The no-PE generation shows this concretely: it produces English words and rough dialogue format but with confused ordering ("thou not let to shalt to of so" — words in wrong grammatical positions).

**Short training caveat:** At 2000 steps, the RoPE vs learned-PE gap (1.55 vs 1.77) is clear but might narrow with longer training. RoPE's stronger advantage typically manifests at longer contexts and during length generalization — neither of which is tested here. The take-away should be: "PE is necessary; RoPE has a principled advantage that often shows even at short scale."
