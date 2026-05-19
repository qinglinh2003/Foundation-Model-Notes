"""
Lab 2 — Sanity checks
======================
Four standalone tests that pin down properties of the Transformer
implementation. Run BEFORE every training run.

Each test is a function returning (bool, str) so they can be invoked
individually from a notebook or all together via __main__.

Tests:
  1. attention_normalizes      Rows of softmax weights sum to 1.0.
  2. no_future_leakage         Decoder output at position t does not
                               depend on dec_in[t+1:].
  3. perm_equivariance_no_pe   Without positional encoding, the encoder
                               output permutes with the input.
  4. pe_breaks_perm            With positional encoding, the same shuffle
                               produces a measurably different output.
"""

from __future__ import annotations

import torch

from data import Vocab
from model import ScaledDotProductAttention, Seq2SeqTransformer


# ---------------------------------------------------------------------------
# Test 1: Attention weights normalize to 1 along the key axis
# ---------------------------------------------------------------------------

def attention_normalizes(tol: float = 1e-5) -> tuple[bool, str]:
    torch.manual_seed(0)
    B, h, T = 2, 4, 8
    Q = torch.randn(B, h, T, 16)
    K = torch.randn(B, h, T, 16)
    V = torch.randn(B, h, T, 16)

    _, attn = ScaledDotProductAttention()(Q, K, V)
    row_sums = attn.sum(dim=-1)
    dev = (row_sums - 1.0).abs().max().item()
    return dev < tol, f"max |row_sum - 1| = {dev:.2e}"


# ---------------------------------------------------------------------------
# Test 2: Causal mask blocks future tokens from influencing earlier outputs
# ---------------------------------------------------------------------------

def no_future_leakage(tol: float = 1e-5) -> tuple[bool, str]:
    torch.manual_seed(0)
    vocab = Vocab()
    model = Seq2SeqTransformer(
        vocab_size=vocab.size, pad_idx=vocab.pad_idx, use_causal_mask=True,
    )
    model.eval()

    B, T_src, T_tgt = 2, 10, 10
    # Avoid PAD/SOS/EOS (token indices 0/1/2) so the padding mask is empty.
    src = torch.randint(3, vocab.size, (B, T_src))
    dec_in_a = torch.randint(3, vocab.size, (B, T_tgt))
    dec_in_b = dec_in_a.clone()

    t = 4  # check that outputs at positions 0..t are invariant
    dec_in_b[:, t + 1 :] = torch.randint(3, vocab.size, (B, T_tgt - t - 1))

    with torch.no_grad():
        out_a, _ = model(src, dec_in_a)
        out_b, _ = model(src, dec_in_b)

    diff = (out_a[:, : t + 1] - out_b[:, : t + 1]).abs().max().item()
    return diff < tol, f"max |diff| over positions <= {t} = {diff:.2e}"


# ---------------------------------------------------------------------------
# Test 3: Without PE, encoder is permutation-equivariant
# ---------------------------------------------------------------------------

def perm_equivariance_no_pe(tol: float = 1e-4) -> tuple[bool, str]:
    torch.manual_seed(0)
    vocab = Vocab()
    model = Seq2SeqTransformer(
        vocab_size=vocab.size, pad_idx=vocab.pad_idx, use_encoder_pe=False,
    )
    model.eval()

    B, T = 1, 8
    src = torch.randint(3, vocab.size, (B, T))
    perm = torch.randperm(T)
    src_perm = src[:, perm]

    with torch.no_grad():
        out, _ = model.encoder(src, model.make_pad_mask(src))
        out_perm, _ = model.encoder(src_perm, model.make_pad_mask(src_perm))

    diff = (out[:, perm] - out_perm).abs().max().item()
    return diff < tol, f"max |out[perm] - out_perm| = {diff:.2e}"


# ---------------------------------------------------------------------------
# Test 4: With PE, permuting the input breaks the symmetry
# ---------------------------------------------------------------------------

def pe_breaks_perm(min_diff: float = 1e-2) -> tuple[bool, str]:
    torch.manual_seed(0)
    vocab = Vocab()
    model = Seq2SeqTransformer(
        vocab_size=vocab.size, pad_idx=vocab.pad_idx, use_encoder_pe=True,
    )
    model.eval()

    B, T = 1, 8
    src = torch.randint(3, vocab.size, (B, T))
    perm = torch.randperm(T)
    src_perm = src[:, perm]

    with torch.no_grad():
        out, _ = model.encoder(src, model.make_pad_mask(src))
        out_perm, _ = model.encoder(src_perm, model.make_pad_mask(src_perm))

    diff = (out[:, perm] - out_perm).abs().max().item()
    return diff > min_diff, f"max |out[perm] - out_perm| = {diff:.2e} (need > {min_diff})"


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

CHECKS = [
    ("1. Attention rows sum to 1",         attention_normalizes),
    ("2. No future leakage (mask on)",     no_future_leakage),
    ("3. Permutation equivariance w/o PE", perm_equivariance_no_pe),
    ("4. PE breaks permutation symmetry",  pe_breaks_perm),
]


def main() -> int:
    print("Running sanity checks...\n")
    all_pass = True
    for name, fn in CHECKS:
        ok, msg = fn()
        status = "[PASS]" if ok else "[FAIL]"
        print(f"  {status}  {name:42s}  {msg}")
        if not ok:
            all_pass = False
    print()
    if all_pass:
        print("All sanity checks passed.")
        return 0
    print("Some checks failed. Fix your implementation before training.")
    return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
