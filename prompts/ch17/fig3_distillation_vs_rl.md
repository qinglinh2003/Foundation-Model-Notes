# Figure 17.3: RL Versus Distillation

**Filename**: `fig_distillation_vs_rl.png`
**LaTeX label**: `fig:distillation-vs-rl`
**Caption**: RL versus distillation as capability transfer mechanisms. RL samples from the current policy and reinforces trajectories that score well, making it strong at sharpening and composition. Distillation can move teacher-generated trajectories into the student's distribution, making it a more direct way to inject reasoning patterns the student rarely samples on its own.

## Prompt

```text
Draw a side-by-side comparison of reinforcement learning and distillation for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
The figure contrasts RL as selecting from the student's current sampled trajectories with distillation as importing trajectories from a teacher model.

MAIN COMPOSITION:
LEFT HALF: RL FROM CURRENT POLICY
Show a student model box sampling many paths inside a pale blue "student support" cloud. A verifier selects paths with check marks. An update arrow thickens selected paths inside the same support cloud. Label: "select and sharpen what student can sample".

RIGHT HALF: DISTILLATION FROM TEACHER
Show a larger teacher model box producing high-quality reasoning traces outside the student's initial support. Arrows carry these traces into the student model training set. The student support cloud expands to include new paths. Label: "import teacher traces into student distribution".

CENTER CONTRAST STRIP:
A vertical divider with two concise rows:
"RL: exploration limited by current policy"
"Distillation: capability source is external teacher"

BOTTOM TAKEAWAY:
Full-width banner: "Strong base + RL sharpens; teacher traces can inject patterns the student rarely discovers alone."

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — use only for teacher trace arrows
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
- Do not imply distillation is always better than RL.
- Make the support-cloud distinction visually clear.
- Use orange only for teacher trace transfer.
- Include verifier check marks only on the RL side.
- All text readable at 50% PDF width.
```

## Review Checklist

- [ ] RL side samples from student support only.
- [ ] Distillation side imports teacher traces.
- [ ] Support cloud expansion is visible on the distillation side.
- [ ] Center contrast strip is readable.
- [ ] Bottom takeaway is present.
- [ ] Orange used only for teacher trace arrows.
- [ ] No cluttered tiny text.
- [ ] Figure fills full landscape width.
