"""
Lab 3 — Experiment 1: Residual Stream and Normalization (CENTERPIECE)
=====================================================================
Corresponds to: Ch.3 Sec.3.3 (residual stream) and Sec.3.8 (failure modes)

This is the centerpiece experiment of Lab 3.

Three 8-layer models, identical except for residual/norm configuration:
  A: No residual, pre-norm        → expect failure (gradient explosion/vanishing)
  B: Residual, post-norm          → expect instability (loss spikes)
  C: Residual, pre-norm (default) → expect stable training

The key deliverable is a gradient-norm-vs-step plot showing three distinct
regimes. This directly parallels Lab 1's RNN-vs-LSTM gradient comparison.

Usage:
    python exp1_residual_norm.py
"""

import torch
import torch.nn.functional as F
from data import get_dataloaders
from model import GPT, GPTConfig
from utils import (train_loop, evaluate, generate_text,
                   plot_loss_curves, plot_grad_norms, count_parameters)


def fixed_ce_loss(logits, input_ids):
    """Properly shifted CE loss."""
    logits_s = logits[:, :-1, :].contiguous()
    targets_s = input_ids[:, 1:].contiguous()
    return F.cross_entropy(logits_s.view(-1, logits_s.size(-1)), targets_s.view(-1))


def make_config(use_residual: bool, norm_type: str, vocab_size: int) -> GPTConfig:
    """Create config for a specific ablation condition."""
    return GPTConfig(
        vocab_size=vocab_size,
        seq_len=256,
        d_model=128,
        n_heads=4,
        n_layers=8,       # Deeper to stress-test residual/norm
        ffn_mult=4,
        dropout=0.1,
        use_residual=use_residual,
        norm_type=norm_type,
        pe_type="learned",
    )


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    train_dl, val_dl, vocab_size, chars = get_dataloaders(seq_len=256, batch_size=64)
    char2idx = {c: i for i, c in enumerate(chars)}

    N_STEPS = 3000

    configs = {
        "A: No residual, pre-norm": make_config(use_residual=False, norm_type="pre", vocab_size=vocab_size),
        "B: Residual, post-norm":   make_config(use_residual=True,  norm_type="post", vocab_size=vocab_size),
        "C: Residual, pre-norm":    make_config(use_residual=True,  norm_type="pre", vocab_size=vocab_size),
    }

    all_results = {}

    for name, config in configs.items():
        print(f"\n{'=' * 60}")
        print(f"Training: {name}")
        print(f"{'=' * 60}")

        model = GPT(config).to(device)
        n_params = count_parameters(model)
        print(f"  Parameters: {n_params:,}")

        optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.01)

        # Use no gradient clipping for the no-residual run to see raw instability
        max_gnorm = 50.0 if config.use_residual else 50.0  # clip to prevent NaN

        log_name = name.split(":")[0].strip().lower()
        results = train_loop(
            model, train_dl, optimizer, fixed_ce_loss,
            n_steps=N_STEPS, log_path=f"logs/exp1_{log_name}.csv",
            max_grad_norm=max_gnorm
        )
        all_results[name] = results

        # Check for NaN
        final_loss = results[-1][1] if results else float("nan")
        if final_loss != final_loss:  # NaN check
            print(f"  WARNING: Training diverged (NaN loss)")
            continue

        val_loss = evaluate(model, val_dl, fixed_ce_loss)
        print(f"  Final train loss: {final_loss:.4f}")
        print(f"  Validation loss:  {val_loss:.4f}")

        # Generate sample
        try:
            sample = generate_text(model, chars, char2idx, prompt="ROMEO:",
                                   max_new_tokens=200, use_cache=config.use_residual)
            print(f"  Generated: {sample[:100]}...")
        except Exception as e:
            print(f"  Generation failed: {e}")

    # --- Plot centerpiece figures ---
    print(f"\n{'=' * 60}")
    print("Generating centerpiece plots")
    print(f"{'=' * 60}")

    plot_grad_norms(
        all_results,
        title="Exp 1 (CENTERPIECE): Gradient Norm — Residual/Norm Ablation",
        save_path="plots/exp1_grad_norm_comparison.png"
    )
    print("  Saved: plots/exp1_grad_norm_comparison.png")

    plot_loss_curves(
        all_results,
        title="Exp 1: Training Loss — Residual/Norm Ablation",
        save_path="plots/exp1_loss_comparison.png"
    )
    print("  Saved: plots/exp1_loss_comparison.png")

    # --- Summary ---
    print(f"\n{'=' * 60}")
    print("DIAGNOSIS")
    print(f"{'=' * 60}")
    print("  Config A (no residual): gradient norms should spike or vanish.")
    print("  Config B (post-norm):   trains but may show occasional spikes.")
    print("  Config C (pre-norm):    stable gradient norms, smooth loss descent.")
    print()
    print("  COMPARE WITH LAB 1:")
    print("    Lab 1 Exp 1: RNN gradient explosion/vanishing vs LSTM stability")
    print("    Lab 3 Exp 1: No-residual instability vs pre-norm stability")
    print("    The parallel: residual stream is to Transformer what cell state is to LSTM.")
    print("    Both provide a 'gradient highway' that enables deep/long computation.")


if __name__ == "__main__":
    import os
    os.makedirs("logs", exist_ok=True)
    os.makedirs("plots", exist_ok=True)
    main()
