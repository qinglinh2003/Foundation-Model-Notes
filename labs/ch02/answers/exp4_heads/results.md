# Exp 4: Multi-Head Ablation + Visualization

We hold `d_model=128` constant and vary `num_heads` in {1, 4, 8}.
Each head sees `d_k = 128/h` dimensions. The trade-off:
fewer heads have more capacity per head but only one attention
pattern; more heads have diverse patterns but each is lower-rank.

## Accuracy

| variant | pure_regular | phonological | irregular | overall |
|---------|--------------|--------------|-----------|---------|
| h=1    |  98.7% |  98.3% |  29.8% |  97.0% |
| h=4    |  98.5% |  98.1% |  42.0% |  97.1% |
| h=8    |  98.0% |  98.8% |  42.0% |  97.0% |

## Detail

### h=1

```
category             PAST     GERUND        3SG     PLURAL   category-avg
-------------------------------------------------------------------------
pure_regular        94.9%      95.8%     100.0%      99.8%          98.7%
phonological        97.5%      99.0%     100.0%      98.9%          98.3%
irregular           29.6%      37.9%      25.0%      20.0%          29.8%
-------------------------------------------------------------------------
tag-avg             91.9%      97.1%      99.5%      99.5%          97.0%
```

### h=4

```
category             PAST     GERUND        3SG     PLURAL   category-avg
-------------------------------------------------------------------------
pure_regular        93.4%      95.9%      99.9%      99.8%          98.5%
phonological        96.9%      99.1%     100.0%     100.0%          98.1%
irregular           38.9%      79.3%      30.0%      20.0%          42.0%
-------------------------------------------------------------------------
tag-avg             91.7%      97.7%      99.4%      99.5%          97.1%
```

### h=8

```
category             PAST     GERUND        3SG     PLURAL   category-avg
-------------------------------------------------------------------------
pure_regular        92.6%      94.6%      99.7%      99.6%          98.0%
phonological        98.3%      99.2%     100.0%     100.0%          98.8%
irregular           38.9%      69.0%      45.0%      20.0%          42.0%
-------------------------------------------------------------------------
tag-avg             92.3%      97.1%      99.3%      99.3%          97.0%
```


## Cross-attention visualization (h=4 model)

Files `cross_attn_<idx>_<tag>_<category>.png` show the four heads'
cross-attention maps on a single test example each. Rows are decoder
output positions; columns are encoder input positions (TAG, lemma
characters, EOS). For each example, look for:

  - One head with a near-diagonal pattern: this head COPIES lemma
    characters position-for-position. It is the workhorse that
    handles the pure_regular cases.
  - One head fixating on the TAG token (column 0) at every output
    step: a "control" head that re-reads which inflection paradigm
    we are in.
  - For phonological / irregular examples, expect at least one head
    to focus on the lemma's final character(s), because those are
    where the rule changes (`y -> ie`, `f -> v`, etc.) and where
    irregulars actually differ from the lemma.

The visualization is not a clean experiment with a single right
answer -- it is interpretive. Different seeds may produce different
specializations.

## Hyperparameters

epochs={args.epochs}, batch={args.batch_size}, lr={args.lr}, seed={args.seed}, device={args.device}
