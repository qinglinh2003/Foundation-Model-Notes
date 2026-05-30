# Figure 20.5: Diagnostic Decision Tree for Context Failures

**Filename**: `fig_diagnostic_decision_tree.png`
**LaTeX label**: `fig:ch20-diagnostic-decision-tree`
**Caption**: Diagnostic decision tree for context failures. When an answer is wrong, use ablations and oracle conditions to locate the bottleneck: retrieval, reader/generator, position sensitivity, distractor robustness, memory staleness, or citation support.

## Prompt

```text
Draw a diagnostic decision-tree figure for context-system failures in a
graduate-level machine learning textbook. Use the course's Zoom-inspired
blue-white visual system. LANDSCAPE orientation, wide and spacious.

CONCEPT:
When a context system gives a wrong answer, diagnostics should locate the
bottleneck: access, reading, position sensitivity, distractors, memory
staleness, or attribution. The figure should look like an investigation board
with a clear test sequence, not a dense yes/no flowchart.

MAIN COMPOSITION:
Use a left-to-right diagnostic board with three visual zones. The board should
have enough direct text to teach the debugging sequence: test name, observed
signal, and likely bottleneck. Avoid long paragraphs, but do not make this a
nearly text-free icon board.

LEFT ZONE -- "WRONG ANSWER":
Show an answer card with a small mismatch marker and two source cards behind it.
Use the single orange accent on the mismatch marker.
Inside the card, show two short lines:
"claim: dataset improved"
"source: old report"
Add the header "wrong answer".

CENTER ZONE -- "ABLATION TESTS":
Show four test stations arranged as connected white cards. Each station has a
bold test label and one short diagnostic note:
1. "remove retrieval" -- source cards are pulled away from the answer.
   Note: "answer unchanged?"
2. "oracle retrieval" -- a gold evidence card is inserted into the context.
   Note: "now correct?"
3. "shuffle order" -- evidence cards change positions in a context window.
   Note: "position sensitive?"
4. "add distractors" -- muted irrelevant cards are inserted around evidence.
   Note: "robust to clutter?"
Each station should have a concrete mini-visual plus these labels.

RIGHT ZONE -- "BOTTLENECK FOUND":
Show six diagnosis tiles in a 2x3 grid. Each tile has a title and a two-word
signal label:
"access miss" / "not retrieved"
"reader fail" / "evidence ignored"
"position bias" / "order matters"
"distractor issue" / "false support"
"stale memory" / "old fact wins"
"bad citation" / "claim unsupported"
Use icons: missing document, model window, position ruler, clutter cards,
calendar/memory file, broken citation thread.

ATTRIBUTION CHECK:
At the bottom of the board, add a thin citation-audit lane: answer claim line
connected to a cited source card through a magnifying lens. This should be a
secondary visual, not a sixth main station.
Label the lane:
"citation audit: does the source support the claim?"

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF
- Pale fills: stepped blues #B7D9F2, #D9EDFB, #E8F4FD
- Muted distractor cards: #E5E7EB
- Orange accent: #FF9F43 only for the initial mismatch marker
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no 3D, no glow

IMPORTANT:
- Do not create a dense decision tree full of yes/no text.
- Do not use red warning symbols or alarmist imagery.
- Make each diagnostic test visually concrete.
- Keep labels short, but include the test notes and bottleneck signal labels.
- The board should feel like a technical debugging workflow.
- All text readable at 50% PDF width.
- Fill the full landscape canvas.
```

## Review Checklist

- [ ] Wrong answer, ablation tests, and bottleneck diagnoses are present
- [ ] Four tests appear: remove retrieval, oracle retrieval, shuffle order, add distractors
- [ ] Four tests include notes: answer unchanged, now correct, position sensitive, robust to clutter
- [ ] Six diagnosis tiles appear with icons and signal labels
- [ ] Citation audit lane appears at the bottom
- [ ] Orange accent appears only on the initial mismatch marker
- [ ] Text is sufficient for diagnosis but not paragraph-heavy
- [ ] Text readable at 50% width in PDF
