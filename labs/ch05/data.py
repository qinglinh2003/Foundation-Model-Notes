"""
Lab 5 -- Data utilities
========================
Handles Tiny Shakespeare loading, BPE tokenizer training (via HuggingFace
``tokenizers``), and dataset construction for both char-level and BPE modes.

Key design: the same ``build_datasets`` entry point returns train/val
DataLoaders for any vocab size, letting experiments sweep tokenizer
configurations cleanly.
"""

import torch
from torch.utils.data import Dataset, DataLoader
from pathlib import Path
from typing import Optional


# ===================================================================
# Tiny Shakespeare download
# ===================================================================

def _get_text(path: Optional[Path] = None) -> str:
    if path is None:
        path = Path(__file__).resolve().parent.parent / "ch03" / "tiny_shakespeare.txt"
    if not path.exists():
        import urllib.request
        url = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
        urllib.request.urlretrieve(url, path)
    return path.read_text()


# ===================================================================
# Character-level dataset (baseline)
# ===================================================================

class CharDataset(Dataset):
    def __init__(self, token_ids: torch.Tensor, seq_len: int):
        self.data = token_ids
        self.seq_len = seq_len

    def __len__(self):
        return (len(self.data) - 1) // self.seq_len

    def __getitem__(self, idx):
        s = idx * self.seq_len
        x = self.data[s : s + self.seq_len]
        y = self.data[s + 1 : s + self.seq_len + 1]
        return x, y


# ===================================================================
# BPE tokenizer training
# ===================================================================

def train_bpe_tokenizer(text: str, vocab_size: int, save_dir: Path) -> "Tokenizer":
    """Train a byte-level BPE tokenizer on *text* with the given vocab_size."""
    from tokenizers import Tokenizer, models, trainers, pre_tokenizers

    tokenizer = Tokenizer(models.BPE())
    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)

    trainer = trainers.BpeTrainer(
        vocab_size=vocab_size,
        special_tokens=["<pad>", "<eos>"],
        show_progress=False,
    )

    # Train from iterator (single string split into lines)
    tokenizer.train_from_iterator(text.splitlines(), trainer=trainer)

    save_dir.mkdir(parents=True, exist_ok=True)
    tokenizer.save(str(save_dir / f"bpe_v{vocab_size}.json"))
    return tokenizer


def load_bpe_tokenizer(save_dir: Path, vocab_size: int) -> "Tokenizer":
    from tokenizers import Tokenizer
    return Tokenizer.from_file(str(save_dir / f"bpe_v{vocab_size}.json"))


# ===================================================================
# Unified dataset builder
# ===================================================================

def build_datasets(
    vocab_size: int = 65,
    seq_len: int = 256,
    batch_size: int = 64,
    val_frac: float = 0.1,
    tokenizer_dir: Optional[Path] = None,
):
    """
    Build train/val DataLoaders for Tiny Shakespeare.

    If ``vocab_size == 65`` (character-level), uses a simple char mapping.
    Otherwise, trains a BPE tokenizer with the requested vocab_size.

    Returns
    -------
    train_dl, val_dl, actual_vocab_size, encode_fn, decode_fn, bytes_per_token
    """
    text = _get_text()
    split_idx = int(len(text) * (1 - val_frac))
    train_text, val_text = text[:split_idx], text[split_idx:]

    if vocab_size <= 65:
        # Character-level
        chars = sorted(set(text))
        c2i = {c: i for i, c in enumerate(chars)}
        i2c = {i: c for c, i in c2i.items()}
        actual_vocab = len(chars)

        def encode(t):
            return torch.tensor([c2i[c] for c in t], dtype=torch.long)

        def decode(ids):
            return "".join(i2c.get(i, "?") for i in ids)

        train_ids = encode(train_text)
        val_ids = encode(val_text)

        # bytes_per_token: for ASCII, 1 char = 1 byte
        bpt = len(train_text.encode("utf-8")) / len(train_ids)
    else:
        # BPE
        if tokenizer_dir is None:
            tokenizer_dir = Path(__file__).resolve().parent / "tokenizers"
        tok = train_bpe_tokenizer(train_text, vocab_size, tokenizer_dir)
        actual_vocab = tok.get_vocab_size()

        def encode(t):
            return torch.tensor(tok.encode(t).ids, dtype=torch.long)

        def decode(ids):
            return tok.decode(list(ids))

        train_ids = encode(train_text)
        val_ids = encode(val_text)

        bpt = len(train_text.encode("utf-8")) / len(train_ids)

    train_ds = CharDataset(train_ids, seq_len)
    val_ds = CharDataset(val_ids, seq_len)
    train_dl = DataLoader(train_ds, batch_size=batch_size, shuffle=True, drop_last=True)
    val_dl = DataLoader(val_ds, batch_size=batch_size, shuffle=False, drop_last=True)

    return train_dl, val_dl, actual_vocab, encode, decode, bpt
