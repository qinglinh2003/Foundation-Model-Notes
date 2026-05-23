# Figure 14.3: REINFORCE Variance and Baselines

**Filename**: `fig_reinforce_variance.png`
**LaTeX label**: `fig:reinforce-variance`
**Caption**: Baselines reduce variance without changing the expected gradient. Raw rewards upweight every positive sample; subtracting a baseline converts rewards into advantages, so above-average responses are reinforced and below-average responses are suppressed.

## Prompt

```text
Draw a REINFORCE variance diagram for a graduate-level machine learning
textbook. Use a clean blue-white visual system: light blue background,
white cards, thin blue borders, charcoal text, and one soft orange
accent for the baseline line.

CONCEPT:
Raw REINFORCE multiplies every sampled response by its reward, creating
high-variance updates. Subtracting a baseline centers the signal and
turns rewards into advantages.

MAIN COMPOSITION:
A two-panel side-by-side comparison. Left panel: raw rewards. Right
panel: centered advantages after subtracting a baseline. Use the same
eight sampled responses in both panels so the transformation is clear.

LEFT PANEL -- "RAW REWARDS":
Inside the panel:
- Eight vertical mini-bars labeled response 1 through response 8
- Bar heights represent rewards: mix of 0, 0.2, 0.5, 0.8, 1.0
- All nonzero bars point upward with blue gradient arrows to "increase
  log probability"
- Add a small noisy-gradient cloud behind the bars: many faint arrows
  pointing in different directions
- Label: "all positive rewards reinforce"

RIGHT PANEL -- "ADVANTAGES":
Inside the panel:
- Same eight bars, but centered around an orange horizontal baseline
- Bars above baseline are blue and point upward: positive advantage
- Bars below baseline are pale gray-blue and point downward: negative
  advantage
- The noisy-gradient cloud is smaller and more aligned
- Label: "above average reinforce; below average suppress"

CENTER TRANSFORM:
Between panels, show a compact equation:
"A = r - b"
with a small arrow from raw rewards to advantages.

BOTTOM STRIP:
Three short notes:
"baseline does not change expected gradient" -> "centers reward signal"
-> "reduces variance"

STYLE:
- Background: #FAFCFF
- Panels: white with #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF
- Pale blue fills: #E8F4FD
- Orange accent: #FF9F43 only for the baseline line and equation badge
- Text: #1A1A2E; secondary labels: #6B7280
- Landscape orientation, high clarity

IMPORTANT:
- Do not draw a generic probability distribution
- Do not use red for negative advantage; use muted gray-blue
- Keep response labels short
- The same eight samples must appear in both panels
- The baseline line should be visually obvious but not overwhelming
```

## Review Checklist

- [ ] Two panels: raw rewards vs centered advantages
- [ ] Same eight samples appear in both panels
- [ ] Raw rewards all reinforce when positive
- [ ] Advantages split into above/below baseline
- [ ] Orange baseline and equation A = r - b
- [ ] Bottom strip explains variance reduction
- [ ] Blue-white style, single orange accent
- [ ] Readable at 50% width in PDF

