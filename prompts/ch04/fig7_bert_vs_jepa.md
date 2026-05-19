# Figure 4.7: BERT vs JEPA — Input-Space vs Latent-Space Prediction

**Filename**: `bert_vs_jepa.png`
**LaTeX label**: `fig:bert-vs-jepa`
**Caption**: BERT predicts masked tokens in input space (left); JEPA predicts masked representations in latent space (right). Both learn through masking, but JEPA avoids surface-level reconstruction.

## Prompt

```
Draw a comparison between BERT and JEPA architectures for a graduate-level
machine learning textbook. Use the course's blue-white visual system.
Landscape orientation, polished editorial style.

LAYOUT:
Two panels side by side, showing how each architecture handles masked prediction.

LEFT PANEL — BERT (Input-Space Prediction):
- Title: "BERT: Predict in Input Space"
- Top: Input sequence with some tokens masked: "The [MASK] sat on the [MASK]"
- Middle: Blue encoder block processing the full corrupted input
- Bottom: Predictions pointing back to TOKEN IDs
  - Position 2: predicting "cat" (token #3797)
  - Position 6: predicting "mat" (token #13523)
- Loss annotation: "CE loss against original token IDs"
- Small note: "Must distinguish 'cat' from 'kitten' from 'feline'..."
  (showing the surface-level disambiguation problem)

RIGHT PANEL — JEPA (Latent-Space Prediction):
- Title: "JEPA: Predict in Latent Space"
- Top: Input divided into two regions:
  - "Context" region (visible tokens): processed by "Context Encoder" (blue)
  - "Target" region (masked tokens): processed by "Target Encoder (EMA)" (lighter blue)
- Middle: A small "Predictor" network (in soft orange #FF9F43)
  takes context representation and predicts target representation
- Bottom: Loss computed as L2 distance between:
  - Predicted representation (from Predictor)
  - Actual target representation (from Target Encoder)
- Loss annotation: "||pred_repr - target_repr||² in latent space"
- Small note: "'cat' and 'kitten' map to similar representations → both OK"

KEY DIFFERENCES (center or bottom annotation):
A comparison table or annotation:
- BERT: "Predicts exact tokens → wastes capacity on synonyms"
- JEPA: "Predicts representations → abstracts away surface details"

ARCHITECTURAL DETAIL (right panel):
- Show the EMA (exponential moving average) arrow from Context Encoder
  to Target Encoder, labeled "EMA update (no gradient)"
- Show stop-gradient symbol on the target representation
- The Predictor is lightweight/small compared to the encoders

VISUAL DETAILS:
- Zoom Blue (#2D8CFF) for both encoders and BERT
- Soft Orange (#FF9F43) for the Predictor network in JEPA —
  this is the figure's orange accent, highlighting the novel component
- Lighter/faded blue for Target Encoder (to show it's EMA, not directly trained)
- White/ice blue (#FAFCFF) background
- Dashed arrow for EMA update
- "sg" (stop-gradient) symbol on target representation
- Sans-serif labels in charcoal (#1A1A2E)
```

## Review Checklist

- [ ] Two panels clearly showing BERT (left) and JEPA (right)
- [ ] BERT: prediction targets are token IDs (discrete, input space)
- [ ] JEPA: prediction targets are latent representations (continuous, abstract)
- [ ] Predictor network highlighted in orange (key novel component)
- [ ] Target Encoder shown with EMA arrow (not gradient-trained)
- [ ] Stop-gradient indicated on target representations
- [ ] Annotation about synonym problem: BERT must distinguish, JEPA doesn't need to
- [ ] Architectural difference clear: BERT = one encoder + MLM head; JEPA = context encoder + target encoder + predictor
