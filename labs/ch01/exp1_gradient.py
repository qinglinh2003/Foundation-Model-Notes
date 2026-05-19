"""
Experiment 1: Gradient Pathology
=================================
Compare gradient norm behavior across RNN, LSTM, and GRU.

Runs two configurations:
  - Normal:  seq_len=128, lr=1e-3, grad clipping ON
  - Stress:  seq_len=256, lr=3e-3, grad clipping OFF, 500 steps only

Usage:
    python exp1_gradient.py --data_path tiny_shakespeare.txt --device cuda
"""

import argparse, os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from data import load_char_data
from model import CharLM
from utils import (MetricLogger, compute_gradient_norm,
                   train_one_epoch_charlm, evaluate_charlm,
                   generate_charlm, plot_gradient_norms)


def run_normal(rnn_type: str, train_ds, val_ds, device: str,
               num_epochs: int = 10, log_dir: str = "logs"):
    """Train a CharLM with standard hyperparameters."""
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{rnn_type}_normal.csv")
    logger = MetricLogger(log_path, ["step", "loss", "grad_norm"])

    model = CharLM(
        vocab_size=train_ds.vocab_size,
        embed_dim=64,
        hidden_size=256,
        rnn_type=rnn_type,
    ).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    train_loader = DataLoader(train_ds, batch_size=64, shuffle=False, drop_last=True)
    val_loader = DataLoader(val_ds, batch_size=64, shuffle=False, drop_last=True)

    print(f"\n{'='*50}")
    print(f"Normal run: {rnn_type.upper()}")
    print(f"Parameters: {model.count_parameters():,}")
    print(f"{'='*50}")

    global_step = 0
    for epoch in range(num_epochs):
        avg_loss, global_step = train_one_epoch_charlm(
            model, train_loader, optimizer, device,
            clip_norm=5.0, logger=logger, global_step=global_step
        )
        val_loss, val_ppl = evaluate_charlm(model, val_loader, device)
        print(f"  Epoch {epoch+1:2d} | train loss {avg_loss:.4f} "
              f"| val loss {val_loss:.4f} | val PPL {val_ppl:.2f}")

    logger.close()
    return model, log_path


def run_stress(rnn_type: str, train_ds, device: str,
               max_steps: int = 500, log_dir: str = "logs"):
    """
    Stress test: high LR, long sequences, NO gradient clipping.
    Goal: expose gradient instability in vanilla RNN.
    """
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{rnn_type}_stress.csv")
    logger = MetricLogger(log_path, ["step", "loss", "grad_norm"])

    # Build a dataset with seq_len=256 reusing the same text/vocab
    from data import CharDataset
    raw_text = "".join(train_ds.chars[i] for i in train_ds.data.tolist())
    stress_ds = CharDataset(raw_text, seq_len=256, chars=train_ds.chars)
    stress_loader = DataLoader(stress_ds, batch_size=64, shuffle=False, drop_last=True)

    model = CharLM(
        vocab_size=train_ds.vocab_size,
        embed_dim=64,
        hidden_size=256,
        rnn_type=rnn_type,
    ).to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=3e-3)
    criterion = nn.CrossEntropyLoss()

    print(f"\n{'='*50}")
    print(f"Stress run: {rnn_type.upper()} (no clipping, lr=3e-3, seq=256)")
    print(f"{'='*50}")

    model.train()
    hidden = None
    step = 0
    data_iter = iter(stress_loader)

    while step < max_steps:
        try:
            x, y = next(data_iter)
        except StopIteration:
            data_iter = iter(stress_loader)
            x, y = next(data_iter)
            hidden = None

        x, y = x.to(device), y.to(device)
        logits, hidden = model(x, hidden)
        loss = criterion(logits.reshape(-1, logits.size(-1)), y.reshape(-1))

        optimizer.zero_grad()
        loss.backward()

        grad_norm = compute_gradient_norm(model)
        # NO clipping
        optimizer.step()

        step += 1
        loss_val = loss.item()
        logger.log(step=step, loss=loss_val, grad_norm=grad_norm)

        if step % 100 == 0 or loss_val != loss_val:
            print(f"  step {step:4d} | loss {loss_val:.4f} | grad_norm {grad_norm:.2f}")

        if loss_val != loss_val:  # NaN
            print(f"  *** {rnn_type.upper()} diverged at step {step} ***")
            break

    logger.close()
    return log_path


def run_stress_sgd(rnn_type: str, train_ds, device: str,
                   max_steps: int = 500, log_dir: str = "logs"):
    """
    SGD stress test: high LR, long sequences, NO gradient clipping, vanilla SGD.
    This removes Adam's adaptive scaling so vanilla RNN gradient explosion
    is no longer masked.
    """
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"{rnn_type}_stress_sgd.csv")
    logger = MetricLogger(log_path, ["step", "loss", "grad_norm"])

    from data import CharDataset
    raw_text = "".join(train_ds.chars[i] for i in train_ds.data.tolist())
    stress_ds = CharDataset(raw_text, seq_len=256, chars=train_ds.chars)
    stress_loader = DataLoader(stress_ds, batch_size=64, shuffle=False, drop_last=True)

    model = CharLM(
        vocab_size=train_ds.vocab_size,
        embed_dim=64,
        hidden_size=256,
        rnn_type=rnn_type,
    ).to(device)

    optimizer = torch.optim.SGD(model.parameters(), lr=1.0)
    criterion = nn.CrossEntropyLoss()

    print(f"\n{'='*50}")
    print(f"Stress SGD run: {rnn_type.upper()} (no clipping, SGD lr=1.0, seq=256)")
    print(f"{'='*50}")

    model.train()
    hidden = None
    step = 0
    data_iter = iter(stress_loader)

    while step < max_steps:
        try:
            x, y = next(data_iter)
        except StopIteration:
            data_iter = iter(stress_loader)
            x, y = next(data_iter)
            hidden = None

        x, y = x.to(device), y.to(device)
        logits, hidden = model(x, hidden)
        loss = criterion(logits.reshape(-1, logits.size(-1)), y.reshape(-1))

        optimizer.zero_grad()
        loss.backward()

        grad_norm = compute_gradient_norm(model)
        # NO clipping
        optimizer.step()

        step += 1
        loss_val = loss.item()
        logger.log(step=step, loss=loss_val, grad_norm=grad_norm)

        if step % 50 == 0 or loss_val != loss_val:
            print(f"  step {step:4d} | loss {loss_val:.4f} | grad_norm {grad_norm:.2f}")

        if loss_val != loss_val:  # NaN
            print(f"  *** {rnn_type.upper()} diverged at step {step} ***")
            break

    logger.close()
    return log_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, default="tiny_shakespeare.txt")
    parser.add_argument("--device", type=str, default="cuda"
                        if torch.cuda.is_available() else "cpu")
    parser.add_argument("--num_epochs", type=int, default=10)
    parser.add_argument("--log_dir", type=str, default="answers/logs")
    parser.add_argument("--fig_dir", type=str, default="answers/figures")
    args = parser.parse_args()

    # Load data
    train_ds, val_ds = load_char_data(args.data_path, seq_len=128)
    print(f"Vocab size: {train_ds.vocab_size}")
    print(f"Train: {len(train_ds)} batches, Val: {len(val_ds)} batches")

    rnn_types = ["rnn", "lstm", "gru"]
    normal_logs = {}
    stress_logs = {}
    stress_sgd_logs = {}

    # ----- Normal runs -----
    for rnn_type in rnn_types:
        model, log_path = run_normal(
            rnn_type, train_ds, val_ds, args.device,
            num_epochs=args.num_epochs, log_dir=args.log_dir
        )
        normal_logs[rnn_type] = log_path

        # Quick generation sample
        sample = generate_charlm(model, train_ds, "The ", length=200,
                                 temperature=1.0, device=args.device)
        print(f"\n  Sample ({rnn_type.upper()}):\n  {sample[:200]}\n")

    # ----- Stress runs (Adam) -----
    print("\n" + "=" * 50)
    print("STRESS TESTS — Adam (no gradient clipping)")
    print("=" * 50)

    for rnn_type in rnn_types:
        log_path = run_stress(
            rnn_type, train_ds, args.device,
            max_steps=500, log_dir=args.log_dir
        )
        stress_logs[rnn_type] = log_path

    # ----- Stress runs (SGD) -----
    print("\n" + "=" * 50)
    print("STRESS TESTS — SGD (no gradient clipping)")
    print("=" * 50)

    for rnn_type in rnn_types:
        log_path = run_stress_sgd(
            rnn_type, train_ds, args.device,
            max_steps=500, log_dir=args.log_dir
        )
        stress_sgd_logs[rnn_type] = log_path

    # ----- Plot -----
    os.makedirs(args.fig_dir, exist_ok=True)
    plot_gradient_norms(
        normal_logs,
        save_path=os.path.join(args.fig_dir, "gradient_norm_normal.png"),
        title="Gradient Norm — Normal Training (clipping ON)"
    )
    plot_gradient_norms(
        stress_logs,
        save_path=os.path.join(args.fig_dir, "gradient_norm_stress_adam.png"),
        title="Gradient Norm — Stress Test: Adam (clipping OFF)"
    )
    plot_gradient_norms(
        stress_sgd_logs,
        save_path=os.path.join(args.fig_dir, "gradient_norm_stress_sgd.png"),
        title="Gradient Norm — Stress Test: SGD (clipping OFF)"
    )

    # ----- Summary table -----
    from utils import load_metrics

    for label, logs in [("ADAM", stress_logs), ("SGD", stress_sgd_logs)]:
        print(f"\n{'='*50}")
        print(f"STRESS TEST SUMMARY — {label}")
        print(f"{'='*50}")
        print(f"  {'Model':<8} {'NaN?':<8} {'Max Grad Norm':<15} {'Stable?'}")
        print(f"  {'-'*45}")
        for rnn_type in rnn_types:
            data = load_metrics(logs[rnn_type])
            norms = data["grad_norm"]
            has_nan = any(n != n for n in norms)  # NaN check
            max_norm = max(n for n in norms if n == n) if norms else 0
            stable = max_norm < 1000 and not has_nan
            print(f"  {rnn_type.upper():<8} {'Yes' if has_nan else 'No':<8} "
                  f"{max_norm:<15.1f} {'Yes' if stable else 'No'}")


if __name__ == "__main__":
    main()
