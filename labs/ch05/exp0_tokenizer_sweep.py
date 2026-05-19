"""
Lab 5 -- Experiment 0: Tokenizer & Vocab Size Sweep
=====================================================
Insight: raw per-token loss is NOT comparable across tokenizers.
A large-vocab tokenizer may show lower per-token loss yet produce
worse bits-per-byte -- because rare tokens have under-trained
embeddings on a small corpus.

We train identical MiniGPTs with different vocab sizes and compare:
  - per-token cross-entropy (the misleading metric)
  - bits-per-byte (the fair metric)
  - bytes-per-token (tokenizer efficiency)
  - generated sample quality (qualitative)
"""

import json
import math
import torch
import matplotlib.pyplot as plt
from pathlib import Path

from model import GPT, GPTConfig
from data import build_datasets
from train import train, TrainConfig


VOCAB_SIZES = [65, 256, 1000, 4000]  # char-level, small BPE, mid BPE, large BPE
SEQ_LEN = 256
BATCH_SIZE = 64
MAX_STEPS = 1500
SEED = 42

OUT_DIR = Path(__file__).parent / "answers"
FIG_DIR = OUT_DIR / "figures"
LOG_DIR = OUT_DIR / "logs"


def main():
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    results = {}

    for vs in VOCAB_SIZES:
        label = f"char" if vs <= 65 else f"bpe_v{vs}"
        print(f"\n{'='*60}")
        print(f"Training with vocab_size={vs} ({label})")
        print(f"{'='*60}")

        # Build data
        train_dl, val_dl, actual_vocab, encode_fn, decode_fn, bpt = build_datasets(
            vocab_size=vs, seq_len=SEQ_LEN, batch_size=BATCH_SIZE
        )
        print(f"  actual vocab = {actual_vocab}, bytes/token = {bpt:.2f}")
        print(f"  train batches = {len(train_dl)}, val batches = {len(val_dl)}")

        # Build model
        config = GPTConfig(
            vocab_size=actual_vocab,
            seq_len=SEQ_LEN,
            d_model=128,
            n_heads=4,
            n_layers=4,
            dropout=0.1,
        )
        model = GPT(config)
        n_params = sum(p.numel() for p in model.parameters())
        print(f"  params = {n_params:,}")

        # Prompt for generation
        prompt_text = "First Citizen:\n"
        prompt_ids = encode_fn(prompt_text).unsqueeze(0)

        # Train
        cfg = TrainConfig(
            lr=3e-4, max_steps=MAX_STEPS, seed=SEED,
            eval_interval=100, log_interval=25, device=device,
            warmup_steps=100, schedule="cosine",
        )
        log = train(model, train_dl, val_dl, cfg, decode_fn, prompt_ids)

        # Compute bits-per-byte from final val loss
        final_ce = log["final_val_loss"]  # nats per token
        bits_per_token = final_ce / math.log(2)
        bits_per_byte = bits_per_token / bpt

        results[label] = {
            "vocab_size": actual_vocab,
            "bytes_per_token": round(bpt, 2),
            "final_val_ce": round(final_ce, 4),
            "bits_per_token": round(bits_per_token, 4),
            "bits_per_byte": round(bits_per_byte, 4),
            "n_params": n_params,
            "wall_time": round(log["wall_time"], 1),
            "sample": log["samples"][-1] if log["samples"] else "",
            "train_losses": log["train_losses"],
            "steps": log["steps"],
        }

        print(f"  final val CE = {final_ce:.4f}")
        print(f"  bits/token = {bits_per_token:.4f}, bits/byte = {bits_per_byte:.4f}")
        if log["samples"]:
            print(f"  sample: {log['samples'][-1][:200]}...")

    # ---------------------------------------------------------------
    # Plot 1: per-token loss vs bits-per-byte (the misleading metric)
    # ---------------------------------------------------------------
    labels = list(results.keys())
    token_losses = [results[l]["final_val_ce"] for l in labels]
    bpb = [results[l]["bits_per_byte"] for l in labels]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    colors = ["#2D8CFF", "#1A6FD1", "#0D4A8F", "#FF6B35"]
    ax1.bar(labels, token_losses, color=colors[:len(labels)], edgecolor="black")
    ax1.set_ylabel("Per-Token Cross-Entropy (nats)", fontsize=12)
    ax1.set_title("Misleading Metric: Raw Token Loss", fontsize=13, fontweight="bold")
    ax1.tick_params(axis="x", rotation=15)

    ax2.bar(labels, bpb, color=colors[:len(labels)], edgecolor="black")
    ax2.set_ylabel("Bits per Byte", fontsize=12)
    ax2.set_title("Fair Metric: Bits per Byte", fontsize=13, fontweight="bold")
    ax2.tick_params(axis="x", rotation=15)

    fig.suptitle("Exp 0: Tokenizer Metrics Trap", fontsize=14, fontweight="bold", y=1.02)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "exp0_tokenizer_sweep.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"\nSaved: {FIG_DIR / 'exp0_tokenizer_sweep.png'}")

    # ---------------------------------------------------------------
    # Plot 2: training curves
    # ---------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, label in enumerate(labels):
        r = results[label]
        ax.plot(r["steps"], r["train_losses"], label=label,
                color=colors[i], alpha=0.8, linewidth=1.5)
    ax.set_xlabel("Step", fontsize=12)
    ax.set_ylabel("Train Loss (per-token CE)", fontsize=12)
    ax.set_title("Training Curves Across Vocab Sizes", fontsize=13, fontweight="bold")
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "exp0_training_curves.png", dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved: {FIG_DIR / 'exp0_training_curves.png'}")

    # ---------------------------------------------------------------
    # Plot 3: bytes-per-token vs vocab size
    # ---------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(8, 5))
    vs_list = [results[l]["vocab_size"] for l in labels]
    bpt_list = [results[l]["bytes_per_token"] for l in labels]
    ax.plot(vs_list, bpt_list, "o-", color="#2D8CFF", linewidth=2, markersize=8)
    ax.set_xlabel("Vocabulary Size", fontsize=12)
    ax.set_ylabel("Bytes per Token", fontsize=12)
    ax.set_title("Tokenizer Compression Efficiency", fontsize=13, fontweight="bold")
    ax.set_xscale("log")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "exp0_compression.png", dpi=150, bbox_inches="tight")
    plt.close()

    # Save results
    # Remove non-serializable fields
    save_results = {}
    for k, v in results.items():
        save_results[k] = {kk: vv for kk, vv in v.items()
                           if kk not in ("train_losses", "steps")}
    with open(LOG_DIR / "exp0_results.json", "w") as f:
        json.dump(save_results, f, indent=2)
    print(f"\nResults saved to {LOG_DIR / 'exp0_results.json'}")

    # Print summary table
    print("\n" + "="*70)
    print("SUMMARY: Tokenizer Sweep")
    print("="*70)
    print(f"{'Config':<12} {'Vocab':>6} {'B/Tok':>6} {'CE':>8} {'BPT':>8} {'BPB':>8} {'Params':>10}")
    print("-"*70)
    for label in labels:
        r = results[label]
        print(f"{label:<12} {r['vocab_size']:>6} {r['bytes_per_token']:>6.2f} "
              f"{r['final_val_ce']:>8.4f} {r['bits_per_token']:>8.4f} "
              f"{r['bits_per_byte']:>8.4f} {r['n_params']:>10,}")


if __name__ == "__main__":
    main()
