"""
Lab 3 — Experiment 2: Positional Encoding Comparison
====================================================
Corresponds to: Ch.3 Sec.3.4 (position in decoder-only models)

Three 4-layer pre-norm models with residual connections:
  A: No positional encoding      → weaker explicit order signal
  B: Learned absolute PE         → standard GPT-2 style
  C: RoPE                        → modern LLaMA style (if scaffold supports it)

IMPORTANT: Do not force a conclusion that "RoPE is better."
Short training on a small model may not show a clear difference.
RoPE's advantage manifests at longer contexts and relative position tasks.

Usage:
    python exp2_positional.py
"""

import torch
import torch.nn.functional as F
from data import get_dataloaders
from model import GPT, GPTConfig
from utils import (train_loop, evaluate, generate_text,
                   plot_loss_curves, count_parameters)


def fixed_ce_loss(logits, input_ids):
    """Properly shifted CE loss."""
    logits_s = logits[:, :-1, :].contiguous()
    targets_s = input_ids[:, 1:].contiguous()
    return F.cross_entropy(logits_s.view(-1, logits_s.size(-1)), targets_s.view(-1))


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    train_dl, val_dl, vocab_size, chars = get_dataloaders(seq_len=256, batch_size=64)
    char2idx = {c: i for i, c in enumerate(chars)}

    N_STEPS = 2000

    configs = {
        "A: No PE": GPTConfig(
            vocab_size=vocab_size, seq_len=256, d_model=128, n_heads=4,
            n_layers=4, dropout=0.1, pe_type="none",
        ),
        "B: Learned absolute PE": GPTConfig(
            vocab_size=vocab_size, seq_len=256, d_model=128, n_heads=4,
            n_layers=4, dropout=0.1, pe_type="learned",
        ),
        "C: RoPE": GPTConfig(
            vocab_size=vocab_size, seq_len=256, d_model=128, n_heads=4,
            n_layers=4, dropout=0.1, pe_type="rope",
        ),
    }

    all_results = {}
    val_losses = {}

    for name, config in configs.items():
        print(f"\n{'=' * 60}")
        print(f"Training: {name}")
        print(f"{'=' * 60}")

        model = GPT(config).to(device)
        n_params = count_parameters(model)
        print(f"  Parameters: {n_params:,}")

        optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.01)

        log_name = name.split(":")[0].strip().lower()
        results = train_loop(
            model, train_dl, optimizer, fixed_ce_loss,
            n_steps=N_STEPS, log_path=f"logs/exp2_{log_name}.csv"
        )
        all_results[name] = results

        val_loss = evaluate(model, val_dl, fixed_ce_loss)
        val_losses[name] = val_loss
        print(f"  Final train loss: {results[-1][1]:.4f}")
        print(f"  Validation loss:  {val_loss:.4f}")

        # Generate sample
        sample = generate_text(model, chars, char2idx, prompt="ROMEO:",
                               max_new_tokens=200, use_cache=True)
        print(f"  Generated: {sample[:150]}...")

    # --- Plot ---
    plot_loss_curves(
        all_results,
        title="Exp 2: Training Loss — Positional Encoding Comparison",
        save_path="plots/exp2_loss_comparison.png"
    )
    print("\n  Saved: plots/exp2_loss_comparison.png")

    # --- Summary table ---
    print(f"\n{'=' * 60}")
    print("RESULTS SUMMARY")
    print(f"{'=' * 60}")
    print(f"  {'Config':<25} {'Val Loss':<12}")
    print(f"  {'-'*37}")
    for name, vl in val_losses.items():
        print(f"  {name:<25} {vl:.4f}")

    print(f"\n{'=' * 60}")
    print("OBSERVATIONS")
    print(f"{'=' * 60}")
    print("  - No PE: model has no position signal beyond causal mask.")
    print("    Causal mask provides partial order (token t cannot see t+1),")
    print("    but within the visible prefix, positions are indistinguishable.")
    print("  - Learned PE / RoPE: model can distinguish positions.")
    print("  - Short training may not clearly separate learned PE from RoPE.")
    print("    RoPE's advantage is in relative-position generalization at")
    print("    longer contexts — not easily visible in 256-length char LM.")


if __name__ == "__main__":
    import os
    os.makedirs("logs", exist_ok=True)
    os.makedirs("plots", exist_ok=True)
    main()
