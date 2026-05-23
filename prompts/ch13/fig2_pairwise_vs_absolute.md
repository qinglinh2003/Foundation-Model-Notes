# Figure 13.2: Pairwise vs Absolute Annotation

**Filename**: `fig_pairwise_vs_absolute.png`
**LaTeX label**: `fig:pairwise-vs-absolute`
**Caption**: Pairwise comparison reduces annotation ambiguity. Absolute scoring asks an annotator to map one response onto a global scale, which is sensitive to personal calibration and drift. Pairwise comparison keeps the prompt fixed and asks for a relative judgment between two candidate responses. The output is less information per annotation, but the annotation task is easier to standardize.

## Prompt

```text
Draw a pairwise-versus-absolute annotation comparison diagram for a
graduate-level machine learning textbook. Use a clean blue-white visual
system: light blue background, white cards, thin blue borders, charcoal
text, and one soft orange accent for the key lesson.

CONCEPT:
Preference learning usually asks annotators to compare two responses
rather than assign one absolute score. The figure should show why:
absolute scores require calibration to a global scale, while pairwise
comparisons are local, easier, and more consistent.

MAIN COMPOSITION:
A wide two-panel comparison layout. The left panel is "ABSOLUTE SCORE"
and the right panel is "PAIRWISE PREFERENCE". Both panels should use
the same prompt at the top so the contrast is clear.

LEFT PANEL -- "ABSOLUTE SCORE":
Inside a white card:
- Prompt card: "Explain dropout to a beginner"
- One response card underneath
- A 1-7 rating scale with several tick marks
- A small annotator silhouette looking uncertain
- Three faint thought bubbles: "Is this a 4?", "What does 6 mean?",
  "Was I stricter yesterday?"
- A calibration drift mini-strip showing three annotators assigning
  different scores: 3, 5, 4
Use muted gray-blue for uncertainty markers.

RIGHT PANEL -- "PAIRWISE PREFERENCE":
Inside a white card:
- Same prompt card at the top
- Two response cards labeled A and B placed side by side
- A simple chooser control between them: "Which is better?"
- Response B selected with a clean checkmark
- A compact output chip: "(x, y_w, y_l)"
- A small agreement mini-strip showing multiple annotators mostly
  selecting the same response
Use the single orange accent only on the selected preference path and
winner chip.

BOTTOM COMPARISON STRIP:
A full-width strip with three short comparisons:
- "Absolute: calibrated score"
- "Pairwise: local comparison"
- "Trade-off: less information per label, cleaner signal per label"
Keep this strip readable and sparse.

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF
- Pale blue fills: #E8F4FD
- Orange accent: #FF9F43 only for the chosen preference on the right
- Text: #1A1A2E; secondary labels: #6B7280
- Clean sans-serif typography
- Landscape orientation, high information density, no empty corners

IMPORTANT:
- Do not use red/green grading colors; keep the palette blue-white with
  one orange accent
- Do not include fake precise agreement percentages
- Do not make the annotator look cartoonish
- Keep all text short; avoid paragraphs inside the figure
- The figure should show cognitive load visually, not just label it
```

## Review Checklist

- [ ] Two clear panels: Absolute Score and Pairwise Preference
- [ ] Same prompt appears in both panels
- [ ] Left panel shows rating-scale ambiguity and calibration drift
- [ ] Right panel shows two responses and a selected winner
- [ ] Output tuple `(x, y_w, y_l)` is visible
- [ ] Bottom strip explains the trade-off
- [ ] Only one soft orange accent, used on the pairwise winner
- [ ] Blue-white textbook style, no dark background
- [ ] Readable at 50% width in PDF

