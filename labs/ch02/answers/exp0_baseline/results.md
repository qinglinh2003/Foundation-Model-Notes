# Exp 0: Vanilla Baseline

**Configuration**: vanilla encoder-decoder Transformer, all 5 modules enabled.
**Parameters**: 936,609
**Wall time**: 9.9 min on cuda
**Hyperparameters**: epochs=20, batch=64, lr=0.0003, seed=42

## Train set accuracy

```
category             PAST     GERUND        3SG     PLURAL   category-avg
-------------------------------------------------------------------------
pure_regular        95.4%      96.1%     100.0%     100.0%          98.8%
phonological        99.9%      99.2%     100.0%     100.0%          99.6%
irregular           54.8%     100.0%      62.5%       0.0%          58.9%
-------------------------------------------------------------------------
tag-avg             95.3%      98.0%      99.8%      99.9%          98.2%
```

## Validation set accuracy

```
category             PAST     GERUND        3SG     PLURAL   category-avg
-------------------------------------------------------------------------
pure_regular        93.0%      95.1%     100.0%      99.9%          98.4%
phonological        99.2%      99.1%     100.0%     100.0%          99.2%
irregular           46.8%      82.8%      45.0%      20.0%          49.6%
-------------------------------------------------------------------------
tag-avg             93.6%      97.4%      99.6%      99.6%          97.5%
```

## Validation sample predictions (first 25)

```
OK  waitlist   (3SG    , pure_regular  ) -> pred='waitlists'    gold='waitlists'
OK  stupefy    (GERUND , pure_regular  ) -> pred='stupefying'   gold='stupefying'
OK  elevate    (PAST   , phonological  ) -> pred='elevated'     gold='elevated'
OK  chairside  (PLURAL , pure_regular  ) -> pred='chairsides'   gold='chairsides'
OK  office     (GERUND , phonological  ) -> pred='officing'     gold='officing'
OK  dulcorate  (PAST   , phonological  ) -> pred='dulcorated'   gold='dulcorated'
OK  gesture    (3SG    , pure_regular  ) -> pred='gestures'     gold='gestures'
OK  ijaza      (PLURAL , pure_regular  ) -> pred='ijazas'       gold='ijazas'
OK  cremate    (GERUND , phonological  ) -> pred='cremating'    gold='cremating'
X   medal      (PAST   , pure_regular  ) -> pred='medalled'     gold='medaled'
OK  blake      (GERUND , phonological  ) -> pred='blaking'      gold='blaking'
OK  swede      (GERUND , phonological  ) -> pred='sweding'      gold='sweding'
OK  refute     (3SG    , pure_regular  ) -> pred='refutes'      gold='refutes'
OK  discompany (3SG    , phonological  ) -> pred='discompanies' gold='discompanies'
OK  herbarise  (3SG    , pure_regular  ) -> pred='herbarises'   gold='herbarises'
OK  retyre     (GERUND , phonological  ) -> pred='retyring'     gold='retyring'
OK  descan     (3SG    , pure_regular  ) -> pred='descans'      gold='descans'
OK  coiner     (PLURAL , pure_regular  ) -> pred='coiners'      gold='coiners'
OK  bumbaze    (PAST   , phonological  ) -> pred='bumbazed'     gold='bumbazed'
OK  shepherde  (PLURAL , pure_regular  ) -> pred='shepherdes'   gold='shepherdes'
OK  intergrow  (PAST   , irregular     ) -> pred='intergrew'    gold='intergrew'
OK  guevi      (PLURAL , pure_regular  ) -> pred='guevis'       gold='guevis'
OK  subsociety (PLURAL , phonological  ) -> pred='subsocieties' gold='subsocieties'
OK  eyefuck    (PAST   , pure_regular  ) -> pred='eyefucked'    gold='eyefucked'
X   undercome  (PAST   , irregular     ) -> pred='undercomed'   gold='undercame'
```

## Notes

This is the ceiling. Every ablation in Exp 1-4 reduces one or more
of the model's structural ingredients and measures how far accuracy
falls. A useful sanity check before reading further: examine the
irregular row in the validation table -- that is the bucket where
attention's per-token routing must combine with FFN's per-token
nonlinearity. If you see the irregular column near 0, your training
budget is probably too small; increase --epochs.
