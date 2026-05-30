# Figure 19.1: Prefill and Decode Timeline

**Filename**: `fig_prefill_decode_timeline.png`
**LaTeX label**: `fig:ch19-prefill-decode-timeline`
**Caption**: **Prefill and decode in one request.** Prefill processes the full prompt and fills the KV cache before the first token appears. Decode then streams tokens sequentially, appending new K/V entries at each step. TTFT and TPOT diagnose different bottlenecks.

## Prompt

```text
Draw a serving timeline diagram for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Show one LLM request split into prefill and decode. The reader should see that prefill handles all prompt tokens in parallel before the first token appears, while decode streams one token at a time and grows the KV cache.

MAIN COMPOSITION:
LEFT THIRD: "Input prompt" block with 4,000 small token chips entering a blue prefill engine. Show parallel arrows from prompt tokens into the engine. Label: "Prefill: parallel prompt processing".

CENTER: "Time to first token (TTFT)" bracket from request arrival to first output token. Under it show KV cache being initialized as stacked blue memory pages labeled K/V for prompt tokens.

RIGHT HALF: decode timeline with token boxes y1, y2, y3, ... yn appearing one by one. Each token has a small arrow down into a growing KV cache strip. Label repeated steps: "read cache", "produce next token", "append K/V".

BOTTOM STRIP: two metric cards:
- TTFT: dominated by prompt length, prefill compute, cache reuse
- TPOT: dominated by decode scheduling, memory bandwidth, batch size

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — use only on the first emitted token y1
- Text: #1A1A2E (headers), #6B7280 (annotations)
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
Do not make this look like a training pipeline.
Do not include backpropagation, gradients, or optimizer states.
Make the sequential nature of decode visually obvious.
Make TTFT and TPOT separate labels, not one generic latency label.
All text must be readable at 50% PDF width.
Fill the full width; avoid empty corners.
```

## Review Checklist

- [ ] Prefill and decode are visually distinct
- [ ] TTFT and TPOT are both labeled
- [ ] KV cache appears before and during decode
- [ ] Decode grows one token at a time
- [ ] Orange accent appears only on first output token
- [ ] No training/backprop elements
- [ ] Text readable at 50% PDF width
- [ ] Full landscape canvas is used
