"""
Project 1: Unified Ablation Runner
------------------------------------
Runs all ablation experiments with consistent logging, wandb tracking,
and result collection.

Core Ablations:
    1. Vocab size sweep (char / 500 / 2000 / 8000)
    2. Depth vs width at fixed ~3.7M params
    3. Context length sweep (64 / 128 / 256 / 512)
    4. Learning rate sweep (1e-5 / 1e-4 / 3e-4 / 1e-3 / 3e-3)
"""

import json
import os
import sys
import copy
import math
import time
from pathlib import Path
from dataclasses import dataclass, asdict, replace

import torch

from config import ModelConfig, TrainConfig
from tokenizer import train_bpe, load_tokenizer, encode, analyze_tokenizer
from model import MiniGPT
from data import tokenize_corpus, create_dataloaders
from train import train as train_model
from evaluate import compute_bits_per_byte, plot_loss_curves, plot_ablation
from generate import generate


# ---------------------------------------------------------------------------
# Ablation result collection
# ---------------------------------------------------------------------------
@dataclass
class AblationResult:
    name: str
    config_desc: str
    params: int
    final_train_loss: float
    final_val_loss: float
    bits_per_byte: float
    bytes_per_token: float
    total_tokens: int
    wall_time_sec: float
    train_log: list


def summarize_result(r: AblationResult) -> dict:
    return {
        "name": r.name,
        "config_desc": r.config_desc,
        "params": r.params,
        "final_train_loss": r.final_train_loss,
        "final_val_loss": r.final_val_loss,
        "bits_per_byte": r.bits_per_byte,
        "bytes_per_token": r.bytes_per_token,
        "total_tokens": r.total_tokens,
        "wall_time_sec": r.wall_time_sec,
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _ensure_tokenizer(corpus_path: str, vocab_size: int, tok_dir: str) -> tuple:
    """Train or load a tokenizer for the given vocab size. Returns (tokenizer, bytes_per_token)."""
    tok_path = os.path.join(tok_dir, f"bpe_v{vocab_size}.json")
    if not os.path.exists(tok_path):
        print(f"\n--- Training tokenizer V={vocab_size} ---")
        train_bpe(corpus_path, vocab_size, tok_path)
    tok = load_tokenizer(tok_path)

    # Compute bytes_per_token
    text = Path(corpus_path).read_text()
    total_bytes = len(text.encode("utf-8"))
    total_tokens = len(tok.encode(text).ids)
    bpt = total_bytes / total_tokens
    return tok, bpt


def _run_single(
    name: str,
    config_desc: str,
    model_cfg: ModelConfig,
    train_cfg: TrainConfig,
    corpus_path: str,
    tokenizer,
    bytes_per_token: float,
    device: str = "cuda",
) -> AblationResult:
    """Run a single training experiment and return the result."""
    print(f"\n{'='*60}")
    print(f"ABLATION: {name}")
    print(f"Config:   {config_desc}")
    print(f"{'='*60}")

    # Get EOS token id
    eos_id = tokenizer.token_to_id("<eos>")

    # Tokenize corpus
    token_ids = tokenize_corpus(corpus_path, tokenizer, eos_id)
    total_tokens = len(token_ids)
    print(f"Total tokens: {total_tokens:,}, bytes/token: {bytes_per_token:.2f}")

    # Create dataloaders
    train_loader, val_loader = create_dataloaders(
        token_ids,
        context_length=model_cfg.context_length,
        batch_size=train_cfg.batch_size,
        val_fraction=train_cfg.val_fraction,
    )
    print(f"Train batches: {len(train_loader)}, Val batches: {len(val_loader)}")

    # Build model
    model = MiniGPT(model_cfg)
    n_params = model.count_parameters()
    print(f"Parameters: {n_params:,}")

    # Train
    t0 = time.time()
    train_log = train_model(model, train_loader, val_loader, train_cfg, device=device)
    wall_time = time.time() - t0

    # Final metrics
    final = train_log[-1] if train_log else {}
    final_val = final.get("val_loss", float("inf"))
    final_train = final.get("train_loss", float("inf"))
    bpb = compute_bits_per_byte(final_val, bytes_per_token)

    # Generate sample
    model.eval()
    with torch.no_grad():
        sample = generate(model, tokenizer, "The ", max_tokens=100, temperature=0.8,
                          top_k=40, device=device)
    print(f"\nSample (T=0.8): {sample[:200]}")

    result = AblationResult(
        name=name,
        config_desc=config_desc,
        params=n_params,
        final_train_loss=final_train,
        final_val_loss=final_val,
        bits_per_byte=bpb,
        bytes_per_token=bytes_per_token,
        total_tokens=total_tokens,
        wall_time_sec=wall_time,
        train_log=train_log,
    )
    print(f"\n  Final val loss: {final_val:.4f}")
    print(f"  Bits-per-byte:  {bpb:.3f}")
    print(f"  Wall time:      {wall_time:.1f}s")
    return result


# ---------------------------------------------------------------------------
# Ablation 1: Vocab Size Sweep
# ---------------------------------------------------------------------------
def run_vocab_sweep(corpus_path: str, device: str = "cuda") -> list[AblationResult]:
    """Sweep vocab sizes: char(65), 500, 2000, 8000."""
    tok_dir = "tokenizer"
    os.makedirs(tok_dir, exist_ok=True)
    results_dir = Path("results/abl1_vocab")
    results_dir.mkdir(parents=True, exist_ok=True)

    # Char-level tokenizer: we use vocab=65 but BPE with min_frequency=1
    # won't produce char-level. Instead, build a simple char tokenizer.
    configs = [
        # (name, vocab_size, desc)
        ("char_v65", 65, "char-level V=65"),
        ("bpe_v500", 500, "BPE V=500"),
        ("bpe_v2000", 2000, "BPE V=2000 (baseline)"),
        ("bpe_v8000", 8000, "BPE V=8000"),
    ]

    results = []
    for name, vocab_size, desc in configs:
        tok, bpt = _ensure_tokenizer(corpus_path, vocab_size, tok_dir)
        actual_vocab = tok.get_vocab_size()

        model_cfg = ModelConfig(
            vocab_size=actual_vocab,
            context_length=256,
            d_model=256, n_heads=4, n_layers=4, d_ff=1024,
            dropout=0.1, pos_encoding="learned",
        )
        train_cfg = TrainConfig(
            corpus_path=corpus_path,
            tokenizer_path=os.path.join(tok_dir, f"bpe_v{vocab_size}.json"),
            max_steps=10_000,
            eval_interval=200,
            batch_size=32,
            lr=3e-4, min_lr=3e-5,
            warmup_steps=200,
            checkpoint_dir=str(results_dir / name / "checkpoints"),
            save_interval=5000,
            use_wandb=True,
            wandb_project="capstone-project1-minigpt",
            wandb_run_name=f"abl1_vocab_{name}",
            gen_interval=5000,
            seed=42,
        )

        r = _run_single(name, desc, model_cfg, train_cfg, corpus_path, tok, bpt, device)
        results.append(r)

        # Save individual log
        log_path = results_dir / name / "train_log.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "w") as f:
            json.dump(r.train_log, f, indent=2)

    # Save summary
    summary = [summarize_result(r) for r in results]
    with open(results_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Plot comparison
    plot_data = {r.name: r.train_log for r in results}
    plot_ablation(plot_data, metric="val_loss",
                  save_path=str(results_dir / "vocab_val_loss.png"))

    # Bits-per-byte bar chart
    _plot_bpb_bar(results, str(results_dir / "vocab_bits_per_byte.png"),
                  "Ablation 1: Vocab Size — Bits-per-Byte")

    print(f"\n{'='*60}")
    print("ABLATION 1: VOCAB SWEEP COMPLETE")
    print(f"{'='*60}")
    for r in results:
        print(f"  {r.name:15s}  val={r.final_val_loss:.4f}  bpb={r.bits_per_byte:.3f}  "
              f"bpt={r.bytes_per_token:.2f}  params={r.params:,}")
    return results


# ---------------------------------------------------------------------------
# Ablation 2: Depth vs Width (fixed ~3.7M params)
# ---------------------------------------------------------------------------
def run_depth_width(corpus_path: str, device: str = "cuda") -> list[AblationResult]:
    """Sweep depth/width at roughly fixed parameter count."""
    tok_dir = "tokenizer"
    tok, bpt = _ensure_tokenizer(corpus_path, 2000, tok_dir)
    actual_vocab = tok.get_vocab_size()

    results_dir = Path("results/abl2_depth_width")
    results_dir.mkdir(parents=True, exist_ok=True)

    # Configs designed for ~3.7M params each
    configs = [
        # (name, n_layers, d_model, d_ff, desc)
        ("deep_narrow",  8, 192, 768,  "8 layers, d=192 (~3.5M)"),
        ("baseline",     4, 256, 1024, "4 layers, d=256 (~3.7M)"),
        ("shallow_wide", 2, 384, 1536, "2 layers, d=384 (~3.8M)"),
    ]

    results = []
    for name, n_layers, d_model, d_ff, desc in configs:
        model_cfg = ModelConfig(
            vocab_size=actual_vocab,
            context_length=256,
            d_model=d_model, n_heads=4, n_layers=n_layers, d_ff=d_ff,
            dropout=0.1, pos_encoding="learned",
        )
        train_cfg = TrainConfig(
            corpus_path=corpus_path,
            tokenizer_path=os.path.join(tok_dir, "bpe_v2000.json"),
            max_steps=10_000,
            eval_interval=200,
            batch_size=32,
            lr=3e-4, min_lr=3e-5,
            warmup_steps=200,
            checkpoint_dir=str(results_dir / name / "checkpoints"),
            save_interval=5000,
            use_wandb=True,
            wandb_project="capstone-project1-minigpt",
            wandb_run_name=f"abl2_dw_{name}",
            gen_interval=5000,
            seed=42,
        )

        r = _run_single(name, desc, model_cfg, train_cfg, corpus_path, tok, bpt, device)
        results.append(r)

        log_path = results_dir / name / "train_log.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "w") as f:
            json.dump(r.train_log, f, indent=2)

    summary = [summarize_result(r) for r in results]
    with open(results_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    plot_data = {r.name: r.train_log for r in results}
    plot_ablation(plot_data, metric="val_loss",
                  save_path=str(results_dir / "depth_width_val_loss.png"))

    print(f"\n{'='*60}")
    print("ABLATION 2: DEPTH VS WIDTH COMPLETE")
    print(f"{'='*60}")
    for r in results:
        print(f"  {r.name:15s}  val={r.final_val_loss:.4f}  bpb={r.bits_per_byte:.3f}  "
              f"params={r.params:,}")
    return results


# ---------------------------------------------------------------------------
# Ablation 3: Context Length Sweep
# ---------------------------------------------------------------------------
def run_context_sweep(corpus_path: str, device: str = "cuda") -> list[AblationResult]:
    """Sweep context lengths: 64, 128, 256, 512."""
    tok_dir = "tokenizer"
    tok, bpt = _ensure_tokenizer(corpus_path, 2000, tok_dir)
    actual_vocab = tok.get_vocab_size()

    results_dir = Path("results/abl3_context")
    results_dir.mkdir(parents=True, exist_ok=True)

    ctx_lengths = [64, 128, 256, 512]

    results = []
    for ctx in ctx_lengths:
        name = f"ctx_{ctx}"
        desc = f"context_length={ctx}"

        model_cfg = ModelConfig(
            vocab_size=actual_vocab,
            context_length=ctx,
            d_model=256, n_heads=4, n_layers=4, d_ff=1024,
            dropout=0.1, pos_encoding="learned",
        )
        train_cfg = TrainConfig(
            corpus_path=corpus_path,
            tokenizer_path=os.path.join(tok_dir, "bpe_v2000.json"),
            max_steps=10_000,
            eval_interval=200,
            batch_size=32,
            lr=3e-4, min_lr=3e-5,
            warmup_steps=200,
            checkpoint_dir=str(results_dir / name / "checkpoints"),
            save_interval=5000,
            use_wandb=True,
            wandb_project="capstone-project1-minigpt",
            wandb_run_name=f"abl3_ctx_{ctx}",
            gen_interval=5000,
            seed=42,
        )

        r = _run_single(name, desc, model_cfg, train_cfg, corpus_path, tok, bpt, device)
        results.append(r)

        log_path = results_dir / name / "train_log.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "w") as f:
            json.dump(r.train_log, f, indent=2)

    summary = [summarize_result(r) for r in results]
    with open(results_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    plot_data = {r.name: r.train_log for r in results}
    plot_ablation(plot_data, metric="val_loss",
                  save_path=str(results_dir / "context_val_loss.png"))

    print(f"\n{'='*60}")
    print("ABLATION 3: CONTEXT LENGTH COMPLETE")
    print(f"{'='*60}")
    for r in results:
        print(f"  {r.name:15s}  val={r.final_val_loss:.4f}  bpb={r.bits_per_byte:.3f}  "
              f"params={r.params:,}")
    return results


# ---------------------------------------------------------------------------
# Ablation 4: Learning Rate Sweep
# ---------------------------------------------------------------------------
def run_lr_sweep(corpus_path: str, device: str = "cuda") -> list[AblationResult]:
    """Sweep peak learning rates: 1e-5, 1e-4, 3e-4, 1e-3, 3e-3."""
    tok_dir = "tokenizer"
    tok, bpt = _ensure_tokenizer(corpus_path, 2000, tok_dir)
    actual_vocab = tok.get_vocab_size()

    results_dir = Path("results/abl4_lr")
    results_dir.mkdir(parents=True, exist_ok=True)

    lrs = [1e-5, 1e-4, 3e-4, 1e-3, 3e-3]

    results = []
    for lr_val in lrs:
        name = f"lr_{lr_val:.0e}".replace("+", "")
        desc = f"peak_lr={lr_val}"

        model_cfg = ModelConfig(
            vocab_size=actual_vocab,
            context_length=256,
            d_model=256, n_heads=4, n_layers=4, d_ff=1024,
            dropout=0.1, pos_encoding="learned",
        )
        train_cfg = TrainConfig(
            corpus_path=corpus_path,
            tokenizer_path=os.path.join(tok_dir, "bpe_v2000.json"),
            max_steps=10_000,
            eval_interval=200,
            batch_size=32,
            lr=lr_val,
            min_lr=lr_val * 0.1,  # min_lr = 10% of peak
            warmup_steps=200,
            checkpoint_dir=str(results_dir / name / "checkpoints"),
            save_interval=5000,
            use_wandb=True,
            wandb_project="capstone-project1-minigpt",
            wandb_run_name=f"abl4_lr_{name}",
            gen_interval=5000,
            seed=42,
        )

        try:
            r = _run_single(name, desc, model_cfg, train_cfg, corpus_path, tok, bpt, device)
        except FloatingPointError as e:
            print(f"\n  !!! {name} diverged: {e}")
            r = AblationResult(
                name=name, config_desc=desc, params=0,
                final_train_loss=float("inf"), final_val_loss=float("inf"),
                bits_per_byte=float("inf"), bytes_per_token=bpt,
                total_tokens=0, wall_time_sec=0.0, train_log=[],
            )
        results.append(r)

        if r.train_log:
            log_path = results_dir / name / "train_log.json"
            log_path.parent.mkdir(parents=True, exist_ok=True)
            with open(log_path, "w") as f:
                json.dump(r.train_log, f, indent=2)

    summary = [summarize_result(r) for r in results]
    with open(results_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    # Plot only runs that didn't diverge
    plot_data = {r.name: r.train_log for r in results if r.train_log}
    if plot_data:
        plot_ablation(plot_data, metric="val_loss",
                      save_path=str(results_dir / "lr_val_loss.png"))

    print(f"\n{'='*60}")
    print("ABLATION 4: LR SWEEP COMPLETE")
    print(f"{'='*60}")
    for r in results:
        vl = f"{r.final_val_loss:.4f}" if r.final_val_loss < float("inf") else "DIVERGED"
        print(f"  {r.name:15s}  val={vl}  bpb={r.bits_per_byte:.3f}")
    return results


# ---------------------------------------------------------------------------
# Bits-per-byte bar chart helper
# ---------------------------------------------------------------------------
def _plot_bpb_bar(results: list[AblationResult], save_path: str, title: str):
    import matplotlib.pyplot as plt
    names = [r.name for r in results]
    bpbs = [r.bits_per_byte for r in results]
    raw_losses = [r.final_val_loss for r in results]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Raw loss
    bars1 = ax1.bar(names, raw_losses, color="#2D8CFF", alpha=0.8)
    ax1.set_ylabel("Raw Val Loss (CE)")
    ax1.set_title("Raw Per-Token Loss")
    ax1.tick_params(axis='x', rotation=30)
    for bar, val in zip(bars1, raw_losses):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                 f"{val:.2f}", ha='center', va='bottom', fontsize=9)

    # Bits-per-byte
    bars2 = ax2.bar(names, bpbs, color="#1A6FD1", alpha=0.8)
    ax2.set_ylabel("Bits per Byte")
    ax2.set_title("Normalized: Bits-per-Byte")
    ax2.tick_params(axis='x', rotation=30)
    for bar, val in zip(bars2, bpbs):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                 f"{val:.2f}", ha='center', va='bottom', fontsize=9)

    fig.suptitle(title, fontsize=13, fontweight='bold')
    plt.tight_layout()
    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"BPB bar chart saved to {save_path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--ablation", type=int, choices=[1,2,3,4],
                        help="Which ablation to run (1=vocab, 2=depth/width, 3=context, 4=lr)")
    parser.add_argument("--corpus", type=str, default="data/corpus.txt")
    parser.add_argument("--all", action="store_true", help="Run all ablations")
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")
    if device == "cuda":
        print(f"GPU: {torch.cuda.get_device_name()}")

    if args.all or args.ablation == 1:
        run_vocab_sweep(args.corpus, device)
    if args.all or args.ablation == 2:
        run_depth_width(args.corpus, device)
    if args.all or args.ablation == 3:
        run_context_sweep(args.corpus, device)
    if args.all or args.ablation == 4:
        run_lr_sweep(args.corpus, device)

    print("\nDone.")
