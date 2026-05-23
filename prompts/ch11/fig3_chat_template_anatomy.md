# Figure 11.3: Anatomy of a Chat Template

**Filename**: `fig_chat_template_anatomy.png`
**LaTeX label**: `fig:chat-template-anatomy`
**Caption**: Anatomy of a chat template. System, user, and assistant spans are serialized into one token sequence with role delimiters. The same structure controls both generation boundaries and loss masking: user tokens are context, assistant tokens are behavior to imitate.

## Prompt

```text
Draw a chat-template anatomy diagram for a machine learning textbook. Use the
course's Zoom-inspired blue-white visual system. LANDSCAPE orientation, wide and
spacious. Match the visual richness of Ch4 "Signal Density" and Ch11 "Sequence
Packing": token-level detail, clear masking overlays, and compact technical
labels.

CONCEPT:
"A chat conversation is serialized into one token sequence, and the template
defines which tokens are context versus supervised assistant behavior."

MAIN COMPOSITION:
Use a three-tier technical diagram.

TOP TIER — HUMAN-READABLE CONVERSATION:
Three stacked chat cards:
1. System: "You are a helpful assistant."
2. User: "Explain LoRA in one sentence."
3. Assistant: "LoRA fine-tunes small low-rank adapter matrices..."
Use role icons or small role badges, but keep them simple.

MIDDLE TIER — SERIALIZED TEMPLATE:
Show the same conversation flattened into a long token strip with role
delimiters:
<|system|> ... <|user|> ... <|assistant|> ...
Represent delimiters as small charcoal badges, system tokens as pale gray-blue,
user tokens as pale blue, assistant tokens as primary blue.

BOTTOM TIER — TRAINING SIGNAL OVERLAY:
Align a loss-mask strip under the serialized sequence. System and user spans are
muted and labeled "context only." Assistant span glows in soft orange (#FF9F43)
and is labeled "loss = 1." Add an EOS/end-of-turn marker at the end of the
assistant span, with a tiny stop-sign icon or stop badge.

SIDE CALLOUTS:
Add three small callout cards:
- "Role boundaries"
- "Stop token"
- "Loss mask"
Each callout should point to the relevant location in the token strip.

STYLE:
Use primary blue #2D8CFF, pale blue #E8F4FD, border #CFE3F7, charcoal #1A1A2E,
steel gray #6B7280, and soft orange #FF9F43 only for supervised assistant
tokens. Clean technical textbook diagram; no dark background, no gradient, no
decorative blobs. Text must be sparse and readable at textbook width.
```

## Review Checklist

- [ ] Human-readable conversation and serialized token sequence are visibly connected.
- [ ] Role delimiters are clear but not over-dominant.
- [ ] Only assistant tokens have loss = 1.
- [ ] EOS/end-of-turn behavior is visible.

