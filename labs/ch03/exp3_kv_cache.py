"""
Lab 3 — Experiment 3: KV Cache Profiling
=========================================
Corresponds to: Ch.3 Sec.3.6 (autoregressive inference and KV cache)

Uses the pre-norm baseline from Exp 1 (config C) to measure generation
latency with and without KV cache.

Key deliverable: a plot showing ms/token vs token position.
  - Without cache: linear growth (recomputing all attention each step)
  - With cache: approximately flat (only computing attention for new token)

Usage:
    python exp3_kv_cache.py
"""

import torch
import torch.nn.functional as F
from data import load_tiny_shakespeare
from model import GPT, GPTConfig
from utils import (train_loop, profile_generation,
                   plot_kv_cache_profiling, count_parameters)


def fixed_ce_loss(logits, input_ids):
    """Properly shifted CE loss."""
    logits_s = logits[:, :-1, :].contiguous()
    targets_s = input_ids[:, 1:].contiguous()
    return F.cross_entropy(logits_s.view(-1, logits_s.size(-1)), targets_s.view(-1))


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    print(f"NOTE: This experiment is most meaningful on GPU.")
    print(f"      On CPU, the 'linear growth' pattern may be less pronounced")
    print(f"      due to CPU memory/compute dynamics vs GPU kernel launch overhead.")

    # Load data for a quick training run
    from torch.utils.data import DataLoader
    from data import CharDataset

    train_ds, val_ds, vocab_size, chars = load_tiny_shakespeare(seq_len=256)
    train_dl = DataLoader(train_ds, batch_size=64, shuffle=True, drop_last=True)
    char2idx = {c: i for i, c in enumerate(chars)}

    # Use the pre-norm baseline config (same as Exp 1 config C)
    config = GPTConfig(
        vocab_size=vocab_size,
        seq_len=512,         # Allow longer generation for profiling
        d_model=128,
        n_heads=4,
        n_layers=8,
        dropout=0.0,         # No dropout during profiling
        use_residual=True,
        norm_type="pre",
        pe_type="learned",
    )

    model = GPT(config).to(device)
    print(f"  Parameters: {count_parameters(model):,}")

    # Quick training so model produces non-random output
    print("\n  Training for 1000 steps (just enough for profiling)...")
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)
    train_loop(model, train_dl, optimizer, fixed_ce_loss, n_steps=1000)
    print("  Training done.")

    # Prepare a short prompt
    prompt_text = "ROMEO:"
    prompt_ids = torch.tensor(
        [[char2idx[c] for c in prompt_text]], dtype=torch.long, device=device
    )

    N_TOKENS = 256  # Generate this many tokens for profiling

    # --- Profile WITHOUT KV cache ---
    print(f"\n  Profiling generation WITHOUT KV cache ({N_TOKENS} tokens)...")
    timings_no_cache = profile_generation(
        model, prompt_ids, n_tokens=N_TOKENS, use_cache=False, warmup=3
    )
    total_no_cache = sum(t[1] for t in timings_no_cache)
    print(f"  Total time (no cache): {total_no_cache:.1f} ms")
    print(f"  Avg ms/token: {total_no_cache / N_TOKENS:.2f}")

    # --- Profile WITH KV cache ---
    print(f"\n  Profiling generation WITH KV cache ({N_TOKENS} tokens)...")
    timings_cache = profile_generation(
        model, prompt_ids, n_tokens=N_TOKENS, use_cache=True, warmup=3
    )
    total_cache = sum(t[1] for t in timings_cache[1:])  # Skip prefill
    print(f"  Total time (with cache, excluding prefill): {total_cache:.1f} ms")
    print(f"  Avg ms/token (decode only): {total_cache / (N_TOKENS - 1):.2f}")
    print(f"  Prefill time: {timings_cache[0][1]:.1f} ms")

    # --- Plot ---
    plot_kv_cache_profiling(
        timings_cache, timings_no_cache,
        title="Exp 3: Generation Latency — KV Cache vs No Cache",
        save_path="plots/exp3_kv_cache_profiling.png"
    )
    print("\n  Saved: plots/exp3_kv_cache_profiling.png")

    # --- Optional: memory profiling ---
    if torch.cuda.is_available():
        print(f"\n  Memory profiling (CUDA):")
        torch.cuda.reset_peak_memory_stats()

        # Generate with cache at different context lengths
        for ctx_len in [64, 128, 256, 400]:
            torch.cuda.reset_peak_memory_stats()
            test_prompt = torch.randint(0, vocab_size, (1, 16), device=device)
            _ = profile_generation(model, test_prompt, n_tokens=ctx_len,
                                   use_cache=True, warmup=1)
            peak_mb = torch.cuda.max_memory_allocated() / 1024 / 1024
            print(f"    Context {ctx_len:>4}: peak memory = {peak_mb:.1f} MB")

    # --- Summary ---
    print(f"\n{'=' * 60}")
    print("DIAGNOSIS")
    print(f"{'=' * 60}")
    speedup = total_no_cache / max(total_cache, 1)
    print(f"  Speedup from KV cache: {speedup:.1f}x")
    print()
    print("  WITHOUT cache: at position t, attention recomputes all T tokens.")
    print("    Cost per token grows linearly with position → total O(T^2).")
    print()
    print("  WITH cache: at position t, only compute attention for the NEW token")
    print("    against cached K/V. Cost per token is approximately constant.")
    print()
    print("  The plot shape tells the story:")
    print("    - No cache: upward slope (linear in position)")
    print("    - With cache: flat line (constant per token)")
    print()
    print("  This is why KV cache is essential for practical autoregressive inference.")


if __name__ == "__main__":
    import os
    os.makedirs("logs", exist_ok=True)
    os.makedirs("plots", exist_ok=True)
    main()
