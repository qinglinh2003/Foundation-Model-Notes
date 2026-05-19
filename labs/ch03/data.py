"""
Lab 3 — Data utilities
======================
Character-level language modeling dataset for Tiny Shakespeare.
Identical to Lab 1's CharDataset — students already know this format.
"""

import torch
from torch.utils.data import Dataset, DataLoader
from pathlib import Path


class CharDataset(Dataset):
    """
    Splits a plain-text file into fixed-length chunks for
    character-level next-token prediction.

    Usage:
        ds = CharDataset(text, seq_len=256)
        x, y = ds[0]   # x: input chars [seq_len], y: shifted targets [seq_len]
    """

    def __init__(self, text: str, seq_len: int = 256, chars=None):
        self.seq_len = seq_len
        self.chars = sorted(set(text)) if chars is None else list(chars)
        self.char2idx = {c: i for i, c in enumerate(self.chars)}
        self.idx2char = {i: c for c, i in self.char2idx.items()}
        self.vocab_size = len(self.chars)
        self.data = torch.tensor(
            [self.char2idx[c] for c in text], dtype=torch.long
        )

    def __len__(self):
        return (len(self.data) - 1) // self.seq_len

    def __getitem__(self, idx):
        start = idx * self.seq_len
        x = self.data[start : start + self.seq_len]
        y = self.data[start + 1 : start + self.seq_len + 1]
        return x, y


def load_tiny_shakespeare(seq_len: int = 256, val_frac: float = 0.1):
    """
    Download (if needed) and split Tiny Shakespeare into train/val datasets.

    Returns:
        train_ds, val_ds, vocab_size, chars
    """
    path = Path(__file__).parent / "tiny_shakespeare.txt"

    if not path.exists():
        import urllib.request
        url = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
        urllib.request.urlretrieve(url, path)

    text = path.read_text()
    chars = sorted(set(text))

    split = int(len(text) * (1 - val_frac))
    train_ds = CharDataset(text[:split], seq_len=seq_len, chars=chars)
    val_ds = CharDataset(text[split:], seq_len=seq_len, chars=chars)

    return train_ds, val_ds, len(chars), chars


def get_dataloaders(seq_len: int = 256, batch_size: int = 64):
    """Convenience wrapper returning train/val DataLoaders + metadata."""
    train_ds, val_ds, vocab_size, chars = load_tiny_shakespeare(seq_len=seq_len)
    train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=True, drop_last=True)
    val_dl = DataLoader(val_ds, batch_size=batch_size, shuffle=False, drop_last=True)
    return train_dl, val_dl, vocab_size, chars
