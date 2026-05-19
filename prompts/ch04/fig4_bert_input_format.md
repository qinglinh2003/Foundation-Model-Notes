# Figure 4.4: BERT Input Format

**Filename**: `bert_input_format.png`
**LaTeX label**: `fig:bert-input`
**Caption**: BERT's input representation: token, position, and segment embeddings are summed. Special tokens [CLS] and [SEP] structure the input for downstream tasks.

## Prompt

```
Draw the BERT input format for a graduate-level machine learning textbook.
Use the course's blue-white visual system. Landscape orientation, polished editorial style.

LAYOUT:
A layered diagram showing how three embedding layers sum together.

INPUT SENTENCE (top):
Show the tokenized input:
[CLS] The cat sat [SEP] It slept [SEP]

THREE EMBEDDING LAYERS (stacked vertically, aligned with tokens):

Layer 1 — TOKEN EMBEDDINGS:
- Row of boxes, each containing the token's word
- All in Zoom Blue (#2D8CFF)
- [CLS] and [SEP] tokens in slightly darker shade to distinguish special tokens

Layer 2 — POSITION EMBEDDINGS:
- Row of boxes: E_0, E_1, E_2, E_3, E_4, E_5, E_6, E_7
- In lighter blue
- Small annotation: "Learned, max 512 positions"

Layer 3 — SEGMENT EMBEDDINGS:
- Row of boxes showing segment IDs
- First sentence (positions 0-4): "Segment A" in one shade
- Second sentence (positions 5-7): "Segment B" in another shade
- Only TWO segment embeddings (E_A, E_B)

SUMMATION:
- "+" symbols between the three layers
- Arrow pointing down to:

FINAL INPUT REPRESENTATION:
- Row of combined embedding boxes
- Formula: x_t = E_token[w_t] + E_pos[t] + E_seg[s_t]

HIGHLIGHT:
- [CLS] token position highlighted with soft orange (#FF9F43) border/glow
- Annotation pointing to [CLS]: "Used as sentence representation for classification"
- [SEP] tokens with dashed border: "Marks sentence boundaries"

VISUAL DETAILS:
- Zoom Blue (#2D8CFF) for token embeddings
- Lighter blue for position embeddings
- Two subtle shades (blue-gray vs blue-purple) for Segment A vs B
- Soft Orange (#FF9F43) ONLY for [CLS] highlight
- White/ice blue (#FAFCFF) background
- Clean "+" operators between layers
- Sans-serif labels in charcoal (#1A1A2E)
- Compact but readable — each layer clearly distinguished
```

## Review Checklist

- [ ] Three embedding layers clearly shown and labeled
- [ ] Tokens include [CLS] at start, [SEP] between sentences, [SEP] at end
- [ ] Position embeddings numbered 0-7 (or appropriate)
- [ ] Segment embeddings show two distinct segments (A and B)
- [ ] Summation ("+" or "⊕") operation clearly shown
- [ ] [CLS] highlighted in orange as the sentence-level representation
- [ ] Formula x_t = E_token + E_pos + E_seg shown
- [ ] "Max 512 positions" noted for position embeddings
