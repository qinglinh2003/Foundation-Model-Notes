# Figure 11.2: Completion Behavior Versus Instruction Behavior

**Filename**: `fig_completion_vs_instruction.png`
**LaTeX label**: `fig:completion-vs-instruction`
**Caption**: Completion behavior versus instruction behavior. A base model treats the prompt as a prefix to continue, while an instruction-tuned model treats it as a request to answer. The architecture and pretrained knowledge are the same; the post-training data changes which continuation the model considers appropriate.

## Prompt

```text
Draw a completion-versus-instruction behavior diagram for a machine learning
textbook. Use the course's Zoom-inspired blue-white visual system. LANDSCAPE
orientation, wide and spacious. Match the visual richness of Ch10 "Prompt
Sensitivity" and Ch10 "ICL Regime Spectrum": concrete prompt blocks, internal
mini-visuals, and a clear conceptual contrast.

CONCEPT:
"Same model family, different conditional distribution." The figure should show
that a pretrained base model continues text, while an instruction-tuned model
answers the user's request.

MAIN COMPOSITION:
A two-panel "before / after" comparison.

LEFT PANEL — BASE MODEL AS COMPLETER:
Header: "Base LM: continue the prefix"
Show a prompt card:
  What is the capital of France?
Below it, show generated continuations as a web-text list:
  What is the capital of Germany?
  What is the capital of Italy?
  What is the capital of Spain?
Add a faint background texture of web documents and list pages. Add a small
conditional label:
  P(continuation | prefix)

RIGHT PANEL — INSTRUCTION-TUNED MODEL AS ASSISTANT:
Header: "Instruction-tuned LM: answer the request"
Show the same prompt card, but now routed into an assistant response card:
  The capital of France is Paris.
Add a small assistant chat bubble, check mark, and concise answer formatting.
Add a conditional label:
  P(response | instruction)

CENTER BRIDGE:
Between panels, draw a blue model chip that is visually the same on both sides,
with a post-training data arrow passing through it. The arrow should be labeled
"SFT demonstrations." Use soft orange (#FF9F43) only on this arrow and a small
"behavior shift" badge.

STYLE:
Use primary blue #2D8CFF, pale blue #E8F4FD, border #CFE3F7, charcoal #1A1A2E,
steel gray #6B7280, and soft orange #FF9F43 for one accent only. Clean technical
textbook diagram, not a business slide. No dark background, no decorative blobs,
no photorealistic people. Keep all text short and legible.
```

## Review Checklist

- [ ] The same prompt appears in both panels.
- [ ] The left side clearly continues text instead of answering.
- [ ] The right side clearly answers as an assistant.
- [ ] The orange accent is reserved for the SFT behavior-shift arrow.

