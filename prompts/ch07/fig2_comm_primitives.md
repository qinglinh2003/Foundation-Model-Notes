# Figure 7.2: Communication Primitives

**Filename**: `comm_primitives.png`
**LaTeX label**: `fig:comm-primitives`
**Caption**: The three core collective operations in distributed training. The layout encodes the key identity: AllReduce (top) decomposes into ReduceScatter (bottom-left) followed by AllGather (bottom-right).

## Prompt

```text
Draw a communication primitives infographic for a graduate-level machine
learning textbook. Use the course's blue-white visual system (#2D8CFF primary
blue, white/light-blue backgrounds). Landscape orientation, polished editorial
style.

THIS FIGURE EXPLAINS DATA MOVEMENT ACROSS GPUs.

LAYOUT: The figure's STRUCTURE encodes the key mathematical identity:

TOP: One wide panel labeled "AllReduce" spanning the full width.
BOTTOM: Two panels side by side — "ReduceScatter" (left) and
"AllGather" (right).
Between the rows: a large, prominent equation in orange (#D35400):

    AllReduce  =  ReduceScatter  +  AllGather

The orange equation is the ONLY orange in the entire figure.

GPU REPRESENTATION:
Use 3 GPUs per panel. Each GPU is drawn as a CLEAN, SIMPLIFIED GPU ICON —
a small card-like rectangle with rounded corners, a subtle hardware
silhouette (like a small PCB board outline or a stylized chip shape),
and a label (GPU 0, GPU 1, GPU 2). NOT photorealistic — think flat
vector icon, like what you'd see in a modern tech diagram.

Each GPU holds COLORED DATA BLOCKS inside or directly above it.
The data blocks represent that GPU's tensor data.

DATA COLORS (cool adjacent hues, harmonious):
  GPU 0 data: primary blue (#2D8CFF)
  GPU 1 data: slate blue (#5B7FFF)
  GPU 2 data: teal (#00B894)
  Combined result: deep navy (#1A3A5C) or striped blue+slate+teal

EACH PANEL has a "BEFORE" state (left) and "AFTER" state (right)
with a clean arrow between them.

PANEL: AllReduce
  BEFORE: Each GPU icon holds a FULL-SIZE colored data block
  (different color per GPU: blue, slate, teal)
  AFTER: Every GPU icon holds the SAME full-size combined block
  (deep navy or striped, showing all 3 merged)
  Subtitle: "Every GPU: full local → full combined"

PANEL: ReduceScatter
  BEFORE: Each GPU icon holds a FULL-SIZE colored data block
  AFTER: Each GPU icon holds only a SMALL SHARD (1/3 size) of the
  combined result. The SIZE SHRINKAGE must be dramatic — the data block
  visually shrinks from full to 1/3 inside/above the GPU.
  Subtitle: "Each GPU: full local → 1/G shard of combined"

PANEL: AllGather
  BEFORE: Each GPU icon holds only a SMALL SHARD (1/3 size)
  AFTER: Every GPU icon holds the FULL reconstructed tensor
  (all 3 shards assembled). The SIZE GROWTH must be dramatic.
  Subtitle: "Each GPU: 1/G shard → full tensor"

THE KEY VISUAL SIGNAL:
The SIZE CHANGE of data blocks (full ↔ 1/3) is the primary visual signal.
In ReduceScatter, blocks dramatically SHRINK.
In AllGather, blocks dramatically GROW.
This must be unmissable.

STYLE:
- Background: #FAFCFF (near-white)
- Panel backgrounds: #F5F9FF (very light blue)
- GPU icons: white/light gray with thin blue borders, flat vector style
- Data blocks: solid colored rectangles (blue/slate/teal family)
- Titles: bold, dark blue (#1A3A5C)
- Orange (#D35400): ONLY the equation line between rows
- Cards with rounded corners, subtle shadows
- Clean sans-serif typography
- Generous white space

DO NOT: photorealistic GPU renders, ring topology diagrams, network
wiring, more than 3 GPUs, neon colors, code, cartoon style, 3D effects,
dark backgrounds. Keep it clean and beautiful.
```

## Review Checklist

- [ ] Layout reads as AllReduce = ReduceScatter + AllGather
- [ ] Orange equation between rows is the visual focal point
- [ ] Only 3 GPUs per panel
- [ ] GPUs drawn as clean flat vector icons (not photorealistic, not just bars)
- [ ] Cool color scheme: blue/slate blue/teal for data
- [ ] Size change (full ↔ 1/3) is dramatic and obvious
- [ ] Generous white space, uncluttered
- [ ] Landscape orientation
- [ ] Premium editorial quality
