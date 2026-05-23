# Figure 11.4: Sequence Packing with Attention and Loss Masking

**Filename**: `fig_packing_masking.png`
**LaTeX label**: `fig:packing-masking`
**Caption**: Sequence packing with attention masking and loss masking. Three instruction-response examples are packed into one training sequence. The attention mask is block-diagonal---each example attends only to itself. The loss mask selects only assistant tokens (shaded). User and system tokens contribute to attention context but not to the gradient.

## Prompt

```text
Draw a sequence packing and masking diagram for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system. LANDSCAPE orientation,
wide and spacious. Match the visual richness of Ch4 "Signal Density" token-level
detail and Ch10 "ICL Regime Spectrum" prompt block stacks.

CONCEPT:
"Context tokens are visible; assistant tokens are supervised." The figure should
make three masks visually distinct: packed examples, attention boundaries, and
loss supervision.

MAIN COMPOSITION:
Use a three-layer horizontal layout.

TOP LAYER — PACKED TOKEN SEQUENCE:
A long horizontal token strip spanning the page. It contains three packed
examples separated by thin vertical dividers:
Example A, Example B, Example C.
Inside each example, show role-colored token blocks:
- system tokens: very pale gray-blue
- user tokens: pale blue
- assistant tokens: primary blue
- padding tokens at the far right: light gray diagonal hatch
Use tiny labels above each role segment: system, user, assistant.

MIDDLE LAYER — ATTENTION MASK:
Below the token strip, draw a square attention matrix split into three
block-diagonal regions. Each diagonal block is filled with pale blue triangular
causal attention texture. Off-diagonal regions are blank/gray, with small "no
cross-example attention" labels. Add faint arrows from Example A/B/C in the
token strip to the corresponding diagonal blocks.

BOTTOM LAYER — LOSS MASK:
Below the matrix, draw a second thin token strip aligned with the top strip.
Only assistant tokens glow in soft orange (#FF9F43). User/system/padding tokens
are muted and labeled "context only" or "no loss." At the far right, show a
small equation card:
L_SFT = - sum m_t log p(x_t | x_<t) / sum m_t
with m_t = 1 only on assistant tokens.

STYLE:
Use primary blue #2D8CFF, pale blue #E8F4FD, border #CFE3F7, charcoal #1A1A2E,
steel gray #6B7280. Use soft orange #FF9F43 only for supervised assistant tokens
and the m_t=1 highlight. Clean technical textbook diagram; no dark background,
no gradient, no decorative icons. Keep all text legible.
```

## Review Checklist

- [ ] Block-diagonal attention mask is visually obvious.
- [ ] Assistant tokens are the only orange/supervised tokens.
- [ ] Padding, user, and system tokens are clearly not loss tokens.
- [ ] Equation card is compact and readable.
