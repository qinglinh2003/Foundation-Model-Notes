"""
Lab 4 — Data utilities
======================
SST-2 sentiment classification dataset via HuggingFace datasets.
Also provides polysemy examples for Exp 0.
"""

import torch
from torch.utils.data import Dataset, DataLoader


# ── Polysemy examples for Exp 0 ─────────────────────────────────────────────

POLYSEMY_EXAMPLES = {
    "bank": [
        ("I deposited money at the bank this morning.", "financial"),
        ("We sat on the bank of the river watching the sunset.", "river"),
        ("The plane banked sharply to the left.", "aviation"),
    ],
    "bat": [
        ("He swung the bat and hit a home run.", "sports"),
        ("A bat flew out of the cave at dusk.", "animal"),
    ],
    "light": [
        ("Please turn on the light in the hallway.", "illumination"),
        ("The suitcase was surprisingly light.", "weight"),
        ("She spoke in a light and cheerful tone.", "mood"),
    ],
}


# ── SST-2 Dataset ───────────────────────────────────────────────────────────

class SST2Dataset(Dataset):
    """
    Wraps tokenized SST-2 examples for classification.

    Each item returns:
        input_ids: [max_len]
        attention_mask: [max_len]
        label: int (0=negative, 1=positive)
    """

    def __init__(self, input_ids, attention_masks, labels):
        self.input_ids = input_ids
        self.attention_masks = attention_masks
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return {
            "input_ids": self.input_ids[idx],
            "attention_mask": self.attention_masks[idx],
            "label": self.labels[idx],
        }


def load_sst2(tokenizer, max_len=128, max_train=5000, max_val=872):
    """
    Load SST-2 from HuggingFace datasets, tokenize with the given tokenizer.

    Returns:
        train_ds, val_ds (SST2Dataset instances)
    """
    from datasets import load_dataset

    ds = load_dataset("glue", "sst2")
    train_split = ds["train"].select(range(min(max_train, len(ds["train"]))))
    val_split = ds["validation"].select(range(min(max_val, len(ds["validation"]))))

    def tokenize_split(split):
        texts = list(split["sentence"])
        labels = list(split["label"])
        enc = tokenizer(
            texts, padding="max_length", truncation=True,
            max_length=max_len, return_tensors="pt",
        )
        return SST2Dataset(
            enc["input_ids"],
            enc["attention_mask"],
            torch.tensor(labels, dtype=torch.long),
        )

    return tokenize_split(train_split), tokenize_split(val_split)


def get_sst2_loaders(tokenizer, batch_size=32, max_len=128,
                     max_train=5000, max_val=872):
    """Convenience wrapper returning train/val DataLoaders."""
    train_ds, val_ds = load_sst2(tokenizer, max_len, max_train, max_val)
    train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=True, drop_last=True)
    val_dl = DataLoader(val_ds, batch_size=batch_size, shuffle=False, drop_last=False)
    return train_dl, val_dl
