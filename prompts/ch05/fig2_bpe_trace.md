# Figure 5.2: BPE Merge Trace

**Filename**: `bpe_trace.png`
**LaTeX label**: `fig:bpe-trace`
**Caption**: Byte Pair Encoding: step-by-step merge trace. Starting from characters, the algorithm merges the most frequent pair at each step. The merge table records the order, and at inference time the same merges are applied to new text.

## Prompt

```
Draw a step-by-step BPE (Byte Pair Encoding) merge trace for a graduate-level
machine learning textbook. Use the course's blue-white visual system. Landscape
orientation, polished editorial style.

LAYOUT:
A vertical sequence of 5 steps showing the BPE algorithm operating on a small corpus.
Each step shows the current state of the corpus and which pair is being merged.

CORPUS: Three words shown as token sequences: "low", "lower", "lowest"

STEP 0 — INITIALIZE:
- Title: "Step 0: Character vocabulary"
- Show: ["l", "o", "w"], ["l", "o", "w", "e", "r"], ["l", "o", "w", "e", "s", "t"]
- Each character is a small blue token pill
- Vocabulary shown on the right: {l, o, w, e, r, s, t} — 7 entries
- Annotation: "Start from individual characters"

STEP 1 — FIRST MERGE:
- Highlight pair: "l" + "o" with an orange bracket/arc connecting them
- Annotation: "Most frequent pair: (l, o) — 3 occurrences"
- Arrow pointing down to result

STEP 2 — AFTER FIRST MERGE:
- Show: ["lo", "w"], ["lo", "w", "e", "r"], ["lo", "w", "e", "s", "t"]
- "lo" is a new merged token pill (slightly wider, still blue)
- Vocabulary: {l, o, w, e, r, s, t, lo} — 8 entries (new one highlighted)

STEP 3 — SECOND MERGE:
- Highlight pair: "lo" + "w" with orange bracket
- Annotation: "Most frequent pair: (lo, w) — 3 occurrences"
- Arrow pointing down

STEP 4 — AFTER SECOND MERGE:
- Show: ["low"], ["low", "e", "r"], ["low", "e", "s", "t"]
- "low" is now a single token
- Vocabulary: {l, o, w, e, r, s, t, lo, low} — 9 entries

RIGHT SIDE — MERGE TABLE:
A small table on the right showing:
| Order | Merge |
|   1   | l + o → lo |
|   2   | lo + w → low |
|  ...  | (continues) |

Caption below: "Merge table is saved and reused at inference time"

VISUAL DETAILS:
- Token pills: rounded rectangles, blue (#2D8CFF) fill, white text
- Merged tokens are slightly wider to show they contain more information
- Orange accent: ONLY on the brackets showing the pair being merged
- Arrows between steps: steel gray, medium weight
- Background: white (#FAFCFF)
- The merge table on the right has a subtle ice-blue background
- Steps are connected by downward arrows
- Clean left-to-right reading flow within each step
- The figure should feel like watching an algorithm execute step by step
```

## Review Checklist

- [ ] Corpus is "low", "lower", "lowest"
- [ ] Characters start as individual tokens
- [ ] First merge: (l, o) → lo, correctly shown as most frequent
- [ ] Second merge: (lo, w) → low, correctly shown
- [ ] Merged tokens are visually distinguishable (wider)
- [ ] Merge table shown on the right
- [ ] Orange accent ONLY on the merge brackets (pair being merged)
- [ ] Vocabulary grows with each merge
- [ ] Sequential steps connected by arrows
- [ ] No extra colors beyond blue + white + orange + gray
