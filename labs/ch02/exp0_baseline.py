"""
Exp 0: Vanilla baseline
========================
Train the unmodified encoder-decoder Transformer on morphological
inflection. Establishes the ceiling against which every ablation in
Experiments 1-4 is compared.

Outputs:
  answers/exp0_baseline/
    log.csv                 per-step training loss
    train_curve.png         loss vs. step
    results.md              accuracy table + sample predictions
    checkpoint.pt           trained weights (reused by Exp 4 visualization)
"""

from __future__ import annotations
import argparse
import time
from pathlib import Path

import torch
import torch.nn as nn
import matplotlib.pyplot as plt

from data import build_dataloaders
from model import Seq2SeqTransformer
from utils import (
    MetricLogger, evaluate, format_results_table, load_metrics,
    set_seed, train_one_epoch,
)


OUT_DIR = Path(__file__).parent / "answers" / "exp0_baseline"


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--epochs", type=int, default=20)
    p.add_argument("--batch-size", type=int, default=64)
    p.add_argument("--lr", type=float, default=3e-4)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    return p.parse_args()


def train_curve_plot(log_csv: Path, out_png: Path):
    data = load_metrics(str(log_csv))
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(data["step"], data["loss"], linewidth=0.8)
    ax.set_xlabel("Training Step")
    ax.set_ylabel("Cross-Entropy Loss")
    ax.set_title("Exp 0: Vanilla Baseline — Training Loss")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close(fig)


def write_results_md(out_md: Path, eval_train, eval_val, args, n_params, wall_min):
    sample_lines = []
    for s in eval_val["samples"][:25]:
        check = "OK " if s["correct"] else "X  "
        sample_lines.append(
            f"{check} {s['lemma']:10s} ({s['tag']:7s}, {s['category']:14s}) "
            f"-> pred={s['pred']!r:14s} gold={s['gold']!r}"
        )

    body = f"""# Exp 0: Vanilla Baseline

**Configuration**: vanilla encoder-decoder Transformer, all 5 modules enabled.
**Parameters**: {n_params:,}
**Wall time**: {wall_min:.1f} min on {args.device}
**Hyperparameters**: epochs={args.epochs}, batch={args.batch_size}, lr={args.lr}, seed={args.seed}

## Train set accuracy

```
{format_results_table(eval_train)}
```

## Validation set accuracy

```
{format_results_table(eval_val)}
```

## Validation sample predictions (first 25)

```
{chr(10).join(sample_lines)}
```

## Notes

This is the ceiling. Every ablation in Exp 1-4 reduces one or more
of the model's structural ingredients and measures how far accuracy
falls. A useful sanity check before reading further: examine the
irregular row in the validation table -- that is the bucket where
attention's per-token routing must combine with FFN's per-token
nonlinearity. If you see the irregular column near 0, your training
budget is probably too small; increase --epochs.
"""
    out_md.write_text(body)


def main():
    args = parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    set_seed(args.seed)

    train_loader, val_loader, _, vocab, info = build_dataloaders(
        batch_size=args.batch_size, seed=args.seed,
    )
    print(f"Train / Val: {info['n_train']} / {info['n_val']}")

    model = Seq2SeqTransformer(vocab_size=vocab.size, pad_idx=vocab.pad_idx).to(args.device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"Model parameters: {n_params:,}")

    optim = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=0.01)
    logger = MetricLogger(str(OUT_DIR / "log.csv"), ["step", "loss"])

    start = time.time()
    global_step = 0
    for epoch in range(args.epochs):
        avg_loss, global_step = train_one_epoch(
            model, train_loader, optim, vocab, args.device,
            logger=logger, global_step=global_step,
        )
        print(f"  epoch {epoch+1:2d}/{args.epochs}  avg loss {avg_loss:.4f}")
    wall_min = (time.time() - start) / 60
    logger.close()

    # Trim eval set on training data: subsample to ~5k to keep eval fast
    print("\nEvaluating on training (subsample) and validation sets...")
    from torch.utils.data import Subset, DataLoader
    sub_idx = list(range(min(5000, len(train_loader.dataset))))
    sub_train_loader = DataLoader(Subset(train_loader.dataset, sub_idx), batch_size=args.batch_size)
    eval_train = evaluate(model, sub_train_loader, vocab, args.device)
    eval_val = evaluate(model, val_loader, vocab, args.device)

    print("\n" + format_results_table(eval_val, "Validation accuracy"))

    train_curve_plot(OUT_DIR / "log.csv", OUT_DIR / "train_curve.png")
    write_results_md(OUT_DIR / "results.md", eval_train, eval_val, args, n_params, wall_min)
    torch.save({"model_state": model.state_dict(),
                "vocab_size": vocab.size, "pad_idx": vocab.pad_idx},
               OUT_DIR / "checkpoint.pt")
    print(f"\nArtifacts saved to {OUT_DIR}")


if __name__ == "__main__":
    main()
