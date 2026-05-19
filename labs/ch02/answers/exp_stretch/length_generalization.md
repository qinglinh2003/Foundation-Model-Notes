# Length generalization (Stretch S3)

We trained on lemmas of length up to 10. Each validation lemma's
length is plotted below. The encoder uses sinusoidal positional
encoding, which is defined for any position; nothing in the model
prevents inference on lengths the optimizer never saw.

## Accuracy by lemma length

| lemma_len | correct | total | accuracy |
|-----------|---------|-------|----------|
|         2 |      12 |    16 |    75.0% |
|         3 |     263 |   276 |    95.3% |
|         4 |     930 |   967 |    96.2% |
|         5 |    1116 |  1148 |    97.2% |
|         6 |    1593 |  1653 |    96.4% |
|         7 |    1852 |  1909 |    97.0% |
|         8 |    1984 |  2030 |    97.7% |
|         9 |    1983 |  2006 |    98.9% |
|        10 |    1431 |  1441 |    99.3% |

Lengths beyond the training cap are an honest test of whether the
inflection rules transferred. Accuracy that holds up at unseen
lengths is evidence for learned-rules-over-memorization;
accuracy that collapses suggests memorization within the trained
length envelope.
