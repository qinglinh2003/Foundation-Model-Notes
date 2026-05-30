# Figure 18.1: Inference-Time Scaling as a Runtime Stack

**Filename**: `fig_runtime_compute_stack.png`  
**LaTeX label**: `fig:ch18-runtime-compute-stack`  
**Caption**: Inference-time scaling as a runtime stack. A fixed model distribution is wrapped by decoding, candidate generation, selection, search, and a cost budget. The system's behavior is the whole stack, not the weights alone.

## Prompt

```text
Create a clean textbook diagram showing inference-time scaling as a runtime stack around a fixed language model.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation, wide and readable.

CONCEPT:
A deployed model system is not just model weights. A fixed model distribution is wrapped by decoding, candidate generation, selection, search, and a cost/latency budget.

MAIN COMPOSITION:
Center-left: a large rounded rectangle labeled "Fixed model weights" with a small probability distribution icon inside, labeled "p_theta(next token)".
Around it, show a left-to-right runtime pipeline:
1. Prompt
2. Decoding rule
3. Candidate pool
4. Selector / verifier / vote
5. Returned answer

Above the pipeline, add a bracket labeled "Runtime algorithm".
Below the pipeline, add a wide constraint bar labeled "Cost + latency budget" with small token, clock, and dollar icons.

Right side: two contrasting output modes:
- "Fast single-shot assistant": one thin path, low cost, lower reliability.
- "Deliberate problem-solving system": many sampled paths feeding a selector, higher cost, higher reliability.

STYLE:
- Background #FAFCFF
- Primary blue #2D8CFF
- Pale blue fills #E8F4FD and #D9EDFB
- Orange accent #FF9F43 only for "cost + latency budget"
- Text #1A1A2E, annotations #6B7280
- Clean sans-serif typography
- Thin borders, no shadows, no gradients, no 3D

IMPORTANT:
- Make the hierarchy obvious: weights are fixed, runtime choices change behavior.
- Do not make it look like cloud infrastructure or a business dashboard.
- All labels must be readable at 50% PDF width.
- Fill the canvas; no empty corners.
```

## Review Checklist

- [ ] Fixed model weights are visually distinct from runtime layers.
- [ ] Pipeline includes prompt, decoding, candidates, selector, answer.
- [ ] Cost/latency budget is shown as a constraint.
- [ ] Single-shot and deliberate modes are contrasted.
- [ ] Text remains readable at PDF size.
