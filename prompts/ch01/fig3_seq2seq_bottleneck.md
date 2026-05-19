# Figure 1.3: Seq2Seq Encoder-Decoder with Bottleneck

**Filename**: `seq2seq_bottleneck.png`
**LaTeX label**: `fig:seq2seq`
**Caption**: The encoder--decoder architecture for sequence-to-sequence modeling. The encoder compresses the entire source sequence into a single fixed-length context vector $\mathbf{c}$, creating an information bottleneck. The decoder must reconstruct the target sequence from $\mathbf{c}$ alone.

## Prompt

```
Draw an encoder-decoder (Seq2Seq) architecture diagram for a machine learning
textbook. Use the course's Zoom-inspired blue-white visual system. The figure
should be polished and editorial, not a rough whiteboard sketch. The key visual
story is the bottleneck: all information is compressed into one vector.

LAYOUT (left to right, three regions):

LEFT REGION — ENCODER:
- Background: translucent #E8F4FD (ice blue) rectangle with rounded corners,
  generous padding
- Section label: "ENCODER" in bold small caps, #0B5CFF
- Three source tokens at the bottom: "the", "cat", "sat" — each in a small
  white rounded capsule with thin #0B5CFF border
- Above each token, an RNN cell: rounded rectangle filled with #2D8CFF
  (Zoom Blue), subtle blue gradient, soft blue-tinted shadow
- Hidden states labeled h_1, h_2, h_3 in white text inside
- Blue arrows connecting h_1 → h_2 → h_3
- Thin upward arrows from each token to its cell

CENTER — BOTTLENECK (the ONE orange accent):
- A narrow hourglass or pinched vertical capsule filled with #FF9F43
  (soft orange), with a slightly darker orange border
- Labeled "c" in bold white text inside, large and centered
- Arrow from h_3 converging into the bottleneck
- The bottleneck should feel like compression: blue flow narrows into orange
- Below the bottleneck, italic annotation in #6B7280:
  "fixed-length context vector"

RIGHT REGION — DECODER:
- Background: translucent #F0F7FF (pale blue mist) rectangle with rounded
  corners — slightly different shade from encoder to distinguish
- Section label: "DECODER" in bold small caps, #0B5CFF
- Arrow from bottleneck c into the first decoder cell
- Three decoder RNN cells: rounded rectangles filled with #5BA3FF (lighter blue)
  with subtle gradient and shadow — different shade from encoder to show
  they are a different phase
- Output tokens above each cell: "le", "chat", "assis" — in white pill shapes
- Thin upward arrows from cells to output tokens

VISUAL HIERARCHY:
- The orange bottleneck is the first thing the eye sees
- Encoder (medium blue #2D8CFF) and decoder (lighter blue #5BA3FF) are
  distinguishable by shade but clearly part of the same blue family
- Above the center, a small annotation in #6B7280:
  "all source information must pass through c"

STYLE:
- Background: #FAFCFF. Outlines: #0B5CFF.
- Only non-blue color: the orange bottleneck.
- Clean, modern, Zoom-like tech aesthetic. Generous whitespace.
- Match the same rounded geometry, line weights, typography, margins, and subtle
  shadows used by the other Chapter 1 figures.
```

## Review Checklist

- [ ] Encoder has 3 cells, decoder has 3 cells
- [ ] Only ONE connection between encoder and decoder: through c
- [ ] Bottleneck is the only orange element in the figure
- [ ] Source tokens are English, target tokens are French
- [ ] Arrow directions are correct (left-to-right)
- [ ] No direct connections from encoder hidden states to decoder
- [ ] Encoder and decoder use different blue shades but same blue family
- [ ] Overall: blue-white with single orange focal point
