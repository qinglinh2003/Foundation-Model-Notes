# Figure 18.2: Decoding as Distribution Navigation

**Filename**: `fig_decoding_distribution.png`  
**LaTeX label**: `fig:ch18-decoding-distribution`  
**Caption**: Decoding as distribution navigation. Greedy decoding follows the highest-probability token path; temperature and truncation methods expose alternative paths; beam search keeps high-likelihood prefixes. Candidate diversity begins at the decoding layer.

## Prompt

```text
Draw a textbook figure comparing decoding methods on a token distribution.
Use the course's Zoom-inspired blue-white visual system.
LANDSCAPE orientation.

CONCEPT:
An autoregressive model gives a next-token distribution. Decoding decides which path through the distribution becomes a candidate answer.

MAIN COMPOSITION:
Use a three-panel horizontal layout.

LEFT PANEL: "Next-token distribution"
Show a bar chart of token probabilities. One tall blue bar, several medium bars, many pale tail bars.
Label the y-axis "probability" and the x-axis "candidate next tokens" without tiny token names.

MIDDLE PANEL: "Sampling controls"
Show three mini overlays on the same distribution:
- Greedy: arrow to tallest bar.
- Temperature: two small curves labeled "lower T: sharper" and "higher T: flatter".
- Top-p / top-k: a highlighted blue subset of bars and a faded gray tail.

RIGHT PANEL: "Candidate paths"
Show a small branching tree of generated continuations.
One thick path labeled "greedy path".
Several thinner blue paths labeled "sampled alternatives".
A small warning note: "diversity helps only if selection works".

STYLE:
- Background #FAFCFF
- Primary blue #2D8CFF
- Pale blue #E8F4FD
- Gray tail #D1D5DB
- Orange #FF9F43 only for warning note
- Text #1A1A2E, annotations #6B7280
- Clean sans-serif typography
- No 3D, no glow, no dark background

IMPORTANT:
- Do not imply high temperature is always better.
- Make top-p/top-k truncation visually clear.
- Avoid tiny token labels; use abstract bars.
- Text must be readable at 50% PDF width.
```

## Review Checklist

- [ ] Greedy, temperature, top-k/top-p, and candidate paths all appear.
- [ ] Long tail is visible but de-emphasized.
- [ ] Candidate diversity is visually tied to decoding.
- [ ] No unreadable token labels.
