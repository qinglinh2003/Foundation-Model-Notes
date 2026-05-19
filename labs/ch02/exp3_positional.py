"""
Exp 3: Positional encoding ablation
====================================
Train four PE variants and measure how each fails on the inflection
task:

    enc_PE  dec_PE   role
    ------  ------   ----------------------------------------
      on      on     vanilla
      off     on     encoder cannot distinguish lemma char order
      on      off    decoder cannot count output positions
      off     off    no positional information anywhere

Outputs:
  answers/exp3_positional/
    train_<config>/log.csv
    results.md
"""

from __future__ import annotations
import argparse
import time
from pathlib import Path

import torch

from data import build_dataloaders
from model import Seq2SeqTransformer
from utils import (
    MetricLogger, evaluate, format_results_table,
    set_seed, train_one_epoch,
)


OUT_DIR = Path(__file__).parent / "answers" / "exp3_positional"

CONFIGS = [
    # (label,         enc_pe, dec_pe)
    ("enc_on_dec_on",   True,  True),
    ("enc_off_dec_on",  False, True),
    ("enc_on_dec_off",  True,  False),
    ("enc_off_dec_off", False, False),
]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--epochs", type=int, default=12)
    p.add_argument("--batch-size", type=int, default=64)
    p.add_argument("--lr", type=float, default=3e-4)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    return p.parse_args()


def train_variant(label, enc_pe, dec_pe, loaders, vocab, args, sub_dir):
    sub_dir.mkdir(parents=True, exist_ok=True)
    set_seed(args.seed)
    model = Seq2SeqTransformer(
        vocab_size=vocab.size, pad_idx=vocab.pad_idx,
        use_encoder_pe=enc_pe, use_decoder_pe=dec_pe,
    ).to(args.device)
    optim = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=0.01)
    logger = MetricLogger(str(sub_dir / "log.csv"), ["step", "loss"])

    print(f"\n[{label}] training (enc_pe={enc_pe}, dec_pe={dec_pe})")
    train_loader, val_loader = loaders
    start = time.time()
    step = 0
    last_loss = float("nan")
    for epoch in range(args.epochs):
        last_loss, step = train_one_epoch(
            model, train_loader, optim, vocab, args.device,
            logger=logger, global_step=step,
        )
        if epoch == 0 or (epoch + 1) % 4 == 0:
            print(f"  epoch {epoch+1:2d}/{args.epochs}  avg loss {last_loss:.4f}")
    wall = (time.time() - start) / 60
    logger.close()
    return {
        "label": label,
        "final_train_loss": last_loss,
        "eval_val": evaluate(model, val_loader, vocab, args.device),
        "wall_min": wall,
    }


def write_results_md(out_md, results, args):
    rows = []
    for cfg, _, _ in [(c[0], c[1], c[2]) for c in CONFIGS]:
        r = results[cfg]["eval_val"]
        pr = r["by_category"].get("pure_regular", 0) * 100
        ph = r["by_category"].get("phonological", 0) * 100
        ir = r["by_category"].get("irregular", 0) * 100
        rows.append(
            f"| {cfg:18s} | {pr:5.1f}% | {ph:5.1f}% | {ir:5.1f}% | {r['overall']*100:5.1f}% |"
        )

    detail = []
    for cfg, _, _ in [(c[0], c[1], c[2]) for c in CONFIGS]:
        detail.append(f"\n### {cfg}\n\n```\n{format_results_table(results[cfg]['eval_val'])}\n```\n")

    body = f"""# Exp 3: Positional Encoding Ablation

Self-attention is permutation-equivariant. Without explicit position
information, the encoder cannot tell `cat` from `act`; the decoder
cannot tell `walk-step-3` from `walk-step-1`. Sinusoidal PE injects
that information by adding fixed per-position vectors to the
embeddings.

## Headline numbers

| variant            | pure_regular | phonological | irregular | overall |
|--------------------|--------------|--------------|-----------|---------|
{chr(10).join(rows)}

## Detail per variant
{chr(10).join(detail)}

## Diagnosis

Removing encoder PE most severely hurts patterns where the lemma's
suffix matters: phonological (e.g., `try -> tried` -- the model must
see that `y` is the last character, not just present somewhere).
Pure regulars suffer too, just less, because the decoder can still
emit a fixed suffix string.

Removing decoder PE breaks the autoregressive count: the decoder
cannot tell whether it has emitted 1 or 5 characters so far. Greedy
generation either truncates early or rambles past the correct ending.

Removing both is the harshest setting and approximates a permutation-
invariant Seq2Seq model, which cannot solve any positional task.

Note: sinusoidal PE generalizes to unseen positions, so the same
model trained on lemma length <= 10 can in principle decode longer
sequences at inference. We probe this in `exp_stretch.py`.

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

    results = {}
    for label, enc_pe, dec_pe in CONFIGS:
        results[label] = train_variant(
            label, enc_pe, dec_pe,
            (train_loader, val_loader), vocab, args,
            OUT_DIR / f"train_{label}",
        )
        r = results[label]["eval_val"]
        print(f"  {label:18s}  overall={r['overall']*100:.1f}%")

    write_results_md(OUT_DIR / "results.md", results, args)
    print(f"\nArtifacts saved to {OUT_DIR}")


if __name__ == "__main__":
    main()
