# Figure 14.6: RL Landscape for LLM Post-Training

**Filename**: `fig_rl_landscape.png`
**LaTeX label**: `fig:rl-landscape`
**Caption**: The RL landscape: what this chapter covered versus what exists. The chapter focuses on policy-gradient methods because they are central to LLM post-training. The muted branches show representative out-of-scope areas; offline RL and temporal credit assignment are noted in the text but are not expanded into a full taxonomy here.

## Prompt

```text
Draw an RL landscape map for a graduate-level machine learning textbook.
Use a clean blue-white visual system: light blue background, white cards,
thin blue borders, charcoal text, and one soft orange accent for the
path covered in this chapter.

CONCEPT:
Reinforcement learning is broad, but LLM post-training mostly uses the
policy-gradient branch. The figure should show the broader landscape
while clearly highlighting the narrow path this chapter covered. This is
a scope map, not a complete taxonomy of every RL subfield.

MAIN COMPOSITION:
A branching roadmap from left to right. Start with a large root node
"Reinforcement Learning". Split into four branches:
1. Policy gradients
2. Value-based methods
3. Model-based RL
4. Multi-agent / exploration-heavy RL

HIGHLIGHTED BRANCH -- "POLICY GRADIENTS":
This branch should be the only branch with a soft orange path line. It
contains four connected nodes:
"REINFORCE" -> "Importance sampling" -> "TRPO" -> "PPO / GRPO-style variants"
Inside each node, include a tiny icon:
- REINFORCE: reward-weighted gradient arrow
- Importance sampling: ratio badge rho
- TRPO: trust-region circle
- PPO/GRPO: clipped ratio bracket
Add label: "covered in this chapter"

OTHER BRANCHES:
Use muted blue-gray cards, not orange:
- Value-based: Q-learning, DQN; icon = value table
- Model-based: world model, planning; icon = small map
- Exploration-heavy: bonuses, curiosity; icon = compass
- Multi-agent: self-play, game dynamics; icon = two policy blocks
Add small note under these branches: "important in RL, not central here"

SIDE NOTE BADGES:
Add two small muted side badges near the bottom edge, separate from the
main branches:
- "Offline RL: related to DPO, not expanded here"
- "Temporal credit assignment: deferred to process rewards"
These should be small annotations, not full branches.

BOTTOM STRIP:
A concise scope statement:
"For LLM post-training: generate -> score -> policy-gradient update ->
stay close to reference"

STYLE:
- Background: #FAFCFF
- Cards: white with #CFE3F7 borders and subtle shadow
- Primary blue: #2D8CFF
- Muted branches: #6B7280 text and #E8F4FD fills
- Orange accent: #FF9F43 only for the covered policy-gradient path
- Text: #1A1A2E; secondary labels: #6B7280
- Landscape orientation, spacious branching map

IMPORTANT:
- Do not make this a dense academic taxonomy
- Do not imply other RL branches are unimportant, only out of scope
- The policy-gradient path must be visually dominant
- Keep text short inside each node
- Do not use dark backgrounds or neon colors
```

## Review Checklist

- [ ] Root node: Reinforcement Learning
- [ ] Four branches: policy gradients, value-based, model-based, multi-agent/exploration
- [ ] Small side badges mention offline RL and temporal credit assignment
- [ ] Orange highlighted path: REINFORCE -> IS -> TRPO -> PPO/GRPO-style variants
- [ ] Other branches muted but visible
- [ ] Bottom strip states LLM post-training loop
- [ ] Does not dismiss non-policy-gradient RL
- [ ] Blue-white style with single orange path
- [ ] Readable at 50% width in PDF
