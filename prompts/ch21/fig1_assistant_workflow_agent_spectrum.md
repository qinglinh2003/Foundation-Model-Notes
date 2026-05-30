# Figure 21.1: Assistant -> Workflow -> Agent Loop Spectrum

**Filename**: `fig_assistant_workflow_agent_spectrum.png`
**LaTeX label**: `fig:ch21-assistant-workflow-agent-spectrum`
**Caption**: From assistant to workflow to agent loop. A normal assistant maps prompt to answer. A workflow executes controlled steps with local model decisions. An agent loop repeatedly observes, reasons, acts, updates state, and decides whether to continue. Side effects require runtime controls.

## Prompt

```text
Draw a wide systems-spectrum diagram for a graduate-level machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, clear and readable at 50% PDF width.

CONCEPT:
Show the transition from ordinary assistant, to controlled workflow, to agent loop.
The key lesson is that external side effects require runtime controls.

MAIN COMPOSITION:
A left-to-right spectrum with three large stations.

LEFT STATION -- "ASSISTANT":
Show a simple prompt card flowing into an answer card.
Label the path: "prompt -> answer".
Add a small caption: "no external side effect".
Inside the station, add two compact callouts:
"single model response" and "low runtime control".

CENTER STATION -- "WORKFLOW":
Show a deterministic pipeline with four blocks:
"classify", "retrieve", "draft", "approve".
One block should contain a small model icon labeled "local model decision".
Add a caption: "known control flow".
Inside the station, add two compact callouts:
"fixed graph" and "human approval point".

RIGHT STATION -- "AGENT LOOP":
Show a circular loop with five nodes:
"observe", "reason", "act", "observe result", "update state".
The "act" node should connect to three external action icons:
"file edit", "API call", "run test".
Add a stop gate labeled "continue / stop".
Inside the loop, add two compact callouts:
"state changes after each tool result" and "retry only with a changed plan".

BOTTOM STRIP:
Four runtime-control cards spanning the full width:
"permissions", "validation", "budget", "trace".
Add the takeaway sentence:
"actions need clearance, not just generation".
Each runtime-control card should include one tiny sublabel:
"who may act", "check result", "limit steps", and "replay path".

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders
- Primary blue: #2D8CFF
- Pale fills: #D9EDFB and #E8F4FD
- Orange accent: #FF9F43 only on the external "act" arrow
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no product logos

IMPORTANT:
- This is a systems diagram, not a robot illustration.
- Include the exact labels listed above.
- Keep text compact but meaningful, like prior chapter figures: add enough internal labels that each station teaches a distinction, but avoid paragraph-length prose.
- Do not add extra paragraphs or tiny prose labels.
```

## Review Checklist

- [ ] Three stations are present: assistant, workflow, agent loop
- [ ] Agent loop includes observe, reason, act, observe result, update state, continue/stop
- [ ] External action icons are visible
- [ ] Runtime controls appear in the bottom strip
- [ ] Orange accent appears only on the external action arrow
