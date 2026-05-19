# Figure 2.4: The Transformer Block

**Filename**: `transformer_block.png`
**LaTeX label**: `fig:transformer-block`
**Caption**: A single Transformer block (pre-norm variant). The input passes through layer normalization, multi-head attention, and a residual connection, then through another normalization, feed-forward network, and residual connection. The residual paths (orange) serve the same gradient-highway role as the LSTM cell state.

## Prompt

```
Draw a single Transformer block diagram for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
The figure should be polished and editorial. Show the PRE-NORM variant.

OVERALL LAYOUT:
- Portrait/vertical orientation (taller than wide)
- Data flows from BOTTOM to TOP
- Two main sub-layers stacked vertically

STRUCTURE (bottom to top):

1. INPUT (bottom):
   - Rounded rectangle labeled "X"
   - The input splits into two paths: one goes through the sub-layer,
     one goes directly as the residual

2. FIRST SUB-LAYER (Attention):
   a. "Layer Norm" box — light gray (#F3F4F6) fill
   b. "Multi-Head Attention" box — Zoom Blue (#2D8CFF) fill, this is
      the largest box in this sub-layer
   c. An addition node "+" where the attention output and the residual
      path merge

3. RESIDUAL CONNECTION 1:
   - Draw a curved or straight bypass arrow from before Layer Norm
     directly to the "+" node
   - Color this residual path in soft orange (#FF9F43)
   - This is one of the orange accents

4. SECOND SUB-LAYER (FFN):
   a. "Layer Norm" box — light gray fill
   b. "Feed-Forward Network" box — Zoom Blue fill
      Small annotation inside or beside: "2 linear layers + activation"
   c. Another addition node "+"

5. RESIDUAL CONNECTION 2:
   - Another orange bypass arrow from after the first "+" node to
     the second "+"
   - Same orange color

6. OUTPUT (top):
   - Rounded rectangle labeled "Output"

VISUAL EMPHASIS:
- The TWO orange residual bypass arrows should be the most visually
  striking elements — they show the gradient highway
- The main processing path (Layer Norm → MHA → +, Layer Norm → FFN → +)
  uses blue boxes
- "+" nodes should be orange-outlined circles

LABELS:
- Each box clearly labeled
- Small annotation near residual paths: "residual (gradient highway)"

STYLE:
- Sans-serif labels in charcoal (#1A1A2E)
- White or very pale blue (#FAFCFF) background
- Clean, spacious layout with generous padding between boxes
- No shadows, no heavy gradients, no 3D effects
- Subtle depth cues OK
- Polished editorial textbook figure
```

## Review Checklist

- [ ] Shows PRE-NORM variant (Layer Norm BEFORE attention/FFN, not after)
- [ ] Two sub-layers: attention + FFN
- [ ] Each sub-layer has: Layer Norm → computation → residual add
- [ ] Two residual connections clearly shown as bypass paths
- [ ] Residual paths use orange accent
- [ ] FFN described as "2 linear layers + activation"
- [ ] Addition nodes present where residual meets main path
- [ ] Data flows bottom to top
- [ ] All labels readable
