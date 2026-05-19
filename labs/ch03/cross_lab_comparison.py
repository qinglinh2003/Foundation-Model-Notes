"""
Lab 3 — Cross-Lab Comparison: LSTM vs Transformer
===================================================
Corresponds to: Ch.1 -> Ch.3 narrative arc

Compares Lab 1's LSTM with Lab 3's Transformer on the same task
(Tiny Shakespeare character-level LM) at similar parameter counts.

Pre-matched configurations:
  LSTM:        2 layers, hidden=512, ~5M params
  Transformer: 4 layers, d_model=256, 4 heads, ~5M params

Usage:
    python cross_lab_comparison.py
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from data import get_dataloaders
from model import GPT, GPTConfig
from utils import (train_loop, evaluate, generate_text,
                   plot_loss_curves, count_parameters)


# ===================================================================
# Simple LSTM baseline (self-contained, no Lab 1 dependency)
# ===================================================================

class CharLSTM(nn.Module):
    """Minimal character-level LSTM for comparison."""

    def __init__(self, vocab_size: int, embed_dim: int = 64,
                 hidden_size: int = 512, num_layers: int = 2):
        super().__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_size, num_layers=num_layers,
                            batch_first=True, dropout=0.1)
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, input_ids, hidden=None):
        x = self.embedding(input_ids)
        out, hidden = self.lstm(x, hidden)
        logits = self.fc(out)
        return logits, hidden

    @torch.no_grad()
    def generate(self, prompt_ids, max_new_tokens=200, temperature=1.0):
        self.eval()
        generated = prompt_ids.clone()
        hidden = None
        # Feed prompt
        logits, hidden = self.forward(generated, hidden)
        # Detach hidden for generation
        hidden = tuple(h.detach() for h in hidden)

        for _ in range(max_new_tokens):
            next_logits = logits[:, -1, :] / temperature
            probs = F.softmax(next_logits, dim=-1)
            next_token = torch.multinomial(probs, 1)
            generated = torch.cat([generated, next_token], dim=1)
            logits, hidden = self.forward(next_token, hidden)
            hidden = tuple(h.detach() for h in hidden)

        return generated


def lstm_ce_loss(logits, input_ids):
    """Shifted CE loss for LSTM (same as GPT)."""
    logits_s = logits[:, :-1, :].contiguous()
    targets_s = input_ids[:, 1:].contiguous()
    return F.cross_entropy(logits_s.view(-1, logits_s.size(-1)), targets_s.view(-1))


def gpt_ce_loss(logits, input_ids):
    """Shifted CE loss for GPT."""
    logits_s = logits[:, :-1, :].contiguous()
    targets_s = input_ids[:, 1:].contiguous()
    return F.cross_entropy(logits_s.view(-1, logits_s.size(-1)), targets_s.view(-1))


def train_lstm(model, train_dl, optimizer, n_steps, log_path=None):
    """Training loop for LSTM (slightly different interface)."""
    from utils import MetricLogger
    import math

    device = next(model.parameters()).device
    logger = MetricLogger(log_path, ["step", "loss", "grad_norm"]) if log_path else None
    results = []
    step = 0

    while step < n_steps:
        for batch in train_dl:
            if step >= n_steps:
                break
            model.train()
            input_ids = batch[0].to(device)

            optimizer.zero_grad()
            logits, _ = model(input_ids)
            loss = lstm_ce_loss(logits, input_ids)
            loss.backward()

            grad_norm = math.sqrt(sum(
                p.grad.norm(2).item() ** 2
                for p in model.parameters() if p.grad is not None
            ))
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            results.append((step, loss.item(), grad_norm))
            if logger:
                logger.log(step=step, loss=loss.item(), grad_norm=grad_norm)
            step += 1

    if logger:
        logger.close()
    return results


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    train_dl, val_dl, vocab_size, chars = get_dataloaders(seq_len=256, batch_size=64)
    char2idx = {c: i for i, c in enumerate(chars)}

    N_STEPS = 3000

    # --- LSTM ---
    print(f"\n{'=' * 60}")
    print("Training: LSTM (2 layers, hidden=512)")
    print(f"{'=' * 60}")

    lstm_model = CharLSTM(vocab_size=vocab_size, embed_dim=64,
                          hidden_size=512, num_layers=2).to(device)
    lstm_params = count_parameters(lstm_model)
    print(f"  Parameters: {lstm_params:,}")

    lstm_opt = torch.optim.AdamW(lstm_model.parameters(), lr=3e-4, weight_decay=0.01)
    lstm_results = train_lstm(lstm_model, train_dl, lstm_opt, N_STEPS,
                              log_path="logs/cross_lstm.csv")

    lstm_val = evaluate_lstm(lstm_model, val_dl)
    print(f"  Validation loss: {lstm_val:.4f}")

    lstm_sample = generate_lstm_text(lstm_model, chars, char2idx)
    print(f"  Generated: {lstm_sample[:150]}...")

    # --- Transformer ---
    print(f"\n{'=' * 60}")
    print("Training: Transformer (4 layers, d_model=256, 4 heads)")
    print(f"{'=' * 60}")

    gpt_config = GPTConfig(
        vocab_size=vocab_size,
        seq_len=256,
        d_model=256,
        n_heads=4,
        n_layers=4,
        ffn_mult=4,
        dropout=0.1,
        pe_type="learned",
    )
    gpt_model = GPT(gpt_config).to(device)
    gpt_params = count_parameters(gpt_model)
    print(f"  Parameters: {gpt_params:,}")

    gpt_opt = torch.optim.AdamW(gpt_model.parameters(), lr=3e-4, weight_decay=0.01)
    gpt_results = train_loop(gpt_model, train_dl, gpt_opt, gpt_ce_loss,
                             n_steps=N_STEPS, log_path="logs/cross_gpt.csv")

    gpt_val = evaluate(gpt_model, val_dl, gpt_ce_loss)
    print(f"  Validation loss: {gpt_val:.4f}")

    gpt_sample = generate_text(gpt_model, chars, char2idx, prompt="ROMEO:",
                               max_new_tokens=200, use_cache=True)
    print(f"  Generated: {gpt_sample[:150]}...")

    # --- Comparison ---
    print(f"\n{'=' * 60}")
    print("CROSS-LAB COMPARISON")
    print(f"{'=' * 60}")
    print(f"  {'Metric':<20} {'LSTM':<15} {'Transformer':<15}")
    print(f"  {'-'*50}")
    print(f"  {'Parameters':<20} {lstm_params:,<15} {gpt_params:,<15}")
    print(f"  {'Val Loss':<20} {lstm_val:<15.4f} {gpt_val:<15.4f}")

    # Measure tokens/sec
    import time
    model_configs = [
        ("LSTM", lstm_model, lambda b: lstm_model(b)[0]),
        ("Transformer", gpt_model, lambda b: gpt_model(b)[0]),
    ]

    for name, model, fwd_fn in model_configs:
        model.eval()
        batch = next(iter(train_dl))[0][:16].to(device)  # small batch
        # Warmup
        for _ in range(5):
            with torch.no_grad():
                _ = fwd_fn(batch)
        # Time
        if torch.cuda.is_available():
            torch.cuda.synchronize()
        start = time.perf_counter()
        n_iters = 50
        for _ in range(n_iters):
            with torch.no_grad():
                _ = fwd_fn(batch)
        if torch.cuda.is_available():
            torch.cuda.synchronize()
        elapsed = time.perf_counter() - start
        tokens_per_sec = (16 * 256 * n_iters) / elapsed
        print(f"  {'Tokens/sec (' + name + ')':<20} {tokens_per_sec:,.0f}")

    # --- Plot ---
    plot_loss_curves(
        {"LSTM": lstm_results, "Transformer": gpt_results},
        title="Cross-Lab: LSTM vs Transformer Training Loss",
        save_path="plots/cross_lab_comparison.png"
    )
    print("\n  Saved: plots/cross_lab_comparison.png")

    print(f"\n{'=' * 60}")
    print("OBSERVATIONS")
    print(f"{'=' * 60}")
    print("  Compare:")
    print("    - Training speed (tokens/sec): Transformer should be faster (parallel)")
    print("    - Validation loss: at similar params, which converges lower?")
    print("    - Generation quality: qualitative comparison of coherence")
    print("    - Training stability: compare gradient norm variance")
    print()
    print("  The key insight from Ch.1 -> Ch.3:")
    print("    LSTM processes tokens sequentially; Transformer processes in parallel.")
    print("    At similar parameter counts, parallelism gives Transformer better")
    print("    GPU utilization → faster training → potentially better final quality.")


# --- Helper functions for LSTM ---

@torch.no_grad()
def evaluate_lstm(model, val_dl) -> float:
    model.eval()
    device = next(model.parameters()).device
    total_loss = 0.0
    n = 0
    for batch in val_dl:
        input_ids = batch[0].to(device)
        logits, _ = model(input_ids)
        loss = lstm_ce_loss(logits, input_ids)
        total_loss += loss.item()
        n += 1
    return total_loss / max(n, 1)


def generate_lstm_text(model, chars, char2idx, prompt="ROMEO:",
                       max_new_tokens=200, temperature=1.0) -> str:
    model.eval()
    device = next(model.parameters()).device
    prompt_ids = torch.tensor(
        [[char2idx[c] for c in prompt]], dtype=torch.long, device=device
    )
    output_ids = model.generate(prompt_ids, max_new_tokens=max_new_tokens,
                                temperature=temperature)
    idx2char = {i: c for c, i in char2idx.items()}
    return "".join(idx2char[i.item()] for i in output_ids[0])


if __name__ == "__main__":
    import os
    os.makedirs("logs", exist_ok=True)
    os.makedirs("plots", exist_ok=True)
    main()
