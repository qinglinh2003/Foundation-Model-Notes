"""
Lab 3 — Experiment 3 (Dramatic Version): KV Cache Profiling
============================================================
Uses a LARGER model (d_model=512, 16 layers, 8 heads, ~25M params)
and LONGER generation (1024 tokens) to make the KV cache advantage
dramatically visible.

On RTX 2080 Ti:
  - No cache: ms/token should grow linearly, reaching ~50-100ms at position 1024
  - With cache: ms/token stays ~5-10ms throughout
  - Expected speedup: 5-15x overall

Usage:
    python exp3_kv_cache_dramatic.py
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
    print("=" * 60)
    print("Exp 3 (DRAMATIC): KV Cache Profiling — Larger Model")
    print("=" * 60)

    # Load data
    from torch.utils.data import DataLoader
    from data import CharDataset

    train_ds, val_ds, vocab_size, chars = load_tiny_shakespeare(seq_len=256)
    train_dl = DataLoader(train_ds, batch_size=32, shuffle=True, drop_last=True)
    char2idx = {c: i for i, c in enumerate(chars)}

    # LARGER model: 512 dim, 16 layers, 8 heads (~25M params)
    config = GPTConfig(
        vocab_size=vocab_size,
        seq_len=2048,        # Allow long generation
        d_model=512,
        n_heads=8,
        n_layers=16,
        dropout=0.0,
        use_residual=True,
        norm_type="pre",
        pe_type="learned",
    )

    model = GPT(config).to(device)
    n_params = count_parameters(model)
    print(f"  Parameters: {n_params:,}")
    print(f"  Config: d_model=512, n_layers=16, n_heads=8")

    # Quick training (500 steps just so model isn't random)
    print("\n  Training for 500 steps (just enough for non-random output)...")
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)
    train_loop(model, train_dl, optimizer, fixed_ce_loss, n_steps=500)
    print("  Training done.")

    # Prepare prompt
    prompt_text = "ROMEO:\nO, "
    prompt_ids = torch.tensor(
        [[char2idx.get(c, 0) for c in prompt_text]], dtype=torch.long, device=device
    )

    N_TOKENS = 1024  # Long generation to make the curve dramatic

    # --- Profile WITHOUT KV cache ---
    print(f"\n  Profiling generation WITHOUT KV cache ({N_TOKENS} tokens)...")
    print(f"  (This will be SLOW — expect ~3-5 minutes)")
    timings_no_cache = profile_generation(
        model, prompt_ids, n_tokens=N_TOKENS, use_cache=False, warmup=2
    )
    total_no_cache = sum(t[1] for t in timings_no_cache)
    avg_no_cache = total_no_cache / N_TOKENS
    print(f"  Total time (no cache): {total_no_cache:.0f} ms ({total_no_cache/1000:.1f} s)")
    print(f"  Avg ms/token: {avg_no_cache:.2f}")
    print(f"  First token: {timings_no_cache[0][1]:.2f} ms")
    print(f"  Last token:  {timings_no_cache[-1][1]:.2f} ms")
    print(f"  Slowdown ratio (last/first): {timings_no_cache[-1][1]/max(timings_no_cache[0][1], 0.01):.1f}x")

    # --- Profile WITH KV cache ---
    print(f"\n  Profiling generation WITH KV cache ({N_TOKENS} tokens)...")
    timings_cache = profile_generation(
        model, prompt_ids, n_tokens=N_TOKENS, use_cache=True, warmup=2
    )
    total_cache = sum(t[1] for t in timings_cache[1:])  # Skip prefill
    avg_cache = total_cache / (N_TOKENS - 1)
    print(f"  Total time (with cache, excluding prefill): {total_cache:.0f} ms ({total_cache/1000:.1f} s)")
    print(f"  Avg ms/token (decode only): {avg_cache:.2f}")
    print(f"  Prefill time: {timings_cache[0][1]:.1f} ms")
    print(f"  First decode token: {timings_cache[1][1]:.2f} ms")
    print(f"  Last decode token:  {timings_cache[-1][1]:.2f} ms")

    # --- Plot ---
    plot_kv_cache_profiling(
        timings_cache, timings_no_cache,
        title="Exp 3 (Dramatic): KV Cache vs No Cache — 25M Model, 1024 Tokens",
        save_path="plots/exp3_kv_cache_dramatic.png"
    )
    print("\n  Saved: plots/exp3_kv_cache_dramatic.png")

    # --- Memory profiling ---
    if torch.cuda.is_available():
        print(f"\n  Memory profiling (CUDA):")
        for ctx_len in [128, 256, 512, 1024]:
            torch.cuda.reset_peak_memory_stats()
            test_prompt = torch.randint(0, vocab_size, (1, 16), device=device)
            try:
                _ = profile_generation(model, test_prompt, n_tokens=ctx_len,
                                       use_cache=True, warmup=1)
                peak_mb = torch.cuda.max_memory_allocated() / 1024 / 1024
                print(f"    Context {ctx_len:>4}: peak memory = {peak_mb:.1f} MB")
            except RuntimeError as e:
                print(f"    Context {ctx_len:>4}: OOM or error — {e}")
                break

    # --- Summary ---
    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    speedup = total_no_cache / max(total_cache, 1)
    print(f"  Overall speedup: {speedup:.1f}x")
    print(f"  No-cache slowdown (last vs first token): {timings_no_cache[-1][1]/max(timings_no_cache[0][1], 0.01):.1f}x")
    print(f"  Cache decode variance: first={timings_cache[1][1]:.2f}ms, last={timings_cache[-1][1]:.2f}ms")
    print()
    print("  INTERPRETATION:")
    print(f"    Without cache: cost per token grows linearly with position.")
    print(f"    At position 1024, each token costs ~{timings_no_cache[-1][1]:.0f}ms")
    print(f"    vs ~{avg_cache:.1f}ms with cache. That's a {timings_no_cache[-1][1]/max(avg_cache, 0.1):.0f}x")
    print(f"    difference at the END of generation.")
    print()
    print("    For a 7B model at 4K context, this difference would be")
    print("    even more extreme — making KV cache non-optional for")
    print("    practical deployment.")


if __name__ == "__main__":
    import os
    os.makedirs("logs", exist_ok=True)
    os.makedirs("plots", exist_ok=True)
    main()
