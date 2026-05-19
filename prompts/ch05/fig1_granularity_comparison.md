# Figure 5.1: Granularity Comparison

**Filename**: `granularity_comparison.png`
**LaTeX label**: `fig:granularity`
**Caption**: The granularity tradeoff. Character-level tokenization produces long sequences with tiny vocabularies. Word-level tokenization produces short sequences but cannot handle unseen words. Subword tokenization (BPE) is the practical middle ground.

## Prompt

```
Draw a three-panel comparison of text tokenization granularity for a graduate-level
machine learning textbook. Use the course's blue-white visual system. Landscape
orientation, polished editorial style.

LAYOUT:
Three horizontal panels, left to right, showing the SAME sentence being tokenized
at three granularity levels. The sentence is: "unbelievably low prices"

LEFT PANEL — CHARACTER-LEVEL:
- Title: "Character-Level"
- Show each character as a small individual token pill: "u", "n", "b", "e", "l", "i",
  "e", "v", "a", "b", "l", "y", " ", "l", "o", "w", " ", "p", "r", "i", "c", "e", "s"
- Count indicator: "23 tokens"
- Below: a small stat box showing "Vocab: ~256" and "Seq length: very long"
- Visual: tokens are tiny, densely packed — feels crowded
- Small gray annotation: "O(T^2) attention cost grows quickly"

CENTER PANEL — WORD-LEVEL:
- Title: "Word-Level"
- Show 3 large token pills: "unbelievably", "low", "prices"
- Count indicator: "3 tokens"
- Below: stat box "Vocab: ~100K+" and "Seq length: short"
- Show a 4th word below in a red/orange dashed box: "unbelieveably" (typo)
  with annotation "[UNK] — unseen word has no representation"
- This is the ONLY orange accent element: the failure case

RIGHT PANEL — SUBWORD (BPE):
- Title: "Subword (BPE)"
- Show tokens: "un", "believ", "ably", "low", "prices"
- Count indicator: "5 tokens"
- Below: stat box "Vocab: ~32K-100K" and "Seq length: moderate"
- A blue highlight banner: "Goldilocks: common words whole, rare words decompose"
- This panel should feel visually balanced — not too crowded, not too sparse

VISUAL DETAILS:
- Token pills: rounded rectangles with blue fill (#2D8CFF) and white text
- Panel backgrounds: ice blue (#E8F4FD) rounded rectangles
- A bottom annotation spanning all three:
  "Too fine-grained → balanced → too brittle"
  with arrows pointing to the subword panel as the sweet spot
- Sans-serif labels in charcoal (#1A1A2E)
- Clean, spacious layout
- The subword panel should feel slightly emphasized (subtle blue glow or
  slightly larger) to show it's the recommended approach
```

## Review Checklist

- [ ] Three panels clearly showing character / word / subword
- [ ] Same input text in all three ("unbelievably low prices")
- [ ] Character panel shows 23 tiny tokens — feels crowded
- [ ] Word panel shows 3 tokens + [UNK] failure case
- [ ] Subword panel shows 5 tokens — balanced feel
- [ ] Vocab size and seq length stats visible for each
- [ ] Orange accent on ONE failure element only: the word-level [UNK] failure
- [ ] "Goldilocks" annotation on subword panel
- [ ] No extra colors beyond blue + white + orange + gray
