"""
Lab 3 — Sanity checks
======================
Run all four structural checks before trusting any experiment.

Usage:
    python verify.py

All checks must pass before running experiments.
"""

import torch
import torch.nn.functional as F
from model import GPT, GPTConfig


def check_logits_shape():
    """Check 1: Logits have shape [B, T, V]."""
    config = GPTConfig(vocab_size=65, seq_len=128, d_model=64, n_heads=4,
                       n_layers=2, pe_type="learned")
    model = GPT(config)
    model.eval()

    B, T = 2, 32
    input_ids = torch.randint(0, 65, (B, T))

    with torch.no_grad():
        logits, _ = model(input_ids)

    assert logits.shape == (B, T, 65), (
        f"FAIL: Expected logits shape ({B}, {T}, 65), got {logits.shape}"
    )
    print("  [PASS] Logits shape is [B, T, V]")


def check_causal_mask():
    """Check 2: Modifying a future token does not change earlier outputs."""
    config = GPTConfig(vocab_size=65, seq_len=128, d_model=64, n_heads=4,
                       n_layers=2, pe_type="learned")
    model = GPT(config)
    model.eval()

    input_ids = torch.randint(0, 65, (1, 16))

    with torch.no_grad():
        logits_original, _ = model(input_ids)

    # Modify the last token
    input_modified = input_ids.clone()
    input_modified[0, -1] = (input_modified[0, -1] + 1) % 65

    with torch.no_grad():
        logits_modified, _ = model(input_modified)

    # All positions BEFORE the last should be unchanged
    diff = (logits_original[0, :-1] - logits_modified[0, :-1]).abs().max().item()
    assert diff < 1e-5, (
        f"FAIL: Changing future token affected earlier logits (max diff = {diff:.6f}). "
        f"Causal mask is broken."
    )
    print("  [PASS] Causal mask prevents future information leakage")


def check_weight_tying():
    """Check 3: token_emb.weight and lm_head.weight are the same tensor."""
    config = GPTConfig(vocab_size=65, weight_tying=True)
    model = GPT(config)

    assert model.token_emb.weight is model.lm_head.weight, (
        "FAIL: Weight tying is not active. "
        "model.token_emb.weight should be the same object as model.lm_head.weight"
    )
    print("  [PASS] Weight tying is active (embedding == lm_head)")


def check_kv_cache_consistency():
    """
    Check 4: Generation with and without KV cache produces identical logits.

    Note: Both paths must produce the same logits for the same input.
    We check on a short sequence to verify cache correctness.
    """
    config = GPTConfig(vocab_size=65, seq_len=128, d_model=64, n_heads=4,
                       n_layers=2, pe_type="learned")
    model = GPT(config)
    model.eval()

    input_ids = torch.randint(0, 65, (1, 8))

    # Full forward pass (no cache)
    with torch.no_grad():
        logits_full, _ = model(input_ids, kv_caches=None)

    # Incremental forward pass (with cache): process token by token
    with torch.no_grad():
        # First token
        logits_inc, kv_caches = model(input_ids[:, :1], kv_caches=None)
        all_logits = [logits_inc]

        # Remaining tokens one by one
        for t in range(1, input_ids.size(1)):
            logits_t, kv_caches = model(input_ids[:, t:t+1], kv_caches=kv_caches)
            all_logits.append(logits_t)

    logits_incremental = torch.cat(all_logits, dim=1)

    # Compare
    diff = (logits_full - logits_incremental).abs().max().item()
    assert diff < 1e-4, (
        f"FAIL: KV cache produces different logits (max diff = {diff:.6f}). "
        f"Cache implementation has a bug."
    )
    print("  [PASS] KV cache produces identical logits to full forward pass")


if __name__ == "__main__":
    print("=" * 60)
    print("Lab 3 Sanity Checks")
    print("=" * 60)
    print()

    checks = [
        ("1. Logits shape", check_logits_shape),
        ("2. Causal mask", check_causal_mask),
        ("3. Weight tying", check_weight_tying),
        ("4. KV cache consistency", check_kv_cache_consistency),
    ]

    passed = 0
    for name, fn in checks:
        print(f"Running: {name}")
        try:
            fn()
            passed += 1
        except (AssertionError, NotImplementedError) as e:
            print(f"  [FAIL] {e}")
        print()

    print("=" * 60)
    print(f"Results: {passed}/{len(checks)} checks passed")
    if passed == len(checks):
        print("All checks passed. You may proceed with experiments.")
    else:
        print("Fix failing checks before running experiments.")
    print("=" * 60)
