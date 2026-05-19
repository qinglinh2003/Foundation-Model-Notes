# Figure 3.4: KV Cache — Prefill vs Decode

**Filename**: `kv_cache.png`
**LaTeX label**: `fig:kv-cache`
**Caption**: KV cache during autoregressive generation: prefill fills the cache, decode appends one entry per step.

## Prompt

```
Draw a KV cache diagram showing prefill and decode phases for autoregressive
Transformer generation, for a graduate-level machine learning textbook.
Use the course's blue-white visual system. Landscape orientation, polished
editorial style.

LAYOUT:
Two panels side by side, separated by a vertical divider or generous whitespace.

LEFT PANEL — PREFILL PHASE:
Title: "Prefill (parallel)"

Show 4 prompt tokens at the bottom: "The", "cat", "sat", "on"
- Each token is a small white pill with blue border

Above the tokens, show the attention computation:
- All 4 tokens processed in PARALLEL (arrows going up together)
- A blue block labeled "Attention Layer"
- Below the attention block, show a 4x4 attention matrix (lower triangular,
  representing causal mask)

To the right, show the KV CACHE being filled:
- A vertical stack of 4 colored blocks (all blue shades)
- Each block labeled: K1/V1, K2/V2, K3/V3, K4/V4
- Label: "KV Cache (filled)"
- Annotation: "All K/V computed in one pass"
- Small label: "Compute-bound"

RIGHT PANEL — DECODE PHASE:
Title: "Decode (sequential)"

Show the generation of token 5 ("the"):
- The 4 cached tokens shown as a faded/lighter column on the left
- One NEW token being generated, shown in Zoom Blue (#2D8CFF)

The attention computation for the new token:
- One query vector (q_5) in blue
- Attending to ALL 5 keys in the cache
- Show arrows from q_5 to each cached K (K1...K5)

The KV cache growing:
- Same vertical stack as left panel, but now with 5 entries
- The newest entry (K5/V5) highlighted in soft orange (#FF9F43)
  — this is the ONE orange accent, showing the NEW addition to cache
- Label: "Cache grows by 1 per step"
- Annotation: "Only K5/V5 computed; K1-K4 reused from cache"
- Small label: "Memory-bound"

BOTTOM ANNOTATION (spanning both panels):
"Prefill: process all prompt tokens in parallel (compute-bound).
 Decode: generate one token at a time, reusing cached K/V (memory-bound)."

VISUAL STYLE:
- Clean, spacious layout
- The KV cache should be visually prominent — it's the key concept
- Use consistent blue for cached entries, orange ONLY for the newly appended entry
- Zoom Blue (#2D8CFF) for processing blocks and cached entries
- Orange (#FF9F43) ONLY for the new K5/V5 cache entry
- White background (#FAFCFF)
- Sans-serif charcoal labels
```

## Review Checklist

- [ ] Two panels: Prefill (left) and Decode (right)
- [ ] Prefill shows ALL tokens processed in parallel
- [ ] Prefill fills the KV cache with K/V for all prompt tokens
- [ ] Decode shows ONE new token being generated
- [ ] Decode shows the new token's query attending to all cached keys
- [ ] KV cache grows by one entry (the new K5/V5)
- [ ] New cache entry is orange (only orange element)
- [ ] Labels: "Compute-bound" for prefill, "Memory-bound" for decode
- [ ] Cached entries are reused, not recomputed
- [ ] No extra colors beyond blue + white + orange
