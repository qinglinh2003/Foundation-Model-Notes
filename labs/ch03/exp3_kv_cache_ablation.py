"""
Lab 3 — Experiment 3: KV Cache Ablation Study
===============================================
Runs KV cache profiling across a grid of (model_size, gen_length) to show
how the speedup scales with both dimensions.

Configurations:
  A: tiny    (d=128,  8 layers,  4 heads, ~5M)   × 256 tokens
  B: medium  (d=512, 16 layers,  8 heads, ~51M)  × 1024 tokens
  C: large   (d=768, 24 layers, 12 heads, ~170M) × 1024 tokens
  D: large   (d=768, 24 layers, 12 heads, ~170M) × 2048 tokens
  E: xlarge  (d=1024,24 layers, 16 heads, ~300M) × 2048 tokens

Usage:
    python exp3_kv_cache_ablation.py
"""

import os
import csv
import time
import torch
import torch.nn.functional as F
from data import load_tiny_shakespeare
from model import GPT, GPTConfig
from utils import profile_generation, count_parameters

os.makedirs("logs", exist_ok=True)
os.makedirs("plots", exist_ok=True)


def fixed_ce_loss(logits, input_ids):
    # model.forward returns (logits, caches); unpack if needed
    if isinstance(logits, tuple):
        logits = logits[0]
    logits_s = logits[:, :-1, :].contiguous()
    targets_s = input_ids[:, 1:].contiguous()
    return F.cross_entropy(logits_s.view(-1, logits_s.size(-1)), targets_s.view(-1))


CONFIGS = [
    {"name": "A_tiny",       "d_model": 128,  "n_layers": 8,  "n_heads": 4,  "gen_len": 256,  "train_steps": 300},
    {"name": "B_medium",     "d_model": 512,  "n_layers": 16, "n_heads": 8,  "gen_len": 512,  "train_steps": 300},
    {"name": "C_medium_long","d_model": 512,  "n_layers": 16, "n_heads": 8,  "gen_len": 1024, "train_steps": 300},
    {"name": "D_large",      "d_model": 768,  "n_layers": 12, "n_heads": 12, "gen_len": 512,  "train_steps": 200},
    {"name": "E_large_long", "d_model": 768,  "n_layers": 12, "n_heads": 12, "gen_len": 1024, "train_steps": 200},
]


def run_config(cfg, device, train_dl, vocab_size, char2idx):
    name = cfg["name"]
    gen_len = cfg["gen_len"]

    print(f"\n{'='*70}")
    print(f"  Config {name}: d={cfg['d_model']}, L={cfg['n_layers']}, "
          f"h={cfg['n_heads']}, gen={gen_len} tokens")
    print(f"{'='*70}")

    # Build model
    config = GPTConfig(
        vocab_size=vocab_size,
        seq_len=max(gen_len + 32, 256),  # enough room
        d_model=cfg["d_model"],
        n_heads=cfg["n_heads"],
        n_layers=cfg["n_layers"],
        dropout=0.0,
        use_residual=True,
        norm_type="pre",
        pe_type="learned",
    )
    model = GPT(config).to(device)
    n_params = count_parameters(model)
    print(f"  Parameters: {n_params:,}")

    # Quick training
    print(f"  Training for {cfg['train_steps']} steps...")
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4)
    model.train()
    step = 0
    for batch in train_dl:
        if step >= cfg["train_steps"]:
            break
        x = batch[0].to(device) if isinstance(batch, (list, tuple)) else batch.to(device)
        logits = model(x)
        loss = fixed_ce_loss(logits, x)
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        step += 1
    print(f"  Training done (final loss: {loss.item():.3f})")

    # Prepare prompt
    prompt_text = "ROMEO:\n"
    prompt_ids = torch.tensor(
        [[char2idx.get(c, 0) for c in prompt_text]], dtype=torch.long, device=device
    )

    # Profile WITHOUT cache
    print(f"  Profiling WITHOUT cache ({gen_len} tokens)...")
    t0 = time.time()
    timings_no_cache = profile_generation(
        model, prompt_ids, n_tokens=gen_len, use_cache=False, warmup=2
    )
    wall_no_cache = time.time() - t0
    total_no_cache = sum(t[1] for t in timings_no_cache)
    avg_no_cache = total_no_cache / gen_len
    first_no = timings_no_cache[0][1]
    last_no = timings_no_cache[-1][1]

    # Profile WITH cache
    print(f"  Profiling WITH cache ({gen_len} tokens)...")
    t0 = time.time()
    timings_cache = profile_generation(
        model, prompt_ids, n_tokens=gen_len, use_cache=True, warmup=2
    )
    wall_cache = time.time() - t0
    total_cache = sum(t[1] for t in timings_cache[1:])  # skip prefill
    avg_cache = total_cache / max(gen_len - 1, 1)
    first_c = timings_cache[1][1] if len(timings_cache) > 1 else 0
    last_c = timings_cache[-1][1]
    prefill = timings_cache[0][1]

    # Compute metrics
    overall_speedup = total_no_cache / max(total_cache, 1)
    slowdown_ratio = last_no / max(first_no, 0.01)
    end_speedup = last_no / max(last_c, 0.01)

    # Memory
    peak_mb = 0
    if torch.cuda.is_available():
        torch.cuda.reset_peak_memory_stats()
        _ = profile_generation(model, prompt_ids, n_tokens=min(gen_len, 512),
                               use_cache=True, warmup=1)
        peak_mb = torch.cuda.max_memory_allocated() / 1024 / 1024

    # Print summary
    print(f"\n  Results for {name}:")
    print(f"    No-cache: avg={avg_no_cache:.2f} ms/tok, "
          f"first={first_no:.2f}ms, last={last_no:.2f}ms, "
          f"slowdown={slowdown_ratio:.1f}x")
    print(f"    Cache:    avg={avg_cache:.2f} ms/tok, "
          f"prefill={prefill:.1f}ms, "
          f"first_decode={first_c:.2f}ms, last={last_c:.2f}ms")
    print(f"    Overall speedup: {overall_speedup:.2f}x")
    print(f"    End-of-generation speedup: {end_speedup:.2f}x")
    if peak_mb > 0:
        print(f"    Peak GPU memory: {peak_mb:.0f} MB")

    # Clean up
    del model, optimizer
    torch.cuda.empty_cache() if torch.cuda.is_available() else None

    return {
        "name": name,
        "d_model": cfg["d_model"],
        "n_layers": cfg["n_layers"],
        "n_heads": cfg["n_heads"],
        "n_params": n_params,
        "gen_len": gen_len,
        "avg_no_cache": avg_no_cache,
        "avg_cache": avg_cache,
        "first_no_cache": first_no,
        "last_no_cache": last_no,
        "first_cache": first_c,
        "last_cache": last_c,
        "prefill": prefill,
        "overall_speedup": overall_speedup,
        "slowdown_ratio": slowdown_ratio,
        "end_speedup": end_speedup,
        "peak_mb": peak_mb,
        "timings_no_cache": timings_no_cache,
        "timings_cache": timings_cache,
    }


def plot_ablation(results):
    """Plot ms/token curves for all configs, and a summary bar chart."""
    import matplotlib.pyplot as plt

    n = len(results)
    fig, axes = plt.subplots(1, n, figsize=(5 * n, 4), sharey=False)
    if n == 1:
        axes = [axes]

    for ax, r in zip(axes, results):
        positions_no = [t[0] for t in r["timings_no_cache"]]
        times_no = [t[1] for t in r["timings_no_cache"]]
        positions_c = [t[0] for t in r["timings_cache"]]
        times_c = [t[1] for t in r["timings_cache"]]

        ax.plot(positions_no, times_no, 'r-', alpha=0.5, linewidth=0.8, label="No cache")
        ax.plot(positions_c, times_c, 'b-', alpha=0.5, linewidth=0.8, label="With cache")

        # Smoothed lines
        window = max(len(times_no) // 50, 5)
        if len(times_no) > window:
            import numpy as np
            kernel = np.ones(window) / window
            smooth_no = np.convolve(times_no, kernel, mode='valid')
            smooth_c = np.convolve(times_c, kernel, mode='valid')
            offset = window // 2
            ax.plot(positions_no[offset:offset+len(smooth_no)], smooth_no,
                    'r-', linewidth=2, label=f"No cache (smooth)")
            ax.plot(positions_c[offset:offset+len(smooth_c)], smooth_c,
                    'b-', linewidth=2, label=f"Cache (smooth)")

        ax.set_xlabel("Token position")
        ax.set_ylabel("ms / token")
        ax.set_title(f"{r['name']}\n{r['n_params']/1e6:.0f}M, {r['gen_len']} tok\n"
                     f"Speedup: {r['overall_speedup']:.1f}x overall, "
                     f"{r['end_speedup']:.1f}x at end")
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("plots/exp3_kv_cache_ablation.png", dpi=150)
    plt.close()
    print("\nSaved: plots/exp3_kv_cache_ablation.png")

    # Summary bar chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    names = [r["name"] for r in results]
    overall = [r["overall_speedup"] for r in results]
    end = [r["end_speedup"] for r in results]

    x = range(len(names))
    ax1.bar(x, overall, color='steelblue', alpha=0.8)
    ax1.set_xticks(x)
    ax1.set_xticklabels(names, rotation=30, ha='right', fontsize=8)
    ax1.set_ylabel("Overall speedup")
    ax1.set_title("KV Cache Overall Speedup vs Model Scale")
    ax1.axhline(y=1, color='gray', linestyle='--', alpha=0.5)
    for i, v in enumerate(overall):
        ax1.text(i, v + 0.1, f"{v:.1f}x", ha='center', fontsize=9)

    ax2.bar(x, end, color='coral', alpha=0.8)
    ax2.set_xticks(x)
    ax2.set_xticklabels(names, rotation=30, ha='right', fontsize=8)
    ax2.set_ylabel("End-of-generation speedup")
    ax2.set_title("KV Cache Speedup at Last Token")
    ax2.axhline(y=1, color='gray', linestyle='--', alpha=0.5)
    for i, v in enumerate(end):
        ax2.text(i, v + 0.1, f"{v:.1f}x", ha='center', fontsize=9)

    plt.tight_layout()
    plt.savefig("plots/exp3_kv_cache_ablation_summary.png", dpi=150)
    plt.close()
    print("Saved: plots/exp3_kv_cache_ablation_summary.png")


def save_csv(results):
    with open("logs/exp3_ablation_summary.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["config", "d_model", "n_layers", "n_heads", "params",
                     "gen_len", "avg_no_cache_ms", "avg_cache_ms",
                     "first_no_cache_ms", "last_no_cache_ms",
                     "first_cache_ms", "last_cache_ms",
                     "overall_speedup", "slowdown_ratio", "end_speedup",
                     "peak_mb"])
        for r in results:
            w.writerow([
                r["name"], r["d_model"], r["n_layers"], r["n_heads"],
                r["n_params"], r["gen_len"],
                f"{r['avg_no_cache']:.2f}", f"{r['avg_cache']:.2f}",
                f"{r['first_no_cache']:.2f}", f"{r['last_no_cache']:.2f}",
                f"{r['first_cache']:.2f}", f"{r['last_cache']:.2f}",
                f"{r['overall_speedup']:.2f}", f"{r['slowdown_ratio']:.2f}",
                f"{r['end_speedup']:.2f}", f"{r['peak_mb']:.0f}",
            ])
    print("\nSaved: logs/exp3_ablation_summary.csv")


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")
    print(f"{'='*70}")
    print(f"  KV Cache Ablation Study: Model Size × Sequence Length")
    print(f"{'='*70}")

    # Load data
    from torch.utils.data import DataLoader
    train_ds, val_ds, vocab_size, chars = load_tiny_shakespeare(seq_len=256)
    train_dl = DataLoader(train_ds, batch_size=32, shuffle=True, drop_last=True)
    char2idx = {c: i for i, c in enumerate(chars)}

    results = []
    for cfg in CONFIGS:
        try:
            r = run_config(cfg, device, train_dl, vocab_size, char2idx)
            results.append(r)
        except RuntimeError as e:
            print(f"\n  CONFIG {cfg['name']} FAILED: {e}")
            print(f"  Skipping and continuing...")
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
            continue

    # Print final summary table
    print(f"\n{'='*70}")
    print("  ABLATION SUMMARY")
    print(f"{'='*70}")
    print(f"  {'Config':<16} {'Params':>8} {'GenLen':>6} "
          f"{'Avg(no)':>9} {'Avg(kv)':>9} {'Overall':>8} "
          f"{'Slowdown':>9} {'End':>8}")
    print(f"  {'-'*16} {'-'*8} {'-'*6} "
          f"{'-'*9} {'-'*9} {'-'*8} "
          f"{'-'*9} {'-'*8}")
    for r in results:
        print(f"  {r['name']:<16} {r['n_params']/1e6:>7.1f}M {r['gen_len']:>6} "
              f"{r['avg_no_cache']:>8.2f}ms {r['avg_cache']:>8.2f}ms "
              f"{r['overall_speedup']:>7.2f}x "
              f"{r['slowdown_ratio']:>8.2f}x {r['end_speedup']:>7.2f}x")

    print(f"\n  Key insight:")
    if len(results) >= 2:
        print(f"    Smallest model ({results[0]['name']}): "
              f"{results[0]['overall_speedup']:.1f}x overall, "
              f"{results[0]['end_speedup']:.1f}x at end")
        print(f"    Largest model  ({results[-1]['name']}): "
              f"{results[-1]['overall_speedup']:.1f}x overall, "
              f"{results[-1]['end_speedup']:.1f}x at end")
        print(f"    → KV cache advantage grows with model size AND sequence length.")

    # Save outputs
    save_csv(results)
    plot_ablation(results)


if __name__ == "__main__":
    main()
