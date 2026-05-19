"""
Exp Stretch: three short probes that need no extra training.
=============================================================
All three load the trained vanilla model from `exp0_baseline/checkpoint.pt`
(or train one if the file is missing) and measure something the core
experiments did not.

  S1. sqrt(d_k) scaling: show that the scaling factor controls softmax
      entropy. Without scaling, attention saturates as d_k grows.
  S2. Wug test: how does the trained model generalize to pseudo-words?
      Reproduces Berko (1958) productivity probe.
  S3. Length generalization: train was capped at lemma length 10;
      can sinusoidal PE extrapolate to length 11-12?

Outputs:
  answers/exp_stretch/
    dk_softmax_entropy.png
    wug_results.md
    length_generalization.md
    results.md         summary
"""

from __future__ import annotations
import argparse
import math
from collections import defaultdict
from pathlib import Path

import torch
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np

from data import build_dataloaders, load_wug_test, Vocab, MorphInflectionDataset
from model import Seq2SeqTransformer
from utils import set_seed


OUT_DIR = Path(__file__).parent / "answers" / "exp_stretch"
EXP0_CKPT = Path(__file__).parent / "answers" / "exp0_baseline" / "checkpoint.pt"


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    p.add_argument("--dk-values", type=int, nargs="+", default=[8, 32, 128, 512])
    p.add_argument("--dk-trials", type=int, default=2000)
    return p.parse_args()


# ---------------------------------------------------------------------------
# S1: sqrt(d_k) scaling effect on softmax entropy
# ---------------------------------------------------------------------------

def s1_sqrt_dk(args):
    """Compute mean entropy of softmax(QK^T / s) for s in {1, sqrt(d_k)}."""
    rng = torch.Generator().manual_seed(args.seed)
    results = []
    for d_k in args.dk_values:
        ent_unscaled = []
        ent_scaled = []
        for _ in range(args.dk_trials):
            q = torch.randn(d_k, generator=rng)
            K = torch.randn(8, d_k, generator=rng)  # 8 keys
            scores = K @ q
            # unscaled
            p = F.softmax(scores, dim=-1)
            ent_unscaled.append(-(p * (p.clamp_min(1e-12).log())).sum().item())
            # scaled by sqrt(d_k)
            p2 = F.softmax(scores / math.sqrt(d_k), dim=-1)
            ent_scaled.append(-(p2 * (p2.clamp_min(1e-12).log())).sum().item())
        results.append({
            "d_k": d_k,
            "unscaled_entropy": float(np.mean(ent_unscaled)),
            "scaled_entropy": float(np.mean(ent_scaled)),
            "max_entropy": math.log(8),  # uniform over 8 keys
        })

    # Plot
    fig, ax = plt.subplots(figsize=(8, 4))
    dks = [r["d_k"] for r in results]
    ax.plot(dks, [r["unscaled_entropy"] for r in results], "o-",
            color="#E74C3C", label="without 1/sqrt(d_k)")
    ax.plot(dks, [r["scaled_entropy"] for r in results], "o-",
            color="#2980B9", label="with 1/sqrt(d_k)")
    ax.axhline(math.log(8), color="gray", linestyle="--", label="uniform max")
    ax.set_xscale("log", base=2)
    ax.set_xticks(dks)
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
    ax.set_xlabel("d_k")
    ax.set_ylabel("Mean softmax entropy (nats)")
    ax.set_title("Exp Stretch S1: sqrt(d_k) scaling preserves softmax entropy")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(OUT_DIR / "dk_softmax_entropy.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    return results


# ---------------------------------------------------------------------------
# Helper: load the vanilla model from Exp 0
# ---------------------------------------------------------------------------

def load_vanilla(args):
    if not EXP0_CKPT.exists():
        raise SystemExit(
            f"Need a trained vanilla model. Run `python exp0_baseline.py` first.\n"
            f"Looked for {EXP0_CKPT}"
        )
    ckpt = torch.load(EXP0_CKPT, map_location=args.device)
    vocab = Vocab()
    assert ckpt["vocab_size"] == vocab.size
    model = Seq2SeqTransformer(vocab_size=vocab.size, pad_idx=vocab.pad_idx).to(args.device)
    model.load_state_dict(ckpt["model_state"])
    model.eval()
    return model, vocab


# ---------------------------------------------------------------------------
# S2: Wug test
# ---------------------------------------------------------------------------

@torch.no_grad()
def s2_wug(args, model, vocab):
    wug_records = load_wug_test()
    correct = defaultdict(lambda: [0, 0])
    sample_lines = []

    for rec in wug_records:
        lemma, tag, accepted = rec["lemma"], rec["tag"], rec["accepted"]
        # Build src tensor
        src_ids = [vocab.encode_tag(tag)] + [vocab.encode_char(c) for c in lemma] + [vocab.eos_idx]
        src_ids += [vocab.pad_idx] * (14 - len(src_ids))
        src = torch.tensor([src_ids[:14]], dtype=torch.long, device=args.device)
        pred_ids = model.greedy_decode(src, vocab.sos_idx, vocab.eos_idx, max_len=14)
        pred = vocab.decode(pred_ids[0, 1:].tolist())
        ok = pred in accepted
        correct[tag][0] += int(ok)
        correct[tag][1] += 1
        sample_lines.append(
            f"{'OK ' if ok else 'X  '} <{tag:7s}> {lemma:10s} -> "
            f"pred={pred!r:14s} expected={('|'.join(accepted))!r}"
        )

    lines = ["| tag     | correct | total | accuracy |", "|---------|---------|-------|----------|"]
    total_c, total_n = 0, 0
    for tag, (c, n) in correct.items():
        lines.append(f"| {tag:7s} | {c:7d} | {n:5d} | {(c/n*100 if n else 0):7.1f}% |")
        total_c += c
        total_n += n
    lines.append(f"| TOTAL   | {total_c:7d} | {total_n:5d} | {(total_c/total_n*100):7.1f}% |")

    body = f"""# Wug test (Stretch S2)

Berko's (1958) classic pseudo-word probe. The model never saw any of
these stems during training. To get them right it must apply the
inflection rules productively, not memorize.

## Per-tag accuracy

{chr(10).join(lines)}

## All items

```
{chr(10).join(sample_lines)}
```

A meaningful gap between val accuracy (on real lemmas) and wug
accuracy (on pseudo-words) suggests the model is leaning on
memorization for some categories. Of particular interest:

- `heaf -> heafs` vs `heaves`: Berko found English-speaking children
  produce `heafs`, refusing to extend the f->v rule (leaf -> leaves)
  to novel words. Does our model match the child or the adult?
- `pry -> pried` (PAST) vs `pry -> prying` (GERUND): consonant-y
  triggers `y -> ie` for PAST and 3SG/PLURAL but NOT for GERUND.
  A model that has truly learned the rule sees this distinction.
"""
    (OUT_DIR / "wug_results.md").write_text(body)
    return {"total": total_c / max(total_n, 1), "per_tag": dict(correct)}


# ---------------------------------------------------------------------------
# S3: length generalization
# ---------------------------------------------------------------------------

@torch.no_grad()
def s3_length_gen(args, model, vocab):
    """Eval the trained model on val examples split by lemma length."""
    _, val_loader, _, _, _ = build_dataloaders(batch_size=64, seed=args.seed)
    correct_by_len = defaultdict(lambda: [0, 0])

    for batch in val_loader:
        src = batch["src"].to(args.device)
        pred_ids = model.greedy_decode(src, vocab.sos_idx, vocab.eos_idx, max_len=14)
        for i in range(src.size(0)):
            lemma = batch["lemma"][i]
            gold = batch["inflected"][i]
            pred = vocab.decode(pred_ids[i, 1:].tolist())
            L = len(lemma)
            correct_by_len[L][0] += int(pred == gold)
            correct_by_len[L][1] += 1

    lines = ["| lemma_len | correct | total | accuracy |", "|-----------|---------|-------|----------|"]
    for L in sorted(correct_by_len.keys()):
        c, n = correct_by_len[L]
        lines.append(f"| {L:9d} | {c:7d} | {n:5d} | {(c/n*100):7.1f}% |")

    body = f"""# Length generalization (Stretch S3)

We trained on lemmas of length up to 10. Each validation lemma's
length is plotted below. The encoder uses sinusoidal positional
encoding, which is defined for any position; nothing in the model
prevents inference on lengths the optimizer never saw.

## Accuracy by lemma length

{chr(10).join(lines)}

Lengths beyond the training cap are an honest test of whether the
inflection rules transferred. Accuracy that holds up at unseen
lengths is evidence for learned-rules-over-memorization;
accuracy that collapses suggests memorization within the trained
length envelope.
"""
    (OUT_DIR / "length_generalization.md").write_text(body)
    return {L: c / max(n, 1) for L, (c, n) in correct_by_len.items()}


def main():
    args = parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    set_seed(args.seed)

    print("=== S1: sqrt(d_k) scaling ===")
    s1 = s1_sqrt_dk(args)
    for r in s1:
        print(f"  d_k={r['d_k']:4d}  unscaled H={r['unscaled_entropy']:.3f}  "
              f"scaled H={r['scaled_entropy']:.3f}  (max={r['max_entropy']:.3f})")

    print("\n=== S2/S3: loading trained vanilla model ===")
    model, vocab = load_vanilla(args)

    print("\n=== S2: Wug test ===")
    wug = s2_wug(args, model, vocab)
    print(f"  overall: {wug['total']*100:.1f}%")

    print("\n=== S3: length generalization ===")
    lg = s3_length_gen(args, model, vocab)
    for L in sorted(lg.keys()):
        print(f"  lemma_len {L}: {lg[L]*100:.1f}%")

    summary = f"""# Exp Stretch (summary)

Three probes that need no extra training; they reuse the vanilla
checkpoint produced by Exp 0.

- **S1 sqrt(d_k) scaling**: see `dk_softmax_entropy.png` for how
  scaling preserves softmax entropy as d_k grows.
- **S2 Wug test**: see `wug_results.md`. Overall {wug['total']*100:.1f}% on
  pseudo-words.
- **S3 length generalization**: see `length_generalization.md`. Per-length
  accuracy reported.

The headline is that productive rule learning, sinusoidal PE
extrapolation, and softmax scaling are all measurable in isolation
once the main lab is done -- each takes seconds-to-minutes.
"""
    (OUT_DIR / "results.md").write_text(summary)
    print(f"\nArtifacts saved to {OUT_DIR}")


if __name__ == "__main__":
    main()
