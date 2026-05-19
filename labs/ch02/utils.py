"""
Lab 2 — Utilities
==================
Foundational helpers shared across all experiments.

All functions in this file are PROVIDED — students should not need to
modify or re-implement anything here.

Currently exposes:
  - classify_form: regular/phonological/irregular categorization used by
    Exp 2 to slice accuracy into three columns.

Training loops, generation, plotting, and rank-collapse metrics live in
this file too and are added incrementally as the experiment scripts need
them.
"""

from __future__ import annotations

import csv
import os
import random
from collections import defaultdict
from pathlib import Path
from typing import Literal

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


Category = Literal["pure_regular", "phonological", "irregular"]


# ---------------------------------------------------------------------------
# Morphological category classifier
# ---------------------------------------------------------------------------
#
# All four tag classes share the same three-way classification:
#
#   pure_regular  - applying the bare suffix rule reproduces the inflected
#                   form. Lemma characters pass through unchanged.
#                   walk -> walked, dog -> dogs, box -> boxes
#
#   phonological  - the bare rule does not match, but a standard English
#                   orthographic adjustment (drop-e, y->ie, consonant
#                   doubling, f->v) does.
#                   make -> making, try -> tried, hop -> hopped, leaf -> leaves
#
#   irregular     - neither matches. The form must be memorized.
#                   go -> went, child -> children, mouse -> mice

VOWELS = set("aeiou")


def _bare_suffix(lemma: str, tag: str) -> str | None:
    """Form produced by the simplest rule per tag, no phonology applied."""
    if tag == "PAST":
        return lemma + "ed"
    if tag == "GERUND":
        return lemma + "ing"
    if tag in ("3SG", "PLURAL"):
        # English orthographic convention: -es after sibilant clusters,
        # otherwise -s. We treat both as "bare" — both are simple suffix
        # selection without modifying the lemma.
        if lemma.endswith(("s", "x", "z")) or lemma.endswith(("sh", "ch")):
            return lemma + "es"
        return lemma + "s"
    return None


def _phonological_candidates(lemma: str, tag: str) -> list[str]:
    """Forms produced by the rule with one standard phonological adjustment."""
    out: list[str] = []
    L = lemma

    if tag in ("PAST", "GERUND"):
        suffix = "ed" if tag == "PAST" else "ing"

        # Drop final e: make + ing -> making, hope + ed -> hoped.
        if L.endswith("e"):
            out.append(L[:-1] + suffix)

        # Consonant doubling: short vowel + single non-y consonant -> CVC.
        # hop -> hopped/hopping, zip -> zipped/zipping.
        if (
            len(L) >= 3
            and L[-1] not in VOWELS and L[-1] != "y"
            and L[-2] in VOWELS
            and L[-3] not in VOWELS
        ):
            out.append(L + L[-1] + suffix)

        # y -> ied (PAST only): try -> tried (gerund preserves y: trying).
        if tag == "PAST" and L.endswith("y") and len(L) >= 2 and L[-2] not in VOWELS:
            out.append(L[:-1] + "ied")

    if tag in ("3SG", "PLURAL"):
        # y -> ies: city -> cities, try -> tries.
        if L.endswith("y") and len(L) >= 2 and L[-2] not in VOWELS:
            out.append(L[:-1] + "ies")

        # f -> ves (PLURAL only by convention): leaf -> leaves, knife -> knives.
        if tag == "PLURAL":
            if L.endswith("fe"):
                out.append(L[:-2] + "ves")
            elif L.endswith("f"):
                out.append(L[:-1] + "ves")

    return out


def classify_form(lemma: str, inflected: str, tag: str) -> Category:
    """
    Classify a (lemma, inflected, tag) triple.

    Examples:
        >>> classify_form("walk", "walked", "PAST")
        'pure_regular'
        >>> classify_form("try", "tried", "PAST")
        'phonological'
        >>> classify_form("go", "went", "PAST")
        'irregular'
    """
    if _bare_suffix(lemma, tag) == inflected:
        return "pure_regular"
    if inflected in _phonological_candidates(lemma, tag):
        return "phonological"
    return "irregular"


# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------

def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


# ---------------------------------------------------------------------------
# CSV training logger
# ---------------------------------------------------------------------------

class MetricLogger:
    """Append-only CSV logger for training metrics."""

    def __init__(self, path: str, fieldnames: list[str]):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self.path = path
        self.fieldnames = fieldnames
        self._file = open(path, "w", newline="")
        self._writer = csv.DictWriter(self._file, fieldnames=fieldnames)
        self._writer.writeheader()

    def log(self, **kwargs):
        self._writer.writerow(kwargs)
        self._file.flush()

    def close(self):
        self._file.close()


def load_metrics(path: str) -> dict[str, list[float]]:
    data: dict[str, list[float]] = {}
    with open(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            for k, v in row.items():
                data.setdefault(k, []).append(float(v))
    return data


# ---------------------------------------------------------------------------
# Training and evaluation
# ---------------------------------------------------------------------------

def train_one_epoch(
    model,
    loader,
    optimizer,
    vocab,
    device,
    logger: MetricLogger | None = None,
    global_step: int = 0,
    clip_norm: float | None = 1.0,
    log_every: int = 50,
):
    """Single epoch of teacher-forcing training. Returns (avg_loss, global_step)."""
    model.train()
    total_loss = 0.0
    total_tokens = 0

    for batch in loader:
        src = batch["src"].to(device)
        dec_in = batch["dec_in"].to(device)
        dec_out = batch["dec_out"].to(device)

        logits, _ = model(src, dec_in)
        loss = F.cross_entropy(
            logits.reshape(-1, logits.size(-1)),
            dec_out.reshape(-1),
            ignore_index=vocab.pad_idx,
        )

        optimizer.zero_grad()
        loss.backward()
        if clip_norm is not None:
            nn.utils.clip_grad_norm_(model.parameters(), clip_norm)
        optimizer.step()

        n_tok = (dec_out != vocab.pad_idx).sum().item()
        total_loss += loss.item() * n_tok
        total_tokens += n_tok
        global_step += 1

        if logger and global_step % log_every == 0:
            logger.log(step=global_step, loss=loss.item())

    avg = total_loss / max(total_tokens, 1)
    return avg, global_step


@torch.no_grad()
def evaluate(model, loader, vocab, device, max_decode_len: int = 14) -> dict:
    """
    Greedy decode and compute exact-match accuracy, sliced by tag and
    morphological category. Returns a dict suitable for
    format_results_table().
    """
    model.eval()
    correct_by: dict = defaultdict(lambda: [0, 0])
    samples: list[dict] = []
    SAMPLE_CAP = 100

    for batch in loader:
        src = batch["src"].to(device)
        pred_ids = model.greedy_decode(
            src, vocab.sos_idx, vocab.eos_idx, max_len=max_decode_len,
        )

        for i in range(src.size(0)):
            lemma = batch["lemma"][i]
            inflected = batch["inflected"][i]
            tag = batch["tag"][i]
            cat = batch["category"][i]
            pred = vocab.decode(pred_ids[i, 1:].tolist())  # skip SOS
            ok = int(pred == inflected)

            correct_by["overall"][0] += ok
            correct_by["overall"][1] += 1
            correct_by[("tag", tag)][0] += ok
            correct_by[("tag", tag)][1] += 1
            correct_by[("cat", cat)][0] += ok
            correct_by[("cat", cat)][1] += 1
            correct_by[("tag_cat", tag, cat)][0] += ok
            correct_by[("tag_cat", tag, cat)][1] += 1

            if len(samples) < SAMPLE_CAP:
                samples.append({
                    "lemma": lemma, "tag": tag, "category": cat,
                    "gold": inflected, "pred": pred, "correct": bool(ok),
                })

    def rate(key):
        c, t = correct_by[key]
        return c / max(t, 1)

    tags = ("PAST", "GERUND", "3SG", "PLURAL")
    cats = ("pure_regular", "phonological", "irregular")

    return {
        "overall": rate("overall"),
        "by_tag": {t: rate(("tag", t)) for t in tags if correct_by[("tag", t)][1] > 0},
        "by_category": {c: rate(("cat", c)) for c in cats if correct_by[("cat", c)][1] > 0},
        "by_tag_cat": {
            (t, c): rate(("tag_cat", t, c))
            for t in tags for c in cats
            if correct_by[("tag_cat", t, c)][1] > 0
        },
        "counts": {
            "overall": correct_by["overall"][1],
            **{("tag", t): correct_by[("tag", t)][1] for t in tags},
            **{("cat", c): correct_by[("cat", c)][1] for c in cats},
            **{("tag_cat", t, c): correct_by[("tag_cat", t, c)][1]
               for t in tags for c in cats if correct_by[("tag_cat", t, c)][1] > 0},
        },
        "samples": samples,
    }


def format_results_table(results: dict, title: str = "") -> str:
    """Pretty-print accuracy grid (categories x tags) for an eval result."""
    cats = ("pure_regular", "phonological", "irregular")
    tags = ("PAST", "GERUND", "3SG", "PLURAL")

    lines = []
    if title:
        lines.append(title)
        lines.append("=" * len(title))
    header = f"{'category':14s} " + " ".join(f"{t:>10s}" for t in tags) + f" {'category-avg':>14s}"
    sep = "-" * len(header)
    lines.append(header)
    lines.append(sep)

    for cat in cats:
        row = f"{cat:14s} "
        for tag in tags:
            v = results["by_tag_cat"].get((tag, cat))
            row += f"{(v*100):9.1f}% " if v is not None else f"{'-':>10s} "
        v = results["by_category"].get(cat)
        row += f"{(v*100):13.1f}%" if v is not None else f"{'-':>14s}"
        lines.append(row)

    lines.append(sep)
    row = f"{'tag-avg':14s} "
    for tag in tags:
        v = results["by_tag"].get(tag)
        row += f"{(v*100):9.1f}% " if v is not None else f"{'-':>10s} "
    row += f"{(results['overall']*100):13.1f}%"
    lines.append(row)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Rank-collapse diagnostics (Dong et al. 2021)
# ---------------------------------------------------------------------------

@torch.no_grad()
def relative_residual(X: torch.Tensor) -> float:
    """
    Dong et al. (2021), eq. 4:  ||X - 1 mean(X)^T||_inf / ||X||_inf

    Measures distance from rank-1 (token uniformity).
      ~0   = each token has a distinct representation
      >=1  = matrix has effectively collapsed to its row mean

    X : (B, T, d)
    """
    mean = X.mean(dim=1, keepdim=True)            # (B, 1, d)
    residual = X - mean                            # (B, T, d)
    num = residual.abs().amax(dim=(1, 2))          # (B,)
    den = X.abs().amax(dim=(1, 2)).clamp_min(1e-8) # (B,)
    return (num / den).mean().item()


@torch.no_grad()
def mean_token_cosine(X: torch.Tensor) -> float:
    """
    Average cosine similarity between distinct token pairs.
      0 = orthogonal
      1 = identical (collapsed)

    X : (B, T, d)
    """
    B, T, _ = X.shape
    X_n = X / (X.norm(dim=-1, keepdim=True) + 1e-8)
    sim = X_n @ X_n.transpose(-2, -1)              # (B, T, T)
    off_diag = ~torch.eye(T, dtype=torch.bool, device=X.device)
    return sim[:, off_diag].mean().item()


@torch.no_grad()
def measure_rank_collapse(blocks, x, self_mask=None) -> list[tuple[float, float]]:
    """
    Forward x through each block sequentially, recording rank metrics
    BEFORE the first layer and AFTER every layer. Returns L+1 entries
    so plots show the full trajectory from the (orthogonal) random input.

    blocks : iterable of TransformerBlock-compatible modules
    x      : (B, T, d) initial hidden states
    Returns list of (relative_residual, mean_cosine) tuples,
        index 0 = input, index k = output of layer k.
    """
    # Make sure dropout/etc are off
    for block in blocks:
        block.eval()
    out = [(relative_residual(x), mean_token_cosine(x))]
    for block in blocks:
        x, _, _ = block(x, self_mask=self_mask)
        out.append((relative_residual(x), mean_token_cosine(x)))
    return out
