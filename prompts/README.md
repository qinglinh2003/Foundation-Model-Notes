# Figure Generation Prompts

This directory contains ChatGPT (GPT-Image-2) prompts for generating textbook figures,
organized by chapter.

## Workflow

1. Open a **new ChatGPT conversation** on chat.openai.com
2. Paste the **session preamble** below as your first message
3. Paste each figure prompt one at a time
4. Review each figure for technical correctness before downloading
5. Save downloaded PNGs to `figures/ch{NN}/` with the filename specified in the prompt file
6. If a figure is wrong, don't regenerate from scratch — send a targeted correction in the same conversation

Recommended output path:

```text
figures/
├── ch01/
│   ├── rnn_unrolled.png
│   ├── lstm_cell.png
│   ├── gru_cell.png
│   ├── seq2seq_bottleneck.png
│   ├── attention_alignment.png
│   ├── word2vec_embedding_space.png
│   └── sequential_vs_parallel.png
├── ch02/
│   ├── scaled_dot_product_attention.png
│   ├── causal_mask.png
│   ├── multi_head_attention.png
│   └── transformer_block.png
├── ch03/
│   ├── three_architectures.png
│   ├── gpt_forward_pass.png
│   ├── residual_stream.png
│   ├── kv_cache.png
│   ├── shifted_labels.png
│   ├── rope_rotation.png
│   ├── activation_functions.png
│   └── mha_vs_gqa.png
└── ch04/
    ├── causal_vs_bidirectional.png
    ├── mlm_training.png
    ├── signal_density.png
    ├── bert_input_format.png
    ├── pretrain_finetune.png
    ├── rag_pipeline.png
    ├── bert_vs_jepa.png
    └── bert_family_evolution.png
└── ch05/
    ├── granularity_comparison.png
    ├── bpe_trace.png
    ├── multilingual_tokens.png
    ├── training_pipeline.png
    └── lr_schedule.png
```

## Design Language: Tech Blue-White (Zoom-inspired)

All figures follow a unified visual identity inspired by Zoom's clean tech aesthetic.
The goal is not a plain whiteboard sketch. The figures should feel like polished
editorial illustrations for a modern graduate AI textbook: crisp, spacious,
technical, and visually coherent across chapters.

### Color Palette

| Role | Color | Hex | Usage |
|------|-------|-----|-------|
| Primary Blue | Zoom Blue | `#2D8CFF` | Main blocks, fills, primary elements |
| Deep Blue | Navy | `#0B5CFF` | Outlines, headers, emphasis borders |
| Light Blue | Ice | `#E8F4FD` | Background regions, soft fills |
| Pale Blue | Mist | `#F0F7FF` | Subtle region backgrounds |
| Dark Text | Charcoal | `#1A1A2E` | Labels, annotations |
| Medium Gray | Steel | `#6B7280` | Secondary labels, axis text |
| Light Gray | Smoke | `#F3F4F6` | Inactive elements, dashed borders |
| Background | White | `#FAFCFF` | Page background (very slight blue tint) |
| Accent (warm) | Soft Orange | `#FF9F43` | Bottlenecks, warnings, emphasis (use sparingly) |

### Rules

- **Blue is the dominant color.** 80%+ of colored elements should be in the blue family.
- **Soft Orange is the only warm color**, used sparingly for one focal element per figure (e.g., bottleneck, critical path).
- **No coral, no teal, no purple, no green, no rainbow.** If you need a secondary distinction, use opacity/shade variations of blue.
- Backgrounds are white or ice blue. Never gray or dark.
- Shadows are very subtle (#0B5CFF at 8% opacity), just enough for depth.
- Gradients only within blue hues (light blue → Zoom Blue), never cross-hue.
- Use the same visual grammar everywhere:
  - Processing blocks: rounded rectangles with blue fills.
  - Tokens: small white pill capsules with blue borders.
  - Operations: white circles with deep-blue outlines.
  - Regions: translucent pale-blue rounded panels.
  - Primary flow arrows: deep blue.
  - Secondary/helper arrows: steel gray.
  - One key limitation or mechanism per figure may be orange.
- Avoid decorative illustration habits: no floating icons, no ornamental frames,
  no abstract background patterns, no glossy app UI cards.

### Figure Style Lock

When a figure from a previous chapter looks good, use it as a style reference for
the next one. In ChatGPT, upload or reference the approved image and say:

```text
Match this exact figure style: same blue-white palette, rounded geometry,
line weights, arrow style, shadows, typography, spacing, and background.
Change only the technical content requested in the new prompt.
```

## Session Preamble (paste this first)

```
I am generating diagrams for a graduate-level machine learning textbook. All
figures must share a unified visual identity: clean, modern, tech-inspired,
using a blue-and-white color scheme similar to Zoom's design language.

MANDATORY COLOR PALETTE for ALL figures:
- Primary: #2D8CFF (bright tech blue) — main blocks, nodes, fills
- Deep: #0B5CFF (darker blue) — outlines, borders, emphasis
- Light fill: #E8F4FD (ice blue) — background regions, soft fills
- Mist: #F0F7FF (pale blue) — subtle region grouping
- Text: #1A1A2E (charcoal) — labels, annotations
- Secondary text: #6B7280 (steel gray) — axis labels, notes
- Background: #FAFCFF (near-white with very slight blue tint)
- Accent: #FF9F43 (soft orange) — use ONLY for one focal/emphasis element
  per figure (e.g., a bottleneck, a critical arrow). Never more than 10%
  of the figure's colored area.

VISUAL STYLE:
- Clean vector-like shapes. Rounded rectangles for processing blocks.
- Circles for operation nodes.
- Smooth, medium-weight arrows with clean pointed heads.
- Very subtle shadows (blue-tinted, not black) for gentle depth.
- Single-hue gradients allowed only within blue range.
- Generous whitespace. Strong alignment. Consistent spacing.
- Landscape orientation (wider than tall).
- Left-to-right or top-to-bottom reading flow.
- Balanced editorial composition: the diagram should look intentionally designed,
  not like a raw slide or a rough sketch.

TYPOGRAPHY:
- Sans-serif (Inter, Helvetica Neue, or similar).
- Crisp, high-contrast labels. Short text only — prefer symbols.
- Section labels may use bold or small caps.
- Subscript notation: x_t, h_t, c_t.

DO NOT:
- Use more than one warm/non-blue color.
- Use coral, teal, purple, green, neon, or rainbow colors.
- Use clip art, icons, emoji, photorealistic textures.
- Use heavy 3D, glassmorphism, neon glow, cartoon style.
- Make it look like a SaaS dashboard or marketing graphic.
- Render complex LaTeX formulas — I will overlay those later.
- Invent data or numbers not specified in the prompt.

The overall aesthetic should feel like: Zoom's UI meets a high-quality
research monograph. Professional, trustworthy, minimal, blue.

I will provide one figure prompt at a time. Generate each figure and wait
for my feedback before moving on.
```

## Targeted Correction Templates

```text
Keep the same composition and blue-white style. Fix only:
1. [specific issue]
2. [specific issue]
Do not change anything else. Do not introduce new colors.
```

```text
The figure looks great visually but has a technical error:
[describe the error precisely]
Regenerate with only this fix. Keep all visual styling identical.
```

```text
The layout is correct but needs more polish. Please:
- Make the blue fills more vibrant (#2D8CFF)
- Add very subtle blue-tinted shadows
- Ensure all labels are crisp and readable
Preserve all labels, arrows, and structural elements exactly.
Do not change the color palette.
```

## QA Checklist (check each figure before downloading)

- [ ] Arrow directions are technically correct
- [ ] All specified labels are present and spelled correctly
- [ ] No extra labels or elements were hallucinated
- [ ] Gate connections are correct (for LSTM, Transformer, etc.)
- [ ] Axes are not swapped (for heatmaps, plots)
- [ ] Style is consistent with previous figures in the session
- [ ] Only blue + white + (optional one soft orange element) — no other colors
- [ ] No watermarks or extra text
- [ ] Figure remains readable when displayed at 50% width in the PDF
- [ ] Color palette matches the Zoom blue-white scheme

## Quality Bar

Use generated images directly only when all of these are true:

- The diagram is conceptually simple.
- The figure does not encode exact experimental data.
- Labels are short and correctly rendered.
- A reader could not reasonably misunderstand the technical mechanism.

Prefer Python, TikZ, or manual vector editing when:

- The figure contains exact numbers, axes, or plotted data.
- The diagram has many labels or formulas.
- A wrong arrow would change the scientific claim.
- The figure needs publication-grade vector editing.

## Tips from Community Research

- **Structure first, style second**: define spatial layout and components before aesthetics
- **Lock text in quotes**: short labels only; long text inside images still fails often
- **Surgical corrections**: don't regenerate, say "Keep composition. Fix only: [specific change]"
- **One variable per iteration**: if trying variants, change only one thing at a time
- **Color discipline**: if GPT adds unauthorized colors, immediately correct: "Remove all non-blue colors except the single orange accent"
- **Use references when available**: upload a rough sketch or a previous approved figure
  and ask ChatGPT to preserve the layout while matching style
- **Avoid synthetic data claims**: do not let the image model invent numeric values
