"""
Lab 4 — Experiment 3: Fine-tune SST-2 Comparison
============================================
Corresponds to: Ch.4 Sec.4.5 (pre-train + fine-tune paradigm)

Full fine-tuning on SST-2: DistilBERT vs DistilGPT2.

Question: Does fine-tuning change the sentence-level parity seen in
Exp 1's frozen probe?

Expected: BERT and GPT remain close on sentence-level SST-2, while
Exp 2 shows the bidirectional advantage on token-level NER.

Usage:
    python exp3_finetune.py
"""

import torch
import copy
from transformers import AutoTokenizer, AutoModel
from data import get_sst2_loaders
from utils import (
    LinearProbe, train_finetune, evaluate_finetune, plot_bar_chart,
)


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # ── Load models ──────────────────────────────────────────────────────
    print("\nLoading models...")

    bert_name = "distilbert-base-uncased"
    gpt_name = "distilgpt2"

    bert_tokenizer = AutoTokenizer.from_pretrained(bert_name)
    gpt_tokenizer = AutoTokenizer.from_pretrained(gpt_name)
    gpt_tokenizer.pad_token = gpt_tokenizer.eos_token

    # Deep copy so we don't mutate the pretrained weights
    bert_model = AutoModel.from_pretrained(bert_name).to(device)
    gpt_model = AutoModel.from_pretrained(gpt_name).to(device)

    bert_hidden = bert_model.config.hidden_size
    gpt_hidden = gpt_model.config.hidden_size

    # ── Load data ────────────────────────────────────────────────────────
    print("Loading SST-2 data...")
    bert_train_dl, bert_val_dl = get_sst2_loaders(
        bert_tokenizer, batch_size=16, max_len=128, max_train=5000, max_val=872
    )
    gpt_train_dl, gpt_val_dl = get_sst2_loaders(
        gpt_tokenizer, batch_size=16, max_len=128, max_train=5000, max_val=872
    )

    results = {}

    # ── A: Fine-tune DistilBERT ──────────────────────────────────────────
    print("\n" + "=" * 60)
    print("A: Fine-tune DistilBERT (3 epochs)")
    print("=" * 60)

    bert_head = LinearProbe(bert_hidden, 2).to(device)
    train_finetune(bert_model, bert_head, bert_train_dl, device,
                   epochs=3, lr=2e-5, log_path="logs/exp3_bert_ft.csv")
    acc_bert = evaluate_finetune(bert_model, bert_head, bert_val_dl, device,
                                 use_last_token=False)
    print(f"  Val accuracy: {acc_bert * 100:.1f}%")
    results["DistilBERT\n(fine-tuned)"] = acc_bert * 100

    # ── B: Fine-tune DistilGPT2 ─────────────────────────────────────────
    print("\n" + "=" * 60)
    print("B: Fine-tune DistilGPT2 (3 epochs)")
    print("=" * 60)

    gpt_head = LinearProbe(gpt_hidden, 2).to(device)

    # Custom fine-tune for GPT (use last token, not first)
    gpt_model.train()
    gpt_head.train()
    params = list(gpt_model.parameters()) + list(gpt_head.parameters())
    opt = torch.optim.AdamW(params, lr=2e-5, weight_decay=0.01)
    step = 0

    import csv, os
    os.makedirs("logs", exist_ok=True)
    log_rows = []

    for epoch in range(3):
        for batch in gpt_train_dl:
            ids = batch["input_ids"].to(device)
            mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)

            outputs = gpt_model(ids, attention_mask=mask, output_hidden_states=True)
            hidden = outputs.hidden_states[-1]
            # Use last non-pad token
            seq_lens = mask.sum(dim=1) - 1
            reps = hidden[torch.arange(hidden.size(0), device=device), seq_lens]

            logits = gpt_head(reps)
            loss = torch.nn.functional.cross_entropy(logits, labels)

            opt.zero_grad()
            loss.backward()
            opt.step()
            step += 1
            log_rows.append((step, loss.item()))

    with open("logs/exp3_gpt_ft.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["step", "loss"])
        w.writerows(log_rows)

    acc_gpt = evaluate_finetune(gpt_model, gpt_head, gpt_val_dl, device,
                                use_last_token=True)
    print(f"  Val accuracy: {acc_gpt * 100:.1f}%")
    results["DistilGPT2\n(fine-tuned)"] = acc_gpt * 100

    # ── Plot ─────────────────────────────────────────────────────────────
    plot_bar_chart(
        list(results.keys()),
        list(results.values()),
        title="Exp 3: Fine-tuned Accuracy on SST-2",
        ylabel="Validation Accuracy (%)",
        save_path="plots/exp3_finetune.png",
        colors=["#e8833a", "#4a90d9"],
    )

    # ── Summary ──────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("DIAGNOSIS")
    print("=" * 60)
    print(f"  DistilBERT (fine-tuned):  {acc_bert * 100:.1f}%")
    print(f"  DistilGPT2 (fine-tuned):  {acc_gpt * 100:.1f}%")
    print()
    gap = (acc_bert - acc_gpt) * 100
    print(f"  Gap after fine-tuning: {gap:.1f} percentage points")
    print()
    if gap > 0:
        print("  BERT leads on fine-tuned SST-2, but compare this with Exp 2:")
        print("  sentence-level classification is not where bidirectional context")
        print("  creates the largest advantage.")
    else:
        print("  GPT matched BERT after fine-tuning. This supports the task")
        print("  granularity result: sentence-level classification can be solved")
        print("  from GPT's final token, while token-level NER exposes the causal")
        print("  mask limitation.")


if __name__ == "__main__":
    import os
    os.makedirs("logs", exist_ok=True)
    os.makedirs("plots", exist_ok=True)
    main()
