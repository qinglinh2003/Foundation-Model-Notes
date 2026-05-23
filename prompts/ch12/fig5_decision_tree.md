# Figure 12.5: Full FT vs. LoRA vs. QLoRA Decision Tree

**Filename**: `fig_decision_tree.png`
**LaTeX label**: `fig:decision-tree`
**Caption**: Choosing a fine-tuning strategy. Four decision inputs---model size, available GPU memory, task type, and deployment requirements---determine whether to use full fine-tuning, LoRA, or QLoRA. The orange path traces the Project~3 scenario: a 3B model on a 24 GB consumer GPU for instruction tuning, leading to QLoRA with rank 16 on Q/K/V/O projections.

## Prompt

```text
Draw a fine-tuning strategy decision tree for a machine learning
textbook. Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious. Match the visual richness
of the book's best figures --- Ch10 "Evaluation Workflow" horizontal
pipeline with internal mini-illustrations, Ch11 "Part III Roadmap"
pathway with embedded mini-visuals, Ch8 "Kaplan vs Chinchilla"
comparison cards with internal details.

CONCEPT:
"Five minutes to a concrete answer." This figure replaces the usual
textbook hedge ("it depends") with a definitive flowchart. The reader
should be able to trace their specific scenario through the tree and
arrive at a concrete recommendation --- not a suggestion, a decision.

MAIN COMPOSITION:
PATHWAY MAP:
A top-to-bottom decision tree, but styled as a VISUAL PATHWAY MAP
rather than a generic flowchart. Decision nodes are styled blue diamond
cards; leaf nodes are styled as recommendation cards with mini-setup
illustrations inside.

DECISION NODES (blue diamond cards):
Four decision diamonds arranged in a branching tree:

NODE 1 (top, root):
Blue diamond (#2D8CFF) with white text:
"Does the bf16 model + Adam fit in GPU memory?"
Two exit paths: "Yes" (left) and "No" (right)

NODE 2 (left branch from Node 1):
"Is this knowledge injection or capability surfacing?"
Exit: "Knowledge injection" → Full FT leaf
Exit: "Capability surfacing" → LoRA leaf

NODE 3 (right branch from Node 1):
"Does the bf16 base alone fit?"
Exit: "Yes" → LoRA leaf (different scenario)
Exit: "No" → QLoRA leaf

NODE 4 (branch from QLoRA path):
"Model > 30B?"
Exit: "Yes" → QLoRA + Paged leaf
Exit: "No" → QLoRA standard leaf

LEAF NODES --- RECOMMENDATION CARDS:
Four large rounded white cards with thin blue borders at the bottom.
Each card contains:

LEAF A --- "Full Fine-Tuning":
- A mini-illustration: a complete model block (no lock, fully colored
  in primary blue) with gradient arrows flowing through all layers
- Text: "Full FT"
- Scenario badge: "1B model, single H100, domain adaptation"
- Key detail: "All parameters trainable"

LEAF B --- "LoRA":
- A mini-illustration: a large gray model block (locked) with small
  blue adapter modules attached to 4 layers
- Text: "LoRA, r=32, all linear layers"
- Scenario badge: "7B model, 8× A100, instruction tuning"
- Key detail: "bf16 base + low-rank adapters"

LEAF C --- "QLoRA":
- A mini-illustration: a compact model block with mesh/quantized
  texture (4-bit) and tiny adapter modules
- Text: "QLoRA, r=16, Q/K/V/O"
- Scenario badge: "3B model, RTX 4090 24 GB, Project 3"
- Key detail: "4-bit base + LoRA adapters"

LEAF D --- "QLoRA + Paged":
- A mini-illustration: same quantized model block but with a small
  CPU↔GPU arrow indicating paged optimizer
- Text: "QLoRA + paged optimizer"
- Scenario badge: "70B model, workstation 48 GB"
- Key detail: "4-bit base + paged Adam"

PROJECT 3 PATH:
The path from Node 1 → "No" → Node 3 → "No" → Node 4 → "No" →
Leaf C (QLoRA) is traced with a thick orange (#FF9F43) line. The
Leaf C card has a clean orange border instead of blue. This is the
ONLY orange in the figure. A small badge on the orange path:
"Your Project 3 path".

BOTTOM STRIP:
A thin white card below the tree spanning full width:
"Rule of thumb: if bf16 base + Adam fits → consider Full FT.
If only bf16 base fits → LoRA. If nothing fits → QLoRA."
Keep this to one line in charcoal text.

STYLE:
- Background: #FAFCFF
- Decision diamonds: #2D8CFF fill with white text
- Leaf cards: white with thin #CFE3F7 borders, subtle shadow
- Path lines: #1A1A2E (default), #FF9F43 (Project 3 path ONLY)
- Mini-illustrations inside leaf cards: schematic, not detailed ---
  use simple block shapes with lock/unlock icons and adapter markers
- Orange accent: #FF9F43 ONLY on Project 3 path + Leaf C border
- Text: #1A1A2E for card labels, #6B7280 for scenario badges
- "Yes"/"No" labels on path lines in small #6B7280 text
- Clean sans-serif typography, generous spacing between nodes

IMPORTANT:
- Do not use generic flowchart symbols (rectangles with rounded corners
  for all nodes) --- diamonds for decisions, cards for recommendations
- Do not use 3D, glow, neon, or gradient fills
- Do not use dark backgrounds
- Do not make the tree too deep --- 3-4 levels maximum
- Each leaf card MUST have a mini-illustration, not just text ---
  the illustration shows the hardware+model configuration
- The Project 3 orange path should be immediately visible and
  traceable without reading all other paths first
- Scenario badges should be concrete (model size, hardware, task)
- Keep the bottom rule-of-thumb strip to one sentence
```

## Review Checklist

- [ ] Decision diamonds styled distinctly from recommendation cards
- [ ] Four leaf nodes with concrete recommendations (Full FT / LoRA / QLoRA / QLoRA+Paged)
- [ ] Each leaf has a mini-illustration showing model+adapter configuration
- [ ] Each leaf has a scenario badge with specific model size + hardware
- [ ] Project 3 path traced in orange from root to QLoRA leaf
- [ ] Orange used ONLY for Project 3 path and QLoRA leaf border
- [ ] Knowledge injection vs capability surfacing distinction visible
- [ ] Bottom strip has one-sentence rule of thumb
- [ ] Tree is 3-4 levels deep, not more
- [ ] Landscape orientation, matches Evaluation Workflow quality
- [ ] Readable at 50% width in PDF
