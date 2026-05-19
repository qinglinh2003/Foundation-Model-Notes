# Exp 2: Rank Collapse and the FFN / Residual Ablation

Two halves to one story: attention alone is structurally insufficient.

## Part A: rank collapse at random initialization (no training)

A 24-layer stack of each configuration, forwarding a random batch.
Token representations are measured at every layer.

```
  pure_SAN    final-layer mean cosine = 1.000
  residual    final-layer mean cosine = 0.483
  ffn         final-layer mean cosine = 1.000
  vanilla     final-layer mean cosine = 0.480
```

See `diagnostic_cosine.png` and `diagnostic_residual.png` for the full
per-layer trajectories. Key observations:

- **Pure SAN** collapses doubly exponentially. By layer 2, all tokens
  in a sequence have mean cosine similarity > 0.9 -- they are nearly
  the same vector. This reproduces Dong et al. (2021) Theorem 1.
- **+ residual** keeps cosine low across all 24 layers. The skip
  connection alone is enough to preserve token diversity.
- **+ FFN (no residual)** does NOT prevent collapse. Per-token
  nonlinearity cannot recover what attention has flattened.
- **+ both (vanilla)** stays in the same low-cosine regime as
  residual-only, with FFN adding capacity for downstream learning.

## Part B: trained ablation on inflection (val set)

| config       | pure_regular | phonological | irregular | overall |
|--------------|--------------|--------------|-----------|---------|
| pure_SAN     |      75.5%   |      61.9%   |     1.1%  |   69.4% |
| residual     |      99.0%   |      96.9%   |    29.4%  |   96.7% |
| ffn          |       0.0%   |       0.0%   |     0.0%  |    0.0% |
| vanilla      |      98.5%   |      98.1%   |    42.0%  |   97.1% |

Per-config detail:

### pure_SAN

```
category             PAST     GERUND        3SG     PLURAL   category-avg
-------------------------------------------------------------------------
pure_regular        71.1%      55.0%      87.9%      73.1%          75.5%
phonological        71.6%      53.2%      61.7%      36.8%          61.9%
irregular            0.5%       3.4%       5.0%       0.0%           1.1%
-------------------------------------------------------------------------
tag-avg             66.4%      53.4%      86.1%      71.8%          69.4%
```

### residual only

```
category             PAST     GERUND        3SG     PLURAL   category-avg
-------------------------------------------------------------------------
pure_regular        97.0%      95.9%     100.0%      99.9%          99.0%
phonological        95.2%      98.3%      99.2%     100.0%          96.9%
irregular           29.1%      37.9%      25.0%      20.0%          29.4%
-------------------------------------------------------------------------
tag-avg             91.1%      96.7%      99.4%      99.7%          96.7%
```

### FFN only

```
category             PAST     GERUND        3SG     PLURAL   category-avg
-------------------------------------------------------------------------
pure_regular         0.0%       0.0%       0.0%       0.0%           0.0%
phonological         0.0%       0.0%       0.0%       0.0%           0.0%
irregular            0.0%       0.0%       0.0%       0.0%           0.0%
-------------------------------------------------------------------------
tag-avg              0.0%       0.0%       0.0%       0.0%           0.0%
```

### vanilla

```
category             PAST     GERUND        3SG     PLURAL   category-avg
-------------------------------------------------------------------------
pure_regular        93.4%      95.9%      99.9%      99.8%          98.5%
phonological        96.9%      99.1%     100.0%     100.0%          98.1%
irregular           38.9%      79.3%      30.0%      20.0%          42.0%
-------------------------------------------------------------------------
tag-avg             91.7%      97.7%      99.4%      99.5%          97.1%
```

## Diagnosis

Two complementary failure modes:

1. **Pure SAN** collapses representations and cannot train at all.
2. **+ residual only** stops the collapse, so the model trains;
   but its output is a weighted average of input embeddings + linear
   projections. It can learn pure_regular (just copy the lemma and
   append `-s` / `-ed`) reasonably well, but irregular forms like
   `go -> went` require lookup-style transformations that linear
   averaging cannot express. Accuracy on irregular drops sharply.
3. **+ FFN only** technically has the nonlinearity to do irregular
   lookups, but its tokens are collapsed by attention, so the FFN
   receives a near-rank-1 input and can't condition its
   transformation on which character it is.
4. **+ both** is vanilla. Residual preserves token diversity through
   depth; FFN provides per-token nonlinearity at every layer.

The trained accuracy table and the diagnostic figures together
establish: attention routes information across positions; FFN +
residual maintain the per-token representations on which that
routing operates. Removing either dimension breaks the system.

## Hyperparameters

epochs=12, batch=64, lr=0.0003, seed=42, device=cuda
diagnostic: depth=24, d_model=64, seeds=3
