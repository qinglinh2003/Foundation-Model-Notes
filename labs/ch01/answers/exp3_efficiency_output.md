# Experiment 3: LSTM vs. GRU Efficiency

## Question

> Does GRU achieve similar performance to LSTM with fewer parameters and less overhead?

This experiment compares the models from Experiments 1 and 2 using parameter count, final character-level validation perplexity, and delayed-memory accuracy at N=128. These metrics test whether the GRU's simpler gate structure preserves most of the LSTM's benefit.

## Results

| Model | CharLM Parameters | Probe Parameters | Final Val PPL | Accuracy at N=128 |
|---|---:|---:|---:|---:|
| RNN | 103,297 | 22,442 | 5.10 | 0.359 |
| LSTM | 350,593 | 84,650 | 4.94 | 0.994 |
| GRU | 268,161 | 63,914 | 4.50 | 0.994 |

Training speed in tokens/sec was not logged by the current scripts, so it is omitted rather than estimated.

## Observation

GRU uses 268,161 parameters in the character language model, compared with 350,593 for LSTM. That is a 23.5% reduction. Despite having fewer parameters, GRU matches LSTM on delayed-memory accuracy at N=128 and produces a lower final validation perplexity in this run.

## Explanation

The result supports the "similar results with less overhead" claim for these tasks. LSTM separates memory control across input, forget, and output gates. GRU merges part of this control into update and reset gates, reducing parameter count while retaining the core ability to carry information across time. The vanilla RNN is cheaper, but its lower delayed-memory accuracy shows that parameter efficiency alone is not enough if the architecture lacks a reliable memory mechanism.
