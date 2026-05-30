# Figure 22.1: Four Effects of Runtime Systems

**Filename**: `fig_four_effects_runtime_systems.png`
**LaTeX label**: `fig:ch22-four-effects`
**Caption**: \textbf{Four effects of runtime systems.} The question is not only whether the system score improved. It is which runtime effect explains the improvement and which diagnostic would make that explanation less plausible.

## Prompt

```text
Draw a wide four-panel audit framework diagram for a graduate-level machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and spacious.

CONCEPT:
Show that runtime systems improve model-system scores through four different mechanisms: exposure, orchestration, delegation, and stabilization. The figure should teach that each mechanism implies a different falsifying diagnostic.

MAIN COMPOSITION:
Create four equal vertical panels across the page, each with a header, a compact mini-illustration, and three short rows:
"What changed?", "Typical scaffold", and "Falsifying diagnostic".

PANEL 1 -- EXPOSURE:
Show a model card with a missing-evidence gap, then a retrieval/context stream inserting a highlighted evidence snippet.
Rows:
What changed? "model saw missing information"
Typical scaffold: "long context, RAG, memory"
Falsifying diagnostic: "no retrieval / oracle retrieval / evidence shuffle"

PANEL 2 -- ORCHESTRATION:
Show several model attempts flowing into a verifier and a selected answer.
Rows:
What changed? "existing abilities coordinated"
Typical scaffold: "best-of-N, verifier, retry loop"
Falsifying diagnostic: "no retry / fixed budget / validator ablation"

PANEL 3 -- DELEGATION:
Show a model handing a subproblem to external tools: calculator, browser, compiler/test icon, and database.
Rows:
What changed? "subproblem moved to a tool"
Typical scaffold: "calculator, tests, database"
Falsifying diagnostic: "tool denied / corrupted tool / oracle tool"

PANEL 4 -- STABILIZATION:
Show a runtime guard layer blocking a risky action, validating an output, and recovering via rollback.
Rows:
What changed? "bad actions blocked or recovered"
Typical scaffold: "schemas, sandbox, approvals"
Falsifying diagnostic: "blocked-action rate / false positives / recovery trace"

BOTTOM STRIP:
Add a thin summary banner spanning the width:
"A score increase is not explained until the runtime effect and falsifying diagnostic are identified."

STYLE:
- Background: #FAFCFF
- Primary blue: #2D8CFF
- Light border: #CFE3F7
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Orange accent: #FF9F43 — use only on the highlighted diagnostic marker in the bottom strip
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
- Do not draw robots, mascots, product logos, or brand names.
- Keep every text label readable at 50% PDF width.
- Use compact labels, not paragraphs.
- Fill the full canvas with the four panels and bottom strip.
- Use one orange accent only; all other emphasis should be blue.
- Do not use a plain table; include mini-illustrations inside every panel.
- Keep the four panels visually parallel.
```

## Review Checklist

- [ ] Four panels are present: Exposure, Orchestration, Delegation, Stabilization
- [ ] Each panel includes a mini-illustration, typical scaffold, and falsifying diagnostic
- [ ] Bottom strip states the audit lesson
- [ ] Orange accent appears only once
- [ ] Text remains readable at 50% PDF width
- [ ] No product logos or robot imagery
