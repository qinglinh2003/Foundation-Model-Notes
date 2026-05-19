"""
Project 1: BPE Tokenizer
-------------------------
Train a byte-pair encoding tokenizer on your corpus, then provide
encode/decode functions for the rest of the pipeline.

Dependencies: `tokenizers` library (pip install tokenizers)
"""

from pathlib import Path
from tokenizers import Tokenizer, models, trainers, pre_tokenizers, decoders, processors
from collections import Counter


def train_bpe(corpus_path: str, vocab_size: int, save_path: str) -> None:
    """Train a byte-level BPE tokenizer on the corpus and save it."""
    tokenizer = Tokenizer(models.BPE())
    tokenizer.pre_tokenizer = pre_tokenizers.ByteLevel(add_prefix_space=False)
    tokenizer.decoder = decoders.ByteLevel()

    special_tokens = ["<pad>", "<eos>", "<unk>"]
    trainer = trainers.BpeTrainer(
        vocab_size=vocab_size,
        special_tokens=special_tokens,
        show_progress=True,
        min_frequency=2,
    )
    tokenizer.train([corpus_path], trainer)

    # Set up post-processing (no automatic additions, just byte-level)
    tokenizer.post_processor = processors.ByteLevel(trim_offsets=False)

    Path(save_path).parent.mkdir(parents=True, exist_ok=True)
    tokenizer.save(save_path)
    print(f"Tokenizer saved to {save_path} (vocab_size={tokenizer.get_vocab_size()})")


def load_tokenizer(path: str) -> Tokenizer:
    """Load a trained tokenizer from disk."""
    return Tokenizer.from_file(path)


def encode(tokenizer: Tokenizer, text: str) -> list[int]:
    """Encode a string into a list of token IDs."""
    return tokenizer.encode(text).ids


def decode(tokenizer: Tokenizer, ids: list[int]) -> str:
    """Decode a list of token IDs back into a string."""
    return tokenizer.decode(ids)


def analyze_tokenizer(tokenizer: Tokenizer, corpus_path: str) -> dict:
    """Compute tokenizer statistics and print failure cases."""
    text = Path(corpus_path).read_text()
    total_bytes = len(text.encode("utf-8"))

    encoded = tokenizer.encode(text)
    total_tokens = len(encoded.ids)
    bytes_per_token = total_bytes / total_tokens

    # Token frequency (top 20)
    freq = Counter(encoded.tokens)
    top20 = dict(freq.most_common(20))

    stats = {
        "vocab_size": tokenizer.get_vocab_size(),
        "total_tokens": total_tokens,
        "total_bytes": total_bytes,
        "bytes_per_token": bytes_per_token,
        "token_frequency": top20,
    }

    print(f"\n{'='*50}")
    print(f"Tokenizer Analysis")
    print(f"{'='*50}")
    print(f"Vocab size:       {stats['vocab_size']:,}")
    print(f"Total tokens:     {stats['total_tokens']:,}")
    print(f"Total bytes:      {stats['total_bytes']:,}")
    print(f"Bytes per token:  {stats['bytes_per_token']:.2f}")
    print(f"\nTop 20 tokens:")
    for tok, cnt in top20.items():
        print(f"  {repr(tok):20s} {cnt:>8,}")

    # Failure cases
    print(f"\n{'='*50}")
    print(f"Tokenization Edge Cases")
    print(f"{'='*50}")

    cases = [
        ("Number boundary", "The year 1847 saw 12345 soldiers."),
        ("Rare word", "The sesquipedalian professor pontificated."),
        ("Non-English", "こんにちは世界 (Hello World in Japanese)"),
        ("Repeated chars", "Nooooooooo! Aaaargh!!!"),
    ]
    for label, test in cases:
        enc = tokenizer.encode(test)
        print(f"\n  {label}: \"{test}\"")
        print(f"  Tokens ({len(enc.ids)}): {enc.tokens}")

    return stats


# ---------------------------------------------------------------------------
# Quick test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    corpus = sys.argv[1] if len(sys.argv) > 1 else "data/corpus.txt"
    save = "tokenizer/bpe.json"

    Path("tokenizer").mkdir(exist_ok=True)
    train_bpe(corpus, vocab_size=2000, save_path=save)

    tok = load_tokenizer(save)
    sample = "The quick brown fox jumps over the lazy dog."
    ids = encode(tok, sample)
    decoded = decode(tok, ids)
    print(f"Original:  {sample}")
    print(f"Token IDs: {ids}")
    print(f"Decoded:   {decoded}")
    assert decoded.strip() == sample.strip(), "Roundtrip failed!"
    print("Roundtrip OK.")
