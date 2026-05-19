"""
Lab 1 — Data utilities
======================
Provides three datasets:
  1. CharDataset        — character-level language modeling (Tiny Shakespeare)
  2. DelayedMemoryData  — synthetic delayed-memory probe (Experiment 2)
  3. ReversalData       — sequence reversal task (Experiment 4)
"""

import random
import torch
from torch.utils.data import Dataset, DataLoader

# ---------------------------------------------------------------------------
# 1. Character-level language modeling dataset
# ---------------------------------------------------------------------------

class CharDataset(Dataset):
    """
    Splits a plain-text file into fixed-length (seq_len) chunks for
    character-level next-token prediction.

    Usage:
        ds = CharDataset("tiny_shakespeare.txt", seq_len=128)
        x, y = ds[0]   # x: input chars, y: shifted targets
    """

    def __init__(self, text: str, seq_len: int = 128, chars=None):
        self.seq_len = seq_len

        # Build character vocabulary
        self.chars = sorted(set(text)) if chars is None else list(chars)
        self.char2idx = {c: i for i, c in enumerate(self.chars)}
        self.idx2char = {i: c for c, i in self.char2idx.items()}
        self.vocab_size = len(self.chars)

        # Encode full text
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

    def decode(self, indices):
        """Convert a list/tensor of indices back to a string."""
        return "".join(self.idx2char[int(i)] for i in indices)


def load_char_data(path: str, seq_len: int = 128, split_ratio: float = 0.9):
    """
    Load a text file and return (train_dataset, val_dataset).
    Split is by contiguous chunks, not random.
    """
    with open(path, "r") as f:
        text = f.read()

    split_idx = int(len(text) * split_ratio)
    chars = sorted(set(text))
    train_ds = CharDataset(text[:split_idx], seq_len=seq_len, chars=chars)
    val_ds = CharDataset(text[split_idx:], seq_len=seq_len, chars=chars)
    return train_ds, val_ds


# ---------------------------------------------------------------------------
# 2. Synthetic delayed-memory task (Experiment 2)
# ---------------------------------------------------------------------------

class DelayedMemoryData(Dataset):
    """
    Generates sequences of the form:

        [MARKER] signal [NOISE x N] [QUERY]

        Target: predict the signal class at the position after [QUERY].

    Args:
        num_samples : number of sequences
        distance    : number of noise tokens between signal and query
        vocab_size  : number of "content" tokens (excluding special tokens)
    """

    MARKER = 0   # special token IDs
    QUERY  = 1
    PAD    = 2
    CONTENT_OFFSET = 3  # content tokens start at index 3

    def __init__(self, num_samples: int, distance: int, vocab_size: int = 10):
        self.num_samples = num_samples
        self.distance = distance
        self.vocab_size = vocab_size
        self.total_vocab = vocab_size + 3  # +MARKER, QUERY, PAD

        # Pre-generate all sequences for reproducibility
        self.sequences = []
        self.targets = []
        for _ in range(num_samples):
            signal = random.randint(self.CONTENT_OFFSET,
                                    self.CONTENT_OFFSET + vocab_size - 1)
            noise = [
                random.choice(
                    [t for t in range(self.CONTENT_OFFSET,
                                      self.CONTENT_OFFSET + vocab_size)
                     if t != signal]
                )
                for _ in range(distance)
            ]
            seq = [self.MARKER, signal] + noise + [self.QUERY]
            self.sequences.append(torch.tensor(seq, dtype=torch.long))
            # Targets are class IDs 0..vocab_size-1, not raw token IDs.
            self.targets.append(signal - self.CONTENT_OFFSET)

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        return self.sequences[idx], self.targets[idx]


def collate_delayed_memory(batch):
    """Pad sequences to the same length within a batch."""
    seqs, targets = zip(*batch)
    max_len = max(s.size(0) for s in seqs)
    padded = torch.full((len(seqs), max_len), DelayedMemoryData.PAD,
                        dtype=torch.long)
    for i, s in enumerate(seqs):
        padded[i, :s.size(0)] = s
    targets = torch.tensor(targets, dtype=torch.long)
    return padded, targets


# ---------------------------------------------------------------------------
# 3. Sequence reversal task (Experiment 4)
# ---------------------------------------------------------------------------

class ReversalData(Dataset):
    """
    Generates (input, target) pairs where target = reversed input.

    Vocabulary: 26 lowercase letters (indices 0–25).
    Special tokens: SOS=26, EOS=27, PAD=28.

    Args:
        num_samples : number of pairs
        seq_len     : length of the input sequence (before SOS/EOS)
    """

    SOS = 26
    EOS = 27
    PAD = 28
    VOCAB_SIZE = 29  # 26 letters + SOS + EOS + PAD

    def __init__(self, num_samples: int, seq_len: int):
        self.num_samples = num_samples
        self.seq_len = seq_len
        self.pairs = []
        for _ in range(num_samples):
            src = [random.randint(0, 25) for _ in range(seq_len)]
            tgt = list(reversed(src))
            # Encoder input: src + [EOS]
            # Decoder input:  [SOS] + tgt
            # Decoder target: tgt + [EOS]
            self.pairs.append((
                torch.tensor(src + [self.EOS], dtype=torch.long),
                torch.tensor([self.SOS] + tgt, dtype=torch.long),
                torch.tensor(tgt + [self.EOS], dtype=torch.long),
            ))

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        return self.pairs[idx]


def collate_reversal(batch):
    """Returns (src, dec_input, dec_target) tensors."""
    src, dec_in, dec_tgt = zip(*batch)
    src = torch.stack(src)
    dec_in = torch.stack(dec_in)
    dec_tgt = torch.stack(dec_tgt)
    return src, dec_in, dec_tgt
