# Figure 7.3: DDP to FSDP — The Sharding Spectrum

**Filename**: `ddp_to_fsdp.png`
**LaTeX label**: `fig:ddp-to-fsdp`
**Caption**: The DDP-to-FSDP spectrum: each stage shards one more component of the training state, trading communication for memory. At ZeRO-3/FSDP, everything is sharded --- each GPU holds only 1/G of every component.

## Prompt

```text
Draw a state-placement comparison infographic for a graduate-level machine
learning textbook. Use the course's blue-white visual system (#2D8CFF primary
blue, white/light-blue backgrounds). Landscape orientation, polished editorial
style.

THIS IS THE MOST IMPORTANT FIGURE IN CHAPTER 7. It must be beautiful,
clear, and immediately convey the central insight: distributed training
strategies form a continuous spectrum from "replicate everything" to
"shard everything."

VISUAL METAPHOR — MOVING TRUCKS:
Think of 4 moving trucks (= 4 GPUs). In DDP, each truck carries a complete
copy of all furniture. In FSDP, each truck carries only 1/4 of the furniture
and they coordinate to assemble the full set when needed.

LAYOUT:
Four vertical "CARDS" arranged left to right, each representing a strategy.
The cards should look like the scale-gap cards in Figure 6.1 — clean,
modern, with consistent internal layout.

Each card contains:
- A TITLE at the top
- A VISUAL REPRESENTATION of 4 GPUs and their contents
- A MEMORY NUMBER
- A ONE-LINE DESCRIPTION at the bottom

CARD 1 — DDP:
- Title: "DDP"
- Visual: 4 GPU icons, each containing 4 FULL-SIZE colored blocks stacked:
  Parameters (blue), Gradients (cyan), Adam m (navy), Adam v (dark teal)
  ALL blocks are full-size and identical across GPUs
- Memory: "112 GB / GPU"
- Description: "Everything replicated"
- The GPUs should look HEAVY — visually stuffed with data

CARD 2 — ZeRO Stage 1:
- Title: "ZeRO-1"
- Visual: 4 GPU icons. Parameters and Gradients are still FULL-SIZE.
  Adam m and Adam v are THIN (1/4 width or faded) — only a shard on each GPU
- Memory: "37 GB / GPU"
- Description: "Optimizer states sharded"
- The GPUs should look slightly LIGHTER than DDP

CARD 3 — ZeRO Stage 2:
- Title: "ZeRO-2"
- Visual: 4 GPU icons. Only Parameters are FULL-SIZE.
  Gradients, Adam m, Adam v are all THIN/sharded
- Memory: "31 GB / GPU"
- Description: "+ Gradients sharded"
- The GPUs look noticeably lighter

CARD 4 — ZeRO-3 / FSDP:
- Title: "ZeRO-3 / FSDP"
- Visual: 4 GPU icons. ALL components (P, G, M, V) are THIN/sharded.
  Each GPU holds only 1/4 of everything
- Memory: "28 GB / GPU"
- Description: "Everything sharded"
- The GPUs look MINIMAL — almost empty compared to DDP
- THIS CARD should have an ORANGE (#D35400) accent border or title
  highlight to mark it as the recommended default

GPU ICON STYLE:
- Use simplified flat GPU icons, not photorealistic hardware.
- Each GPU should be a clean icon/card hybrid: rounded device silhouette,
  subtle fan/circuit hints, and enough interior space to show state blocks.
- The icons should be elegant and minimal, closer to editorial vector design
  than to real hardware diagrams.
- The data/state blocks inside each GPU are the important visual signal.

VISUAL ENCODING FOR "SHARDED" VS "REPLICATED":
The key design challenge. Suggestions (pick the most visually striking):
- Full blocks = solid, saturated color, full width
- Sharded blocks = same color but at 25% width, or with diagonal stripes,
  or with a "torn edge" effect
- The transition from Card 1 (all full) to Card 4 (all thin) should create
  a DRAMATIC visual lightening — the eye should immediately see that
  Card 4's GPUs are nearly empty

TOP ANNOTATION: An arrow spanning all 4 cards:
"← Replicate everything     Shard everything →"

BOTTOM ANNOTATION: An arrow spanning all 4 cards:
"← More memory per GPU     Less memory per GPU →"

BOTTOM CALLOUT (below Card 4):
A small note: "Communication cost only ~50% more than DDP"
This is surprising and should be highlighted.

LEGEND (small, in corner):
4 color swatches: Parameters, Gradients, Adam m, Adam v
"Solid = replicated on every GPU"
"Thin = 1/G shard per GPU"

STYLE LOCK:
- Background: #FAFCFF
- Card backgrounds: white with light blue border
- Primary blocks: #2D8CFF family (4 shades for P, G, M, V)
- Orange accent: #D35400 (ONLY on ZeRO-3/FSDP card highlight)
- Text: #1A1A2E (charcoal), #6B7280 (steel gray for descriptions)
- Clean vector infographic, modern tech textbook aesthetic
- Cards should have subtle drop shadows or borders, similar to Ch6 Fig 6.1
- Sans-serif labels, generous spacing

DO NOT: 3D GPUs, photorealistic hardware, code, circuit diagrams,
more than 4 GPUs per card, complex animations, neon, rainbow
```

## Review Checklist

- [ ] 4 cards: DDP, ZeRO-1, ZeRO-2, ZeRO-3/FSDP
- [ ] Progressive visual lightening from left to right
- [ ] 4 simplified GPU icons inside each card
- [ ] Full state blocks vs thin sharded blocks clearly distinguishable
- [ ] Memory numbers on each card: 112GB, 37GB, 31GB, 28GB
- [ ] Orange accent ONLY on ZeRO-3/FSDP
- [ ] Top arrow: "Replicate everything → Shard everything"
- [ ] Bottom arrow: "More memory per GPU → Less memory per GPU"
- [ ] Bottom legend with 4 components
- [ ] "~50% more communication" callout
- [ ] Matches Ch6 Fig 6.1 card style exactly
- [ ] Beautiful, spacious, immediately understandable
