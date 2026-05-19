"""
Lab 2 — Data utilities
=======================
Loads the UniMorph English morphological inflection dataset and exposes:
  - Vocab: shared character + tag + special token vocabulary
  - MorphInflectionDataset: __getitem__ returns the encoder/decoder
    tensors plus the original strings (lemma, inflected, tag, category)
    so downstream analysis is easy.
  - load_records / split_records: hybrid train/val/test policy
        regulars (pure_regular + phonological) split by LEMMA
                                  -> tests rule generalization
        irregulars                split by (LEMMA, TAG)
                                  -> increases irregular test coverage
  - load_wug_test: pseudo-word probe set for Stretch experiments.

All functions are provided; students do not modify this file.
"""

from __future__ import annotations
import random
import string
from pathlib import Path

import torch
from torch.utils.data import Dataset, DataLoader

from utils import classify_form


TAGS: tuple[str, ...] = ("PAST", "GERUND", "3SG", "PLURAL")

DATA_DIR = Path(__file__).parent / "data"
INFLECTION_TSV = DATA_DIR / "unimorph_eng_filtered.tsv"
WUG_TSV = DATA_DIR / "wug_test.tsv"


# ===========================================================================
# Vocabulary
# ===========================================================================

class Vocab:
    """
    Shared encoder/decoder vocabulary.

    Token layout:
        index 0      <PAD>
        index 1      <SOS>
        index 2      <EOS>
        index 3..6   <PAST> <GERUND> <3SG> <PLURAL>
        index 7..32  a..z
    """

    PAD, SOS, EOS = "<PAD>", "<SOS>", "<EOS>"

    def __init__(self):
        specials = [self.PAD, self.SOS, self.EOS]
        tag_tokens = [f"<{t}>" for t in TAGS]
        chars = list(string.ascii_lowercase)

        self.itos: list[str] = specials + tag_tokens + chars
        self.stoi: dict[str, int] = {t: i for i, t in enumerate(self.itos)}
        self.size: int = len(self.itos)

        self.pad_idx = self.stoi[self.PAD]
        self.sos_idx = self.stoi[self.SOS]
        self.eos_idx = self.stoi[self.EOS]

    def encode_char(self, c: str) -> int:
        return self.stoi[c]

    def encode_tag(self, tag: str) -> int:
        return self.stoi[f"<{tag}>"]

    def decode(self, indices) -> str:
        """Token IDs -> string, stopping at EOS and skipping special tokens."""
        chars = []
        for i in indices:
            i = int(i)
            if i == self.eos_idx or i == self.pad_idx:
                break
            tok = self.itos[i]
            if not (tok.startswith("<") and tok.endswith(">")):
                chars.append(tok)
        return "".join(chars)


# ===========================================================================
# Dataset
# ===========================================================================

class MorphInflectionDataset(Dataset):
    """
    Each item is a dict with both tensor fields and string fields. String
    fields survive default_collate as lists, which makes per-batch
    analysis (split by tag / category) painless.

    Encoder src      = [<TAG>, c1, c2, ..., cL, <EOS>]            padded
    Decoder dec_in   = [<SOS>, c1', c2', ..., cK']                padded
    Decoder dec_out  = [c1', c2', ..., cK', <EOS>]                padded
    """

    def __init__(
        self,
        records: list[dict],
        vocab: Vocab,
        max_src_len: int = 14,
        max_tgt_len: int = 14,
    ):
        self.records = records
        self.vocab = vocab
        self.max_src_len = max_src_len
        self.max_tgt_len = max_tgt_len

    def __len__(self) -> int:
        return len(self.records)

    def __getitem__(self, idx: int) -> dict:
        rec = self.records[idx]
        lemma, inflected, tag = rec["lemma"], rec["inflected"], rec["tag"]
        v = self.vocab

        src = [v.encode_tag(tag)] + [v.encode_char(c) for c in lemma] + [v.eos_idx]
        tgt = [v.encode_char(c) for c in inflected]
        dec_in = [v.sos_idx] + tgt
        dec_out = tgt + [v.eos_idx]

        return {
            "src": torch.tensor(self._pad(src, self.max_src_len), dtype=torch.long),
            "dec_in": torch.tensor(self._pad(dec_in, self.max_tgt_len), dtype=torch.long),
            "dec_out": torch.tensor(self._pad(dec_out, self.max_tgt_len), dtype=torch.long),
            "lemma": lemma,
            "inflected": inflected,
            "tag": tag,
            "category": rec["category"],
        }

    def _pad(self, seq: list[int], max_len: int) -> list[int]:
        if len(seq) >= max_len:
            return seq[:max_len]
        return seq + [self.vocab.pad_idx] * (max_len - len(seq))


# ===========================================================================
# Loading + splitting
# ===========================================================================

def load_records(tsv_path: Path | str = INFLECTION_TSV) -> list[dict]:
    """Load the filtered TSV and attach a 'category' field to every record."""
    records: list[dict] = []
    with open(tsv_path) as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) != 3:
                continue
            lemma, inflected, tag = parts
            records.append({
                "lemma": lemma,
                "inflected": inflected,
                "tag": tag,
                "category": classify_form(lemma, inflected, tag),
            })
    return records


def split_records(
    records: list[dict],
    val_frac: float = 0.15,
    test_frac: float = 0.15,
    seed: int = 42,
) -> tuple[list[dict], list[dict], list[dict]]:
    """
    Hybrid split:
      pure_regular + phonological -> split by lemma
      irregular                    -> split by (lemma, tag)
    """
    rng = random.Random(seed)

    regulars = [r for r in records if r["category"] != "irregular"]
    irregulars = [r for r in records if r["category"] == "irregular"]

    # ---- regulars: group by lemma, then assign each lemma to one split ----
    by_lemma: dict[str, list[dict]] = {}
    for r in regulars:
        by_lemma.setdefault(r["lemma"], []).append(r)

    lemmas = sorted(by_lemma.keys())
    rng.shuffle(lemmas)
    n = len(lemmas)
    n_test = int(n * test_frac)
    n_val = int(n * val_frac)
    test_lemmas = set(lemmas[:n_test])
    val_lemmas = set(lemmas[n_test : n_test + n_val])

    train: list[dict] = []
    val: list[dict] = []
    test: list[dict] = []
    for lemma, recs in by_lemma.items():
        if lemma in test_lemmas:
            test.extend(recs)
        elif lemma in val_lemmas:
            val.extend(recs)
        else:
            train.extend(recs)

    # ---- irregulars: independent random split, by (lemma, tag) ----
    rng.shuffle(irregulars)
    n_irr = len(irregulars)
    n_irr_test = int(n_irr * test_frac)
    n_irr_val = int(n_irr * val_frac)
    test.extend(irregulars[:n_irr_test])
    val.extend(irregulars[n_irr_test : n_irr_test + n_irr_val])
    train.extend(irregulars[n_irr_test + n_irr_val :])

    rng.shuffle(train)
    rng.shuffle(val)
    rng.shuffle(test)
    return train, val, test


# ===========================================================================
# Wug test
# ===========================================================================

def load_wug_test(path: Path | str = WUG_TSV) -> list[dict]:
    """
    Load the pseudo-word probe set. Pipe-separated values in the
    'expected' column are alternative acceptable answers (e.g. heafs|heaves).
    """
    records: list[dict] = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 3:
                continue
            lemma, expected, tag = parts[0], parts[1], parts[2]
            records.append({
                "lemma": lemma,
                "accepted": expected.split("|"),
                "tag": tag,
            })
    return records


# ===========================================================================
# Convenience: full setup in one call
# ===========================================================================

def build_dataloaders(
    tsv_path: Path | str = INFLECTION_TSV,
    batch_size: int = 64,
    seed: int = 42,
    num_workers: int = 0,
) -> tuple[DataLoader, DataLoader, DataLoader, Vocab, dict]:
    """
    Returns (train_loader, val_loader, test_loader, vocab, info).
    info is a dict with split sizes and per-category counts for reporting.
    """
    records = load_records(tsv_path)
    vocab = Vocab()
    train, val, test = split_records(records, seed=seed)

    def _categorize(recs):
        from collections import Counter
        return Counter((r["tag"], r["category"]) for r in recs)

    info = {
        "n_train": len(train),
        "n_val": len(val),
        "n_test": len(test),
        "train_categories": _categorize(train),
        "val_categories": _categorize(val),
        "test_categories": _categorize(test),
    }

    train_ds = MorphInflectionDataset(train, vocab)
    val_ds = MorphInflectionDataset(val, vocab)
    test_ds = MorphInflectionDataset(test, vocab)

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True,
                              num_workers=num_workers)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False,
                            num_workers=num_workers)
    test_loader = DataLoader(test_ds, batch_size=batch_size, shuffle=False,
                             num_workers=num_workers)

    return train_loader, val_loader, test_loader, vocab, info


if __name__ == "__main__":
    # Quick sanity print: show split sizes and one example batch
    train_loader, val_loader, test_loader, vocab, info = build_dataloaders()
    print(f"Vocab size:    {vocab.size}")
    print(f"Splits:        train={info['n_train']}  val={info['n_val']}  test={info['n_test']}")
    print(f"\nTest set per (tag, category):")
    for (tag, cat), n in sorted(info["test_categories"].items()):
        print(f"  {tag:7s} {cat:14s} {n}")

    batch = next(iter(train_loader))
    print(f"\nSample batch shapes:")
    print(f"  src     {batch['src'].shape}")
    print(f"  dec_in  {batch['dec_in'].shape}")
    print(f"  dec_out {batch['dec_out'].shape}")
    print(f"\nFirst record in batch:")
    print(f"  lemma     {batch['lemma'][0]}")
    print(f"  inflected {batch['inflected'][0]}")
    print(f"  tag       {batch['tag'][0]}")
    print(f"  category  {batch['category'][0]}")
    print(f"  src ids   {batch['src'][0].tolist()}")
    print(f"  decoded   {vocab.decode(batch['src'][0])!r}")
