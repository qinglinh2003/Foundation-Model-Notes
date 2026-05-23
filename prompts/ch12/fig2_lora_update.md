# Figure 12.2: LoRA Reparameterization

**Filename**: `fig_lora_update.png`
**LaTeX label**: `fig:lora-update`
**Caption**: LoRA reparameterization. The pretrained weight matrix $W$ remains frozen (gray). A small low-rank path $BA$ learns the task-specific update and is scaled by $\alpha/r$ before addition. At deployment, the adapter merges into $W$, adding zero inference latency. For a $4096 \times 4096$ projection with rank $r{=}16$, the trainable path contains $128\times$ fewer parameters than the full matrix.

## Prompt

```text
Draw a LoRA reparameterization diagram for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system. LANDSCAPE
orientation, wide and spacious. Match the visual richness of the book's
best figures --- Ch11 "Chat Template Anatomy" three-tier technical layout,
Ch10 "Three-Layer Schema" with rich internal textures, Ch9 "Data Funnel"
left-to-right transformation.

CONCEPT:
"Train the update, not the model --- then merge at deployment." The
figure has TWO visual stories: (1) during training, only the tiny
low-rank path is trainable while the large matrix is frozen; (2) at
deployment, the adapter folds back into the base matrix for zero
inference cost. This merge-at-inference property is LoRA's killer
engineering advantage.

MAIN COMPOSITION:
SPLIT ANATOMY (two panels):

LEFT PANEL --- "DURING TRAINING" (~60% width):
A computation flow diagram showing input x on the left, output h on
the right, with two parallel paths meeting at an addition node (+).

TOP PATH --- FROZEN BASE:
A large rectangular block labeled "W" with:
- Pale gray-blue fill (#D9EDFB) with a subtle dense grid texture
  (many tiny cells, suggesting millions of parameters)
- A small lock icon in the top-right corner
- Dimensions labeled on edges: "d × d" in small gray text
- Label below: "frozen --- no gradients, no optimizer states"
An arrow from x passes through W to the addition node.

BOTTOM PATH --- TRAINABLE LOW-RANK UPDATE:
Two small rectangular blocks:
- Block A: thin and wide, labeled "A", dimensions "r × d", pale blue
  fill (#E8F4FD), no lock icon
- Block B: tall and thin, labeled "B", dimensions "d × r", primary
  blue fill (#2D8CFF), no lock icon
Arrow from x through A, then through B, to a small scale badge.

SCALE BADGE:
Between B's output and the addition node, a small rounded badge in
soft orange (#FF9F43) containing "α/r". This is the ONLY orange element
in the left panel. A tiny annotation below: "normalizes update scale".

ADDITION NODE:
A circled "+" combining Wx and (α/r)BAx into h.

PARAMETER COMPARISON CARD:
A small white card with thin blue border below the two paths:
"Full matrix: d² = 16.8M | LoRA path: 2dr = 131K | Compression: 128×"
The "128×" should be in slightly bolder text.

RIGHT PANEL --- "AT DEPLOYMENT" (~35% width):
Show the merge operation. A simple visual:
- The same gray W block and the small B×A blocks from the left panel
- An arrow labeled "merge" pointing to a single combined block
- The merged block is labeled "W' = W + (α/r)BA" in primary blue
- Below the merged block: "single matrix, zero extra latency"
- A small badge: "adapter disappears at inference"
This panel should feel like a RESOLUTION --- the complexity of the
left panel collapses into simplicity.

CONNECTING ELEMENT:
A thin dashed arrow from the left panel's addition node to the right
panel's merged block, with annotation: "after training, fold BA into W"

BOTTOM STRIP:
A thin white strip spanning full width with three compact info cells:
- "Trainable params: 0.78%" (small model icon)
- "Memory saved: gradients + Adam states scale with 2dr, not d²"
- "Multi-adapter: swap LoRA modules on same frozen base"

STYLE:
- Background: #FAFCFF
- Frozen W: #D9EDFB with subtle grid texture, lock icon
- Trainable A: #E8F4FD (pale blue)
- Trainable B: #2D8CFF (primary blue)
- Merged W': #2D8CFF (primary blue, solid)
- Orange accent: #FF9F43 ONLY on the α/r scale badge
- Cards: white with thin #CFE3F7 borders, subtle shadow
- Text: #1A1A2E for labels, #6B7280 for annotations
- Arrows: #1A1A2E for computation flow, #6B7280 for dashed annotations
- Clean sans-serif typography, generous spacing

IMPORTANT:
- Do not draw a neural network diagram with layers/neurons
- Do not use generic flowchart shapes (circles, diamonds)
- Do not use 3D, glow, neon, or gradient fills
- Do not use dark backgrounds
- The size contrast between W (large) and B,A (small) must be dramatic
  --- this is the core visual message
- The right panel should feel simpler and cleaner than the left ---
  the merge resolves complexity
- Keep text minimal inside the diagram; put details in the bottom strip
```

## Review Checklist

- [ ] Two-panel layout: "During Training" (computation) and "At Deployment" (merge)
- [ ] Frozen W has lock icon, grid texture, and "no gradients" label
- [ ] Size contrast between W and B×A is dramatic and immediate
- [ ] α/r scale badge in orange is the single accent
- [ ] Parameter comparison card shows 128× compression
- [ ] Right panel shows BA folding into W → single matrix
- [ ] "Zero extra latency" message is visible
- [ ] Bottom strip includes multi-adapter serving note
- [ ] Dashed arrow connects training view to deployment view
- [ ] Landscape orientation, matches Chat Template Anatomy quality
- [ ] Readable at 50% width in PDF
