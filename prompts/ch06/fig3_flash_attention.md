# Figure 6.3: Standard Attention vs FlashAttention

**Filename**: `flash_attention.png`
**LaTeX label**: `fig:flash-attention`
**Caption**: Standard attention (top) materializes the full T x T attention matrix in HBM, requiring multiple round-trips between HBM and compute units. FlashAttention (bottom) tiles the computation and keeps intermediate results in SRAM, never writing the full attention matrix to HBM.

## Prompt

```text
Draw a two-panel comparison diagram of Standard Attention vs FlashAttention
memory access patterns, for a graduate-level machine learning textbook.
Use the course's blue-white visual system. Landscape orientation, polished
editorial style.

Purpose:
- The figure should teach that FlashAttention's speedup comes from avoiding
  HBM round-trips, not from changing the math.
- The main visual message is: same computation, radically different memory
  access pattern.

LAYOUT:
Two panels stacked vertically, separated by a horizontal divider.
Each panel shows a simplified data flow between HBM (main GPU memory)
and SRAM (on-chip fast memory / registers).

TOP PANEL — STANDARD ATTENTION:
Title: "Standard Attention"

Left side: a large rounded rectangle labeled "HBM (High Bandwidth Memory)"
containing:
- Three matrices: Q, K, V (small blue blocks)
- One LARGE matrix: S = QK^T (a prominent T x T grid, medium blue)
- One LARGE matrix: P = softmax(S) (another T x T grid, medium blue)
- One output matrix: O = PV (small blue block)

Right side: a small rounded rectangle labeled "SRAM (On-Chip)"
- Much smaller than HBM box
- Shows "Compute" happening here

Arrows showing the data flow (numbered 1-5):
1. Q, K read from HBM to SRAM -> compute S
2. S written BACK to HBM (big arrow, labeled "Write T x T")
3. S read from HBM to SRAM -> compute P = softmax(S)
4. P written BACK to HBM (big arrow, labeled "Write T x T")
5. P, V read from HBM to SRAM -> compute O -> write O to HBM

The ONE orange accent: the two "Write T x T" arrows (steps 2 and 4),
highlighting that the T x T matrices are the expensive HBM writes.

Annotation below: "3 HBM round-trips. The T x T attention matrix is
materialized twice in HBM."

BOTTOM PANEL — FLASHATTENTION:
Title: "FlashAttention"

Left side: same "HBM" box, but now containing:
- Q, K, V (same small blue blocks)
- O (output, small blue block)
- NO S matrix, NO P matrix — they do not exist in HBM
- A crossed-out or ghosted T x T grid with label "Never materialized"

Right side: the "SRAM" box, now more prominent:
- Shows Q_block, K_block, V_block (small tile pieces)
- Shows "Local S_tile", "Local P_tile" (tiny blocks, NOT full T x T)
- Shows "Running softmax accumulator"
- Label: "All intermediate computation stays in SRAM"

Arrows showing data flow:
1. Q_block, K_block, V_block read from HBM to SRAM (one read per tile)
2. Compute attention LOCALLY in SRAM (no write-back of intermediates)
3. Only final O_block written back to HBM

Annotation below: "1 read + 1 write per tile. The T x T matrix never
exists in HBM. Memory: O(T) instead of O(T^2)."

BETWEEN THE PANELS:
A divider line with centered text: "Same math. Different memory access."

STYLE LOCK:
- Match the course's Zoom-inspired blue-white textbook visual system.
- Background: #FAFCFF
- HBM box: light fill #E8F4FD with #0B5CFF border
- SRAM box: slightly darker fill to indicate "fast/special"
- Matrices Q/K/V/O: #2D8CFF blocks
- T x T matrices (in standard attention): larger, visually prominent
- Ghosted/crossed-out T x T (in FlashAttention): faded gray with X
- Arrows: #0B5CFF for normal flow
- Orange accent: #FF9F43 ONLY on the "Write T x T" arrows in the top panel
- Text: #1A1A2E charcoal, sans-serif
- Clean vector geometry, generous whitespace between panels

DO NOT: cartoon style, photorealism, clip art, SaaS dashboard, heavy 3D,
neon, rainbow, coral, teal, purple, green, decorative borders, abstract
background patterns, complex formulas inside the diagram.
```

## Review Checklist

- [ ] Two panels: Standard (top) and FlashAttention (bottom)
- [ ] Top panel shows Q, K, V, S (T x T), P (T x T), O in HBM
- [ ] Top panel shows 3 HBM round-trips with numbered arrows
- [ ] Bottom panel shows Q, K, V, O in HBM but NO S or P matrices
- [ ] Bottom panel shows tiled computation happening in SRAM
- [ ] "Never materialized" ghosted T x T in bottom panel
- [ ] Orange accent ONLY on the "Write T x T" arrows in top panel
- [ ] Divider text: "Same math. Different memory access."
- [ ] HBM and SRAM clearly labeled and visually distinct
- [ ] No extra colors beyond blue + white + orange + gray
