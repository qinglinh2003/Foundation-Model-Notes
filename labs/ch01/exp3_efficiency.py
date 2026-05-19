"""
Experiment 3: LSTM vs GRU Efficiency
=====================================
Collects metrics from Experiments 1 and 2 and produces a comparison table.
Also includes an optional parameter-matched comparison.

Usage:
    python exp3_efficiency.py --exp1_dir logs --exp2_results results/distance_probe.json
"""

import argparse, json, os
import torch
from model import CharLM, DelayedMemoryClassifier
from utils import load_metrics


def count_params(rnn_type: str, task: str = "charlm"):
    """Instantiate a model and count parameters."""
    if task == "charlm":
        model = CharLM(vocab_size=65, embed_dim=64, hidden_size=256,
                       rnn_type=rnn_type)
    else:
        model = DelayedMemoryClassifier(vocab_size=13, embed_dim=32,
                                        hidden_size=128, num_classes=10,
                                        rnn_type=rnn_type)
    return sum(p.numel() for p in model.parameters())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--exp1_dir", type=str, default="answers/logs")
    parser.add_argument("--exp2_results", type=str,
                        default="answers/results/distance_probe.json")
    args = parser.parse_args()

    rnn_types = ["rnn", "lstm", "gru"]

    # ----- Parameter counts -----
    print("\n" + "=" * 60)
    print("PARAMETER COUNTS")
    print("=" * 60)
    print(f"  {'Model':<8} {'CharLM (h=256)':<20} {'Probe (h=128)':<20}")
    print(f"  {'-'*48}")
    for rt in rnn_types:
        charlm_params = count_params(rt, "charlm")
        probe_params = count_params(rt, "probe")
        print(f"  {rt.upper():<8} {charlm_params:>15,}     {probe_params:>15,}")

    # Load exp1 logs for final loss (approximate PPL)
    import math
    exp1_metrics = {}
    for rt in rnn_types:
        log_path = os.path.join(args.exp1_dir, f"{rt}_normal.csv")
        if os.path.exists(log_path):
            data = load_metrics(log_path)
            # Use last 100 steps average loss as proxy for final performance
            losses = data["loss"]
            final_loss = sum(losses[-100:]) / min(len(losses), 100)
            ppl = math.exp(min(final_loss, 20))
            exp1_metrics[rt] = {"final_loss": final_loss, "ppl": ppl,
                                "total_steps": len(losses)}
        else:
            exp1_metrics[rt] = {"final_loss": float("nan"), "ppl": float("nan"),
                                "total_steps": 0}

    # Load exp2 results
    exp2_acc = {}
    if os.path.exists(args.exp2_results):
        with open(args.exp2_results, "r") as f:
            exp2_data = json.load(f)
        for rt in rnn_types:
            exp2_acc[rt] = exp2_data.get(rt, {}).get("128", exp2_data.get(rt, {}).get(128, float("nan")))
    else:
        for rt in rnn_types:
            exp2_acc[rt] = float("nan")

    # Print comparison table
    print("\n" + "=" * 60)
    print("EFFICIENCY COMPARISON")
    print("=" * 60)
    print(f"  {'Model':<8} {'Params':<15} {'Val PPL':<12} {'Acc@N=128':<12}")
    print(f"  {'-'*47}")
    for rt in rnn_types:
        params = count_params(rt, "charlm")
        ppl = exp1_metrics[rt]["ppl"]
        acc = exp2_acc[rt]
        print(f"  {rt.upper():<8} {params:>12,}   {ppl:>8.2f}     {acc:>8.4f}")

    # Analysis
    lstm_params = count_params("lstm", "charlm")
    gru_params = count_params("gru", "charlm")
    ratio = gru_params / lstm_params
    print(f"\n  GRU/LSTM parameter ratio: {ratio:.2f}")
    print(f"  GRU has {(1-ratio)*100:.1f}% fewer parameters than LSTM.")
    print(f"  Conclusion: GRU achieves {'similar' if abs(exp1_metrics['gru']['ppl'] - exp1_metrics['lstm']['ppl']) < 1.0 else 'different'} "
          f"PPL with fewer parameters.")

    # ----- Optional: parameter-matched GRU -----
    print("\n" + "=" * 60)
    print("OPTIONAL: Parameter-matched comparison")
    print("=" * 60)
    print("""
    To do a fair comparison, try training GRU with hidden_size=295
    (so total params ≈ LSTM with hidden_size=256).

    Then compare convergence speed and final metrics.

    This is optional — skip if time is short.
    """)


if __name__ == "__main__":
    main()
