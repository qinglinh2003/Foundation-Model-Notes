# Exp 3: Positional Encoding Ablation

Self-attention is permutation-equivariant. Without explicit position
information, the encoder cannot tell `cat` from `act`; the decoder
cannot tell `walk-step-3` from `walk-step-1`. Sinusoidal PE injects
that information by adding fixed per-position vectors to the
embeddings.

## Headline numbers

| variant            | pure_regular | phonological | irregular | overall |
|--------------------|--------------|--------------|-----------|---------|
| enc_on_dec_on      |  98.5% |  98.1% |  42.0% |  97.1% |
| enc_off_dec_on     |  20.9% |  25.6% |   7.6% |  22.1% |
| enc_on_dec_off     |  98.0% |  98.3% |  33.2% |  96.6% |
| enc_off_dec_off    |  19.9% |  24.8% |   9.2% |  21.2% |

## Detail per variant

### enc_on_dec_on

```
category             PAST     GERUND        3SG     PLURAL   category-avg
-------------------------------------------------------------------------
pure_regular        93.4%      95.9%      99.9%      99.8%          98.5%
phonological        96.9%      99.1%     100.0%     100.0%          98.1%
irregular           38.9%      79.3%      30.0%      20.0%          42.0%
-------------------------------------------------------------------------
tag-avg             91.7%      97.7%      99.4%      99.5%          97.1%
```


### enc_off_dec_on

```
category             PAST     GERUND        3SG     PLURAL   category-avg
-------------------------------------------------------------------------
pure_regular        27.5%      28.3%      28.1%       8.8%          20.9%
phonological        25.3%      26.6%      27.8%      10.3%          25.6%
irregular            5.9%      17.2%      15.0%       0.0%           7.6%
-------------------------------------------------------------------------
tag-avg             24.6%      27.2%      28.0%       8.8%          22.1%
```


### enc_on_dec_off

```
category             PAST     GERUND        3SG     PLURAL   category-avg
-------------------------------------------------------------------------
pure_regular        94.1%      93.6%      99.7%      99.3%          98.0%
phonological        97.5%      99.1%      99.2%      97.7%          98.3%
irregular           31.0%      55.2%      30.0%      20.0%          33.2%
-------------------------------------------------------------------------
tag-avg             91.8%      96.5%      99.2%      99.0%          96.6%
```


### enc_off_dec_off

```
category             PAST     GERUND        3SG     PLURAL   category-avg
-------------------------------------------------------------------------
pure_regular        24.2%      25.7%      26.7%       9.5%          19.9%
phonological        24.5%      25.7%      26.3%      11.5%          24.8%
irregular            7.4%      13.8%      15.0%      20.0%           9.2%
-------------------------------------------------------------------------
tag-avg             23.2%      25.6%      26.6%       9.6%          21.2%
```


## Diagnosis

Removing encoder PE most severely hurts patterns where the lemma's
suffix matters: phonological (e.g., `try -> tried` -- the model must
see that `y` is the last character, not just present somewhere).
Pure regulars suffer too, just less, because the decoder can still
emit a fixed suffix string.

Removing decoder PE breaks the autoregressive count: the decoder
cannot tell whether it has emitted 1 or 5 characters so far. Greedy
generation either truncates early or rambles past the correct ending.

Removing both is the harshest setting and approximates a permutation-
invariant Seq2Seq model, which cannot solve any positional task.

Note: sinusoidal PE generalizes to unseen positions, so the same
model trained on lemma length <= 10 can in principle decode longer
sequences at inference. We probe this in `exp_stretch.py`.

## Hyperparameters

epochs=12, batch=64, lr=0.0003, seed=42, device=cuda
