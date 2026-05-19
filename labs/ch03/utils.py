"""
Lab 3 — Utilities
==================
Training loop, evaluation, generation profiling, and plotting helpers.
All provided — students do NOT need to modify this file.
"""

import csv
import os
import math
import time
from pathlib import Path
from typing import Optional

import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.pyplot as plt
import numpy as np


# ===================================================================
# Logging
# ===================================================================

class MetricLogger:
    """Simple CSV logger for training metrics."""

    def __init__(self, path: str, fieldnames: list):
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


def load_metrics(path: str) -> dict:
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
# Training loop
# ===================================================================

def train_step(model, batch, optimizer, loss_fn, max_grad_norm: float = 1.0):
    """
    Single training step. Returns (loss, grad_norm).

    Args:
        model: GPT model
        batch: (input_ids,) or (input_ids, targets) — we use input_ids for both
        optimizer: optimizer instance
        loss_fn: callable(logits, input_ids) -> scalar loss
        max_grad_norm: gradient clipping threshold
    """
    model.train()
    input_ids = batch[0].to(next(model.parameters()).device)

    optimizer.zero_grad()
    logits, _ = model(input_ids)
    loss = loss_fn(logits, input_ids)
    loss.backward()

    grad_norm = compute_gradient_norm(model)
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
    optimizer.step()

    return loss.item(), grad_norm


def train_loop(model, train_dl, optimizer, loss_fn, n_steps: int,
               log_path: Optional[str] = None, max_grad_norm: float = 1.0):
    """
    Train for n_steps. Returns list of (step, loss, grad_norm).

    Cycles through the dataloader if n_steps > len(dataloader).
    """
    device = next(model.parameters()).device
    logger = None
    if log_path:
        logger = MetricLogger(log_path, ["step", "loss", "grad_norm"])

    results = []
    step = 0
    while step < n_steps:
        for batch in train_dl:
            if step >= n_steps:
                break
            loss, grad_norm = train_step(model, batch, optimizer, loss_fn, max_grad_norm)
            results.append((step, loss, grad_norm))
            if logger:
                logger.log(step=step, loss=loss, grad_norm=grad_norm)
            step += 1

    if logger:
        logger.close()
    return results


# ===================================================================
# Evaluation
# ===================================================================

@torch.no_grad()
def evaluate(model, val_dl, loss_fn) -> float:
    """Compute average validation loss."""
    model.eval()
    device = next(model.parameters()).device
    total_loss = 0.0
    n_batches = 0
    for batch in val_dl:
        input_ids = batch[0].to(device)
        logits, _ = model(input_ids)
        loss = loss_fn(logits, input_ids)
        total_loss += loss.item()
        n_batches += 1
    return total_loss / max(n_batches, 1)


# ===================================================================
# Generation
# ===================================================================

@torch.no_grad()
def generate_text(model, chars, char2idx, prompt: str = "ROMEO:",
                  max_new_tokens: int = 200, temperature: float = 1.0,
                  use_cache: bool = True) -> str:
    """Generate text from a prompt string."""
    model.eval()
    device = next(model.parameters()).device

    # Encode prompt
    prompt_ids = torch.tensor(
        [[char2idx[c] for c in prompt]], dtype=torch.long, device=device
    )

    # Generate
    output_ids = model.generate(
        prompt_ids, max_new_tokens=max_new_tokens,
        temperature=temperature, use_cache=use_cache
    )

    # Decode
    idx2char = {i: c for c, i in char2idx.items()}
    text = "".join(idx2char[i.item()] for i in output_ids[0])
    return text


# ===================================================================
# Profiling: generation latency per token
# ===================================================================

@torch.no_grad()
def profile_generation(model, prompt_ids: torch.Tensor, n_tokens: int = 512,
                       use_cache: bool = True, warmup: int = 5) -> list:
    """
    Generate n_tokens and record wall-clock time for each token.

    Returns:
        List of (token_position, ms_per_token) tuples.
    """
    model.eval()
    device = next(model.parameters()).device
    prompt_ids = prompt_ids.to(device)

    # Warmup
    for _ in range(warmup):
        _ = model(prompt_ids[:, :10])

    if torch.cuda.is_available():
        torch.cuda.synchronize()

    timings = []
    generated = prompt_ids.clone()
    kv_caches = None

    if use_cache:
        # Prefill: process full prompt at once
        start = time.perf_counter()
        logits, kv_caches = model(generated)
        if torch.cuda.is_available():
            torch.cuda.synchronize()
        prefill_time = (time.perf_counter() - start) * 1000
        timings.append((generated.size(1), prefill_time))

        # Sample first token
        next_logits = logits[:, -1, :]
        next_token = torch.multinomial(F.softmax(next_logits, dim=-1), 1)
        generated = torch.cat([generated, next_token], dim=1)

        # Decode: one token at a time
        for i in range(n_tokens - 1):
            start = time.perf_counter()
            logits, kv_caches = model(next_token, kv_caches=kv_caches)
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            elapsed = (time.perf_counter() - start) * 1000
            timings.append((generated.size(1), elapsed))

            next_logits = logits[:, -1, :]
            next_token = torch.multinomial(F.softmax(next_logits, dim=-1), 1)
            generated = torch.cat([generated, next_token], dim=1)
    else:
        # No cache: recompute everything at each step
        for i in range(n_tokens):
            start = time.perf_counter()
            logits, _ = model(generated)
            if torch.cuda.is_available():
                torch.cuda.synchronize()
            elapsed = (time.perf_counter() - start) * 1000
            timings.append((generated.size(1), elapsed))

            next_logits = logits[:, -1, :]
            next_token = torch.multinomial(F.softmax(next_logits, dim=-1), 1)
            generated = torch.cat([generated, next_token], dim=1)

    return timings


# ===================================================================
# Plotting
# ===================================================================

def plot_loss_curves(results_dict: dict, title: str = "Training Loss",
                    save_path: Optional[str] = None):
    """
    Plot overlaid loss curves.

    Args:
        results_dict: {"label": [(step, loss, grad_norm), ...], ...}
    """
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    for label, results in results_dict.items():
        steps = [r[0] for r in results]
        losses = [r[1] for r in results]
        ax.plot(steps, losses, label=label, alpha=0.8)
    ax.set_xlabel("Step")
    ax.set_ylabel("Loss")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
    else:
        plt.show()


def plot_grad_norms(results_dict: dict, title: str = "Gradient Norm",
                    save_path: Optional[str] = None, clip_val: float = 50.0):
    """
    Plot overlaid gradient norm curves.
    Clips extreme values for readability.
    """
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    for label, results in results_dict.items():
        steps = [r[0] for r in results]
        gnorms = [min(r[2], clip_val) for r in results]
        ax.plot(steps, gnorms, label=label, alpha=0.8)
    ax.set_xlabel("Step")
    ax.set_ylabel("Gradient Norm (clipped)")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_ylim(bottom=0)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
    else:
        plt.show()


def plot_kv_cache_profiling(timings_cache: list, timings_no_cache: list,
                            title: str = "Generation Latency",
                            save_path: Optional[str] = None):
    """
    Plot ms/token vs token position for with/without KV cache.
    """
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))

    positions_c = [t[0] for t in timings_cache]
    ms_c = [t[1] for t in timings_cache]
    ax.plot(positions_c, ms_c, label="With KV Cache", alpha=0.8)

    positions_nc = [t[0] for t in timings_no_cache]
    ms_nc = [t[1] for t in timings_no_cache]
    ax.plot(positions_nc, ms_nc, label="Without KV Cache", alpha=0.8)

    ax.set_xlabel("Sequence Position (tokens generated)")
    ax.set_ylabel("Time per Token (ms)")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
    else:
        plt.show()


def plot_multi_loss(log_paths: dict, title: str = "Training Loss Comparison",
                    save_path: Optional[str] = None):
    """Plot loss curves from multiple CSV log files."""
    fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    for label, path in log_paths.items():
        data = load_metrics(path)
        ax.plot(data["step"], data["loss"], label=label, alpha=0.8)
    ax.set_xlabel("Step")
    ax.set_ylabel("Loss")
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close()
    else:
        plt.show()


def count_parameters(model: nn.Module) -> int:
    """Count total trainable parameters."""
    return sum(p.numel() for p in model.parameters() if p.requires_grad)
