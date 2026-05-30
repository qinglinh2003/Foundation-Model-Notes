# Figure 19.5: Speculative Decoding

**Filename**: `fig_speculative_decoding.png`
**LaTeX label**: `fig:ch19-speculative-decoding`
**Caption**: **Speculative decoding.** A small draft model proposes multiple future tokens. The target model verifies them in parallel and accepts a prefix of the draft when it matches the target distribution. The gain is lower decode latency, not new reasoning capability.

## Prompt

```text
Draw a speculative decoding pipeline for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Show that a cheap draft model proposes several tokens, then the expensive target model verifies those tokens in parallel. Accepted tokens advance the sequence; rejected tokens trigger correction. Emphasize latency reduction, not better reasoning.

MAIN COMPOSITION:
LEFT: current prefix tokens in a blue strip.

CENTER TOP: small "draft model" box quickly proposing tokens y1 y2 y3 y4 y5. Use light blue token chips and speed lines.

CENTER BOTTOM: large "target model verification" box evaluating the proposed tokens in one parallel pass. Show check marks over y1 y2 y3 and an X over y4.

RIGHT: output prefix advances by accepted tokens y1 y2 y3; rejected token y4 is replaced by target-sampled token z4. Show loop arrow back to draft model.

BOTTOM METRIC STRIP:
Helps when: high acceptance rate, expensive target, decode-heavy workload.
Does not mean: higher quality, best-of-N, verifier reranking.

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — use only on the rejected token y4
- Text: #1A1A2E (headers), #6B7280 (annotations)
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
Do not depict multiple candidate answers or voting.
Do not imply the draft model improves quality.
Make parallel target verification visually distinct from sequential decode.
Make accepted prefix and rejected token obvious.
All text readable at 50% PDF width.
Use full landscape width.
```

## Review Checklist

- [ ] Draft model and target model are distinct
- [ ] Multiple draft tokens are proposed
- [ ] Target verifies in parallel
- [ ] Accepted prefix and rejected token are clear
- [ ] Bottom strip says latency, not quality
- [ ] Orange accent only marks rejected token
- [ ] Text readable at 50% PDF width
- [ ] No best-of-N or voting imagery
