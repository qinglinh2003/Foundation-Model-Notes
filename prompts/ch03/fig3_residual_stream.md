# Figure 3.3: The Residual Stream

**Filename**: `residual_stream.png`
**LaTeX label**: `fig:residual-stream`
**Caption**: The residual stream as the backbone of a decoder-only Transformer.

## Prompt

```
Draw a residual stream diagram for a decoder-only Transformer, for a graduate-level
machine learning textbook. Use the course's blue-white visual system. Landscape
orientation, polished editorial style.

CONCEPT:
The key insight is that the residual stream — not attention — is the backbone
of a Transformer. Attention and FFN modules are "reader-writer" tributaries
that contribute additive updates to a persistent stream.

LAYOUT:
The diagram shows 3 decoder layers side by side (left to right = depth),
with the residual stream as a wide horizontal band flowing through all layers.

MAIN ELEMENT — THE RESIDUAL STREAM:
- A wide horizontal band (like a river or highway) flowing from left to right
- Starts at the left with "Embedding + PE" and ends at the right with "LM Head"
- Use a light blue fill (#E8F4FD) with a darker blue border (#2D8CFF)
- This band should be the WIDEST and most visually prominent element
- Label it: "Residual Stream (T x d_model)"
- The stream maintains constant width throughout — it is never narrowed or broken

AT EACH LAYER (3 layers shown):
- Two modules branch OFF the stream and then merge BACK:

  Module 1 (above the stream):
  - A rounded blue box labeled "LN + MHA"
  - An arrow goes UP from the stream into this box (reading)
  - An arrow comes DOWN from this box back to the stream with a "+" symbol (writing)
  - Small label: "inter-token mixing"

  Module 2 (below the stream):
  - A rounded blue box labeled "LN + FFN"
  - An arrow goes DOWN from the stream into this box (reading)
  - An arrow comes UP from this box back to the stream with a "+" symbol (writing)
  - Small label: "per-token transform"

- The "+" symbols (additive updates) should use soft orange (#FF9F43)
  — this is the ONE orange accent, highlighting that updates are ADDITIVE

ANNOTATIONS:
- Left side: "x^(0) = E_{w_t} + PE_t" near the stream start
- Right side: "x^(L)" near the stream end
- Between layers: small labels "Layer 1", "Layer 2", "Layer 3"
- Below the whole diagram, a one-line annotation:
  "The stream is never replaced — each module adds to it."

VISUAL METAPHOR:
- The stream should feel like a highway or river
- The MHA and FFN modules are like tributaries or on-ramps
- The "+" symbols emphasize that information accumulates, not replaces

STYLE:
- The residual stream band should be the dominant visual element
- MHA and FFN boxes are smaller, secondary
- Zoom Blue (#2D8CFF) for all processing blocks
- Light blue (#E8F4FD) for the stream fill
- Orange (#FF9F43) ONLY for the "+" additive symbols
- White background (#FAFCFF)
- Sans-serif charcoal labels
```

## Review Checklist

- [ ] Residual stream is the DOMINANT visual element (wide horizontal band)
- [ ] Stream flows continuously from embedding to LM head — never broken
- [ ] MHA modules branch off ABOVE and merge back with "+"
- [ ] FFN modules branch off BELOW and merge back with "+"
- [ ] "+" symbols are orange (only orange element)
- [ ] Three layers shown
- [ ] Labels: "inter-token mixing" for MHA, "per-token transform" for FFN
- [ ] Stream maintains constant width throughout
- [ ] No extra colors beyond blue + white + orange
