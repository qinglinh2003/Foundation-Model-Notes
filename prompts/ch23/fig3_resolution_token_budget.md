# Figure 23.3: Resolution Is a Visual Token Budget

**Filename**: `fig_resolution_token_budget.png`
**LaTeX label**: `fig:ch23-resolution-token-budget`
**Caption**: \textbf{Resolution is a visual token budget.} With fixed $16 \times 16$ patches, $224 \times 224$ produces 196 visual tokens, $448 \times 448$ produces 784, and $1024 \times 1024$ produces 4096. Detail preservation competes with attention cost and context budget.

## Prompt

```text
Draw a wide quantitative tradeoff figure for a graduate-level machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Show that increasing image resolution with fixed patch size increases visual token count quadratically. The figure should make resolution feel like a budget choice, not a free quality knob.

MAIN COMPOSITION:
Create three large side-by-side cards across the canvas, each showing the same image at a different input resolution with a patch grid density and token count. Under the cards, add a shared cost arrow from "detail" to "compute / memory / context".

CARD 1 -- 224 x 224:
Show a coarse 14 x 14 grid over a simplified table image. The small cup is barely visible. Label:
"224 x 224"
"16 x 16 patches"
"14 x 14 = 196 tokens"
Add tiny chips for "low cost" and "coarse detail".

CARD 2 -- 448 x 448:
Show a denser 28 x 28 grid. The small cup is more visible. Label:
"448 x 448"
"16 x 16 patches"
"28 x 28 = 784 tokens"
Add tiny chips for "4x tokens" and "better detail".

CARD 3 -- 1024 x 1024:
Show a very dense grid stylized as many tiny cells; do not draw all 4096 cells individually if it becomes unreadable, but suggest density with a detailed grid inset. The small cup has a clear local crop callout. Label:
"1024 x 1024"
"16 x 16 patches"
"64 x 64 = 4096 tokens"
Add tiny chips for "21x vs 224" and "high cost".

BOTTOM TRADEOFF BAND:
Draw a horizontal band with two ends:
Left: "More local evidence"
Right: "More attention cost + memory + context pressure"
Place the orange accent on a central warning marker labeled "budget decision".

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — use only on the "budget decision" marker in the bottom band
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
- Include the exact token counts: 196, 784, 4096.
- Include the fixed patch size: 16 x 16 patches.
- Make the token growth visually obvious from left to right.
- Do not clutter the figure with too many tiny unreadable grid cells.
- Use one orange focal marker only.
- Fill the full canvas with the three cards and bottom band.
- All text must be readable at 50% PDF width.
- Avoid implying higher resolution is always best; show the cost tradeoff.
```

## Review Checklist

- [ ] Three resolutions are shown: 224 x 224, 448 x 448, 1024 x 1024
- [ ] Exact token counts appear: 196, 784, 4096
- [ ] Patch size 16 x 16 is visible in every card
- [ ] Grid density increases from left to right
- [ ] Bottom band frames resolution as a budget decision
- [ ] Orange accent appears only once
- [ ] Text remains readable at 50% PDF width
- [ ] The figure shows both detail gain and cost pressure
