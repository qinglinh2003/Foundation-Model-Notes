"""
Lab 5 -- Experiment 2: Checkpoint Resume Ablation
==================================================
Insight: a checkpoint is not just model weights.  Resuming with
incomplete state produces subtle trajectory shifts that are easy
to mistake for normal training noise.

Four runs:
  1. uninterrupted:    full training, no interruption (reference)
  2. full_resume:      train to 50%, save full checkpoint, resume
  3. model_only:       resume from model weights only (no optimizer)
  4. no_scheduler:     resume model + optimizer but reset scheduler/step
"""

import json
import shutil
import torch
import matplotlib.pyplot as plt
from pathlib import Path

from model import GPT, GPTConfig
from data import build_datasets
from train import train, TrainConfig


SEQ_LEN = 256
BATCH_SIZE = 64
MAX_STEPS = 2000
MIDPOINT = MAX_STEPS // 2  # Resume at 50%
SEED = 42

OUT_DIR = Path(__file__).parent / "answers"
FIG_DIR = OUT_DIR / "figures"
LOG_DIR = OUT_DIR / "logs"
CKPT_DIR = Path(__file__).parent / "checkpoints"


def _make_model(vocab_size):
    torch.manual_seed(SEED)
    config = GPTConfig(vocab_size=vocab_size, seq_len=SEQ_LEN,
                       d_model=128, n_heads=4, n_layers=4, dropout=0.1)
    return GPT(config)


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    train_dl, val_dl, vocab_size, encode_fn, decode_fn, _ = build_datasets(
        vocab_size=65, seq_len=SEQ_LEN, batch_size=BATCH_SIZE
    )

    prompt_text = "First Citizen:\n"
    prompt_ids = encode_fn(prompt_text).unsqueeze(0)

    results = {}

    # ------------------------------------------------------------------
    # Run 1: Uninterrupted reference
    # ------------------------------------------------------------------
    print(f"\n{'='*60}")
    print("Run 1: Uninterrupted (reference)")
    print(f"{'='*60}")
    model = _make_model(vocab_size)
    cfg = TrainConfig(
        lr=3e-4, schedule="cosine", warmup_steps=100,
        max_steps=MAX_STEPS, seed=SEED, device=device,
        eval_interval=50, log_interval=25,
    )
    log = train(model, train_dl, val_dl, cfg, decode_fn, prompt_ids)
    results["uninterrupted"] = log
    print(f"  final val = {log['final_val_loss']:.4f}")

    # ------------------------------------------------------------------
    # Phase 1: Train to midpoint with checkpointing
    # ------------------------------------------------------------------
    print(f"\n{'='*60}")
    print(f"Phase 1: Train to step {MIDPOINT} (for resume experiments)")
    print(f"{'='*60}")

    # Clean checkpoint dir
    if CKPT_DIR.exists():
        shutil.rmtree(CKPT_DIR)

    model_phase1 = _make_model(vocab_size)
    cfg_phase1 = TrainConfig(
        lr=3e-4, schedule="cosine", warmup_steps=100,
        max_steps=MIDPOINT, seed=SEED, device=device,
        eval_interval=50, log_interval=25,
        checkpoint_dir=str(CKPT_DIR),
        checkpoint_interval=MIDPOINT,  # Save at the end
    )
    log_phase1 = train(model_phase1, train_dl, val_dl, cfg_phase1)
    print(f"  phase1 final val = {log_phase1['final_val_loss']:.4f}")

    ckpt_path = str(CKPT_DIR / f"ckpt_step{MIDPOINT}.pt")

    # ------------------------------------------------------------------
    # Resume runs
    # ------------------------------------------------------------------
    resume_configs = {
        "full_resume": "full",
        "model_only": "model_only",
        "no_scheduler": "no_scheduler",
    }

    for name, mode in resume_configs.items():
        print(f"\n{'='*60}")
        print(f"Run: {name} (resume_mode={mode})")
        print(f"{'='*60}")

        model_resume = _make_model(vocab_size)
        cfg_resume = TrainConfig(
            lr=3e-4, schedule="cosine", warmup_steps=100,
            max_steps=MAX_STEPS, seed=SEED, device=device,
            eval_interval=50, log_interval=25,
            resume_from=ckpt_path,
            resume_mode=mode,
        )
        log_resume = train(model_resume, train_dl, val_dl, cfg_resume,
                           decode_fn, prompt_ids)

        # Stitch phase1 + resume logs
        combined_steps = log_phase1["steps"] + log_resume["steps"]
        combined_train = log_phase1["train_losses"] + log_resume["train_losses"]
        combined_val = log_phase1["val_losses"] + log_resume["val_losses"]

        results[name] = {
            "train_losses": combined_train,
            "steps": combined_steps,
            "val_losses": combined_val,
            "final_val_loss": log_resume["final_val_loss"],
            "wall_time": round(log_phase1["wall_time"] + log_resume["wall_time"], 1),
            "samples": log_resume.get("samples", []),
        }
        print(f"  final val = {log_resume['final_val_loss']:.4f}")

    # ------------------------------------------------------------------
    # Plot: All four loss curves
    # ------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    styles = {
        "uninterrupted": {"color": "#2D8CFF", "label": "Uninterrupted (reference)",
                          "ls": "-", "lw": 2.5},
        "full_resume":   {"color": "#00AA55", "label": "Full Checkpoint Resume",
                          "ls": "--", "lw": 2},
        "model_only":    {"color": "#FF4444", "label": "Model-Only Resume",
                          "ls": "-.", "lw": 2},
        "no_scheduler":  {"color": "#FFA500", "label": "Missing Scheduler",
                          "ls": ":", "lw": 2},
    }

    for name in ["uninterrupted", "full_resume", "model_only", "no_scheduler"]:
        r = results[name]
        s = styles[name]
        ax1.plot(r["steps"], r["train_losses"],
                 color=s["color"], label=s["label"], ls=s["ls"],
                 linewidth=s["lw"], alpha=0.85)

    ax1.axvline(x=MIDPOINT, color="gray", ls="--", alpha=0.5, label=f"Resume point (step {MIDPOINT})")
    ax1.set_xlabel("Step", fontsize=12)
    ax1.set_ylabel("Train Loss", fontsize=12)
    ax1.set_title("Training Loss", fontsize=13, fontweight="bold")
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Val loss
    for name in ["uninterrupted", "full_resume", "model_only", "no_scheduler"]:
        r = results[name]
        s = styles[name]
        val_steps = [v[0] for v in r["val_losses"]]
        val_vals = [v[1] for v in r["val_losses"]]
        ax2.plot(val_steps, val_vals,
                 color=s["color"], label=s["label"], ls=s["ls"],
                 linewidth=s["lw"], marker="o", markersize=3, alpha=0.85)

    ax2.axvline(x=MIDPOINT, color="gray", ls="--", alpha=0.5)
    ax2.set_xlabel("Step", fontsize=12)
    ax2.set_ylabel("Validation Loss", fontsize=12)
    ax2.set_title("Validation Loss", fontsize=13, fontweight="bold")
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    fig.suptitle("Exp 2: Checkpoint State Trap",
                 fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "exp2_checkpoint_resume.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\nSaved: {FIG_DIR / 'exp2_checkpoint_resume.png'}")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("\n" + "="*60)
    print("SUMMARY: Checkpoint Resume Ablation")
    print("="*60)
    for name in ["uninterrupted", "full_resume", "model_only", "no_scheduler"]:
        r = results[name]
        print(f"  {name:<16}: final_val={r['final_val_loss']:.4f}  "
              f"time={r['wall_time']:.0f}s")

    # Save
    save_results = {}
    for k, v in results.items():
        save_results[k] = {
            "final_val_loss": v["final_val_loss"],
            "wall_time": v["wall_time"],
        }
    with open(LOG_DIR / "exp2_results.json", "w") as f:
        json.dump(save_results, f, indent=2)


if __name__ == "__main__":
    main()
