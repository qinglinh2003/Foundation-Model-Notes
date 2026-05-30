# Figure 19.2: Serving Memory Budget and KV Cache

**Filename**: `fig_memory_budget_kv_cache.png`
**LaTeX label**: `fig:ch19-memory-budget-kv-cache`
**Caption**: **Serving memory budget.** Weights occupy a fixed block; KV cache grows with active requests, context length, and generated tokens. Paged KV-cache management reduces fragmentation by storing sequences in reusable blocks rather than requiring one contiguous region per request.

## Prompt

```text
Draw a memory budget diagram for LLM serving in a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Show that serving memory has a fixed weight block and a dynamic KV-cache region that grows with concurrency and context length. Show why paged KV cache reduces fragmentation.

MAIN COMPOSITION:
LEFT PANEL: a GPU memory bar labeled "80 GB GPU memory". Inside it, a fixed dark-blue block labeled "7B bf16 weights ≈ 14 GB". Next to it show runtime overhead as a small pale block.

CENTER PANEL: dynamic KV cache blocks for three requests:
- Request A: 2K prompt + 200 decode tokens
- Request B: 8K prompt + 1K decode tokens
- Request C: 1K prompt + 50 decode tokens
Represent K/V as stacked blue pages. Request B should visibly consume much more cache.

RIGHT PANEL: "Paged KV cache" with many equal-size memory pages, a logical-to-physical mapping table, and small gaps avoided. Contrast with a faint crossed-out "contiguous reservation" strip showing fragmented holes.

BOTTOM FORMULA STRIP:
KV per request ≈ 2 × L × n_kv × T × d_k × bytes
Batch KV ≈ sum over active requests

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — use only to highlight "Request B: long context"
- Text: #1A1A2E (headers), #6B7280 (annotations)
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
Do not show optimizer states or gradients.
Do not imply weights grow with request length.
Make KV cache growth with T and concurrency visually dominant.
Make paged allocation understandable without dense text.
Use concrete numbers: 14 GB, 80 GB, 2K, 8K, 1K.
All text readable at 50% PDF width.
```

## Review Checklist

- [ ] Fixed weight memory and dynamic KV memory are clearly separated
- [ ] Long-context request uses visibly more cache
- [ ] Paged allocation contrasts with fragmentation
- [ ] Formula strip is legible
- [ ] Orange accent only highlights the long request
- [ ] No training memory terms
- [ ] Concrete numbers included
- [ ] Full canvas used
