# Figure 4.1: Causal vs Bidirectional Attention

**Filename**: `causal_vs_bidirectional.png`
**LaTeX label**: `fig:causal-vs-bidirectional`
**Caption**: The same sentence processed with causal (left) and bidirectional (right) attention. Bidirectional attention allows "bank" to attend to "river," resolving ambiguity instantly.

## Prompt

```
Draw a side-by-side comparison of causal vs bidirectional attention for a
graduate-level machine learning textbook. Use the course's blue-white visual system.
Landscape orientation, polished editorial style.

LAYOUT:
Two panels side by side, sharing the same input sentence:
"The bank by the river was eroding"

LEFT PANEL — CAUSAL ATTENTION (GPT-style):
- Title: "Causal (Left-to-Right)"
- Show 8 token boxes in a horizontal row
- Draw attention arrows: each token can ONLY attend to itself and tokens to its left
- Highlight the token "bank" (position 2) — show it can only attend to "The" and itself
- Below "bank": annotation "Context: only 'The' → ambiguous"
- Use a 8×8 attention matrix below showing lower-triangular pattern
  (white = can attend, dark gray = masked)
- Draw a red/orange X on the connections from "bank" to "river" and "eroding"
  to emphasize what is BLOCKED

RIGHT PANEL — BIDIRECTIONAL ATTENTION (BERT-style):
- Title: "Bidirectional (Full Context)"
- Same 8 token boxes
- Draw attention arrows: every token attends to every other token
- Highlight "bank" — show it attending to ALL tokens, especially "river" and "eroding"
- The attention connections from "bank" to "river" and "eroding" should be
  in soft orange (#FF9F43) — this is the figure's orange accent, showing
  the KEY connections that resolve the ambiguity
- Below "bank": annotation "Context: full sentence → 'riverbank'"
- Use a 8×8 attention matrix below showing ALL-WHITE pattern (fully visible)

VISUAL DETAILS:
- Token boxes: rounded rectangles in Zoom Blue (#2D8CFF), white text
- "bank" token: slightly larger or highlighted with a glow
- Attention arrows: thin gray for normal connections, orange for the
  disambiguating right-context connections in the bidirectional panel
- Background: ice white (#FAFCFF)
- A centered annotation between the panels:
  "Same word, different information access → different representation"
- Sans-serif labels in charcoal (#1A1A2E)
- Clean, minimal — no unnecessary decoration
```

## Review Checklist

- [ ] Two panels clearly labeled "Causal" and "Bidirectional"
- [ ] Same sentence "The bank by the river was eroding" in both
- [ ] Causal panel: "bank" can only see "The" — future tokens blocked
- [ ] Bidirectional panel: "bank" sees everything, especially "river" and "eroding"
- [ ] Orange accent ONLY on the disambiguating connections (bank→river, bank→eroding)
- [ ] Attention matrices correct: lower-triangular (left) vs full (right)
- [ ] Annotations explain the consequence: ambiguous vs resolved
- [ ] No extra colors beyond blue + white + orange + gray
