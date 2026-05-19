# Lab 1 Report: Why Context and Gating Matter

Lab 1 tested three related claims: static embeddings collapse context, gates stabilize recurrent memory, and attention removes the fixed-context bottleneck in encoder-decoder models.

## Experiment 0: Static Embeddings

GloVe captured useful global semantic structure but failed to represent context-specific meaning. The neighbors of `bank` were entirely financial (`banks`, `banking`, `credit`, `investment`, `finance`), with no river-bank sense. `cell` mixed biology and phone meanings, but biology dominated most neighbors. `spring` was mostly seasonal.

![Sense distribution](figures/sense_distribution.png)
*Figure 1: Sense composition of top-10 neighbors per polysemous word.*

![t-SNE of polysemous words](figures/polysemy_tsne.png)
*Figure 2: t-SNE projection shows single-sense dominance for `bank` and `spring`; only `cell` exhibits visible sense mixing.*

This shows that one static vector becomes an average over contexts. Analogy arithmetic still worked for cleaner relations: `king - man + woman -> queen`, `berlin - paris + france -> germany`, and `fast - slow + slower -> faster`. Static embeddings are useful, but they cannot produce different representations for the same word in different sentences.

## Experiment 1: Gradient Pathology

Under normal training with gradient clipping, all recurrent models stayed stable. Average gradient norms were 0.344 for RNN, 0.269 for LSTM, and 0.260 for GRU.

![Gradient norms during normal training](figures/gradient_norm_normal.png)
*Figure 3: Normal training with clipping. All models remain stable.*

The Adam stress test did not reproduce the expected gradient explosion. With sequence length 256, learning rate 3e-3, and no clipping, all models still remained stable.

![Gradient norms under Adam stress](figures/gradient_norm_stress_adam.png)
*Figure 4: Adam stress test. Adam's adaptive scaling masks the instability.*

This negative result is important: optimizer choice affects what the experiment reveals. The SGD control exposed the classical pathology. With SGD at learning rate 1.0 and no clipping, the vanilla RNN reached a maximum gradient norm of 60,240.6 and became unstable. LSTM and GRU remained stable, with maximum norms of 0.591 and 1.788.

![Gradient norms under SGD stress](figures/gradient_norm_stress_sgd.png)
*Figure 5: SGD stress test. RNN gradients explode; gated models remain stable.*

This supports the theory that vanilla RNNs repeatedly multiply through recurrent transitions, while LSTM and GRU gates create more reliable paths for information and gradients.

## Experiment 2: Long-Range Dependency

The delayed-memory task gave the clearest evidence for gating. RNN accuracy fell as distance increased: 100.0% at 8, 56.0% at 32, 35.9% at 128, and 26.0% at 256. LSTM stayed near perfect: 100.0%, 98.8%, 99.4%, and 99.2%. GRU behaved similarly: 100.0%, 99.5%, 99.4%, and 99.4%.

![Accuracy vs dependency distance](figures/distance_probe.png)
*Figure 6: RNN accuracy degrades with distance; LSTM and GRU maintain long-range memory.*

The result matches the architectural story: LSTM cell state acts like a memory and gradient highway, while GRU obtains a similar effect with fewer gates.

## Experiment 3: LSTM vs GRU Efficiency

GRU achieved the gated-model benefit with fewer parameters. LSTM had 350,593 parameters; GRU had 268,161, a 23.5% reduction. GRU also matched LSTM on the N=128 dependency task at 99.4% and reached lower validation perplexity in this run, 4.50 versus 4.94. The vanilla RNN was smaller, with 103,297 parameters, but its 35.9% N=128 accuracy showed that cheap recurrence without gates was not enough.

| Model | Params | Val PPL | Distance Acc (N=128) |
|-------|--------|---------|----------------------|
| RNN   | 103,297 | 5.82 | 35.9% |
| LSTM  | 350,593 | 4.94 | 99.4% |
| GRU   | 268,161 | 4.50 | 99.4% |

## Experiment 4: Seq2Seq Bottleneck + Attention

The reversal task separated gating from attention. The no-attention encoder-decoder reached 98.1% exact-match accuracy at length 10, then collapsed to 0.0% at lengths 30, 50, and 100. Attention reached 99.9% at length 10 and 51.4% at length 30, but also failed at lengths 50 and 100 under the current training budget.

![Accuracy vs input length](figures/accuracy_vs_length.png)
*Figure 7: Fixed-context decoding collapses beyond short inputs; attention extends the working range.*

The heatmap showed a clean anti-diagonal, meaning the decoder learned to attend to input positions in reverse order.

![Attention heatmap](figures/attention_heatmap.png)
*Figure 8: Attention learns position-specific alignment instead of relying only on one final context vector.*

Overall, gates solve recurrent memory and gradient flow, while attention solves the encoder-decoder bottleneck by letting each decoding step retrieve the relevant encoder states directly.
