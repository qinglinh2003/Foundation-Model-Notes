"""
Experiment 4: Seq2Seq Bottleneck and Attention
===============================================
Train Seq2Seq (with and without attention) on a sequence reversal task.
Compare accuracy vs. input length to demonstrate the bottleneck effect.

Usage:
    python exp4_seq2seq.py --device cuda
"""

import argparse, os, json
import torch
import torch.nn as nn
import numpy as np
from torch.utils.data import DataLoader

from data import ReversalData, collate_reversal
from model import Seq2Seq
from utils import plot_seq2seq_accuracy, plot_attention_heatmap


LENGTHS = [10, 30, 50, 100]


def train_seq2seq(seq_len: int, use_attention: bool, device: str,
                  num_epochs: int = 100, patience: int = 15):
    """
    Train a Seq2Seq model on the reversal task for a given input length.
    Returns (test_accuracy, model, test_loader).
    """
    # Data
    train_data = ReversalData(10000, seq_len)
    test_data = ReversalData(1000, seq_len)

    train_loader = DataLoader(train_data, batch_size=64, shuffle=True,
                              collate_fn=collate_reversal)
    test_loader = DataLoader(test_data, batch_size=256,
                             collate_fn=collate_reversal)

    # Model
    model = Seq2Seq(
        src_vocab_size=ReversalData.VOCAB_SIZE,
        tgt_vocab_size=ReversalData.VOCAB_SIZE,
        embed_dim=64,
        hidden_size=128,
        use_attention=use_attention,
    ).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss(ignore_index=ReversalData.PAD)

    best_acc = 0.0
    no_improve = 0

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0.0
        for src, dec_in, dec_tgt in train_loader:
            src, dec_in, dec_tgt = (src.to(device), dec_in.to(device),
                                    dec_tgt.to(device))
            logits, _ = model(src, dec_in)
            loss = criterion(logits.reshape(-1, logits.size(-1)),
                             dec_tgt.reshape(-1))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_loss = total_loss / len(train_loader)

        # Evaluate with greedy decoding every 5 epochs
        if (epoch + 1) % 5 == 0 or epoch == 0:
            acc = evaluate_exact_match(model, test_loader, device)
            print(f"    epoch {epoch+1:3d} | loss {avg_loss:.4f} | exact_match {acc:.4f}")

            if acc >= 0.99:
                best_acc = acc
                break

            if acc > best_acc:
                best_acc = acc
                no_improve = 0
            else:
                no_improve += 5
                if no_improve >= patience:
                    print(f"    Early stop at epoch {epoch+1}")
                    break

    # Final eval
    final_acc = evaluate_exact_match(model, test_loader, device)
    best_acc = max(best_acc, final_acc)
    return best_acc, model, test_loader


@torch.no_grad()
def evaluate_exact_match(model, test_loader, device):
    """Compute exact sequence match accuracy with greedy decoding."""
    model.eval()
    correct = 0
    total = 0
    for src, dec_in, dec_tgt in test_loader:
        src, dec_in, dec_tgt = (src.to(device), dec_in.to(device),
                                dec_tgt.to(device))
        preds, _ = model.greedy_decode(
            src, sos_idx=ReversalData.SOS, max_len=dec_tgt.size(1)
        )

        # Compare only non-PAD positions
        mask = dec_tgt != ReversalData.PAD
        match = ((preds == dec_tgt) | ~mask).all(dim=-1)
        correct += match.sum().item()
        total += src.size(0)

    return correct / max(total, 1)


@torch.no_grad()
def extract_attention_map(model, test_loader, device, example_idx: int = 0):
    """
    Extract attention weights for a single test example.
    Returns (weights, src_tokens, tgt_tokens).
    """
    model.eval()
    for src, dec_in, dec_tgt in test_loader:
        src, dec_in, dec_tgt = (src.to(device), dec_in.to(device),
                                dec_tgt.to(device))
        _, attn_weights = model.greedy_decode(
            src, sos_idx=ReversalData.SOS, max_len=dec_in.size(1)
        )

        if attn_weights is None:
            return None, None, None

        # Take one example
        w = attn_weights[example_idx].cpu().numpy()  # (tgt_len, src_len)

        # Create token labels
        src_tokens = [chr(ord('a') + t.item()) if t.item() < 26
                      else ["SOS", "EOS", "PAD"][t.item() - 26]
                      for t in src[example_idx]]
        tgt_tokens = [chr(ord('a') + t.item()) if t.item() < 26
                      else ["SOS", "EOS", "PAD"][t.item() - 26]
                      for t in dec_tgt[example_idx]]
        return w, src_tokens, tgt_tokens


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", type=str, default="cuda"
                        if torch.cuda.is_available() else "cpu")
    parser.add_argument("--num_epochs", type=int, default=100)
    parser.add_argument("--fig_dir", type=str, default="answers/figures")
    parser.add_argument("--results_path", type=str,
                        default="answers/results/seq2seq_results.json")
    args = parser.parse_args()

    results = {"no_attention": {}, "with_attention": {}}
    attention_model = None
    attention_test_loader = None

    for use_attn in [False, True]:
        name = "with_attention" if use_attn else "no_attention"
        print(f"\n{'='*60}")
        print(f"Training: {name.replace('_', ' ').upper()}")
        print(f"{'='*60}")

        for seq_len in LENGTHS:
            print(f"\n  Sequence length = {seq_len}")
            acc, model, test_loader = train_seq2seq(
                seq_len, use_attn, args.device, num_epochs=args.num_epochs
            )
            results[name][seq_len] = acc
            print(f"  → Exact match accuracy: {acc:.4f}")

            # Save attention model at L=30 for heatmap
            if use_attn and seq_len == 30:
                attention_model = model
                attention_test_loader = test_loader

    # Save results
    os.makedirs(os.path.dirname(args.results_path) or ".", exist_ok=True)
    with open(args.results_path, "w") as f:
        json.dump(results, f, indent=2)

    # Plot accuracy vs. length
    os.makedirs(args.fig_dir, exist_ok=True)
    plot_results = {
        name: {int(k): v for k, v in d.items()}
        for name, d in results.items()
    }
    plot_seq2seq_accuracy(
        plot_results,
        save_path=os.path.join(args.fig_dir, "accuracy_vs_length.png")
    )

    # Attention heatmap
    if attention_model is not None:
        weights, src_tok, tgt_tok = extract_attention_map(
            attention_model, attention_test_loader, args.device
        )
        if weights is not None:
            plot_attention_heatmap(
                weights, src_tok, tgt_tok,
                save_path=os.path.join(args.fig_dir, "attention_heatmap.png")
            )

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY: Exact Match Accuracy vs. Input Length")
    print("=" * 60)
    print(f"  {'Model':<20}", end="")
    for l in LENGTHS:
        print(f"  {'L='+str(l):<10}", end="")
    print()
    print(f"  {'-'*60}")
    for name in ["no_attention", "with_attention"]:
        label = name.replace("_", " ").title()
        print(f"  {label:<20}", end="")
        for l in LENGTHS:
            acc = results[name].get(l, results[name].get(str(l), 0))
            print(f"  {acc:<10.4f}", end="")
        print()

    # ---------------------------------------------------------------
    # TODO: YOUR CODE HERE
    # Print a brief interpretation:
    # 1. At what length does the no-attention model start failing?
    # 2. Does attention maintain accuracy at L=100?
    # 3. Does the attention heatmap show an anti-diagonal pattern?
    #    What does this mean for the reversal task?
    # 4. How does this relate to §1.5 (Seq2Seq bottleneck)?
    # ---------------------------------------------------------------
    print("\n  [Write your interpretation here]")


if __name__ == "__main__":
    main()
