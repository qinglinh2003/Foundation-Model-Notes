"""
Lab 1 — Utilities
==================
Plotting, logging, and training helpers.
All provided — students do NOT need to modify this file.
"""

import csv, os, math
from pathlib import Path
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np


# ===================================================================
# Logging
# ===================================================================

class MetricLogger:
    """Simple CSV logger for training metrics."""

    def __init__(self, path: str, fieldnames: list[str]):
        self.path = path
        self.fieldnames = fieldnames
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self._file = open(path, "w", newline="")
        self._writer = csv.DictWriter(self._file, fieldnames=fieldnames)
        self._writer.writeheader()

    def log(self, **kwargs):
        self._writer.writerow(kwargs)
        self._file.flush()

    def close(self):
        self._file.close()


def load_metrics(path: str) -> dict[str, list[float]]:
    """Load a CSV log into a dict of lists."""
    data = {}
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for key, val in row.items():
                data.setdefault(key, []).append(float(val))
    return data


# ===================================================================
# Gradient utilities
# ===================================================================

def compute_gradient_norm(model: nn.Module) -> float:
    """Compute the total L2 norm of all parameter gradients."""
    total = 0.0
    for p in model.parameters():
        if p.grad is not None:
            total += p.grad.data.norm(2).item() ** 2
    return math.sqrt(total)


# ===================================================================
# Plotting helpers
# ===================================================================

COLORS = {
    "rnn": "#E74C3C",     # red
    "lstm": "#2980B9",    # blue
    "gru": "#27AE60",     # green
}


def plot_gradient_norms(logs: dict[str, str], save_path: str = None,
                        title: str = "Gradient Norm vs. Training Step"):
    """
    Plot gradient norms for multiple models.

    Args:
        logs : {"rnn": "path/to/rnn_log.csv", "lstm": ..., "gru": ...}
        save_path : if provided, save figure to this path
    """
    fig, ax = plt.subplots(figsize=(10, 4))
    for name, path in logs.items():
        data = load_metrics(path)
        steps = data.get("step", list(range(len(data["grad_norm"]))))
        ax.plot(steps, data["grad_norm"], label=name.upper(),
                color=COLORS.get(name, None), alpha=0.8, linewidth=0.8)
    ax.set_xlabel("Training Step")
    ax.set_ylabel("Gradient Norm (before clipping)")
    ax.set_title(title)
    ax.legend()
    ax.set_yscale("log")
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Saved: {save_path}")
    plt.show()


def plot_distance_probe(results: dict[str, dict[int, float]],
                        save_path: str = None):
    """
    Plot accuracy vs. dependency distance for each model type.

    Args:
        results : {"rnn": {8: 0.95, 32: 0.7, ...}, "lstm": {...}, "gru": {...}}
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    for name, dist_acc in results.items():
        distances = sorted(dist_acc.keys())
        accuracies = [dist_acc[d] for d in distances]
        ax.plot(distances, accuracies, marker="o", label=name.upper(),
                color=COLORS.get(name, None), linewidth=2)
    ax.set_xlabel("Dependency Distance (number of noise tokens)")
    ax.set_ylabel("Test Accuracy")
    ax.set_title("Long-Range Dependency Probe")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.set_xscale("log", base=2)
    ax.set_xticks([8, 32, 128, 256])
    ax.get_xaxis().set_major_formatter(plt.ScalarFormatter())
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Saved: {save_path}")
    plt.show()


def plot_seq2seq_accuracy(results: dict[str, dict[int, float]],
                          save_path: str = None):
    """
    Plot exact-match accuracy vs. input length for Seq2Seq models.

    Args:
        results : {"no_attention": {10: 0.99, 30: 0.6, ...},
                    "with_attention": {10: 1.0, 30: 0.98, ...}}
    """
    fig, ax = plt.subplots(figsize=(8, 5))
    styles = {
        "no_attention": {"color": "#E74C3C", "linestyle": "--"},
        "with_attention": {"color": "#2980B9", "linestyle": "-"},
    }
    for name, len_acc in results.items():
        lengths = sorted(len_acc.keys())
        accs = [len_acc[l] for l in lengths]
        style = styles.get(name, {})
        ax.plot(lengths, accs, marker="s", label=name.replace("_", " ").title(),
                linewidth=2, **style)
    ax.set_xlabel("Input Sequence Length")
    ax.set_ylabel("Exact Sequence Match Accuracy")
    ax.set_title("Seq2Seq Bottleneck: Effect of Attention")
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Saved: {save_path}")
    plt.show()


def plot_attention_heatmap(weights: np.ndarray, src_tokens: list[str],
                           tgt_tokens: list[str], save_path: str = None):
    """
    Plot an attention weight heatmap.

    Args:
        weights    : (tgt_len, src_len) numpy array
        src_tokens : list of source token labels
        tgt_tokens : list of target token labels
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(weights, cmap="Blues", aspect="auto")
    ax.set_xticks(range(len(src_tokens)))
    ax.set_xticklabels(src_tokens, fontsize=7, rotation=45)
    ax.set_yticks(range(len(tgt_tokens)))
    ax.set_yticklabels(tgt_tokens, fontsize=7)
    ax.set_xlabel("Source (Encoder)")
    ax.set_ylabel("Target (Decoder)")
    ax.set_title("Attention Weights")
    fig.colorbar(im, ax=ax, shrink=0.8)
    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Saved: {save_path}")
    plt.show()


# ===================================================================
# Training utilities
# ===================================================================

def train_one_epoch_charlm(model, dataloader, optimizer, device,
                           clip_norm=5.0, logger=None, global_step=0):
    """
    Train CharLM for one epoch. Returns (avg_loss, global_step).

    Logs per-step: step, loss, grad_norm.
    """
    model.train()
    total_loss = 0.0
    hidden = None
    criterion = nn.CrossEntropyLoss()

    for batch_idx, (x, y) in enumerate(dataloader):
        x, y = x.to(device), y.to(device)
        logits, hidden = model(x, hidden)

        loss = criterion(logits.reshape(-1, logits.size(-1)), y.reshape(-1))

        optimizer.zero_grad()
        loss.backward()

        grad_norm = compute_gradient_norm(model)

        if clip_norm is not None and clip_norm > 0:
            nn.utils.clip_grad_norm_(model.parameters(), clip_norm)

        optimizer.step()
        total_loss += loss.item()
        global_step += 1

        if logger:
            logger.log(step=global_step, loss=loss.item(), grad_norm=grad_norm)

    avg_loss = total_loss / max(len(dataloader), 1)
    return avg_loss, global_step


@torch.no_grad()
def evaluate_charlm(model, dataloader, device):
    """Evaluate CharLM. Returns (avg_loss, perplexity)."""
    model.eval()
    total_loss = 0.0
    total_tokens = 0
    hidden = None
    criterion = nn.CrossEntropyLoss(reduction="sum")

    for x, y in dataloader:
        x, y = x.to(device), y.to(device)
        logits, hidden = model(x, hidden)
        loss = criterion(logits.reshape(-1, logits.size(-1)), y.reshape(-1))
        total_loss += loss.item()
        total_tokens += y.numel()

    avg_loss = total_loss / max(total_tokens, 1)
    ppl = math.exp(min(avg_loss, 20))  # clamp to avoid overflow
    return avg_loss, ppl


@torch.no_grad()
def generate_charlm(model, dataset, seed_text: str, length: int = 200,
                    temperature: float = 1.0, device: str = "cpu"):
    """Generate text from a trained CharLM."""
    model.eval()
    indices = [dataset.char2idx.get(c, 0) for c in seed_text]
    x = torch.tensor([indices], dtype=torch.long, device=device)

    hidden = None
    # Process seed
    logits, hidden = model(x, hidden)

    # Generate
    generated = list(seed_text)
    current = logits[:, -1, :]  # last position logits

    for _ in range(length):
        probs = torch.softmax(current / temperature, dim=-1)
        next_idx = torch.multinomial(probs, 1)
        generated.append(dataset.idx2char[next_idx.item()])
        x = next_idx  # already (1, 1) from multinomial
        logits, hidden = model(x, hidden)
        current = logits[:, -1, :]

    return "".join(generated)
