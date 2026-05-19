"""
Lab 3 — Experiment 0: Shifted-Label Bug Hunt
=============================================
Corresponds to: Ch.3 Sec.3.2 (shifted cross-entropy loss)

This experiment trains two models:
  1. BUGGY: uses a local no-shift loss
  2. FIXED: uses the correct shifted_ce_loss from model.py

The buggy model will have suspiciously low loss but generate garbage.
The fixed model will have higher loss but generate coherent text.

Usage:
    python exp0_shifted_label.py
"""

import torch
import torch.nn.functional as F
from data import get_dataloaders
from model import GPT, GPTConfig, shifted_ce_loss
from utils import train_loop, evaluate, generate_text, plot_loss_curves, count_parameters


def buggy_ce_loss(logits: torch.Tensor, input_ids: torch.Tensor) -> torch.Tensor:
    """Deliberately wrong loss: predicts the current token."""
    B, T, V = logits.shape
    return F.cross_entropy(
        logits.reshape(-1, V),
        input_ids.reshape(-1)
    )


def main():
    # Setup
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    train_dl, val_dl, vocab_size, chars = get_dataloaders(seq_len=256, batch_size=64)
    char2idx = {c: i for i, c in enumerate(chars)}

    config = GPTConfig(
        vocab_size=vocab_size,
        seq_len=256,
        d_model=128,
        n_heads=4,
        n_layers=4,
        dropout=0.1,
        pe_type="learned",
    )

    # --- Run 1: BUGGY loss ---
    print("\n" + "=" * 60)
    print("Run 1: BUGGY no-shift loss")
    print("=" * 60)

    model_buggy = GPT(config).to(device)
    opt_buggy = torch.optim.AdamW(model_buggy.parameters(), lr=3e-4, weight_decay=0.01)
    results_buggy = train_loop(
        model_buggy, train_dl, opt_buggy, buggy_ce_loss,
        n_steps=500, log_path="logs/exp0_buggy.csv"
    )

    val_loss_buggy = evaluate(model_buggy, val_dl, buggy_ce_loss)
    print(f"  Final val loss (buggy): {val_loss_buggy:.4f}")
    print(f"  NOTE: This is suspiciously low!")

    sample_buggy = generate_text(model_buggy, chars, char2idx, prompt="ROMEO:", max_new_tokens=200)
    print(f"\n  Generated (buggy):\n  {sample_buggy[:200]}")

    # --- Run 2: FIXED loss ---
    print("\n" + "=" * 60)
    print("Run 2: FIXED shifted_ce_loss from model.py")
    print("=" * 60)

    model_fixed = GPT(config).to(device)
    opt_fixed = torch.optim.AdamW(model_fixed.parameters(), lr=3e-4, weight_decay=0.01)
    results_fixed = train_loop(
        model_fixed, train_dl, opt_fixed, shifted_ce_loss,
        n_steps=500, log_path="logs/exp0_fixed.csv"
    )

    val_loss_fixed = evaluate(model_fixed, val_dl, shifted_ce_loss)
    print(f"  Final val loss (fixed): {val_loss_fixed:.4f}")
    print(f"  NOTE: Higher loss is expected — model is now solving the REAL task.")

    sample_fixed = generate_text(model_fixed, chars, char2idx, prompt="ROMEO:", max_new_tokens=200)
    print(f"\n  Generated (fixed):\n  {sample_fixed[:200]}")

    # --- Plot comparison ---
    plot_loss_curves(
        {"Buggy (no shift)": results_buggy, "Fixed (shifted)": results_fixed},
        title="Exp 0: Buggy vs Fixed Loss",
        save_path="plots/exp0_loss_comparison.png"
    )
    print("\n  Plot saved: plots/exp0_loss_comparison.png")

    # --- Summary ---
    print("\n" + "=" * 60)
    print("DIAGNOSIS")
    print("=" * 60)
    print(f"  Buggy val loss:  {val_loss_buggy:.4f}  (too good to be true)")
    print(f"  Fixed val loss:  {val_loss_fixed:.4f}  (realistic)")
    print()
    print("  The buggy model 'predicts' the current token (trivial copy task).")
    print("  The fixed model predicts the NEXT token (the actual LM objective).")
    print("  Low loss + bad generation = label alignment bug.")
    print("  This is the same pattern as Lab 2's mask bug: loss lies.")


if __name__ == "__main__":
    import os
    os.makedirs("logs", exist_ok=True)
    os.makedirs("plots", exist_ok=True)
    main()
