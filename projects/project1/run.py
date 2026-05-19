"""
Project 1: Entry Point
-----------------------
Ties all components together. Run this to execute the full pipeline:
    1. Train tokenizer (if not already trained)
    2. Tokenize corpus and build data loaders
    3. Initialize model
    4. Train (or resume from checkpoint)
    5. Generate samples
    6. Save results

Usage:
    python run.py                    # Full pipeline from scratch
    python run.py --resume ckpt.pt   # Resume from checkpoint
    python run.py --generate-only    # Load trained model and generate
"""

import argparse
import json
import sys
from pathlib import Path

import torch

from config import ModelConfig, TrainConfig


def main():
    parser = argparse.ArgumentParser(description="Project 1: Train a MiniGPT")
    parser.add_argument("--resume", type=str, default=None, help="Path to checkpoint")
    parser.add_argument("--generate-only", action="store_true", help="Skip training")
    parser.add_argument("--smoke-test", action="store_true",
                        help="Quick run: 100 steps, small batch, to verify pipeline")
    args = parser.parse_args()

    # ---- Configuration ----
    model_cfg = ModelConfig()
    train_cfg = TrainConfig()

    if args.smoke_test:
        train_cfg.max_steps = 100
        train_cfg.eval_interval = 25
        train_cfg.save_interval = 50
        train_cfg.batch_size = 8
        print("=== SMOKE TEST MODE ===")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")

    # ---- Create directories ----
    for d in ["tokenizer", "checkpoints", "figures", "results"]:
        Path(d).mkdir(exist_ok=True)

    from tokenizer import train_bpe, load_tokenizer, analyze_tokenizer
    from data import tokenize_corpus, create_dataloaders
    from model import MiniGPT
    from train import train as train_model
    from generate import generate, generate_samples
    from evaluate import plot_loss_curves, compute_bits_per_byte

    # ---- Step 1: Tokenizer ----
    tok_path = Path(train_cfg.tokenizer_path)
    if not tok_path.exists():
        print(f"\n=== Step 1: Training BPE tokenizer (vocab={model_cfg.vocab_size}) ===")
        train_bpe(train_cfg.corpus_path, model_cfg.vocab_size, str(tok_path))
    else:
        print(f"\n=== Step 1: Loading existing tokenizer from {tok_path} ===")
    tok = load_tokenizer(str(tok_path))
    stats = analyze_tokenizer(tok, train_cfg.corpus_path)
    bytes_per_token = stats["bytes_per_token"]
    print(f"Tokenizer: vocab={tok.get_vocab_size()}, bytes/token={bytes_per_token:.2f}")

    # ---- Step 2: Data pipeline ----
    print(f"\n=== Step 2: Building data pipeline ===")
    eos_id = tok.token_to_id("<eos>")
    token_ids = tokenize_corpus(train_cfg.corpus_path, tok, eos_id=eos_id)
    train_loader, val_loader = create_dataloaders(
        token_ids, model_cfg.context_length, train_cfg.batch_size, train_cfg.val_fraction
    )
    print(f"Train batches: {len(train_loader)}, Val batches: {len(val_loader)}")

    # ---- Step 3: Model ----
    print(f"\n=== Step 3: Initializing model ===")
    model = MiniGPT(model_cfg).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"Model: {n_params:,} parameters")

    # ---- Step 4: Train (or resume) ----
    if not args.generate_only:
        print(f"\n=== Step 4: Training ({train_cfg.max_steps} steps) ===")
        log = train_model(model, train_loader, val_loader, train_cfg, device, args.resume)

        # Plot loss curves
        plot_loss_curves(log, "figures/loss_curves.png")

        # Compute final bits-per-byte
        final_val = log[-1]["val_loss"]
        bpb = compute_bits_per_byte(final_val, bytes_per_token)
        print(f"\nFinal val loss: {final_val:.4f}")
        print(f"Bits-per-byte: {bpb:.4f}")
    else:
        # Load latest checkpoint for generation
        ckpts = sorted(Path(train_cfg.checkpoint_dir).glob("step_*.pt"))
        if not ckpts:
            print("No checkpoints found! Train first.")
            sys.exit(1)
        ckpt = torch.load(ckpts[-1], map_location=device, weights_only=False)
        model.load_state_dict(ckpt["model"])
        log = ckpt.get("train_log", [])
        print(f"Loaded checkpoint: {ckpts[-1]} (step {ckpt.get('step', '?')})")

    # ---- Step 5: Generate samples ----
    print(f"\n=== Step 5: Generating samples ===")
    prompts = [
        "The ",
        "In the beginning ",
        "She looked at him and ",
        "It was a dark and ",
    ]
    samples = generate_samples(
        model, tok, prompts,
        temperatures=[0.5, 0.8, 1.2],
        max_tokens=train_cfg.gen_max_tokens,
        device=device,
    )

    # Save samples
    results_path = Path("results/samples.json")
    results_path.parent.mkdir(parents=True, exist_ok=True)
    with open(results_path, "w") as f:
        json.dump(samples, f, indent=2, ensure_ascii=False)
    print(f"Samples saved to {results_path}")

    # Print a few samples
    for s in samples[:6]:
        print(f"\n--- Prompt: {s['prompt']!r}, T={s['temperature']} ---")
        print(s["generated"][:300])

    print(f"\n=== Done! ===")


if __name__ == "__main__":
    main()
