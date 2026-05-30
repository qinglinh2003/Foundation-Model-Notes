# Figure 21.3: Typed Tool Interface

**Filename**: `fig_typed_tool_interface.png`
**LaTeX label**: `fig:ch21-typed-tool-interface`
**Caption**: Typed tool interface. The model proposes a tool call, the runtime validates arguments and permissions, the tool executes in an appropriate environment, and a structured observation returns to the trace. Tool design determines what the agent can safely and reliably do.

## Prompt

```text
Draw a typed tool interface diagram for a graduate-level machine learning textbook.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation.

CONCEPT:
Tool design is interface design. A model proposal must pass schema validation,
permission checks, execution policy, and structured observation capture.

MAIN COMPOSITION:
A left-to-right pipeline with five large stages.

STAGE 1 -- "MODEL PROPOSAL":
Show a model card emitting a tool call card:
"run_test(path='tests/test_api.py')".

STAGE 2 -- "SCHEMA VALIDATION":
Show a form/checklist with fields:
"tool name", "typed args", "required fields".
Add formula-like label: "JSON schema -> valid / reject".

STAGE 3 -- "PERMISSION + RISK":
Show a gate with badges:
"read-only", "reversible", "costly", "external side effect".
Use orange accent on "external side effect".

STAGE 4 -- "TOOL EXECUTION":
Show a sandbox box containing terminal, browser, and database icons.
Add label: "scoped environment".

STAGE 5 -- "STRUCTURED OBSERVATION":
Show a returned object card:
"status", "stdout", "stderr", "exit_code", "elapsed".
Connect it to a trace ledger labeled "trace".

BOTTOM STRIP:
Add the takeaway:
"tool design = schema + permissions + side effects + observation contract".

STYLE:
- Background: #FAFCFF
- Cards: white with thin #CFE3F7 borders
- Primary blue: #2D8CFF
- Pale fills: #D9EDFB and #E8F4FD
- Orange accent: #FF9F43 only on external side effect risk
- Text: #1A1A2E for headers, #6B7280 for annotations
- Clean sans-serif typography
- No gradients, no dark background, no product logos

IMPORTANT:
- This should look like an interface boundary, not a chatbot UI.
- Include the example function call and returned fields exactly.
- Keep the text technical and readable.
```

## Review Checklist

- [ ] Model proposal, validation, permission/risk, execution, observation are all present
- [ ] Example typed tool call appears
- [ ] Returned observation fields appear
- [ ] Bottom takeaway includes schema, permissions, side effects, observation contract

