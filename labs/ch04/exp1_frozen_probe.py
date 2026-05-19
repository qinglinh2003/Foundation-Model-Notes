"""
Lab 4 — Experiment 1: Frozen Probe (CENTERPIECE)
=================================================
Corresponds to: Ch.4 Sec.4.2, 4.6 (bidirectional vs causal representations)

The core experiment of Lab 4. Freezes three types of encoders and trains
only a linear probe on SST-2 sentiment classification:

  A) Static embeddings (mean of token embeddings, no context)
  B) DistilGPT2 (causal, left-only context)
  C) DistilBERT (bidirectional, full context)

If bidirectional context helps, DistilBERT should score highest.
The gap between B and C measures the value of right-context.

Usage:
    python exp1_frozen_probe.py
"""

import torch
from transformers import AutoTokenizer, AutoModel
from data import get_sst2_loaders
from utils import (
    LinearProbe, train_probe, evaluate_probe,
    make_bert_extractor, make_gpt_extractor, make_static_extractor,
    plot_bar_chart,
)


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # ── Load models ──────────────────────────────────────────────────────
    print("\nLoading models...")

    bert_name = "distilbert-base-uncased"
    gpt_name = "distilgpt2"

    bert_tokenizer = AutoTokenizer.from_pretrained(bert_name)
    bert_model = AutoModel.from_pretrained(bert_name).to(device).eval()

    gpt_tokenizer = AutoTokenizer.from_pretrained(gpt_name)
    gpt_tokenizer.pad_token = gpt_tokenizer.eos_token
    gpt_model = AutoModel.from_pretrained(gpt_name).to(device).eval()

    bert_hidden = bert_model.config.hidden_size  # 768
    gpt_hidden = gpt_model.config.hidden_size    # 768

    print(f"  DistilBERT: {sum(p.numel() for p in bert_model.parameters()) / 1e6:.1f}M params, hidden={bert_hidden}")
    print(f"  DistilGPT2: {sum(p.numel() for p in gpt_model.parameters()) / 1e6:.1f}M params, hidden={gpt_hidden}")

    # ── Load data ────────────────────────────────────────────────────────
    # Use BERT tokenizer for static + BERT runs, GPT tokenizer for GPT run
    print("\nLoading SST-2 data...")
    bert_train_dl, bert_val_dl = get_sst2_loaders(
        bert_tokenizer, batch_size=32, max_len=128, max_train=5000, max_val=872
    )
    gpt_train_dl, gpt_val_dl = get_sst2_loaders(
        gpt_tokenizer, batch_size=32, max_len=128, max_train=5000, max_val=872
    )

    # ── Extractors ───────────────────────────────────────────────────────
    bert_extract = make_bert_extractor(bert_model, device)
    gpt_extract = make_gpt_extractor(gpt_model, device)
    static_extract = make_static_extractor(bert_model, device)

    results = {}

    # ── A: Static embeddings ─────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("A: Static Embeddings (mean token embedding, no context)")
    print("=" * 60)

    probe_static = LinearProbe(bert_hidden, 2).to(device)
    train_probe(probe_static, bert_train_dl, static_extract, device,
                epochs=10, lr=1e-3, log_path="logs/exp1_static.csv")
    acc_static, loss_static = evaluate_probe(probe_static, bert_val_dl,
                                             static_extract, device)
    print(f"  Val accuracy: {acc_static * 100:.1f}%")
    results["Static\n(no context)"] = acc_static * 100

    # ── B: DistilGPT2 (causal) ──────────────────────────────────────────
    print("\n" + "=" * 60)
    print("B: DistilGPT2 (causal, left-only context)")
    print("=" * 60)

    probe_gpt = LinearProbe(gpt_hidden, 2).to(device)
    train_probe(probe_gpt, gpt_train_dl, gpt_extract, device,
                epochs=10, lr=1e-3, log_path="logs/exp1_gpt.csv")
    acc_gpt, loss_gpt = evaluate_probe(probe_gpt, gpt_val_dl,
                                       gpt_extract, device)
    print(f"  Val accuracy: {acc_gpt * 100:.1f}%")
    results["DistilGPT2\n(causal)"] = acc_gpt * 100

    # ── C: DistilBERT (bidirectional) ────────────────────────────────────
    print("\n" + "=" * 60)
    print("C: DistilBERT (bidirectional, full context)")
    print("=" * 60)

    probe_bert = LinearProbe(bert_hidden, 2).to(device)
    train_probe(probe_bert, bert_train_dl, bert_extract, device,
                epochs=10, lr=1e-3, log_path="logs/exp1_bert.csv")
    acc_bert, loss_bert = evaluate_probe(probe_bert, bert_val_dl,
                                         bert_extract, device)
    print(f"  Val accuracy: {acc_bert * 100:.1f}%")
    results["DistilBERT\n(bidirectional)"] = acc_bert * 100

    # ── Plot ─────────────────────────────────────────────────────────────
    plot_bar_chart(
        list(results.keys()),
        list(results.values()),
        title="Exp 1: Frozen Probe Accuracy on SST-2",
        ylabel="Validation Accuracy (%)",
        save_path="plots/exp1_frozen_probe.png",
    )

    # ── Summary ──────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("DIAGNOSIS")
    print("=" * 60)
    print(f"  Static embeddings:  {acc_static * 100:.1f}%")
    print(f"  DistilGPT2 (causal): {acc_gpt * 100:.1f}%")
    print(f"  DistilBERT (bidir):  {acc_bert * 100:.1f}%")
    print()
    if acc_bert > acc_gpt:
        gap = (acc_bert - acc_gpt) * 100
        print(f"  DistilBERT beats DistilGPT2 by {gap:.1f} percentage points.")
        print("  Bidirectional context encodes more task-relevant information")
        print("  than causal (left-only) context — measurably, not just in theory.")
    else:
        print("  Unexpected: GPT matched or beat BERT. Check probe training.")
    print()
    print("  This is the centerpiece finding of Lab 4:")
    print("  Same Transformer block + different mask → different representation quality.")


if __name__ == "__main__":
    import os
    os.makedirs("logs", exist_ok=True)
    os.makedirs("plots", exist_ok=True)
    main()
