# Figure 3.6: Rotary Position Embedding (RoPE) Intuition

**Filename**: `rope_rotation.png`
**LaTeX label**: `fig:rope-rotation`
**Caption**: Rotary Position Embedding (RoPE) encodes position by rotating pairs of dimensions in the query and key vectors. Each dimension pair rotates at a different frequency: low-index pairs rotate fast (distinguishing nearby tokens), high-index pairs rotate slowly (preserving long-range structure). The dot product between a rotated query and key depends only on their relative distance $t - s$, not on absolute positions.

## Prompt

```
Draw a diagram for a machine learning textbook explaining
Rotary Position Embedding (RoPE) intuitively.
Use the course's Zoom-inspired blue-white visual system.
The figure should be polished and editorial.

LAYOUT: Two panels side by side.

LEFT PANEL — "Rotation by position"
- Show a 2D coordinate plane (one pair of dimensions from
  the embedding vector)
- Draw 4 vectors from the origin, each representing the same
  token at different positions (pos 0, 1, 2, 3)
- Each vector has the same length but is rotated by an
  increasing angle:
  - pos 0: angle 0 (pointing right)
  - pos 1: rotated by θ
  - pos 2: rotated by 2θ
  - pos 3: rotated by 3θ
- Color: all vectors in medium blue (#2563EB)
- Label each vector endpoint: "pos 0", "pos 1", "pos 2", "pos 3"
- Show the angle θ between consecutive vectors with a small arc
- Title above: "Same token, different positions"
- Subtitle: "Each position rotates by angle θ"

RIGHT PANEL — "Different frequencies for different dimensions"
- Show 3 small clock-like circles stacked vertically,
  representing 3 dimension pairs
- Top clock: "dims 0-1" — hand rotates FAST
  (large angle between pos 0 and pos 1)
- Middle clock: "dims 2-3" — hand rotates MEDIUM
- Bottom clock: "dims 4-5" — hand rotates SLOW
  (small angle between pos 0 and pos 1)
- Each clock shows 2 hands in different blue shades:
  one for pos 0, one for pos 3
- The fast clock has large angular separation between hands
- The slow clock has small angular separation
- Title above: "Multi-frequency encoding"
- Subtitle: "Low dims → fast rotation → local discrimination"
  and "High dims → slow rotation → long-range structure"

ORANGE ACCENT:
- In the LEFT panel, highlight the angle arc between pos 1 and
  pos 3 in orange (#FF9F43), labeled "relative distance = 2"
- This emphasizes that the dot product depends on RELATIVE position

BOTTOM ANNOTATION (spanning both panels):
- "Key property: q_t · k_s depends on content and (t − s),
   not on absolute positions t or s"
- In charcoal text, centered

VISUAL STYLE:
- Clean, minimal coordinate axes (thin gray lines)
- Sans-serif labels in charcoal (#374151)
- White background (#FAFCFF)
- No shadows, no 3D, no heavy gradients
- Clock faces are simple circles with tick marks
- Polished editorial textbook figure style
```

## Review Checklist

- [ ] Left panel shows rotation increasing linearly with position
- [ ] Right panel shows different frequencies for different dimension pairs
- [ ] Fast rotation = low dimensions, slow rotation = high dimensions
- [ ] Orange accent highlights RELATIVE distance, not absolute position
- [ ] Bottom annotation mentions the key property: dot product depends on t − s
- [ ] No more than one orange focal element
- [ ] Labels are readable and mathematically correct
