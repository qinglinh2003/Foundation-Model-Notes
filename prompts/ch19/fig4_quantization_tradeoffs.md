# Figure 19.4: Quantization Targets for Serving

**Filename**: `fig_quantization_tradeoffs.png`
**LaTeX label**: `fig:ch19-quantization-tradeoffs`
**Caption**: **Quantization targets for serving.** Weight quantization reduces model footprint; activation quantization can accelerate matmuls when kernels support it; KV-cache quantization expands batch and context capacity. Each target has a different quality and systems risk.

## Prompt

```text
Draw a quantization tradeoff diagram for LLM serving in a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Show that "quantization" can target weights, activations, or KV cache, and each target changes a different bottleneck. The reader should not think bit width alone determines speed or quality.

MAIN COMPOSITION:
THREE LARGE CARDS across the canvas:
1. "Weight quantization" with a model-weight block shrinking from bf16 14 GB to int4 3.5 GB. Benefits: lower footprint, less weight bandwidth. Risk: quality loss on hard tasks.
2. "Activation quantization" with a matmul tile labeled W8A8 and a small outlier warning icon. Benefits: faster kernels when supported. Risk: activation outliers.
3. "KV-cache quantization" with cache pages changing from bf16 to int8/int4 and more concurrent request icons fitting. Benefits: longer context, bigger batches. Risk: attention quality over long contexts.

BOTTOM STRIP: "Compression is not speed unless kernels use it" with tiny GPU kernel icon and backend label.

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — use only for the "kernel support required" warning
- Text: #1A1A2E (headers), #6B7280 (annotations)
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
Do not present quantization as universally free.
Do not mix finetuning optimizer memory into the figure.
Keep weight, activation, and KV-cache targets visually distinct.
Use concrete numbers in the weight card.
All text readable at 50% PDF width.
No large empty spaces.
```

## Review Checklist

- [ ] Three quantization targets are distinct
- [ ] Weight card includes 14 GB to 3.5 GB example
- [ ] KV-cache card shows more concurrency/context capacity
- [ ] Kernel support warning is visible
- [ ] Orange accent only on warning
- [ ] No finetuning optimizer states
- [ ] Text readable at 50% PDF width
- [ ] Canvas is full and balanced
