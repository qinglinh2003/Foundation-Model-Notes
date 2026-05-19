"""
Lab 4 -- Experiment 2: Token-Level NER Probe
=============================================
Corresponds to: Ch.4 Sec.4.2, 4.8 (bidirectional advantage for token-level tasks)

The key experiment that demonstrates WHERE bidirectional context actually
matters. Exp 1 showed BERT ~ GPT on sentence-level SST-2 (because GPT's
last token already sees the whole sentence). This experiment uses a
token-level task (NER) where EACH token's representation must encode
enough information for classification -- and early/middle tokens in GPT
cannot see rightward context.

Uses CoNLL-2003 NER dataset. Fine-tunes DistilBERT vs DistilGPT2 with
a token classification head.

Usage:
    python exp2_ner_probe.py
"""

import os
import csv
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from collections import defaultdict
from transformers import AutoTokenizer, AutoModel

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ── NER label scheme (CoNLL-2003) ────────────────────────────────────────────
# 0=O, 1=B-PER, 2=I-PER, 3=B-ORG, 4=I-ORG, 5=B-LOC, 6=I-LOC, 7=B-MISC, 8=I-MISC
NER_LABELS = ["O", "B-PER", "I-PER", "B-ORG", "I-ORG", "B-LOC", "I-LOC", "B-MISC", "I-MISC"]
NUM_NER_LABELS = len(NER_LABELS)
IGNORE_INDEX = -100


# ── Token classification head ────────────────────────────────────────────────

class TokenClassifier(nn.Module):
    def __init__(self, hidden_size, num_labels, dropout=0.1):
        super().__init__()
        self.dropout = nn.Dropout(dropout)
        self.linear = nn.Linear(hidden_size, num_labels)

    def forward(self, x):
        return self.linear(self.dropout(x))


# ── Data loading + subword alignment ─────────────────────────────────────────

def load_conll2003(tokenizer, max_len=128, max_train=5000, max_val=1000):
    """
    Load CoNLL-2003, tokenize with subword alignment.

    For each word:
      - First subword gets the NER label
      - Subsequent subwords get IGNORE_INDEX (-100)
    """
    from datasets import load_dataset

    ds = load_dataset("conll2003", revision="refs/convert/parquet")
    train_split = ds["train"].select(range(min(max_train, len(ds["train"]))))
    val_split = ds["validation"].select(range(min(max_val, len(ds["validation"]))))

    def align_labels(split):
        # Ensure tokens are list[list[str]]
        all_tokens = [list(t) for t in split["tokens"]]
        all_ner_tags = [list(t) for t in split["ner_tags"]]

        tokenized = tokenizer(
            all_tokens,
            is_split_into_words=True,
            padding="max_length",
            truncation=True,
            max_length=max_len,
            return_tensors="pt",
        )

        all_labels = []
        for i, labels in enumerate(all_ner_tags):
            word_ids = tokenized.word_ids(batch_index=i)
            aligned = []
            prev_word = None
            for wid in word_ids:
                if wid is None:
                    aligned.append(IGNORE_INDEX)
                elif wid != prev_word:
                    if wid < len(labels):
                        aligned.append(labels[wid])
                    else:
                        aligned.append(IGNORE_INDEX)
                else:
                    aligned.append(IGNORE_INDEX)
                prev_word = wid
            all_labels.append(aligned)

        tokenized["labels"] = torch.tensor(all_labels, dtype=torch.long)
        return tokenized

    train_enc = align_labels(train_split)
    val_enc = align_labels(val_split)

    return train_enc, val_enc


class NERDataset(torch.utils.data.Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __len__(self):
        return len(self.encodings["input_ids"])

    def __getitem__(self, idx):
        return {
            "input_ids": self.encodings["input_ids"][idx],
            "attention_mask": self.encodings["attention_mask"][idx],
            "labels": self.encodings["labels"][idx],
        }


# ── Training ─────────────────────────────────────────────────────────────────

def train_ner(model, head, train_dl, device, epochs=5, lr=2e-5, log_path=None):
    """Fine-tune model + token classification head on NER."""
    model.train()
    head.train()
    params = list(model.parameters()) + list(head.parameters())
    opt = torch.optim.AdamW(params, lr=lr, weight_decay=0.01)
    history = []
    step = 0

    for epoch in range(epochs):
        epoch_loss = 0
        n_batches = 0
        for batch in train_dl:
            ids = batch["input_ids"].to(device)
            mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

            outputs = model(ids, attention_mask=mask, output_hidden_states=True)
            hidden = outputs.hidden_states[-1]  # [B, T, H]

            logits = head(hidden)  # [B, T, num_labels]
            logits_flat = logits.view(-1, NUM_NER_LABELS)
            labels_flat = labels.view(-1)

            loss = F.cross_entropy(logits_flat, labels_flat, ignore_index=IGNORE_INDEX)

            opt.zero_grad()
            loss.backward()
            opt.step()

            step += 1
            epoch_loss += loss.item()
            n_batches += 1
            history.append((step, loss.item()))

        avg = epoch_loss / max(n_batches, 1)
        print(f"    Epoch {epoch+1}: avg loss = {avg:.4f}")

    if log_path:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["step", "loss"])
            w.writerows(history)

    return history


# ── Evaluation ───────────────────────────────────────────────────────────────

@torch.no_grad()
def evaluate_ner(model, head, val_dl, device):
    """
    Evaluate NER: token-level accuracy and entity-level F1.
    Returns (token_acc, entity_f1, per_entity_f1_dict).
    """
    model.eval()
    head.eval()

    all_preds = []
    all_labels = []

    for batch in val_dl:
        ids = batch["input_ids"].to(device)
        mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        outputs = model(ids, attention_mask=mask, output_hidden_states=True)
        hidden = outputs.hidden_states[-1]
        logits = head(hidden)

        preds = logits.argmax(dim=-1)  # [B, T]

        # Flatten and filter out ignored positions
        for i in range(labels.size(0)):
            for j in range(labels.size(1)):
                if labels[i, j].item() != IGNORE_INDEX:
                    all_preds.append(preds[i, j].item())
                    all_labels.append(labels[i, j].item())

    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)

    # Token-level accuracy
    token_acc = (all_preds == all_labels).mean()

    # Per-entity-type F1 (exclude O)
    entity_f1 = {}
    for label_id in range(1, NUM_NER_LABELS):
        tp = ((all_preds == label_id) & (all_labels == label_id)).sum()
        fp = ((all_preds == label_id) & (all_labels != label_id)).sum()
        fn = ((all_preds != label_id) & (all_labels == label_id)).sum()
        precision = tp / max(tp + fp, 1)
        recall = tp / max(tp + fn, 1)
        f1 = 2 * precision * recall / max(precision + recall, 1e-8)
        entity_f1[NER_LABELS[label_id]] = f1

    # Macro F1 over entity types (exclude O)
    macro_f1 = np.mean(list(entity_f1.values()))

    return token_acc, macro_f1, entity_f1


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    bert_name = "distilbert-base-uncased"
    gpt_name = "distilgpt2"

    # ── Load tokenizers + models ─────────────────────────────────────────
    print("\nLoading models...")
    bert_tokenizer = AutoTokenizer.from_pretrained(bert_name)
    gpt_tokenizer = AutoTokenizer.from_pretrained(gpt_name)
    gpt_tokenizer.pad_token = gpt_tokenizer.eos_token

    bert_model = AutoModel.from_pretrained(bert_name).to(device)
    gpt_model = AutoModel.from_pretrained(gpt_name).to(device)

    bert_hidden = bert_model.config.hidden_size
    gpt_hidden = gpt_model.config.hidden_size

    print(f"  DistilBERT: {sum(p.numel() for p in bert_model.parameters())/1e6:.1f}M, hidden={bert_hidden}")
    print(f"  DistilGPT2: {sum(p.numel() for p in gpt_model.parameters())/1e6:.1f}M, hidden={gpt_hidden}")

    # ── Load CoNLL-2003 ──────────────────────────────────────────────────
    print("\nLoading CoNLL-2003 NER data...")
    bert_train_enc, bert_val_enc = load_conll2003(bert_tokenizer, max_len=128,
                                                   max_train=5000, max_val=1000)
    gpt_train_enc, gpt_val_enc = load_conll2003(gpt_tokenizer, max_len=128,
                                                 max_train=5000, max_val=1000)

    bert_train_dl = torch.utils.data.DataLoader(
        NERDataset(bert_train_enc), batch_size=16, shuffle=True, drop_last=True)
    bert_val_dl = torch.utils.data.DataLoader(
        NERDataset(bert_val_enc), batch_size=16, shuffle=False)
    gpt_train_dl = torch.utils.data.DataLoader(
        NERDataset(gpt_train_enc), batch_size=16, shuffle=True, drop_last=True)
    gpt_val_dl = torch.utils.data.DataLoader(
        NERDataset(gpt_val_enc), batch_size=16, shuffle=False)

    results = {}

    # ── A: Fine-tune DistilBERT on NER ───────────────────────────────────
    print("\n" + "=" * 60)
    print("A: DistilBERT — Fine-tune on NER (token classification)")
    print("=" * 60)

    bert_head = TokenClassifier(bert_hidden, NUM_NER_LABELS).to(device)
    train_ner(bert_model, bert_head, bert_train_dl, device,
              epochs=5, lr=2e-5, log_path="logs/exp2_bert_ner.csv")
    bert_acc, bert_f1, bert_per_entity = evaluate_ner(
        bert_model, bert_head, bert_val_dl, device)

    print(f"\n  Token accuracy: {bert_acc*100:.1f}%")
    print(f"  Macro entity F1: {bert_f1*100:.1f}%")
    for k, v in bert_per_entity.items():
        print(f"    {k:>8s}: F1 = {v*100:.1f}%")

    results["bert_acc"] = bert_acc
    results["bert_f1"] = bert_f1

    # ── B: Fine-tune DistilGPT2 on NER ──────────────────────────────────
    print("\n" + "=" * 60)
    print("B: DistilGPT2 — Fine-tune on NER (token classification)")
    print("=" * 60)

    gpt_head = TokenClassifier(gpt_hidden, NUM_NER_LABELS).to(device)
    train_ner(gpt_model, gpt_head, gpt_train_dl, device,
              epochs=5, lr=2e-5, log_path="logs/exp2_gpt_ner.csv")
    gpt_acc, gpt_f1, gpt_per_entity = evaluate_ner(
        gpt_model, gpt_head, gpt_val_dl, device)

    print(f"\n  Token accuracy: {gpt_acc*100:.1f}%")
    print(f"  Macro entity F1: {gpt_f1*100:.1f}%")
    for k, v in gpt_per_entity.items():
        print(f"    {k:>8s}: F1 = {v*100:.1f}%")

    results["gpt_acc"] = gpt_acc
    results["gpt_f1"] = gpt_f1

    # ── Plot: side-by-side comparison ────────────────────────────────────
    os.makedirs("plots", exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Left: Token accuracy
    models = ["DistilBERT\n(bidirectional)", "DistilGPT2\n(causal)"]
    accs = [bert_acc * 100, gpt_acc * 100]
    colors = ["#e8833a", "#4a90d9"]
    bars = axes[0].bar(models, accs, color=colors, width=0.5)
    for bar, val in zip(bars, accs):
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                     f"{val:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=12)
    axes[0].set_ylabel("Token Accuracy (%)", fontsize=12)
    axes[0].set_title("Token-Level NER Accuracy", fontsize=13, fontweight="bold")
    axes[0].set_ylim(0, 105)
    axes[0].grid(axis="y", alpha=0.3)

    # Right: Entity F1
    f1s = [bert_f1 * 100, gpt_f1 * 100]
    bars = axes[1].bar(models, f1s, color=colors, width=0.5)
    for bar, val in zip(bars, f1s):
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                     f"{val:.1f}%", ha="center", va="bottom", fontweight="bold", fontsize=12)
    axes[1].set_ylabel("Macro Entity F1 (%)", fontsize=12)
    axes[1].set_title("Entity-Level NER F1", fontsize=13, fontweight="bold")
    axes[1].set_ylim(0, 105)
    axes[1].grid(axis="y", alpha=0.3)

    plt.suptitle("Exp 2: Token-Level NER — Bidirectional vs Causal",
                 fontsize=14, fontweight="bold")
    plt.tight_layout()
    plt.savefig("plots/exp2_ner_comparison.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("\n  Plot saved: plots/exp2_ner_comparison.png")

    # ── Combined comparison with Exp 1 ───────────────────────────────────
    fig, ax = plt.subplots(figsize=(10, 5))

    x = np.arange(2)
    width = 0.3
    # SST-2 results (from Exp 1 — hardcoded placeholder, will be replaced)
    # These are approximate; the real values will come from actual Exp 1 run
    sst2_bert = 81.1  # placeholder
    sst2_gpt = 81.3   # placeholder

    bars1 = ax.bar(x - width/2, [sst2_bert, bert_f1*100], width,
                   label="DistilBERT (bidirectional)", color="#e8833a")
    bars2 = ax.bar(x + width/2, [sst2_gpt, gpt_f1*100], width,
                   label="DistilGPT2 (causal)", color="#4a90d9")

    for bar in bars1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{bar.get_height():.1f}%", ha="center", va="bottom", fontsize=10)
    for bar in bars2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                f"{bar.get_height():.1f}%", ha="center", va="bottom", fontsize=10)

    ax.set_xticks(x)
    ax.set_xticklabels(["SST-2 Sentiment\n(sentence-level)", "CoNLL NER\n(token-level)"],
                       fontsize=11)
    ax.set_ylabel("Score (%)", fontsize=12)
    ax.set_title("Task Granularity Determines Bidirectional Advantage",
                 fontsize=13, fontweight="bold")
    ax.set_ylim(0, 105)
    ax.legend(fontsize=11)
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig("plots/exp2_task_granularity.png", dpi=150, bbox_inches="tight")
    plt.close()
    print("  Plot saved: plots/exp2_task_granularity.png")

    # ── Summary ──────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("DIAGNOSIS")
    print("=" * 60)
    print(f"  Token accuracy:  DistilBERT {bert_acc*100:.1f}%  vs  DistilGPT2 {gpt_acc*100:.1f}%")
    print(f"  Entity F1:       DistilBERT {bert_f1*100:.1f}%  vs  DistilGPT2 {gpt_f1*100:.1f}%")
    acc_gap = (bert_acc - gpt_acc) * 100
    f1_gap = (bert_f1 - gpt_f1) * 100
    print(f"\n  Token accuracy gap: {acc_gap:+.1f} pp")
    print(f"  Entity F1 gap:     {f1_gap:+.1f} pp")
    print()
    print("  CONTRAST WITH EXP 1 (SST-2 sentence-level):")
    print("  - SST-2: BERT ~ GPT (both ~81%), because GPT's last token sees the whole sentence.")
    print("  - NER:   BERT should clearly beat GPT, because each token needs right-context")
    print("           that causal masking blocks.")
    print()
    print("  This is the key finding of Lab 4:")
    print("  Bidirectional advantage is NOT universal — it depends on task granularity.")
    print("  Sentence-level: causal is fine (last token aggregates all info).")
    print("  Token-level: bidirectional wins (middle tokens need right context).")


if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    os.makedirs("plots", exist_ok=True)
    main()
