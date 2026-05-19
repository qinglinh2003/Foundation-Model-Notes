"""
Project 1: Evaluation
----------------------
Validation metrics, bits-per-byte, loss curve plotting, and sample generation.
"""

import json
import math
from pathlib import Path

import torch
import torch.nn as nn
import matplotlib.pyplot as plt


def compute_bits_per_byte(avg_ce_loss: float, bytes_per_token: float) -> float:
    """
    Convert average cross-entropy loss (nats) to bits-per-byte.

    Formula:
        bits_per_byte = (avg_ce_loss / ln(2)) * (1 / bytes_per_token)

    This is a fairer metric when comparing across different tokenizers
    (see Lab 5, Experiment 0).

    Args:
        avg_ce_loss:    Average cross-entropy loss in nats (natural log base).
        bytes_per_token: Average number of UTF-8 bytes per token in the corpus.

    Returns:
        Bits per byte (float).
    """
    return (avg_ce_loss / math.log(2)) / bytes_per_token


def plot_loss_curves(train_log: list, save_path: str = "figures/loss_curves.png") -> None:
    """
    Plot training and validation loss curves with LR overlay.
    """
    steps = [r["step"] for r in train_log]
    train_losses = [r["train_loss"] for r in train_log]
    val_losses = [r["val_loss"] for r in train_log]
    lrs = [r["lr"] for r in train_log]

    fig, ax1 = plt.subplots(figsize=(10, 5))

    ax1.plot(steps, train_losses, "b-", alpha=0.7, label="Train loss")
    ax1.plot(steps, val_losses, "r-", alpha=0.7, label="Val loss")
    ax1.set_xlabel("Step")
    ax1.set_ylabel("Cross-entropy loss")
    ax1.legend(loc="upper left")
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    ax2.plot(steps, lrs, "g--", alpha=0.5, label="Learning rate")
    ax2.set_ylabel("Learning rate")
    ax2.legend(loc="upper right")

    plt.title("MiniGPT Training")
    plt.tight_layout()
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"Loss curves saved to {save_path}")


def plot_ablation(
    results: dict[str, list],
    metric: str = "val_loss",
    save_path: str = "figures/ablation.png",
) -> None:
    """
    Plot ablation comparison.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    for name, log in results.items():
        steps = [r["step"] for r in log]
        values = [r[metric] for r in log]
        ax.plot(steps, values, label=name, alpha=0.8)

    ax.set_xlabel("Step")
    ax.set_ylabel(metric.replace("_", " ").title())
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.title(f"Ablation: {metric}")
    plt.tight_layout()
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"Ablation plot saved to {save_path}")


# ---------------------------------------------------------------------------
# Quick test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Test bits-per-byte
    bpb = compute_bits_per_byte(avg_ce_loss=2.0, bytes_per_token=4.0)
    expected = (2.0 / math.log(2)) / 4.0
    print(f"bits_per_byte: {bpb:.4f} (expected {expected:.4f})")
    print("Evaluate module loaded.")
