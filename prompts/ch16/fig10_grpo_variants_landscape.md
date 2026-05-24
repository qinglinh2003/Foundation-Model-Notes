# Figure 16.6: GRPO Variant Landscape

**Filename**: `fig_grpo_variants_landscape.png`
**LaTeX label**: `fig:grpo-variants-landscape`
**Caption**: \textbf{GRPO variants as competing bets on the right abstraction level.} DAPO adds targeted fixes for vanilla GRPO pathologies, GSPO moves ratio logic toward the sequence level, Dr.GRPO removes heuristic normalizations, and REINFORCE++ simplifies the baseline. The field is moving quickly, so the durable question is which failure mode each variant is trying to solve.

## Prompt

```text
Draw a conceptual landscape map for a machine learning textbook.
Use a clean blue-white technical style with one orange emphasis color.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Map the main 2025-2026 critic-free reasoning-RL variants around vanilla GRPO. The figure should show that variants differ by which failure mode they treat as primary: clipping/entropy, zero-gradient groups, token-vs-sequence mismatch, normalization bias, or rollout cost. The figure should feel like a design-space map, not a leaderboard.

MAIN COMPOSITION:
CENTER:
- Place "Vanilla GRPO" as a central blue node.
- Inside the node show its core recipe in tiny icons:
  group sampling -> verifier rewards -> group baseline -> token-level clipped update.
- Keep this central node blue, not orange.

AROUND THE CENTER: FOUR VARIANT CARDS
1. DAPO — "targeted repairs"
   - Orange-highlighted card because this is the main worked example in the chapter.
   - Four small chips inside: Clip-Higher, Dynamic Sampling, Token-Level Loss, Overlong Shaping.
   - Mini chart: entropy curve stabilized.
   - Failure mode label: "entropy collapse / dead groups / length bias".

2. GSPO — "sequence-level view"
   - Show an entire response strip bundled as one unit.
   - Ratio label: rho_seq, not rho_t.
   - Failure mode label: "long-CoT token-ratio noise".
   - Small note: "unit of reward = unit of optimization".

3. Dr.GRPO — "remove heuristic bias"
   - Show two crossed-out normalization gadgets: sigma_r normalization and 1/|y| per-sample scaling.
   - Failure mode label: "normalization-induced bias".
   - Visual tone: minimalist, sparse.

4. REINFORCE++ — "cheaper baseline"
   - Show one response per prompt feeding into a global running baseline.
   - Failure mode label: "group sampling cost".
   - Small note: "global advantage normalization".

CONNECTORS:
- Thin blue lines from Vanilla GRPO to each variant card.
- Each connector has a short label:
  "fix clipping", "change granularity", "remove heuristics", "reduce sampling cost".

RIGHT SIDE MINI DECISION GUIDE:
- Compact vertical guide titled "Remember the question, not the acronym".
- Rows:
  "Entropy collapse? -> DAPO-style clipping"
  "All pass/all fail? -> dynamic sampling / curriculum refresh"
  "Long CoT ratio noise? -> sequence-level methods"
  "Length bias? -> revisit normalization"
  "Rollout budget tight? -> cheaper baselines"

BOTTOM BANNER:
- "2026 status: active design space, not settled leaderboard."

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — use only for the DAPO card or one thin highlight
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- Flat vector style, no gradients, no dark background, no 3D, no glow

IMPORTANT:
- Do not make the figure a leaderboard.
- Do not rank methods by performance.
- Do not include more than these four variants.
- Do not imply REINFORCE++ is a GRPO-only method; show it as a related critic-free direction.
- Keep acronyms readable and minimize body text.
- Fill the full landscape canvas with balanced spacing.
- All text readable at 50% PDF width.
```

## Review Checklist

- [ ] Vanilla GRPO appears as the central reference point.
- [ ] DAPO, GSPO, Dr.GRPO, and REINFORCE++ each have distinct visual logic.
- [ ] DAPO is highlighted without implying permanent best status.
- [ ] GSPO clearly uses sequence-level ratio logic.
- [ ] Dr.GRPO clearly removes normalization heuristics.
- [ ] REINFORCE++ clearly uses a global baseline / lower sampling-cost idea.
- [ ] Decision guide is organized by failure modes, not acronyms.
- [ ] Bottom banner communicates field instability.
- [ ] Only one orange focal area is used.
- [ ] Text remains readable at 50% PDF width.
