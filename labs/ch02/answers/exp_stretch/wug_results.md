# Wug test (Stretch S2)

Berko's (1958) classic pseudo-word probe. The model never saw any of
these stems during training. To get them right it must apply the
inflection rules productively, not memorize.

## Per-tag accuracy

| tag     | correct | total | accuracy |
|---------|---------|-------|----------|
| PLURAL  |      13 |    14 |    92.9% |
| 3SG     |      10 |    10 |   100.0% |
| PAST    |       9 |    10 |    90.0% |
| GERUND  |      10 |    10 |   100.0% |
| TOTAL   |      42 |    44 |    95.5% |

## All items

```
OK  <PLURAL > wug        -> pred='wugs'         expected='wugs'
OK  <PLURAL > tor        -> pred='tors'         expected='tors'
OK  <PLURAL > lun        -> pred='luns'         expected='luns'
OK  <PLURAL > cra        -> pred='cras'         expected='cras'
OK  <PLURAL > niz        -> pred='nizzes'       expected='nizzes'
OK  <PLURAL > tass       -> pred='tasses'       expected='tasses'
OK  <PLURAL > gutch      -> pred='gutches'      expected='gutches'
X   <PLURAL > kazh       -> pred='kazhs'        expected='kazhes'
OK  <PLURAL > heaf       -> pred='heafs'        expected='heafs|heaves'
OK  <PLURAL > bodde      -> pred='boddes'       expected='boddes'
OK  <PLURAL > nung       -> pred='nungs'        expected='nungs'
OK  <PLURAL > chuk       -> pred='chuks'        expected='chuks'
OK  <PLURAL > soo        -> pred='soos'         expected='soos'
OK  <PLURAL > boddy      -> pred='boddies'      expected='boddies'
OK  <3SG    > spow       -> pred='spows'        expected='spows'
OK  <3SG    > mot        -> pred='mots'         expected='mots'
OK  <3SG    > bod        -> pred='bods'         expected='bods'
OK  <3SG    > rick       -> pred='ricks'        expected='ricks'
OK  <3SG    > gling      -> pred='glings'       expected='glings'
OK  <3SG    > bing       -> pred='bings'        expected='bings'
OK  <3SG    > niz        -> pred='nizzes'       expected='nizzes'
OK  <3SG    > gutch      -> pred='gutches'      expected='gutches'
OK  <3SG    > pry        -> pred='pries'        expected='pries'
OK  <3SG    > blay       -> pred='blays'        expected='blays'
OK  <PAST   > spow       -> pred='spowed'       expected='spowed'
OK  <PAST   > mot        -> pred='motted'       expected='motted'
OK  <PAST   > bod        -> pred='bodded'       expected='bodded'
OK  <PAST   > rick       -> pred='ricked'       expected='ricked'
OK  <PAST   > gling      -> pred='glinged'      expected='glinged'
OK  <PAST   > bing       -> pred='binged'       expected='binged'
OK  <PAST   > nope       -> pred='noped'        expected='noped'
OK  <PAST   > zip        -> pred='zipped'       expected='zipped'
OK  <PAST   > pry        -> pred='pried'        expected='pried'
X   <PAST   > blay       -> pred='blaid'        expected='blayed'
OK  <GERUND > spow       -> pred='spowing'      expected='spowing'
OK  <GERUND > mot        -> pred='motting'      expected='motting'
OK  <GERUND > rick       -> pred='ricking'      expected='ricking'
OK  <GERUND > gling      -> pred='glinging'     expected='glinging'
OK  <GERUND > nope       -> pred='noping'       expected='noping'
OK  <GERUND > zip        -> pred='zipping'      expected='zipping'
OK  <GERUND > pry        -> pred='prying'       expected='prying'
OK  <GERUND > blay       -> pred='blaying'      expected='blaying'
OK  <GERUND > bod        -> pred='bodding'      expected='bodding'
OK  <GERUND > chuk       -> pred='chukking'     expected='chukking'
```

A meaningful gap between val accuracy (on real lemmas) and wug
accuracy (on pseudo-words) suggests the model is leaning on
memorization for some categories. Of particular interest:

- `heaf -> heafs` vs `heaves`: Berko found English-speaking children
  produce `heafs`, refusing to extend the f->v rule (leaf -> leaves)
  to novel words. Does our model match the child or the adult?
- `pry -> pried` (PAST) vs `pry -> prying` (GERUND): consonant-y
  triggers `y -> ie` for PAST and 3SG/PLURAL but NOT for GERUND.
  A model that has truly learned the rule sees this distinction.
