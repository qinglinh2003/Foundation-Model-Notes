# Exp Stretch (summary)

Three probes that need no extra training; they reuse the vanilla
checkpoint produced by Exp 0.

- **S1 sqrt(d_k) scaling**: see `dk_softmax_entropy.png` for how
  scaling preserves softmax entropy as d_k grows.
- **S2 Wug test**: see `wug_results.md`. Overall 95.5% on
  pseudo-words.
- **S3 length generalization**: see `length_generalization.md`. Per-length
  accuracy reported.

The headline is that productive rule learning, sinusoidal PE
extrapolation, and softmax scaling are all measurable in isolation
once the main lab is done -- each takes seconds-to-minutes.
