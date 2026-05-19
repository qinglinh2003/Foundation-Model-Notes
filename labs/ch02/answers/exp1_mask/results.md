# Exp 1: Causal Mask Ablation

Two trainings of the same model. The only difference is whether the
decoder applies a causal mask in self-attention.

## The trap

A model trained without the causal mask sees future target tokens
during teacher forcing. Loss drops near zero. Then at inference
(greedy decoding), there is no future to see, and the model has
never learned to predict from past-only context.

## Headline numbers

| Variant                              | Final train loss | Val exact-match |
|--------------------------------------|------------------|-----------------|
| Vanilla (causal mask **on**)         | 0.0169            | 97.1%        |
| Broken  (causal mask **off**)        | 0.0030            | 0.0%        |

Notice the broken model's training loss is essentially solved, yet
greedy-decode accuracy collapses.

## Full accuracy tables

### Vanilla

```
category             PAST     GERUND        3SG     PLURAL   category-avg
-------------------------------------------------------------------------
pure_regular        93.4%      95.9%      99.9%      99.8%          98.5%
phonological        96.9%      99.1%     100.0%     100.0%          98.1%
irregular           38.9%      79.3%      30.0%      20.0%          42.0%
-------------------------------------------------------------------------
tag-avg             91.7%      97.7%      99.4%      99.5%          97.1%
```

### Broken (no causal mask)

```
category             PAST     GERUND        3SG     PLURAL   category-avg
-------------------------------------------------------------------------
pure_regular         0.0%       0.0%       0.0%       0.0%           0.0%
phonological         0.0%       0.0%       0.0%       0.0%           0.0%
irregular            0.0%       0.0%       0.0%       0.0%           0.0%
-------------------------------------------------------------------------
tag-avg              0.0%       0.0%       0.0%       0.0%           0.0%
```

## Sample predictions (greedy decode)

### Vanilla

```
OK  waitlist   (3SG    ) -> pred='waitlists'    gold='waitlists'
OK  stupefy    (GERUND ) -> pred='stupefying'   gold='stupefying'
OK  elevate    (PAST   ) -> pred='elevated'     gold='elevated'
OK  chairside  (PLURAL ) -> pred='chairsides'   gold='chairsides'
OK  office     (GERUND ) -> pred='officing'     gold='officing'
OK  dulcorate  (PAST   ) -> pred='dulcorated'   gold='dulcorated'
OK  gesture    (3SG    ) -> pred='gestures'     gold='gestures'
OK  ijaza      (PLURAL ) -> pred='ijazas'       gold='ijazas'
OK  cremate    (GERUND ) -> pred='cremating'    gold='cremating'
X   medal      (PAST   ) -> pred='medalled'     gold='medaled'
OK  blake      (GERUND ) -> pred='blaking'      gold='blaking'
OK  swede      (GERUND ) -> pred='sweding'      gold='sweding'
OK  refute     (3SG    ) -> pred='refutes'      gold='refutes'
OK  discompany (3SG    ) -> pred='discompanies' gold='discompanies'
OK  herbarise  (3SG    ) -> pred='herbarises'   gold='herbarises'
```

### Broken

```
X   waitlist   (3SG    ) -> pred='wwwww'        gold='waitlists'
X   stupefy    (GERUND ) -> pred=''             gold='stupefying'
X   elevate    (PAST   ) -> pred='lll'          gold='elevated'
X   chairside  (PLURAL ) -> pred=''             gold='chairsides'
X   office     (GERUND ) -> pred=''             gold='officing'
X   dulcorate  (PAST   ) -> pred=''             gold='dulcorated'
X   gesture    (3SG    ) -> pred=''             gold='gestures'
X   ijaza      (PLURAL ) -> pred='jjz'          gold='ijazas'
X   cremate    (GERUND ) -> pred=''             gold='cremating'
X   medal      (PAST   ) -> pred=''             gold='medaled'
X   blake      (GERUND ) -> pred=''             gold='blaking'
X   swede      (GERUND ) -> pred=''             gold='sweding'
X   refute     (3SG    ) -> pred=''             gold='refutes'
X   discompany (3SG    ) -> pred=''             gold='discompanies'
X   herbarise  (3SG    ) -> pred='hhhhhhhhhh'   gold='herbarises'
```

## Diagnosis

The training objective is teacher forcing: the model receives the
correct previous targets and predicts the next token. Without the
causal mask, the decoder self-attention can attend to ALL target
positions including the future. The optimal solution is to read the
target at position t+1 directly when predicting position t -- a
shortcut that vanishes at inference. This is the most expensive
silent bug in Transformer implementations. Always run
`verify.no_future_leakage` before trusting a training-loss curve.

## Hyperparameters

epochs=12, batch=64, lr=0.0003, seed=42, device=cuda
