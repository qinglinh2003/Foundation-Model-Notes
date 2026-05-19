"""
Experiment 2: Long-Range Dependency Probe
==========================================
Train RNN/LSTM/GRU on a synthetic delayed-memory task at varying
dependency distances: 8, 32, 128, 256.

Usage:
    python exp2_distance.py --device cuda
"""

import argparse, os, json
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from data import DelayedMemoryData, collate_delayed_memory
from model import DelayedMemoryClassifier
from utils import plot_distance_probe


DISTANCES = [8, 32, 128, 256]
CONTENT_VOCAB = 10


def train_probe(rnn_type: str, distance: int, device: str,
                num_epochs: int = 50, patience: int = 10):
    """
    Train a single probe model for one (rnn_type, distance) pair.
    Returns test accuracy.
    """
    # Data
    train_data = DelayedMemoryData(10000, distance, vocab_size=CONTENT_VOCAB)
    test_data = DelayedMemoryData(1000, distance, vocab_size=CONTENT_VOCAB)

    train_loader = DataLoader(train_data, batch_size=64, shuffle=True,
                              collate_fn=collate_delayed_memory)
    test_loader = DataLoader(test_data, batch_size=256,
                             collate_fn=collate_delayed_memory)

    # Model
    model = DelayedMemoryClassifier(
        vocab_size=train_data.total_vocab,
        embed_dim=32,
        hidden_size=128,
        num_classes=CONTENT_VOCAB,
        rnn_type=rnn_type,
    ).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    best_acc = 0.0
    no_improve = 0

    for epoch in range(num_epochs):
        model.train()
        total_loss = 0.0
        for x, y in train_loader:
            x, y = x.to(device), y.to(device)
            logits = model(x)
            loss = criterion(logits, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        avg_loss = total_loss / len(train_loader)
        acc = evaluate_probe(model, test_loader, device)

        if (epoch + 1) % 10 == 0 or acc >= 0.99:
            print(f"    epoch {epoch+1:3d} | loss {avg_loss:.4f} | acc {acc:.4f}")

        if acc >= 0.99:
            best_acc = acc
            break

        if acc > best_acc:
            best_acc = acc
            no_improve = 0
        else:
            no_improve += 1
            if no_improve >= patience:
                print(f"    Early stop at epoch {epoch+1}")
                break

    return best_acc


def evaluate_probe(model, test_loader, device):
    """Compute accuracy on test set."""
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for x, y in test_loader:
            x, y = x.to(device), y.to(device)
            logits = model(x)
            preds = logits.argmax(dim=-1)
            correct += (preds == y).sum().item()
            total += y.size(0)
    return correct / max(total, 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", type=str, default="cuda"
                        if torch.cuda.is_available() else "cpu")
    parser.add_argument("--num_epochs", type=int, default=50)
    parser.add_argument("--fig_dir", type=str, default="answers/figures")
    parser.add_argument("--results_path", type=str,
                        default="answers/results/distance_probe.json")
    args = parser.parse_args()

    rnn_types = ["rnn", "lstm", "gru"]
    results = {}

    for rnn_type in rnn_types:
        results[rnn_type] = {}
        print(f"\n{'='*50}")
        print(f"Model: {rnn_type.upper()}")
        print(f"{'='*50}")

        for dist in DISTANCES:
            print(f"\n  Distance = {dist}")
            acc = train_probe(rnn_type, dist, args.device, args.num_epochs)
            results[rnn_type][dist] = acc
            print(f"  → Final accuracy: {acc:.4f}")

    # Save results
    os.makedirs(os.path.dirname(args.results_path) or ".", exist_ok=True)
    with open(args.results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {args.results_path}")

    # Plot
    os.makedirs(args.fig_dir, exist_ok=True)
    # Convert string keys to int for plotting
    plot_results = {
        name: {int(k): v for k, v in d.items()}
        for name, d in results.items()
    }
    plot_distance_probe(
        plot_results,
        save_path=os.path.join(args.fig_dir, "distance_probe.png")
    )

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY: Accuracy vs. Dependency Distance")
    print("=" * 60)
    print(f"  {'Model':<8}", end="")
    for d in DISTANCES:
        print(f"  {'N='+str(d):<10}", end="")
    print()
    print(f"  {'-'*50}")
    for rnn_type in rnn_types:
        print(f"  {rnn_type.upper():<8}", end="")
        for d in DISTANCES:
            acc = results[rnn_type][d]
            print(f"  {acc:<10.4f}", end="")
        print()


if __name__ == "__main__":
    main()
