# Experiment 0: Polysemy Sanity Check

## Question

Can BERT's contextual embeddings distinguish word senses that static embeddings cannot?

## Setup

- Model: DistilBERT (`distilbert-base-uncased`, 66M params)
- Words: "bank" (financial/river/aviation), "bat" (sports/animal), "light" (illumination/weight/mood)
- Static: raw token embedding layer (no Transformer processing)
- Contextual: last hidden layer output

## Results

### Static embeddings (type-level, no context)

| Word | Sense pair | Cosine |
|------|-----------|--------|
| bank | financial vs river | 1.0000 |
| bank | financial vs aviation | 1.0000 |
| bank | river vs aviation | 1.0000 |
| bat | sports vs animal | 1.0000 |
| light | illumination vs weight | 1.0000 |
| light | illumination vs mood | 1.0000 |
| light | weight vs mood | 1.0000 |

### Contextual embeddings (BERT, full bidirectional context)

| Word | Sense pair | Cosine |
|------|-----------|--------|
| bank | financial vs river | 0.6268 |
| bank | financial vs aviation | 0.4885 |
| bank | river vs aviation | 0.5426 |
| bat | sports vs animal | 0.6415 |
| light | illumination vs weight | 0.6329 |
| light | illumination vs mood | 0.5648 |
| light | weight vs mood | 0.6925 |

## Diagnosis

Static embeddings map each word type to exactly one vector. "Bank" is always the same point in vector space, regardless of whether it means a financial institution or a riverbank. Cosine similarity = 1.0 in all cases — the embedding literally cannot distinguish senses.

BERT's contextual embeddings produce different vectors for the same word in different contexts. Cosine similarity drops to 0.49-0.69, with the largest drops for the most semantically distant pairs (e.g., bank-financial vs bank-aviation = 0.49).

This directly closes the loop from Lab 1 Exp 0, where we showed static embeddings have a structural polysemy limitation. BERT solves it through bidirectional attention: each token's representation is a function of its entire sentence context, not just its type identity.
