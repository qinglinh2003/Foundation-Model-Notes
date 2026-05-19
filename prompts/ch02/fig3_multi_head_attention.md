# Figure 2.3: Multi-Head Attention

**Filename**: `multi_head_attention.png`
**LaTeX label**: `fig:mha`
**Caption**: Multi-head attention with $h$ parallel heads. The input is projected into $h$ independent query-key-value triples, each producing a separate attention output. These are concatenated and linearly projected back to the model dimension, allowing different heads to capture different types of relationships.

## Prompt

```
Draw a multi-head attention diagram for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
The figure should be polished and editorial.

OVERALL LAYOUT:
- Landscape orientation, generous whitespace
- Data flows from BOTTOM to TOP

STRUCTURE (bottom to top):

1. INPUT (bottom):
   - A single wide rounded rectangle labeled "X ∈ R^{T×d}"
   - Zoom Blue (#2D8CFF) fill

2. LINEAR PROJECTIONS:
   - Three sets of h parallel narrow rectangles branching out from X
   - Left set: labeled "W_Q^1 ... W_Q^h" (query projections)
   - Center set: labeled "W_K^1 ... W_K^h" (key projections)
   - Right set: labeled "W_V^1 ... W_V^h" (value projections)
   - Show h=3 heads explicitly (3 parallel lanes)
   - Use three slightly different shades of blue for the three heads:
     Head 1: #0B5CFF (deep blue)
     Head 2: #2D8CFF (zoom blue)
     Head 3: #6BB5FF (light blue)

3. PARALLEL ATTENTION:
   - h=3 separate "Scaled Dot-Product Attention" boxes arranged horizontally
   - Each box receives its own Q_i, K_i, V_i
   - Label each box "Head 1", "Head 2", "Head 3"
   - Use the same blue shade as its corresponding projection

4. CONCAT:
   - All h head outputs converge into a "Concat" operation node
   - Use orange (#FF9F43) outline for the concat node — this is the ONE
     orange accent, emphasizing the merge point

5. FINAL LINEAR:
   - A rounded rectangle labeled "W_O"
   - Standard Zoom Blue

6. OUTPUT (top):
   - A rounded rectangle labeled "MultiHead(X)"

VISUAL EMPHASIS:
- The parallel lanes (3 heads) should be the main visual feature
- Each head's lane should be visually distinct via its blue shade
- The concat merge point in orange draws attention to where heads reunite
- Show that each head operates independently on its own subspace

ARROWS:
- Clean thin arrows connecting stages
- Arrows within each head's lane use that head's blue shade

STYLE:
- Sans-serif labels in charcoal (#1A1A2E)
- White or very pale blue (#FAFCFF) background
- No shadows, no heavy gradients, no 3D effects
- Subtle depth cues OK (very light shadow on boxes)
- Polished editorial textbook figure
```

## Review Checklist

- [ ] Shows 3 parallel heads, each with its own Q, K, V projections
- [ ] Each head has a separate attention computation
- [ ] Outputs are concatenated (not averaged or summed)
- [ ] Final linear projection W_O is present after concat
- [ ] Three different blue shades distinguish the heads
- [ ] Orange accent only on the concat node
- [ ] Input is X, output is MultiHead(X)
- [ ] All labels readable
