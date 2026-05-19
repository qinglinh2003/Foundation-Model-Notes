"""
Project 1: Data Pipeline
--------------------------
Tokenize corpus, create context windows with shifted targets, build DataLoader.

Pipeline:
    raw text -> tokenize -> insert <eos> at doc boundaries -> chunk into windows
    -> create (input, target) pairs where target = input shifted by 1
    -> DataLoader with shuffled batches
"""

import torch
from torch.utils.data import Dataset, DataLoader


class TextDataset(Dataset):
    """
    A dataset of (input, target) pairs for next-token prediction.

    Each sample is a pair of tensors:
        input:  token IDs [t_0, t_1, ..., t_{T-1}]    shape (context_length,)
        target: token IDs [t_1, t_2, ..., t_T]         shape (context_length,)

    The total sequence from the corpus is (context_length + 1) tokens.
    Input and target are shifted by exactly one position.
    """

    def __init__(self, token_ids: list[int], context_length: int):
        self.context_length = context_length
        # Non-overlapping windows of (context_length + 1) tokens
        window_size = context_length + 1
        n_windows = len(token_ids) // window_size
        # Truncate to exact fit
        trimmed = token_ids[: n_windows * window_size]
        self.data = torch.tensor(trimmed, dtype=torch.long).view(n_windows, window_size)

    def __len__(self) -> int:
        return self.data.size(0)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        window = self.data[idx]
        return window[:-1], window[1:]


def tokenize_corpus(corpus_path: str, tokenizer, eos_id: int) -> list[int]:
    """
    Read the corpus, tokenize it, and append <eos> at the end.

    For a single-file corpus with no explicit document boundaries,
    we tokenize the full text and append one <eos>.

    For multi-document corpora (separated by blank lines or markers),
    we insert <eos> between documents.
    """
    with open(corpus_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Split on double newlines as rough document boundaries
    docs = [d.strip() for d in text.split("\n\n\n") if d.strip()]

    all_ids: list[int] = []
    for doc in docs:
        ids = tokenizer.encode(doc).ids
        all_ids.extend(ids)
        all_ids.append(eos_id)

    return all_ids


def create_dataloaders(
    token_ids: list[int],
    context_length: int,
    batch_size: int,
    val_fraction: float = 0.05,
) -> tuple[DataLoader, DataLoader]:
    """
    Split token_ids into train/val and create DataLoaders.
    Split at a clean window boundary so no window straddles the split.
    """
    window_size = context_length + 1
    n_total = len(token_ids) // window_size
    n_val = max(1, int(n_total * val_fraction))
    n_train = n_total - n_val

    split_point = n_train * window_size
    train_ids = token_ids[:split_point]
    val_ids = token_ids[split_point: split_point + n_val * window_size]

    train_ds = TextDataset(train_ids, context_length)
    val_ds = TextDataset(val_ids, context_length)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, drop_last=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, drop_last=False)

    return train_loader, val_loader


# ---------------------------------------------------------------------------
# Quick test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Test 1: basic shift correctness with fake data
    fake_ids = list(range(1000))
    ds = TextDataset(fake_ids, context_length=128)
    print(f"Dataset size: {len(ds)}")
    inp, tgt = ds[0]
    print(f"Input shape: {inp.shape}, Target shape: {tgt.shape}")
    assert inp.shape == tgt.shape == (128,)
    assert (inp[1:] == tgt[:-1]).all(), "Shift is wrong!"
    print("Shift verified OK.")

    # Test 2: verify no data leakage between windows
    inp0, tgt0 = ds[0]
    inp1, tgt1 = ds[1]
    # tgt0[-1] should be the token just before inp1[0]
    print(f"Window 0 last target: {tgt0[-1].item()}, Window 1 first input: {inp1[0].item()}")
    assert tgt0[-1].item() + 1 == inp1[0].item(), "Windows not contiguous!"
    print("Window contiguity verified OK.")

    # Test 3: DataLoader creation
    train_loader, val_loader = create_dataloaders(fake_ids, context_length=128, batch_size=4)
    batch_inp, batch_tgt = next(iter(train_loader))
    print(f"Batch input shape: {batch_inp.shape}, Batch target shape: {batch_tgt.shape}")
    assert batch_inp.shape == batch_tgt.shape == (4, 128)
    print("DataLoader OK.")
    print(f"Train batches: {len(train_loader)}, Val batches: {len(val_loader)}")
