# Figure 21.6: Trace Diagnostic Tree

**Filename**: `fig_trace_diagnostic_tree.png`
**LaTeX label**: `fig:ch21-trace-diagnostic-tree`
**Caption**: Trace diagnostic tree. A wrong outcome can originate in planning, tool choice, argument construction, execution, observation interpretation, state update, stopping, safety policy, or budget control. Trace review localizes the first broken layer.

## Prompt

```text
Draw a trace diagnostic tree for a graduate-level machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation.

CONCEPT:
When an agent fails, inspect the trace to find the first broken layer rather
than blaming "the model" generically.

MAIN COMPOSITION:
A wide diagnostic board with a top node:
"wrong outcome".
Branch downward into seven diagnosis stations:
"goal", "action selection", "arguments", "execution", "observation",
"state update", "stopping".

EACH STATION:
Use a visual mini-card:
- goal: target card with mismatched objective
- action selection: fork with wrong tool highlighted
- arguments: schema form with invalid field
- execution: sandbox with timeout icon
- observation: document with warning text
- state update: ledger with stale scratchpad note
- stopping: traffic-light gate

SIDE PANEL -- "SAFETY + COST":
Show two diagnostic alarms:
"prompt injection via tool output"
"hidden cost explosion"
Use orange accent only on "prompt injection".

BOTTOM STRIP:
Add the takeaway:
"diagnose the first broken layer in the trace".

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders
- Primary blue: #2D8CFF
- Pale fills: #D9EDFB and #E8F4FD
- Orange accent: #FF9F43 only on prompt injection alarm
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no product logos

IMPORTANT:
- Make this look like an investigation board, not a dense yes/no flowchart.
- Include all seven diagnosis stations.
- Keep text compact but not too sparse.
- Text must be readable at 50% PDF width.
```

## Review Checklist

- [ ] Top node says wrong outcome
- [ ] Seven diagnosis stations are present
- [ ] Safety + cost side panel includes prompt injection and hidden cost explosion
- [ ] Bottom takeaway appears
- [ ] Orange accent only highlights prompt injection

