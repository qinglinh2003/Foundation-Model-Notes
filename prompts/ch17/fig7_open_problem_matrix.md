# Figure 17.7: Open Problem Matrix

**Filename**: `fig_open_problem_matrix.png`
**LaTeX label**: `fig:open-problem-matrix`
**Caption**: Open problems as audit targets. Each frontier question pairs a feedback source with an independent diagnostic and a concrete sign of progress. The point is to turn "open problem" from an inventory label into a research-direction guide: what evidence would make the field update?

## Prompt

```text
Create a polished textbook diagram for a graduate AI curriculum chapter on post-training frontiers.

CONCEPT:
Open problems should be presented as audit targets, not as a flat inventory. Each frontier question should connect: feedback source -> blind spot -> independent diagnostic -> what would constitute progress.

MAIN COMPOSITION:
Use a wide 16:9 canvas with a clean matrix layout.

LEFT COLUMN: "Frontier Question"
Show 5 stacked rows with concise labels:
1. Discovery vs elicitation
2. Self-improvement stability
3. Weak supervision
4. Multi-objective alignment
5. Oversight composition

MIDDLE COLUMN: "Independent Diagnostic"
For each row, show a compact visual diagnostic:
- pass@k curve with low-k/high-k separation
- iteration dashboard with score and diversity curves
- PGR gap bar showing weak, weak-to-strong, strong ceiling
- multi-objective radar or small bar chart for helpfulness/safety/honesty/calibration
- layered feedback icons: human, verifier, principle, weak supervisor

RIGHT COLUMN: "What Would Change Our Mind?"
For each row, show one concrete research-progress signal:
- high-k support expands, not only pass@1
- held-out score and diversity survive multiple rounds
- PGR stays high as capability gap widens
- per-property constraints hold, not only average reward
- ablations show which feedback source catches which failure

VISUAL STRUCTURE:
Use arrows from left to middle to right in each row. Add a thin top banner: "From inventory to research-direction guide". At the bottom, include a small caption-like note: "A method is audited when it says what evidence would make it update."

STYLE:
- Crisp vector-like educational illustration, not photorealistic.
- White background with subtle grid lines.
- Use dark navy text (#1F2937), blue accents (#2D8CFF), orange highlights (#FF9F43), and green success markers (#2FB344).
- Use simple icons only: magnifying glass, chart, shield, verifier check, human labeler, model node.
- Professional textbook figure style matching previous chapter figures.

IMPORTANT:
- Do not include tiny unreadable paragraphs.
- Keep all text short and readable at textbook scale.
- Avoid decorative gradients or 3D effects.
- Do not imply that the open problems are solved.
- Emphasize diagnostics and evidence, not paper names.
```

## Review Checklist

- [ ] Matrix clearly has frontier question, diagnostic, and progress signal columns.
- [ ] Each row maps a specific open problem to a concrete diagnostic.
- [ ] The figure reads as a research-direction guide, not a paper inventory.
- [ ] Text is large enough to read in a PDF.
- [ ] Colors match the chapter figure style.
- [ ] No claim visually implies the problems are solved.
