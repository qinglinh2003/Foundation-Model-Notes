# Figure 10.2: Prompt Sensitivity as Measurement Variance

**Filename**: `fig_prompt_sensitivity.png`
**LaTeX label**: `fig:prompt-sensitivity`
**Caption**: The same model can produce different benchmark scores under different templates, shot counts, and demonstration orders. Published scores should therefore report the full prompt protocol, not only the benchmark name and final accuracy.

## Prompt

```text
Draw a prompt-sensitivity visualization for a machine learning textbook.
Use the course's Zoom-inspired blue-white visual system. LANDSCAPE
orientation, wide and spacious. Match the visual richness of the book's
best figures — Ch4 "Signal Density" token-level visualization, Ch9
"Mixing Experiment" side-by-side chart with recipe cards, Ch8 "Power
Law Curves" annotated dual-panel chart.

CONCEPT:
"Same model, different scores — the protocol IS a variable." This figure
should make the reader viscerally feel that a single benchmark number
is an illusion. The same 900M model on the same MMLU benchmark produces
a CLOUD of scores depending on how you prompt it.

MAIN COMPOSITION — TWO-PANEL LAYOUT:
The figure has TWO major panels side by side.

LEFT PANEL — "THE ILLUSION" (narrow, ~30% width):
A single tall white card with thin blue border showing "the published
result" — the way scores usually appear in papers:
- A large bold number: "68.3%" in primary blue (#2D8CFF)
- Below it: "MMLU accuracy" in charcoal
- Below that: "900M model, 5-shot" in steel gray
- The card looks clean, authoritative, precise — like a leaderboard entry
- A thin vertical blue left border gives it a "paper excerpt" feel
- This card should feel deceptively simple and confident

RIGHT PANEL — "THE REALITY" (wide, ~65% width):
A rich, detailed visualization showing the SPREAD of actual scores.

Inside this panel, draw a single vertical axis on the left:
- Y-axis: "Accuracy (%)" ranging from 55% to 80%
- Light blue horizontal gridlines at 5% intervals

Three COLUMNS of dots are arranged left to right, each representing a
different source of variance:

COLUMN A — "Template":
- 6 blue dots (#2D8CFF) scattered vertically between ~60% and ~76%
- Each dot has a tiny label on hover/side showing a template snippet:
  "Q: {q}\nA:" / "Question: {q}\nAnswer:" / "{q}\n(A)(B)(C)(D)" etc.
  (show 2-3 of these as tiny code-font annotations near the dots)
- A thin vertical BRACKET on the right spanning the dot range,
  labeled "~16 pp" in orange (#FF9F43) — this is the first orange accent
- Below: "6 templates"

COLUMN B — "Shot Count":
- 5 dots connected by a thin ascending blue line:
  0-shot (~60%), 1-shot (~63%), 3-shot (~67%), 5-shot (~70%), 8-shot (~72%)
- Tiny shot count labels ("0", "1", "3", "5", "8") next to each dot
- Bracket labeled "~12 pp"
- Below: "same template, different K"

COLUMN C — "Example Order":
- 8 dots clustered vertically between ~65% and ~74% at the same
  horizontal position (like a beeswarm)
- These dots should form a visible CLOUD, slightly jittered horizontally
  for readability
- Bracket labeled "~9 pp"
- Below: "5-shot, same examples, shuffled"

ACROSS ALL COLUMNS:
A prominent DASHED HORIZONTAL LINE at 68.3% spanning the entire right
panel, labeled "reported score" in small gray text. This is the same
number shown in the left panel — making the connection unmistakable.

CONNECTING ELEMENT:
A thin dashed arrow from the left panel's "68.3%" to the dashed line
in the right panel, with a small annotation: "just one point in
the cloud" in steel gray italic.

BOTTOM CALLOUT (spanning full width):
A white card with thin blue border:
"The protocol is part of the result."
"protocol" in orange (#FF9F43).
Below in smaller gray text: "Always report: template, K, example
selection method, and example order (or averaged over N orders)."

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders, subtle shadow
- Dots: #2D8CFF, ~8px diameter, subtle shadow for depth
- Dashed reference line: #2D8CFF at 40% opacity
- Orange accent: #FF9F43 on "~16 pp" bracket and "protocol" in callout
- Template snippet labels: small monospace font in #6B7280
- Text: #1A1A2E for titles, #6B7280 for annotations
- Clean sans-serif typography, generous margins

IMPORTANT:
- Do not use bar charts (dots show variance better)
- Do not add error bars or confidence bands
- Do not make it look like a matplotlib/seaborn export
- Do not use 3D, glow, or gradient fills
- The left "illusion" panel should feel deliberately oversimplified
  compared to the rich right "reality" panel — this contrast is the
  whole point of the figure
```

## Review Checklist

- [ ] Two-panel layout: "The Illusion" (single number) vs "The Reality" (dot cloud)
- [ ] Left panel: clean 68.3% leaderboard-style card
- [ ] Right panel: three dot columns (Template, Shot Count, Example Order)
- [ ] Dashed arrow connecting left panel number to right panel reference line
- [ ] Template snippets shown as tiny code-font annotations near Column A dots
- [ ] Ascending trend visible in Column B (shot count)
- [ ] Brackets showing spread: ~16pp, ~12pp, ~9pp
- [ ] Orange accents only on largest bracket (~16pp) and "protocol" in callout
- [ ] Contrast between oversimplified left and rich right is visually clear
- [ ] Landscape orientation, matches Signal Density / Mixing Experiment quality
- [ ] Readable at 50% width in PDF
