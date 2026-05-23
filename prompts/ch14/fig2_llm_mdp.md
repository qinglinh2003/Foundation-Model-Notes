# Figure 14.2: Language Generation as a Degenerate MDP

**Filename**: `fig_llm_mdp.png`
**LaTeX label**: `fig:llm-mdp`
**Caption**: Language generation as a degenerate MDP. Each state is the prompt plus tokens generated so far; each action is the next token; transitions are deterministic; reward is sparse and arrives after the complete response.

## Prompt

```text
Draw a language-model MDP diagram for a graduate-level machine learning
textbook. Use a clean blue-white visual system: light blue background,
white cards, thin blue borders, charcoal text, and one soft orange
accent for the terminal reward.

CONCEPT:
Autoregressive generation is an MDP with unusually simple dynamics.
The state is the prompt plus prior tokens, the action is the next token,
the transition is deterministic append, and reward arrives only at the
end of the response.

MAIN COMPOSITION:
A left-to-right token-generation trajectory with 5 states. Each state is
a white card showing the growing text sequence. Between states, draw a
blue action token chip and a deterministic append arrow. At the far
right, show a verifier/reward box with the only orange element: a reward
badge.

STATE CARDS:
Create five state cards:
- State 0: "Prompt: Solve 7 x 8 + 3"
- State 1: "Prompt + The"
- State 2: "Prompt + The answer"
- State 3: "Prompt + The answer is"
- State 4: "Prompt + The answer is 59"
Use short text; do not include full reasoning traces.

ACTION CHIPS:
Between states, show token chips:
- "The"
- "answer"
- "is"
- "59"
Each chip is a small blue pill labeled "action = next token".

DETERMINISTIC TRANSITIONS:
Each arrow should be labeled "append token" in small gray text. Add a
small lock or gear icon near the arrows labeled "known transition".

SPARSE REWARD:
Above intermediate states, show tiny gray "r=0" tags. At the final
verifier box, show:
- A small calculator/checker icon
- Orange badge: "r = 1 if final answer correct"
- Label: "reward after full response"

BOTTOM STRIP:
A thin summary strip with four mapping chips:
"state = prompt + prefix" | "action = token" | "transition = append" |
"reward = end-of-sequence"

STYLE:
- Background: #FAFCFF
- Cards: white with #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF
- Pale blue fills: #E8F4FD
- Orange accent: #FF9F43 only for terminal reward badge
- Text: #1A1A2E; secondary labels: #6B7280
- Landscape orientation; clean sans-serif typography

IMPORTANT:
- Do not draw robots, games, or physical environments
- Do not use long paragraphs inside the figure
- The deterministic append operation must be visually clear
- Reward should be visibly absent until the final state
- Use only one orange focal point: the terminal reward
```

## Review Checklist

- [ ] Shows token-by-token state growth
- [ ] Actions are next-token chips
- [ ] Arrows are deterministic append transitions
- [ ] Intermediate rewards are r=0
- [ ] Final verifier gives orange reward badge
- [ ] Bottom strip maps MDP components to LLM generation
- [ ] Blue-white style with single orange accent
- [ ] Readable at 50% width in PDF

