# Figure 11.8: Where SFT Helps and Where It Reaches Its Boundary

**Filename**: `fig_sft_boundary.png`
**LaTeX label**: `fig:sft-boundary`
**Caption**: Where SFT helps and where it reaches its boundary. Demonstration learning is strong for instruction following, formatting, tone, and basic refusal behavior. It is weaker when the target requires comparing alternatives, optimizing outcomes, or discovering reasoning strategies. Those gaps motivate preference learning, RLHF, and reasoning RL in later chapters.

## Prompt

```text
Draw an SFT capability-boundary diagram for a machine learning textbook. Use the
course's Zoom-inspired blue-white visual system. LANDSCAPE orientation, wide and
spacious. Match the visual richness of Ch10 "Three-Layer Schema" and Ch11
"Part III Roadmap": conceptual structure with concrete mini-illustrations inside
each region.

CONCEPT:
"SFT is strong imitation, but not direct outcome optimization." The figure should
separate what demonstration learning handles well from what requires preference
or reward signals.

MAIN COMPOSITION:
A wide horizontal boundary map with two main zones.

LEFT ZONE — SFT WORKS WELL:
Four filled capability cards arranged in a 2x2 grid:
- Instruction following: checklist response
- Format compliance: JSON/markdown card
- Tone/style: concise assistant bubble
- Basic refusal: safe refusal card
Each card should have a small internal example icon and a mostly filled blue
progress bar.

RIGHT ZONE — SFT HITS A CEILING:
Four partially filled cards:
- Preference nuance: chosen vs rejected response cards
- Complex reasoning: math scratchpad with uncertain final answer
- Distribution shift: out-of-domain user prompt
- Mode collapse: repeated same-shaped response cards
Each card should have a partial blue bar and a forward arrow to a later chapter:
Ch.13 DPO, Ch.15 RLHF, or Ch.16 reasoning RL.

CENTER BOUNDARY:
Draw a vertical dashed boundary labeled "imitation signal ends here." Use soft
orange (#FF9F43) only on this boundary and on one small tag:
"Need comparison or outcome signal."

BOTTOM SIGNAL STRIP:
Show the signal progression:
Demonstrations -> Preferences -> Human/AI reward -> Verifiable reward
as a thin blue strip with increasing signal strength. Keep Ch.11 highlighted as
the current point.

STYLE:
Use primary blue #2D8CFF, pale blue #E8F4FD, border #CFE3F7, charcoal #1A1A2E,
steel gray #6B7280, and soft orange #FF9F43 for the boundary accent only. Clean
technical textbook diagram, no dark background, no decorative blobs, no
photorealistic imagery. Text must be short and legible.
```

## Review Checklist

- [ ] SFT strengths and limits are visually separated.
- [ ] Later chapters are used as forward arrows, not as dense explanations.
- [ ] The central boundary communicates "imitation vs outcome signal."
- [ ] Only one orange focal element is used.

