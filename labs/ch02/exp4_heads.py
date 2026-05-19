"""
Exp 4: Multi-head ablation + cross-attention visualization
===========================================================
Train h = 1, 4, 8 head variants (d_model fixed at 128). Compare
accuracy. Then take the h=4 trained model and plot cross-attention
heatmaps for a handful of test examples -- show whether different
heads have specialized to different parts of the input (tag token
vs. lemma stem vs. lemma suffix).

Outputs:
  answers/exp4_heads/
    train_h<N>/log.csv
    train_h<N>/results.md
    cross_attn_<example>.png   per-test-example, 4-head grid
    results.md
"""

from __future__ import annotations
import argparse
import time
from pathlib import Path

import torch
import matplotlib.pyplot as plt
import numpy as np

from data import build_dataloaders
from model import Seq2SeqTransformer
from utils import (
    MetricLogger, evaluate, format_results_table,
    set_seed, train_one_epoch,
)


OUT_DIR = Path(__file__).parent / "answers" / "exp4_heads"

HEAD_COUNTS = [1, 4, 8]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--epochs", type=int, default=12)
    p.add_argument("--batch-size", type=int, default=64)
    p.add_argument("--lr", type=float, default=3e-4)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    p.add_argument("--num-vis-examples", type=int, default=6)
    return p.parse_args()


def train_variant(num_heads, loaders, vocab, args, sub_dir):
    sub_dir.mkdir(parents=True, exist_ok=True)
    set_seed(args.seed)
    model = Seq2SeqTransformer(
        vocab_size=vocab.size, pad_idx=vocab.pad_idx, num_heads=num_heads,
    ).to(args.device)
    optim = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=0.01)
    logger = MetricLogger(str(sub_dir / "log.csv"), ["step", "loss"])

    print(f"\n[h={num_heads}] training")
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
    print(f"[h={num_heads}] evaluating...")
    eval_val = evaluate(model, val_loader, vocab, args.device)
    return {
        "h": num_heads, "model": model, "final_train_loss": last_loss,
        "eval_val": eval_val, "wall_min": wall,
    }


def visualize_cross_attention(model, vocab, val_loader, args, num_examples):
    """Pick a few diverse validation examples and plot per-head cross-attention."""
    model.eval()
    picked = []  # records to visualize: aim for one per (tag, category) combo
    seen = set()
    for batch in val_loader:
        for i in range(batch["src"].size(0)):
            key = (batch["tag"][i], batch["category"][i])
            if key in seen:
                continue
            seen.add(key)
            picked.append({
                "src": batch["src"][i:i+1].to(args.device),
                "dec_in": batch["dec_in"][i:i+1].to(args.device),
                "lemma": batch["lemma"][i],
                "inflected": batch["inflected"][i],
                "tag": batch["tag"][i],
                "category": batch["category"][i],
            })
            if len(picked) >= num_examples:
                break
        if len(picked) >= num_examples:
            break

    for ex_idx, ex in enumerate(picked):
        # Run a forward pass to collect cross-attention weights
        # cross_ws is a list (per decoder layer) of (B, num_heads, T_tgt, T_src)
        with torch.no_grad():
            _, cross_ws = model(ex["src"], ex["dec_in"])

        # Use the LAST decoder layer; usually carries the cleanest alignment.
        attn = cross_ws[-1][0].cpu().numpy()  # (h, T_tgt, T_src)
        h = attn.shape[0]

        src_labels = [vocab.itos[int(t)] for t in ex["src"][0].tolist()]
        tgt_labels = [vocab.itos[int(t)] for t in ex["dec_in"][0].tolist()]

        # Trim padding for clarity
        def trim(labels):
            cut = len(labels)
            for j, t in enumerate(labels):
                if t == vocab.PAD:
                    cut = j
                    break
            return cut
        src_cut = trim(src_labels)
        tgt_cut = trim(tgt_labels)

        cols = min(h, 4)
        rows = (h + cols - 1) // cols
        fig, axes = plt.subplots(rows, cols, figsize=(3.5 * cols, 3 * rows),
                                  squeeze=False)
        for head in range(h):
            ax = axes[head // cols][head % cols]
            im = ax.imshow(attn[head, :tgt_cut, :src_cut],
                           aspect="auto", cmap="Blues", vmin=0, vmax=1)
            ax.set_xticks(range(src_cut))
            ax.set_xticklabels(src_labels[:src_cut], fontsize=7)
            ax.set_yticks(range(tgt_cut))
            ax.set_yticklabels(tgt_labels[:tgt_cut], fontsize=7)
            ax.set_title(f"head {head}", fontsize=9)
        for k in range(h, rows * cols):
            axes[k // cols][k % cols].axis("off")
        fig.suptitle(
            f"Cross-attention (last decoder layer)  "
            f"{ex['lemma']!r} -> {ex['inflected']!r}  "
            f"({ex['tag']}, {ex['category']})",
            fontsize=10,
        )
        plt.tight_layout()
        fname = f"cross_attn_{ex_idx:02d}_{ex['tag']}_{ex['category']}.png"
        fig.savefig(OUT_DIR / fname, dpi=150, bbox_inches="tight")
        plt.close(fig)


def write_results_md(out_md, results, args):
    rows = []
    for h in HEAD_COUNTS:
        r = results[h]["eval_val"]
        rows.append(
            f"| h={h}    | {r['by_category'].get('pure_regular',0)*100:5.1f}% "
            f"| {r['by_category'].get('phonological',0)*100:5.1f}% "
            f"| {r['by_category'].get('irregular',0)*100:5.1f}% "
            f"| {r['overall']*100:5.1f}% |"
        )

    body = f"""# Exp 4: Multi-Head Ablation + Visualization

We hold `d_model=128` constant and vary `num_heads` in {{1, 4, 8}}.
Each head sees `d_k = 128/h` dimensions. The trade-off:
fewer heads have more capacity per head but only one attention
pattern; more heads have diverse patterns but each is lower-rank.

## Accuracy

| variant | pure_regular | phonological | irregular | overall |
|---------|--------------|--------------|-----------|---------|
{chr(10).join(rows)}

## Detail
"""
    for h in HEAD_COUNTS:
        body += f"\n### h={h}\n\n```\n{format_results_table(results[h]['eval_val'])}\n```\n"

    body += """

## Cross-attention visualization (h=4 model)

Files `cross_attn_<idx>_<tag>_<category>.png` show the four heads'
cross-attention maps on a single test example each. Rows are decoder
output positions; columns are encoder input positions (TAG, lemma
characters, EOS). For each example, look for:

  - One head with a near-diagonal pattern: this head COPIES lemma
    characters position-for-position. It is the workhorse that
    handles the pure_regular cases.
  - One head fixating on the TAG token (column 0) at every output
    step: a "control" head that re-reads which inflection paradigm
    we are in.
  - For phonological / irregular examples, expect at least one head
    to focus on the lemma's final character(s), because those are
    where the rule changes (`y -> ie`, `f -> v`, etc.) and where
    irregulars actually differ from the lemma.

The visualization is not a clean experiment with a single right
answer -- it is interpretive. Different seeds may produce different
specializations.

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
    for h in HEAD_COUNTS:
        results[h] = train_variant(
            h, (train_loader, val_loader), vocab, args, OUT_DIR / f"train_h{h}",
        )
        r = results[h]["eval_val"]
        print(f"  h={h}  overall={r['overall']*100:.1f}%")

    # Visualization on the h=4 model
    print("\nGenerating cross-attention visualizations (h=4)...")
    visualize_cross_attention(results[4]["model"], vocab, val_loader, args,
                               args.num_vis_examples)

    # Drop the model objects before writing markdown
    for h in HEAD_COUNTS:
        results[h].pop("model")
    write_results_md(OUT_DIR / "results.md", results, args)
    print(f"\nArtifacts saved to {OUT_DIR}")


if __name__ == "__main__":
    main()
