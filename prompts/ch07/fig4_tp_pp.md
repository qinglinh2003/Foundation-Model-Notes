# Figure 7.4: Tensor Parallelism and Pipeline Parallelism

**Filename**: `tp_pp.png`
**LaTeX label**: `fig:tp-pp`
**Caption**: Two complementary model-parallelism strategies. Tensor parallelism splits each layer across GPUs (left), requiring high-bandwidth NVLink. Pipeline parallelism assigns different layers to different GPUs (right), creating idle bubbles.

## Prompt

```text
Create a clean, minimal dual-panel infographic for a graduate-level ML
textbook. Landscape orientation. Match the visual style of this book:
flat blue-white design, generous white space, simple geometric shapes.
Light blue background (#EBF5FF or similar).

REFERENCE STYLE: Use the same flat, clean aesthetic as the book's
"Step-by-Step BPE Merge Trace" figure: numbered steps, rounded boxes,
clean arrows, small labels. No 3D, no hardware illustrations.

CONCEPT: Show two fundamentally different ways to split a model across
GPUs. Left panel = split within a layer (TP). Right panel = split
across layers (PP).

LAYOUT:
Two panels side by side, separated by a thin vertical line or gap.
Each panel is self-contained with its own title and visual.

LEFT PANEL — "Tensor Parallelism"
Subtitle: "Split within each layer"

Show a simple flow diagram (top to bottom):

  [Input activation]  (full-width rounded blue bar)
        |
  [    Layer    ]     (a wide rounded rectangle, DIVIDED into 4 vertical
                       strips colored in 4 shades of blue, labeled
                       GPU 0, GPU 1, GPU 2, GPU 3)
        |
  [  AllReduce  ]     (small circle with sigma icon)
        |
  [Output activation] (full-width rounded blue bar)

Key label below: "AllReduce every layer = needs NVLink"

RIGHT PANEL — "Pipeline Parallelism"
Subtitle: "Split across layers"

Show a GANTT CHART (time on x-axis, GPUs on y-axis):

  4 horizontal swim lanes: GPU 0, GPU 1, GPU 2, GPU 3
  Time flows left to right.

  Show 4 microbatches (u1, u2, u3, u4) as small colored blocks moving
  through the pipeline:

  Forward passes: blue blocks flowing diagonally (GPU 0 first, then
  GPU 1, etc.)
  Backward passes: lighter blue blocks flowing back

  IDLE GAPS between blocks should be clearly visible and labeled
  "Bubble" in ORANGE (#D35400). The bubbles are the ONLY orange
  elements in the entire figure.

  Key label below: "Pipeline bubbles = GPU idle time"

BOTTOM COMPARISON (spanning both panels):
A simple two-column comparison strip:

  TP: "Splits layers | NVLink required | No idle time"
  PP: "Splits depth  | InfiniBand OK   | Has bubbles"

COLOR SYSTEM:
- Background: light blue (#EBF5FF)
- All structural elements: blue family (#2D8CFF)
- 4 GPU shades: light blue, medium blue, teal, navy
- Orange (#D35400): ONLY on pipeline bubbles
- Gantt chart background: white or very light gray
- Clean sans-serif throughout

BEAUTY PRINCIPLES:
- The left panel should be vertically oriented and simple — just 4 boxes
  connected by arrows
- The right panel's Gantt chart should be CLEAN — not a project
  management tool. Minimal grid lines, generous spacing
- Both panels should feel balanced in visual weight
- Lots of white space

DO NOT: GPU hardware, 3D perspective, complex scheduling algorithms,
more than 4 GPUs, photorealism, neon, code snippets
```

## Review Checklist

- [ ] Two clean panels: TP (left), PP (right)
- [ ] TP shows layer split into 4 GPU strips with AllReduce
- [ ] PP shows Gantt chart with visible bubbles
- [ ] Orange ONLY on pipeline bubbles
- [ ] Bottom comparison strip
- [ ] Matches book's flat blue-white visual language
- [ ] Both panels balanced in visual weight
- [ ] Landscape orientation
- [ ] Clean, spacious, beautiful
