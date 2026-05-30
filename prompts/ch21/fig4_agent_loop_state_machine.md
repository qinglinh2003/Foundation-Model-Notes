# Figure 21.4: Agent Loop State Machine

**Filename**: `fig_agent_loop_state_machine.png`
**LaTeX label**: `fig:ch21-agent-loop-state-machine`
**Caption**: Agent loop state machine. The runtime observes state, asks the model to reason or choose an action, validates the typed tool call, executes it, records the observation, updates task-local state, and either continues, retries, escalates, or stops.

## Prompt

```text
Draw an agent loop state-machine diagram for a graduate-level machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation.

CONCEPT:
An agent loop is not an unbounded while-loop. It is a controlled state machine
with validation, budget checks, retries, escalation, and stopping.

MAIN COMPOSITION:
A large circular loop in the center with six nodes:
"observe", "reason", "choose action", "validate call", "execute tool",
"update state".
The "validate call" node should have a small schema/check icon.
The "execute tool" node should point to an external tool box.

STATE PANEL:
On the left, show a structured state object with fields:
"goal", "plan", "scratchpad", "budget", "approvals", "trace".

CONTROL GATES:
On the right, show three exit gates:
"retry", "escalate", "stop".
Use orange accent only on the "stop condition" gate.

BUDGET STRIP:
At the bottom, show a compact cost expression:
"total cost = model calls + tool latency + validation + retries".

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders
- Primary blue: #2D8CFF
- Pale fills: #D9EDFB and #E8F4FD
- Orange accent: #FF9F43 only on stop condition
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no product logos

IMPORTANT:
- The loop should feel controlled, not chaotic.
- Include the state fields and cost expression exactly.
- Keep labels readable and not overly small.
```

## Review Checklist

- [ ] Six loop nodes are present
- [ ] State panel includes goal, plan, scratchpad, budget, approvals, trace
- [ ] Retry, escalate, and stop exits are visible
- [ ] Budget expression appears at bottom

