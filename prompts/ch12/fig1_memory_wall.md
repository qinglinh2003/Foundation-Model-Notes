# Figure 12.1: Fine-Tuning Memory Wall

**Filename**: `fig_memory_wall.png`
**LaTeX label**: `fig:peft-memory-wall`
**Caption**: The fine-tuning memory wall. Peak GPU memory for full fine-tuning of a 7B model with Adam in mixed precision reaches over 112 GB---more than four times the capacity of a 24 GB consumer GPU. LoRA eliminates most optimizer cost; QLoRA additionally compresses the frozen base to 4-bit. The dominant cost shifts from optimizer states (full FT) to the base model (LoRA) to activations (QLoRA).

## Prompt

```text
Draw a fine-tuning memory comparison for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system. LANDSCAPE
orientation, wide and spacious. Match the visual richness of Ch10
"Prompt Sensitivity" two-panel contrast and Ch11 "Source Taxonomy"
full-width card layout.

CONCEPT:
Three fine-tuning regimes (Full FT, LoRA, QLoRA) compared as three
wide cards that fill the entire canvas horizontally. The visual
punchline: Full FT is physically impossible on a 24 GB GPU, LoRA
barely fits, QLoRA fits comfortably. Each card is a self-contained
"memory anatomy" showing what lives in GPU memory.

MAIN COMPOSITION:
THREE WIDE CARDS arranged side-by-side, filling the full landscape
width with small gaps between them. Each card has a thin blue border,
white background, and a header strip.

CARD 1 --- FULL FINE-TUNING (left third, ~33% width):
Header strip: "Full Fine-Tuning" in charcoal, with a charcoal warning
triangle icon and "112 GB total".
Inside the card, a top-to-bottom memory breakdown shown as wide
horizontal bands (not thin vertical columns). From top to bottom:
- "Parameters (bf16)" — medium blue bar labeled "14 GB"
- "Gradients (bf16)" — lighter blue bar labeled "14 GB"
- "Adam States (fp32)" — a VERY WIDE pale blue bar labeled "56 GB",
  visually dominating the card. Inside this bar, four tiny square
  tensor icons in a row: m, v, m-hat, v-hat.
- "Master Weights (fp32)" — medium-pale bar labeled "28 GB"
At the bottom of this card, a small consequence strip:
"Requires: 8x A100 cluster" with a dollar icon "$$$$".
A PROMINENT dashed orange (#FF9F43) line crosses all three cards
horizontally at the 24 GB level. In Card 1, this line cuts through
very early (below "Parameters"), with most of the card ABOVE it ---
visually showing that almost everything overflows.

CARD 2 --- LoRA (center third):
Header strip: "LoRA" in charcoal, with a blue checkmark icon and
"~20 GB total".
Inside, horizontal bars:
- "Frozen Base (bf16)" — medium blue with a small lock icon, "14 GB"
- "LoRA Adapters" — a TINY sliver, "~0.1 GB"
- "Adapter Optimizer" — small sliver, "~0.4 GB"
- "Activations" — pale blue, "4-8 GB"
The 24 GB threshold line passes near the top of this card --- the
content just barely fits under it. Small note: "Fits on: A100 40 GB".

CARD 3 --- QLoRA (right third):
Header strip: "QLoRA" in charcoal, with a blue checkmark icon and
"~8 GB total".
Inside, horizontal bars:
- "Frozen Base (4-bit NF4)" — compact bar with subtle diagonal hatch
  texture indicating quantization, "3.5 GB"
- "Adapters + Optimizer" — tiny sliver, "~0.5 GB"
- "Activations" — pale blue, "4-6 GB"
The 24 GB threshold line passes well above the content --- large
visible gap showing headroom. Small note: "Fits on: RTX 4090 24 GB".

24 GB THRESHOLD LINE:
A single horizontal dashed line in soft orange (#FF9F43) that spans
all three cards at the same y-position. At the right edge, a small
GPU card silhouette with "24 GB" label. This is the ONLY orange
element in the figure.

BOTTOM BANNER:
Below all three cards, a single wide white strip with thin border:
"Dominant cost:  optimizer states  -->  frozen base  -->  activations"
with small arrows between, showing how the bottleneck shifts across
regimes. This fills the bottom of the canvas.

STYLE:
- Background: #FAFCFF
- Card borders: thin #2D8CFF
- Bar segments: stepped blues from #2D8CFF through #7AB8F5, #B7D9F2,
  #D9EDFB --- no gradients, flat fills
- Quantized base: #B7D9F2 with subtle diagonal hatch texture
- Orange accent: #FF9F43 ONLY on 24 GB threshold line + GPU silhouette
- Text: #1A1A2E for headers/labels, #6B7280 for annotations
- Clean sans-serif typography
- Cards should be generous in width --- fill the canvas, no empty
  corners

IMPORTANT:
- Do not use 3D perspective or isometric views
- Do not use pie charts, donut charts, or circular layouts
- Do not use gradient fills or glow effects
- Do not use dark backgrounds or neon colors
- The three cards MUST fill the full landscape width edge-to-edge
  with only small gaps --- NO large empty regions
- Card 1's content must visually overflow well past the 24 GB line
- All numeric labels readable at 50% PDF width
- Horizontal bar layout inside cards, NOT vertical columns
```

## Review Checklist

- [ ] Three cards fill the full landscape width (no empty right corner)
- [ ] Full FT card shows ~112 GB total, with Adam States visually dominant
- [ ] Mini tensor icons (m, v, m-hat, v-hat) visible inside Adam bar
- [ ] 24 GB threshold line in orange crosses all three cards
- [ ] Full FT content overflows far past 24 GB line
- [ ] LoRA bar sits near but under 24 GB line
- [ ] QLoRA bar sits well below with visible headroom
- [ ] Quantized base has distinct hatch/mesh texture
- [ ] Lock icon on frozen base segments
- [ ] Bottom banner shows dominant-cost shift across regimes
- [ ] GPU card silhouette at right end of threshold line
- [ ] Orange used ONLY for threshold line and GPU silhouette
- [ ] No empty corners or unbalanced whitespace
- [ ] Readable at 50% width in PDF
