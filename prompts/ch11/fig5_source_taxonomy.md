# Figure 11.5: Instruction Data Source Landscape

**Filename**: `fig_source_taxonomy.png`
**LaTeX label**: `fig:source-taxonomy`
**Caption**: Instruction data source landscape. The four source categories occupy different regions of the quality-scale trade-off space. Human-written data is highest quality but smallest scale. Template-based data is massive but formulaic. LLM-generated and distillation data fill the middle ground. Modern practice combines multiple sources.

## Prompt

```text
Draw an instruction data source landscape for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system. LANDSCAPE orientation,
wide and spacious. Match the visual richness of Ch9 "Source Composition" and
Ch10 "Evaluation Workflow": each category should contain a concrete miniature
scene, not just a label.

CONCEPT:
"Data is the moat." Show four instruction-data sources as regions in a
quality-scale landscape. The visual should communicate trade-offs: human data is
high quality but small; template data is huge but formulaic; LLM-generated data
scales cheaply; distillation has high response quality but licensing risk.

MAIN COMPOSITION:
A large 2D map on a white panel:
- x-axis: Scale (small -> large)
- y-axis: Response quality / naturalness (low -> high)
Use thin blue axes, charcoal labels, and light grid lines.

FOUR SOURCE REGIONS:
1. Human-written demonstrations: upper-left. Show a small annotator desk icon,
   handwritten response card, and "$5-$50/example" cost tag.
2. Template-based / FLAN: lower-right. Show repeated template cards generated
   from a dataset table, with a "massive but formulaic" tag.
3. LLM-generated / Self-Instruct: middle-right. Show a model chip producing many
   instruction cards, with a small diversity warning marker.
4. Distillation from frontier models: upper-middle/right. Show a large teacher
   model sending polished response cards to a smaller student model, with a
   small license/terms tag.

MIXTURE CALLOUT:
At the bottom, add a wide white callout card:
"Modern SFT mixes sources: high-quality core + synthetic scale."
Highlight "mixes sources" in soft orange (#FF9F43). This is the only orange
element.

STYLE:
Use primary blue #2D8CFF, pale blue #E8F4FD, border #CFE3F7, charcoal #1A1A2E,
steel gray #6B7280, soft orange #FF9F43 for one accent only. Avoid dark
backgrounds, 3D effects, business-slide style, and large decorative gradients.
Use concise labels only.
```

## Review Checklist

- [ ] Axes show quality and scale clearly.
- [ ] Each source has a concrete internal visual.
- [ ] Distillation includes a small licensing/terms warning.
- [ ] Bottom callout emphasizes mixture, not a single best source.
