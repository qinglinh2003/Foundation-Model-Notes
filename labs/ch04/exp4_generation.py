"""
Lab 4 — Experiment 4: Generation Flip
=======================================
Corresponds to: Ch.4 Sec.4.6 (why BERT lost the frontier role)

Shows the other side of the coin: GPT can generate coherent text,
BERT can only fill in [MASK] tokens. Same Transformer block,
fundamentally different interface.

No training required — pure inference.

Usage:
    python exp4_generation.py
"""

import torch
from transformers import (
    AutoTokenizer, AutoModelForCausalLM, AutoModelForMaskedLM,
    pipeline,
)


PROMPTS = [
    "The movie was absolutely",
    "In the beginning of the story",
    "The scientist discovered that",
]

FILL_SENTENCES = [
    "The movie was absolutely [MASK].",
    "The [MASK] ran quickly through the forest.",
    "She felt [MASK] after hearing the news.",
    "The experiment was a complete [MASK].",
]


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # ── Load models ──────────────────────────────────────────────────────
    print("\nLoading models...")
    gpt_name = "distilgpt2"
    bert_name = "distilbert-base-uncased"

    gpt_tokenizer = AutoTokenizer.from_pretrained(gpt_name)
    gpt_tokenizer.pad_token = gpt_tokenizer.eos_token
    gpt_model = AutoModelForCausalLM.from_pretrained(gpt_name).to(device).eval()

    bert_tokenizer = AutoTokenizer.from_pretrained(bert_name)
    bert_model = AutoModelForMaskedLM.from_pretrained(bert_name).to(device).eval()

    fill_mask = pipeline("fill-mask", model=bert_model, tokenizer=bert_tokenizer,
                         device=device)

    # ── GPT: Autoregressive generation ───────────────────────────────────
    print("\n" + "=" * 70)
    print("GPT: Autoregressive Generation (continuation)")
    print("=" * 70)

    for prompt in PROMPTS:
        inputs = gpt_tokenizer(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            output_ids = gpt_model.generate(
                **inputs,
                max_new_tokens=50,
                do_sample=True,
                temperature=0.8,
                top_k=50,
                pad_token_id=gpt_tokenizer.eos_token_id,
            )
        generated = gpt_tokenizer.decode(output_ids[0], skip_special_tokens=True)
        print(f'\n  Prompt: "{prompt}"')
        print(f"  Output: {generated}")

    # ── BERT: Mask filling ───────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("BERT: Mask Filling ([MASK] → single token prediction)")
    print("=" * 70)

    for sentence in FILL_SENTENCES:
        results = fill_mask(sentence, top_k=5)
        print(f'\n  Input: "{sentence}"')
        print(f"  Top predictions:")
        for r in results:
            print(f"    {r['token_str']:>12s}  (score: {r['score']:.3f})")

    # ── BERT attempting generation (awkward) ──────────────────────────────
    print("\n" + "=" * 70)
    print("BERT: Attempting multi-step 'generation' (iterative mask filling)")
    print("=" * 70)

    template = "The movie was [MASK] [MASK] [MASK] [MASK] [MASK] ."
    print(f'\n  Template: "{template}"')

    # Iteratively fill masks left-to-right
    current = template
    for step in range(5):
        if "[MASK]" not in current:
            break
        results = fill_mask(current, top_k=1)
        if isinstance(results[0], list):
            results = results[0]
        top = results[0]
        current = top["sequence"]
        print(f"  Step {step + 1}: {current}")

    print(f"\n  Final: {current}")

    # ── Summary ──────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("DIAGNOSIS")
    print("=" * 70)
    print("  GPT generates fluent continuations because autoregressive decoding")
    print("  is its native interface: causal mask → next-token prediction → generation.")
    print()
    print("  BERT can only fill [MASK] tokens — one at a time, conditioned on the")
    print("  entire surrounding context. Multi-step 'generation' via iterative mask")
    print("  filling is awkward and incoherent because each fill sees ALL other")
    print("  positions (including yet-to-be-filled ones).")
    print()
    print("  This is the architectural reason BERT lost the interface war:")
    print("  bidirectional attention is better for representation,")
    print("  but it fundamentally cannot do autoregressive generation.")
    print()
    print("  Together with Exp 1-2, this completes the Lab 4 thesis:")
    print("  BERT wins understanding. GPT wins generation.")
    print("  Same Transformer block, different capability.")


if __name__ == "__main__":
    main()
