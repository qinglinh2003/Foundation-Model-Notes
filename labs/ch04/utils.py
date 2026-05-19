"""
Lab 4 — Utility functions
=========================
Training, evaluation, and visualization helpers for representation diagnostics.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import csv
import os
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ── Linear Probe ────────────────────────────────────────────────────────────

class LinearProbe(nn.Module):
    """Single linear layer for probing frozen representations."""

    def __init__(self, hidden_size, num_classes):
        super().__init__()
        self.linear = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        return self.linear(x)


# ── Training ────────────────────────────────────────────────────────────────

def train_probe(probe, train_dl, extract_fn, device, epochs=5, lr=1e-3,
                log_path=None):
    """
    Train a linear probe on frozen representations.

    Args:
        probe: LinearProbe module
        train_dl: DataLoader yielding dicts with input_ids, attention_mask, label
        extract_fn: callable(input_ids, attention_mask) -> [B, hidden] representations
        device: torch device
        epochs: number of training epochs
        lr: learning rate
        log_path: optional CSV path for logging

    Returns:
        list of (step, loss) tuples
    """
    opt = torch.optim.Adam(probe.parameters(), lr=lr)
    probe.train()
    history = []
    step = 0

    for epoch in range(epochs):
        for batch in train_dl:
            ids = batch["input_ids"].to(device)
            mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)

            with torch.no_grad():
                reps = extract_fn(ids, mask)

            logits = probe(reps)
            loss = F.cross_entropy(logits, labels)

            opt.zero_grad()
            loss.backward()
            opt.step()

            step += 1
            history.append((step, loss.item()))

    if log_path:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["step", "loss"])
            w.writerows(history)

    return history


def train_finetune(model, head, train_dl, device, epochs=3, lr=2e-5,
                   log_path=None):
    """
    Full fine-tuning: update both model and classification head.

    Args:
        model: pretrained transformer model
        head: LinearProbe classification head
        train_dl: DataLoader
        device: torch device
        epochs: number of epochs
        lr: learning rate
        log_path: optional CSV path

    Returns:
        list of (step, loss) tuples
    """
    model.train()
    head.train()
    params = list(model.parameters()) + list(head.parameters())
    opt = torch.optim.AdamW(params, lr=lr, weight_decay=0.01)
    history = []
    step = 0

    for epoch in range(epochs):
        for batch in train_dl:
            ids = batch["input_ids"].to(device)
            mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)

            outputs = model(ids, attention_mask=mask, output_hidden_states=True)
            # Use [CLS] for BERT-like, last token for GPT-like
            hidden = outputs.hidden_states[-1]
            # We'll use the first token for BERT, last non-pad for GPT
            # This is handled by the caller setting up the model appropriately
            # Here we just use first token (works for BERT [CLS])
            reps = hidden[:, 0, :]

            logits = head(reps)
            loss = F.cross_entropy(logits, labels)

            opt.zero_grad()
            loss.backward()
            opt.step()

            step += 1
            history.append((step, loss.item()))

    if log_path:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["step", "loss"])
            w.writerows(history)

    return history


# ── Evaluation ──────────────────────────────────────────────────────────────

@torch.no_grad()
def evaluate_probe(probe, val_dl, extract_fn, device):
    """Evaluate probe accuracy on validation set."""
    probe.eval()
    correct = total = 0
    total_loss = 0.0
    n_batches = 0

    for batch in val_dl:
        ids = batch["input_ids"].to(device)
        mask = batch["attention_mask"].to(device)
        labels = batch["label"].to(device)

        reps = extract_fn(ids, mask)
        logits = probe(reps)
        loss = F.cross_entropy(logits, labels)

        preds = logits.argmax(dim=-1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)
        total_loss += loss.item()
        n_batches += 1

    acc = correct / total
    avg_loss = total_loss / max(n_batches, 1)
    return acc, avg_loss


@torch.no_grad()
def evaluate_finetune(model, head, val_dl, device, use_last_token=False):
    """Evaluate fine-tuned model + head on validation set."""
    model.eval()
    head.eval()
    correct = total = 0

    for batch in val_dl:
        ids = batch["input_ids"].to(device)
        mask = batch["attention_mask"].to(device)
        labels = batch["label"].to(device)

        outputs = model(ids, attention_mask=mask, output_hidden_states=True)
        hidden = outputs.hidden_states[-1]

        if use_last_token:
            # Find last non-pad token position
            seq_lens = mask.sum(dim=1) - 1
            reps = hidden[torch.arange(hidden.size(0)), seq_lens]
        else:
            reps = hidden[:, 0, :]

        logits = head(reps)
        preds = logits.argmax(dim=-1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

    return correct / total


# ── Representation extraction helpers ───────────────────────────────────────

def make_bert_extractor(model, device):
    """Return a function that extracts [CLS] representations from BERT."""
    model.eval()

    def extract(input_ids, attention_mask):
        outputs = model(input_ids, attention_mask=attention_mask,
                        output_hidden_states=True)
        hidden = outputs.hidden_states[-1]  # last layer
        return hidden[:, 0, :]  # [CLS] token

    return extract


def make_gpt_extractor(model, device):
    """Return a function that extracts last-token representations from GPT."""
    model.eval()

    def extract(input_ids, attention_mask):
        outputs = model(input_ids, attention_mask=attention_mask,
                        output_hidden_states=True)
        hidden = outputs.hidden_states[-1]
        # Use last non-pad token
        seq_lens = attention_mask.sum(dim=1) - 1
        reps = hidden[torch.arange(hidden.size(0)), seq_lens]
        return reps

    return extract


def make_static_extractor(model, device):
    """
    Return a function that extracts mean-of-token-embeddings (no context).
    Works for both BERT and GPT models.
    """
    model.eval()

    def extract(input_ids, attention_mask):
        # Get the raw token embeddings (before any transformer layers)
        if hasattr(model, "embeddings"):
            # BERT-style
            embs = model.embeddings.word_embeddings(input_ids)
        elif hasattr(model, "transformer"):
            # GPT2-style
            embs = model.transformer.wte(input_ids)
        else:
            raise ValueError("Cannot find embedding layer")

        # Mean pool over non-pad tokens
        mask_expanded = attention_mask.unsqueeze(-1).float()
        summed = (embs * mask_expanded).sum(dim=1)
        counts = mask_expanded.sum(dim=1).clamp(min=1)
        return summed / counts

    return extract


# ── Plotting ────────────────────────────────────────────────────────────────

def plot_bar_chart(labels, values, title, ylabel, save_path, colors=None):
    """Simple bar chart for comparing accuracies."""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))

    if colors is None:
        colors = ["#999999", "#4a90d9", "#e8833a"]
        if len(labels) > len(colors):
            colors = plt.cm.tab10(np.linspace(0, 1, len(labels)))

    bars = ax.bar(labels, values, color=colors[:len(labels)], width=0.6)

    # Add value labels on bars
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                f"{val:.1f}%", ha="center", va="bottom", fontweight="bold",
                fontsize=12)

    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_ylim(0, 105)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Plot saved: {save_path}")


def plot_layer_probing(layer_accs, title, save_path):
    """Line plot for layer-wise probe accuracy."""
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5))

    layers = list(range(len(layer_accs)))
    ax.plot(layers, [a * 100 for a in layer_accs], "o-", color="#e8833a",
            linewidth=2, markersize=8)

    ax.set_xlabel("Layer", fontsize=12)
    ax.set_ylabel("Probe Accuracy (%)", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.set_xticks(layers)
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"  Plot saved: {save_path}")
