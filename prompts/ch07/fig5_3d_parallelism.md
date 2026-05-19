# Figure 7.5: 3D Parallelism

**Filename**: `3d_parallelism.png`
**LaTeX label**: `fig:3d-parallelism`
**Caption**: 3D parallelism assigns tensor parallelism to the fastest intra-node links, pipeline parallelism to inter-node links, and data parallelism across the remaining GPUs. The design rule: communication-heavy parallelism on the fastest fabric.

## Prompt

```text
Create a clean, minimal infographic for a graduate-level ML textbook.
Landscape orientation. Match the visual style of this book: flat
blue-white design, generous white space, nested/hierarchical layout.
Light blue background (#EBF5FF or similar).

REFERENCE STYLE: Use the book's established card-based visual language.
Clean rounded rectangles, thin blue borders, simple icons, lots of
breathing room. NOT a 3D perspective cube — use a NESTED HIERARCHY
instead.

CONCEPT: Show how TP, PP, and DP combine as NESTED LEVELS of a GPU
cluster, from innermost (fastest) to outermost (any speed).

LAYOUT — NESTED BOXES (Russian dolls):

Outermost level: A large rounded rectangle labeled "Data Parallelism / FSDP"
  Subtitle: "DP = 8 replicas"
  Contains 2 (or 3) identical inner boxes side by side
  Connection label: "Any fabric"

Middle level: Each DP replica is a rounded rectangle labeled "Pipeline"
  Subtitle: "PP = 4 stages"
  Contains 4 small boxes stacked vertically
  Connection label: "InfiniBand 200 GB/s"

Innermost level: Each pipeline stage is a small rounded rectangle
  labeled "Node"
  Subtitle: "TP = 8 GPUs"
  Contains 8 tiny colored squares (the GPUs)
  Connection label: "NVLink 900 GB/s"

The NESTING visually communicates the hierarchy:
  GPU cluster → DP replicas → pipeline stages → TP nodes → individual GPUs

HIGHLIGHTED EXAMPLE:
ONE innermost node should have an ORANGE (#D35400) border to highlight
"this is one NVLink domain." A thin orange callout line points to it
with the label: "All 8 GPUs in this node share NVLink —
tensor parallelism lives here."
This is the ONLY orange in the figure.

BOTTOM SUMMARY BAR:
A clean horizontal strip with 3 sections:

  | TP = 8     | Within node  | NVLink 900 GB/s | Splits each layer |
  | PP = 4     | Across nodes | IB 200 GB/s     | Splits model depth |
  | DP/FSDP = 8 | Across groups | Any fabric    | Splits data        |

  Total: 8 x 4 x 8 = 256 GPUs

DESIGN RULE (prominent callout at the very bottom):
"Communication-heavy parallelism on the fastest fabric."

COLOR SYSTEM:
- Background: light blue (#EBF5FF)
- Nested boxes: white with thin blue borders, each level slightly
  different shade (outermost lightest, innermost deepest)
- GPU squares: small filled blue squares
- Orange: #D35400, ONLY on the one highlighted node
- Summary bar: white cards with blue headers

BEAUTY PRINCIPLES:
- The nesting should be immediately obvious — like looking at a
  matryoshka doll diagram
- Each level should have enough padding that it doesn't feel cramped
- Only show 2-3 DP replicas (not all 8) to keep the figure readable
  — use "..." or a faded extra box to suggest more
- The figure should be understandable in 5 seconds: big box contains
  medium boxes contains small boxes contains tiny GPU squares

DO NOT: literal 3D cube with perspective, complex wiring diagrams,
server rack photos, more than ~50 visible GPU squares (use "..." for
the rest), dark backgrounds, neon
```

## Review Checklist

- [ ] Nested hierarchy clearly visible (3 levels)
- [ ] TP innermost, PP middle, DP outermost
- [ ] Bandwidth labeled at each level
- [ ] One node highlighted in orange (ONLY orange element)
- [ ] Summary bar at bottom with TP/PP/DP configuration
- [ ] "Communication-heavy on fastest fabric" design rule prominent
- [ ] Total GPU count: 256
- [ ] Matches book's flat blue-white visual language
- [ ] Not a 3D perspective cube
- [ ] Clean, spacious, beautiful
