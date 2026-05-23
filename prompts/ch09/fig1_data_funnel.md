# Figure 9.1: The Data Funnel

**Filename**: `fig_data_funnel.png`
**LaTeX label**: `fig:data-funnel`
**Caption**: The data funnel: raw web text enters at the top and a curated training corpus exits at the bottom. Each stage drops or reshapes data, and each stage encodes choices that affect what the model can learn.

## Prompt

```text
Create a polished editorial infographic for a graduate-level machine
learning textbook. PORTRAIT orientation, tall and elegant. The figure
should feel like a premium technical textbook spread, not a simple
flowchart. Match the book's blue-white visual system: #2D8CFF primary
blue, #FAFCFF background, white cards, light-blue borders, charcoal text.

REFERENCE STYLE:
Use the same visual language as the book's best figures:
- Ch6 "Scale Gap" cards: clean geometric cards, subtle shadow, precise labels.
- Ch7 "DDP to FSDP" cards: dense but organized state blocks, strong visual
  progression from heavy to light.
- Ch8 "Compute Allocation" figures: editorial chart design, clear hierarchy,
  one orange insight accent.

CONCEPT:
"The Data Funnel." Raw web data starts as a huge noisy ocean and is refined
through filtering, quality selection, deduplication, and mixing until only a
small curated stream reaches Project 2. The visual should immediately convey:
the final 18B-token training set is not "the web"; it is the result of many
selection decisions.

MAIN COMPOSITION:
Build a beautiful vertical funnel as a sequence of five floating rounded
panels, stacked from top to bottom along a thin central spine. Each panel is
centered, progressively narrower, and visually more refined than the one
above. Use soft shadows, thin blue outlines, and generous spacing. Do NOT use
a literal kitchen funnel. This should look like a modern systems diagram.

At the top, show a wide "noisy" data reservoir: many tiny pale-blue text
tiles, small dots, and fragmented mini-lines inside the panel. As the panels
descend, the internal marks become cleaner, fewer, and more regular. The
bottom panel should look precise and curated: a small, saturated blue capsule
with an orange accent.

TITLE:
At the very top, large but restrained:
"The Data Funnel"
Subtitle below in smaller gray text:
"Raw web tokens become a curated training distribution"

PANEL 1 — RAW WEB:
- Label: "Raw Web"
- Volume: "~100T tokens"
- Width: nearly full figure width
- Color: very pale blue-gray (#EAF3FB) with many tiny irregular marks
- Small right-side tag: "messy, duplicated, multilingual, noisy"

PANEL 2 — RULE-BASED FILTERING:
- Label: "Rule-Based Filtering"
- Volume: "~40T tokens"
- Keep tag: "keep ~40%"
- Width: about 60% of Panel 1
- Color: pale blue (#D8EAF8)
- Tiny removed chips around the arrow: "HTML", "boilerplate", "short docs",
  "repetition"

PANEL 3 — QUALITY FILTERING:
- Label: "Quality Filtering"
- Volume: "~15T tokens"
- Keep tag: "keep ~35%"
- Width: about 40% of Panel 1
- Color: medium light blue (#B7D9F2)
- Add a small clean classifier/checkmark symbol, abstract and flat
- Annotation: "classifier selects higher-quality documents"

PANEL 4 — DEDUPLICATION:
- Label: "Deduplication"
- Volume: "~10T tokens"
- Keep tag: "keep ~65%"
- Width: about 28% of Panel 1
- Color: stronger blue (#7DBFF0)
- Show duplicate ghost tiles fading away beside the panel
- Annotation: "near-duplicates removed"

PANEL 5 — MIXED & BATCHED:
- Label: "Mixed & Batched"
- Volume: "~18B tokens"
- Secondary label: "Project 2 training stream"
- Width: very narrow compared to Panel 1, but still legible
- Color: primary blue (#2D8CFF)
- Add the ONLY orange accent (#D35400): a thin border, small corner tab, or
  small target marker reading "Project 2"

CONNECTORS:
Use thin vertical blue arrows between panels, aligned to the central spine.
Between panels, include small gray "removed" labels, but keep them compact
and visually secondary. The figure should not feel text-heavy.

SIDE ANNOTATION:
On the right side, add a vertical bracket or axis:
Top label: "more raw data"
Bottom label: "more curated distribution"
Use small gray text. Do not use a confusing left arrow in portrait layout.

BOTTOM CALLOUT:
Below the final panel, add a small white callout card with a light blue border:
"Data engineering is not preprocessing.
It is the hidden optimizer."
Use the orange accent only on a tiny left rule or key phrase.

STYLE LOCK:
- Background: #FAFCFF
- Cards/panels: white or pale blue with thin #CFE3F7 borders
- Primary blue: #2D8CFF
- Supporting blues: #EAF3FB, #D8EAF8, #B7D9F2, #7DBFF0
- Orange accent: #D35400 ONLY on Project 2 / hidden optimizer emphasis
- Text: #1A1A2E for main labels, #6B7280 for secondary annotations
- Clean sans-serif typography, high polish, generous margins
- Subtle shadow allowed, but no dramatic glow

DO NOT:
- Do not draw a literal kitchen funnel
- Do not make it look like a generic business funnel slide
- Do not use photos, 3D, hardware, network diagrams, code, neon, rainbow colors
- Do not overload the figure with text
- Do not use more than five stages
```

## Review checklist

- [ ] 5 bands, progressively narrower
- [ ] Band 1 full width, Band 5 barely visible
- [ ] Volume numbers: 100T → 40T → 15T → 10T → 18B
- [ ] Keep rates labeled between bands
- [ ] Final band has orange accent
- [ ] Blue gradient from light (raw) to saturated (curated)
- [ ] Right-side "more data ↔ higher quality" annotation
- [ ] Portrait orientation
- [ ] Matches book's blue-white visual system
