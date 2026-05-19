"""
Lab 5 -- Experiment 1: Learning-Rate Schedule Ablation (Centerpiece)
=====================================================================
Insight: a falling loss curve does not mean the schedule is good.
No-warmup and too-high LR runs can look alive but end on worse
trajectories that never recover.

Three configurations, same model, same data, same total steps:
  1. too_high:       lr=3e-3, no warmup, constant
  2. no_warmup:      lr=3e-4, no warmup, constant
  3. warmup_cosine:  lr=3e-4, 100 warmup + cosine decay  (standard)
"""

import json
import torch
import matplotlib.pyplot as plt
from pathlib import Path

from model import GPT, GPTConfig
from data import build_datasets
from train import train, TrainConfig


SEQ_LEN = 256
BATCH_SIZE = 64
MAX_STEPS = 2000
SEED = 42

OUT_DIR = Path(__file__).parent / "answers"
FIG_DIR = OUT_DIR / "figures"
LOG_DIR = OUT_DIR / "logs"

CONFIGS = {
    "too_high": TrainConfig(
        lr=1e-1, schedule="none", warmup_steps=0,
        max_steps=MAX_STEPS, seed=SEED, grad_clip=0.0,  # no clip → can explode
        eval_interval=100, log_interval=25,
    ),
    "no_warmup": TrainConfig(
        lr=1e-3, schedule="constant", warmup_steps=0,
        max_steps=MAX_STEPS, seed=SEED, grad_clip=1.0,
        eval_interval=100, log_interval=25,
    ),
    "warmup_cosine": TrainConfig(
        lr=1e-3, schedule="cosine", warmup_steps=200,
        max_steps=MAX_STEPS, seed=SEED, grad_clip=1.0,
        eval_interval=100, log_interval=25,
    ),
}


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Use char-level (same as Lab 3) so tokenizer isn't a variable
    train_dl, val_dl, vocab_size, encode_fn, decode_fn, _ = build_datasets(
        vocab_size=65, seq_len=SEQ_LEN, batch_size=BATCH_SIZE
    )

    prompt_text = "First Citizen:\n"
    prompt_ids = encode_fn(prompt_text).unsqueeze(0)

    results = {}

    for name, cfg in CONFIGS.items():
        print(f"\n{'='*60}")
        print(f"Schedule: {name}")
        print(f"  lr={cfg.lr}, warmup={cfg.warmup_steps}, schedule={cfg.schedule}")
        print(f"{'='*60}")

        # Fresh model each time (same seed for init)
        torch.manual_seed(SEED)
        config = GPTConfig(vocab_size=vocab_size, seq_len=SEQ_LEN,
                           d_model=128, n_heads=4, n_layers=4, dropout=0.1)
        model = GPT(config)

        cfg.device = device
        log = train(model, train_dl, val_dl, cfg, decode_fn, prompt_ids)

        results[name] = {
            "train_losses": log["train_losses"],
            "val_losses": log["val_losses"],
            "steps": log["steps"],
            "lr_history": log["lr_history"],
            "final_val_loss": log["final_val_loss"],
            "wall_time": round(log["wall_time"], 1),
            "sample": log["samples"][-1] if log["samples"] else "",
        }

        print(f"  final val loss = {log['final_val_loss']:.4f}")
        if log["samples"]:
            print(f"  sample: {log['samples'][-1][:200]}...")

    # ---------------------------------------------------------------
    # Plot 1: Loss curves (the centerpiece figure)
    # ---------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    styles = {
        "too_high":      {"color": "#FF4444", "label": "Too High LR (3e-3, no warmup)", "ls": "-"},
        "no_warmup":     {"color": "#FFA500", "label": "No Warmup (3e-4, constant)", "ls": "--"},
        "warmup_cosine": {"color": "#2D8CFF", "label": "Warmup + Cosine (3e-4)", "ls": "-"},
    }

    for name, r in results.items():
        s = styles[name]
        ax1.plot(r["steps"], r["train_losses"],
                 color=s["color"], label=s["label"], ls=s["ls"],
                 linewidth=2, alpha=0.85)

    ax1.set_xlabel("Step", fontsize=12)
    ax1.set_ylabel("Train Loss", fontsize=12)
    ax1.set_title("Training Loss", fontsize=13, fontweight="bold")
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)

    # Val loss
    for name, r in results.items():
        s = styles[name]
        val_steps = [v[0] for v in r["val_losses"]]
        val_vals = [v[1] for v in r["val_losses"]]
        ax2.plot(val_steps, val_vals,
                 color=s["color"], label=s["label"], ls=s["ls"],
                 linewidth=2, marker="o", markersize=4, alpha=0.85)

    ax2.set_xlabel("Step", fontsize=12)
    ax2.set_ylabel("Validation Loss", fontsize=12)
    ax2.set_title("Validation Loss", fontsize=13, fontweight="bold")
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)

    fig.suptitle("Exp 1: Schedule Stability Trap (Centerpiece)",
                 fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "exp1_lr_schedule.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\nSaved: {FIG_DIR / 'exp1_lr_schedule.png'}")

    # ---------------------------------------------------------------
    # Plot 2: LR schedule curves
    # ---------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 4))
    for name, r in results.items():
        s = styles[name]
        ax.plot(r["steps"], r["lr_history"],
                color=s["color"], label=s["label"], ls=s["ls"], linewidth=2)
    ax.set_xlabel("Step", fontsize=12)
    ax.set_ylabel("Learning Rate", fontsize=12)
    ax.set_title("LR Schedule Comparison", fontsize=13, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "exp1_lr_curves.png", dpi=150, bbox_inches="tight")
    plt.close()

    # ---------------------------------------------------------------
    # Summary
    # ---------------------------------------------------------------
    print("\n" + "="*60)
    print("SUMMARY: LR Schedule Ablation")
    print("="*60)
    for name, r in results.items():
        print(f"  {name:<16}: final_val={r['final_val_loss']:.4f}  "
              f"time={r['wall_time']:.0f}s")

    # Save
    save_results = {}
    for k, v in results.items():
        save_results[k] = {
            "final_val_loss": v["final_val_loss"],
            "wall_time": v["wall_time"],
        }
    with open(LOG_DIR / "exp1_results.json", "w") as f:
        json.dump(save_results, f, indent=2)


if __name__ == "__main__":
    main()
