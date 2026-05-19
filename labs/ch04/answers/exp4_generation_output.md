# Experiment 4: Generation Flip

## Question

If BERT is better at understanding, what is GPT better at?

## Setup

- DistilGPT2: autoregressive generation from prompts (50 tokens, temperature=0.8, top_k=50)
- DistilBERT (masked LM): [MASK] filling (top-5 predictions per position)
- DistilBERT: iterative mask filling as attempted "generation"
- No training required — pure inference

## Results

### GPT: Autoregressive Generation

| Prompt | Output (first 50 tokens) |
|--------|-------------------------|
| "The movie was absolutely" | "...one step on the way. The story is a perfect way to tell stories, stories that have a lot of similarities..." |
| "In the beginning of the story" | "...we see the rise of the rebel movement, a movement that has been the catalyst behind the events..." |
| "The scientist discovered that" | "...a small amount of DNA was in the same sample that was recovered from the lab's laboratory..." |

GPT produces fluent, coherent multi-sentence continuations. The outputs are topical, grammatical, and naturally extend the prompts.

### BERT: Mask Filling

| Input | Top prediction | Score |
|-------|---------------|-------|
| "The movie was absolutely [MASK]." | fantastic | 0.110 |
| "The [MASK] ran quickly through the forest." | trail | 0.052 |
| "She felt [MASK] after hearing the news." | relieved | 0.075 |
| "The experiment was a complete [MASK]." | success | 0.462 |

BERT makes contextually appropriate single-token predictions. But it can only fill one position at a time.

### BERT: Iterative Mask Filling ("Generation")

Template: "The movie was [MASK] [MASK] [MASK] [MASK] [MASK] ."

| Step | Result |
|------|--------|
| 1 | "the movie was **released** [MASK] [MASK] [MASK] [MASK]." |
| 2 | "the movie was released **on** [MASK] [MASK] [MASK]." |
| 3 | "the movie was released on **dvd** [MASK] [MASK]." |
| 4 | "the movie was released on dvd **by** [MASK]." |
| 5 | "the movie was released on dvd by **netflix**." |

The result is grammatical but only because the template is short and simple. This "generation" strategy has fundamental problems:
- Each fill step sees ALL positions (including unfilled [MASK] tokens)
- No notion of left-to-right coherence
- Cannot generate beyond the pre-specified number of [MASK] tokens
- Would degrade rapidly with longer sequences

## Diagnosis

GPT generates fluent text because autoregressive decoding is its native interface: causal mask ensures left-to-right coherence, and each new token is conditioned only on previous tokens.

BERT can only fill [MASK] tokens — it is structurally incapable of open-ended generation. Bidirectional attention means every position sees every other position simultaneously, which is perfect for understanding but prevents the sequential, left-to-right process that generation requires.

This is the architectural reason BERT lost the interface war. When users wanted AI that talks back, BERT could not comply — not because it lacks intelligence, but because its attention mask makes generation architecturally impossible without awkward workarounds.

**Together with Exp 1-2, this completes the Lab 4 thesis:**
- BERT wins understanding (Exp 1-2: better frozen-probe accuracy on classification)
- GPT wins generation (Exp 3: fluent text vs single-token fill)
- Same Transformer block, different capability
