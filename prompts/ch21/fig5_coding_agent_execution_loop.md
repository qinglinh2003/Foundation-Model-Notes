# Figure 21.5: Coding-Agent Execution Loop

**Filename**: `fig_coding_agent_execution_loop.png`
**LaTeX label**: `fig:ch21-coding-agent-loop`
**Caption**: Coding-agent execution loop. Coding agents work well when the environment provides inspectable files, structured edit actions, executable tests, error messages, and reversible patches. Dense feedback turns action into a recoverable loop.

## Prompt

```text
Draw a coding-agent execution loop for a graduate-level machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, polished textbook infographic.

CONCEPT:
Coding agents work because the environment gives dense, structured, checkable
feedback: files, diffs, tests, errors, and validation. The figure should feel like
a clean software-engineering workbench, not a plain four-box flowchart.

MAIN COMPOSITION:
Create a visually rich "repository workbench" scene with a large central codebase
surface and a clockwise execution loop around it. Use four large stations, each
with one strong visual object and a few readable labels. The stations should be
connected by a thick blue loop arrow that feels continuous and intentional.

CENTERPIECE:
In the middle, show a repository workbench:
- a layered folder/file stack labeled "repo state"
- a highlighted source file strip
- a small test-status meter with red -> green states
This center area should visually tie all four stations together.

NODE 1 -- "INSPECT":
Top-left station. Show a file browser plus magnifying glass over one highlighted
source file. Add a tiny code preview with line numbers 38--44.
Internal text:
"inspect files"
"read failing area"

NODE 2 -- "EDIT":
Top-right station. Show a large diff card with green and red line highlights,
but only 4--5 visible changed lines. Add a small patch badge.
Internal text:
"apply patch"
"reversible diff"

NODE 3 -- "RUN TESTS":
Bottom-right station. Show a terminal panel with one command:
"pytest tests/test_api.py"
Beside it, show a compact progress bar or test gauge.
Internal text:
"run tests"
"check result"

NODE 4 -- "OBSERVE":
Bottom-left station. Show a structured result panel with two large stacked
outcome bands, not many small cards:
- orange failure band: "IndexError line 42"
- green success band: "tests pass"
Use orange accent only on the failure band.

CONNECTIONS:
Use thick blue arrows:
inspect -> edit -> run tests -> observe.
From the orange error card, draw a clear loop-back arrow to EDIT labeled:
"patch again".
From the green success card, draw a short arrow to a stop badge labeled:
"stop".

BOTTOM STRIP:
Use three large lesson cards with small supporting icons:
"inspectable state"
"executable feedback"
"measurable success"
Add one tiny sublabel under each:
"files and traces"
"tests and errors"
"validated patch"

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders
- Primary blue: #2D8CFF
- Pale fills: #D9EDFB and #E8F4FD
- Orange accent: #FF9F43 only on the error card
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no product logos

IMPORTANT:
- Do not show a humanoid robot programmer.
- The repository, diff, terminal, error, and passing test must be concrete and visually recognizable.
- This should be more designed than a basic flowchart: use depth, grouping, iconography, and visual hierarchy, but no tiny dense panels.
- Do not add a separate right-side mini-panel.
- Maximum visible text: four node titles, eight short internal labels, two outcome labels, one command, three bottom cards, and three bottom sublabels.
- Each station should use at most two short internal labels, plus its visual object.
- Keep text readable at 50% PDF width.
```

## Review Checklist

- [ ] Four large stations are present: inspect, edit, run tests, observe
- [ ] Central repository workbench ties the loop together
- [ ] Terminal command and error line appear
- [ ] Error loops back to edit, success goes to stop
- [ ] Figure is more visually designed than a basic flowchart
- [ ] No right-side mini-panel or dense small cards
- [ ] Bottom strip has exactly three lesson cards with tiny sublabels
