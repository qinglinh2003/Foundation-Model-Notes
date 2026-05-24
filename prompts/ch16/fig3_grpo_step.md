# Figure 16.3: One GRPO Training Step

**Filename**: `fig_grpo_step.png`
**LaTeX label**: `fig:grpo-step`
**Caption**: \textbf{One GRPO training step.} For each prompt, sample a group of responses, score each response with a verifier, normalize rewards within the group, and apply a PPO-style token-level clipped update. The learned value model from PPO is replaced by a group baseline, which is why GRPO is critic-free.

## Prompt

```text
Draw an algorithm anatomy diagram for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Explain the GRPO loop: sample multiple responses for one prompt, score with verifier, compute group-relative advantages, and perform token-level clipped policy updates without a value model.

MAIN COMPOSITION:
LEFT: PROMPT AND GROUP SAMPLING
- One prompt card: "Solve 7 x 8 + 3".
- Four response cards branching from the policy model.
- Each response card contains tiny token strips, not long text.

CENTER: VERIFIER AND GROUP BASELINE
- Responses feed into a verifier box.
- Output rewards: [1, 0, 1, 0].
- A small mean/std calculator shows mean=0.5, advantages=[+1,-1,+1,-1].
- The group baseline box is the orange focal element.

RIGHT: TOKEN-LEVEL UPDATE
- Show token strips receiving + or - advantage labels.
- PPO-style clipped update module with ratio rho_t.
- Frozen reference policy shown as a gray locked card for KL.
- No separate value model; include a crossed-out critic silhouette labeled "no critic".

BOTTOM STRIP:
- "Sequence-level reward, token-level gradient"
- "PPO critic V(s) -> GRPO group baseline".

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — ONE focal element only
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
- Do not draw a value network as active.
- Do not make the update sequence-level only; token strips must be visible.
- Do not overfill with equations.
- Keep the reward vector and advantage vector readable.
- Fill the full width with a clear left-to-right flow.
- All text readable at 50% PDF width.
```

## Review Checklist

- [ ] Group sampling from one prompt is obvious.
- [ ] Verifier rewards and group mean are visible.
- [ ] Group baseline replaces critic.
- [ ] Token-level update is visually explicit.
- [ ] KL reference is present but secondary.
- [ ] One orange focal element only.
- [ ] No active value model appears.
- [ ] Bottom strip states sequence reward -> token gradient.
