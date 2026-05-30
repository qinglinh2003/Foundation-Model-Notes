# Figure 23.4: Dynamic Visual Token Selection

**Filename**: `fig_dynamic_visual_token_selection.png`
**LaTeX label**: `fig:ch23-dynamic-token-selection`
**Caption**: \textbf{Dynamic visual token selection.} High-resolution encoders often manage a visual token budget by combining a global overview with selected local detail, compressed tokens, or pruned low-salience regions. The gain is efficiency; the risk is dropping task-relevant evidence.

## Prompt

```text
Draw a wide systems diagram for a graduate-level machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Show how a high-resolution image produces too many visual tokens, so the system selects, compresses, or prunes tokens before passing them downstream. The figure should teach that compression improves efficiency but can remove task-relevant evidence.

MAIN COMPOSITION:
Create a left-to-right flow with a high-resolution image, a dense token grid, a budget manager in the center, and three possible output streams on the right.

LEFT -- HIGH-RESOLUTION INPUT:
Show a table image with many small visual details. Include a small cup on the left edge, central plate, background texture, and a printed note. Label: "High-resolution image".

SECOND -- MANY PATCH TOKENS:
Show the image becoming a dense matrix of many small blue token squares labeled "N_v large". Include several tokens with tiny icons for texture, object, text, and background.

CENTER -- VISUAL TOKEN BUDGET MANAGER:
Show a compact control box labeled "B_v token budget". It receives the dense token grid and has three mini-controls:
- merge redundant tokens
- select local crops
- prune low-salience regions
Use a gauge showing "kept tokens <= B_v".

RIGHT OUTPUT STREAMS:
Create three stacked output lanes:
1. "Global overview" with a small low-res scene token group.
2. "Selected local detail" with a crop around the small cup.
3. "Compressed tokens" with fewer larger tokens summarizing repeated table texture.

RISK CALLOUT:
Add a small callout near a pruned left-edge token: "risk: relevant evidence dropped". Use the single orange accent on this warning callout.

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — use only on the "risk: relevant evidence dropped" callout
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
- Do not make this a generic compression figure; it must be about visual tokens.
- Show both benefits and risks of token selection.
- Keep the global overview, local detail, and compressed token output lanes distinct.
- Include the symbols N_v and B_v.
- Use one orange accent only on the risk callout.
- Fill the full width with the pipeline; no empty right side.
- Keep text readable at 50% PDF width.
- Do not use product logos, robot mascots, or photorealistic images.
```

## Review Checklist

- [ ] Dense input tokens feed into a budget manager
- [ ] The figure includes both N_v and B_v
- [ ] Three output lanes are present: global overview, selected local detail, compressed tokens
- [ ] Token merging, local selection, and pruning are all represented
- [ ] The small-cup detail appears as the task-relevant evidence
- [ ] Orange accent appears only on the dropped-evidence risk
- [ ] Text labels are readable at 50% PDF width
- [ ] The figure communicates efficiency gain and attribution risk
