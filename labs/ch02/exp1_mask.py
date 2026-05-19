"""
Exp 1: Causal mask ablation
============================
Train the same model twice -- once with the decoder causal mask enabled
(vanilla) and once with it disabled (broken). The broken model lets the
decoder peek at future target tokens during training. Loss looks great;
greedy decoding (which has no future to peek at) collapses.

The pedagogical point: a single missing mask invalidates an entire
training run, and the training-loss number alone will not tell you.

Outputs:
  answers/exp1_mask/
    masked/log.csv        unmasked/log.csv
    results.md            side-by-side metrics and sample contrast
    train_curves.png      both curves on one axes
"""

from __future__ import annotations
import argparse
import time
from pathlib import Path

import torch
import matplotlib.pyplot as plt

from data import build_dataloaders
from model import Seq2SeqTransformer
from utils import (
    MetricLogger, evaluate, format_results_table, load_metrics,
    set_seed, train_one_epoch,
)


OUT_DIR = Path(__file__).parent / "answers" / "exp1_mask"


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--epochs", type=int, default=12)
    p.add_argument("--batch-size", type=int, default=64)
    p.add_argument("--lr", type=float, default=3e-4)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    return p.parse_args()


def train_variant(name, use_causal_mask, train_loader, val_loader, vocab, args, sub_dir):
    sub_dir.mkdir(parents=True, exist_ok=True)
    set_seed(args.seed)
    model = Seq2SeqTransformer(
        vocab_size=vocab.size, pad_idx=vocab.pad_idx,
        use_causal_mask=use_causal_mask,
    ).to(args.device)
    optim = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=0.01)
    logger = MetricLogger(str(sub_dir / "log.csv"), ["step", "loss"])

    print(f"\n[{name}] training (use_causal_mask={use_causal_mask})")
    start = time.time()
    step = 0
    final_train_loss = None
    for epoch in range(args.epochs):
        final_train_loss, step = train_one_epoch(
            model, train_loader, optim, vocab, args.device,
            logger=logger, global_step=step,
        )
        if epoch == 0 or (epoch + 1) % 4 == 0:
            print(f"  epoch {epoch+1:2d}/{args.epochs}  avg loss {final_train_loss:.4f}")
    wall = (time.time() - start) / 60
    logger.close()

    print(f"[{name}] evaluating (greedy decode)...")
    eval_val = evaluate(model, val_loader, vocab, args.device)
    return {
        "name": name,
        "final_train_loss": final_train_loss,
        "eval_val": eval_val,
        "wall_min": wall,
    }


def write_results_md(out_md, results, args):
    masked = results["masked"]
    unmasked = results["unmasked"]

    # Pull aligned sample predictions
    def sample_str(samples, n=15):
        lines = []
        for s in samples[:n]:
            check = "OK " if s["correct"] else "X  "
            lines.append(
                f"{check} {s['lemma']:10s} ({s['tag']:7s}) "
                f"-> pred={s['pred']!r:14s} gold={s['gold']!r}"
            )
        return "\n".join(lines)

    body = f"""# Exp 1: Causal Mask Ablation

Two trainings of the same model. The only difference is whether the
decoder applies a causal mask in self-attention.

## The trap

A model trained without the causal mask sees future target tokens
during teacher forcing. Loss drops near zero. Then at inference
(greedy decoding), there is no future to see, and the model has
never learned to predict from past-only context.

## Headline numbers

| Variant                              | Final train loss | Val exact-match |
|--------------------------------------|------------------|-----------------|
| Vanilla (causal mask **on**)         | {masked['final_train_loss']:.4f}            | {masked['eval_val']['overall']*100:.1f}%        |
| Broken  (causal mask **off**)        | {unmasked['final_train_loss']:.4f}            | {unmasked['eval_val']['overall']*100:.1f}%        |

Notice the broken model's training loss is essentially solved, yet
greedy-decode accuracy collapses.

## Full accuracy tables

### Vanilla

```
{format_results_table(masked['eval_val'])}
```

### Broken (no causal mask)

```
{format_results_table(unmasked['eval_val'])}
```

## Sample predictions (greedy decode)

### Vanilla

```
{sample_str(masked['eval_val']['samples'])}
```

### Broken

```
{sample_str(unmasked['eval_val']['samples'])}
```

## Diagnosis

The training objective is teacher forcing: the model receives the
correct previous targets and predicts the next token. Without the
causal mask, the decoder self-attention can attend to ALL target
positions including the future. The optimal solution is to read the
target at position t+1 directly when predicting position t -- a
shortcut that vanishes at inference. This is the most expensive
silent bug in Transformer implementations. Always run
`verify.no_future_leakage` before trusting a training-loss curve.

## Hyperparameters

epochs={args.epochs}, batch={args.batch_size}, lr={args.lr}, seed={args.seed}, device={args.device}
"""
    out_md.write_text(body)


def main():
    args = parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    train_loader, val_loader, _, vocab, info = build_dataloaders(
        batch_size=args.batch_size, seed=args.seed,
    )
    print(f"Train / Val: {info['n_train']} / {info['n_val']}")

    masked = train_variant("masked", True, train_loader, val_loader, vocab, args, OUT_DIR / "masked")
    unmasked = train_variant("unmasked", False, train_loader, val_loader, vocab, args, OUT_DIR / "unmasked")

    # Combined train-curve plot
    fig, ax = plt.subplots(figsize=(8, 4))
    for variant, color, label in [(masked, "#2980B9", "vanilla (mask on)"),
                                   (unmasked, "#E74C3C", "broken (mask off)")]:
        data = load_metrics(str(OUT_DIR / variant["name"] / "log.csv"))
        ax.plot(data["step"], data["loss"], color=color, linewidth=0.8, label=label)
    ax.set_xlabel("Training Step")
    ax.set_ylabel("Cross-Entropy Loss")
    ax.set_title("Exp 1: Training loss with and without decoder causal mask")
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(OUT_DIR / "train_curves.png", dpi=150, bbox_inches="tight")
    plt.close(fig)

    write_results_md(OUT_DIR / "results.md", {"masked": masked, "unmasked": unmasked}, args)
    print(f"\nArtifacts saved to {OUT_DIR}")


if __name__ == "__main__":
    main()
