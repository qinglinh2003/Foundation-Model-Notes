"""
Project 1: Text Generation
----------------------------
Autoregressive generation with temperature scaling and top-k sampling.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


@torch.no_grad()
def generate(
    model: nn.Module,
    tokenizer,
    prompt: str,
    max_tokens: int = 100,
    temperature: float = 0.8,
    top_k: int = 40,
    device: str = "cuda",
) -> str:
    """
    Generate text autoregressively from a prompt.

    Algorithm:
        1. Encode the prompt into token IDs.
        2. For each new token:
            a. Forward pass: get logits for the last position.
            b. Divide logits by temperature.
            c. Keep only the top-k logits; set the rest to -inf.
            d. Apply softmax to get probabilities.
            e. Sample one token from the distribution.
            f. Append to the sequence.
            g. If the token is <eos>, stop.
        3. Decode the full sequence back to text.

    Args:
        model:       Trained MiniGPT in eval mode.
        tokenizer:   The trained tokenizer.
        prompt:      Text string to start generation from.
        max_tokens:  Maximum number of tokens to generate.
        temperature: Sampling temperature (lower = more deterministic).
        top_k:       Number of top tokens to sample from.
        device:      "cuda" or "cpu".

    Returns:
        The generated text (including the prompt).

    Notes:
        - If the sequence exceeds context_length, truncate from the left
          (sliding window) so the model always sees the most recent tokens.
        - Temperature = 0 is undefined; use greedy (argmax) for T < 0.01.
    """
    model.eval()
    # Get context length from model
    if hasattr(model, "config"):
        ctx_len = model.config.context_length
    elif hasattr(model, "pos_emb"):
        ctx_len = model.pos_emb.size(1)
    else:
        ctx_len = 256  # fallback

    # Encode prompt
    ids = tokenizer.encode(prompt).ids
    tokens = torch.tensor(ids, dtype=torch.long, device=device).unsqueeze(0)

    eos_id = tokenizer.token_to_id("<eos>")

    for _ in range(max_tokens):
        # Truncate from left if exceeding context length (sliding window)
        if tokens.size(1) > ctx_len:
            tokens = tokens[:, -ctx_len:]

        logits = model(tokens)              # (1, T, V)
        logits = logits[:, -1, :]           # (1, V) — last position

        # Temperature scaling
        if temperature < 0.01:
            # Greedy
            next_id = logits.argmax(dim=-1)  # (1,)
        else:
            logits = logits / temperature

            # Top-k filtering
            if top_k > 0 and top_k < logits.size(-1):
                topk_vals, _ = torch.topk(logits, top_k, dim=-1)
                threshold = topk_vals[:, -1].unsqueeze(-1)
                logits[logits < threshold] = float("-inf")

            probs = F.softmax(logits, dim=-1)
            next_id = torch.multinomial(probs, num_samples=1).squeeze(-1)  # (1,)

        tokens = torch.cat([tokens, next_id.unsqueeze(-1)], dim=1)

        if eos_id is not None and next_id.item() == eos_id:
            break

    # Decode full sequence
    output_ids = tokens.squeeze(0).tolist()
    return tokenizer.decode(output_ids)


def generate_samples(
    model: nn.Module,
    tokenizer,
    prompts: list[str],
    temperatures: list[float] = [0.5, 0.8, 1.2],
    max_tokens: int = 100,
    top_k: int = 40,
    device: str = "cuda",
) -> list[dict]:
    """
    Generate samples for multiple prompts and temperatures.

    Returns:
        List of dicts: {"prompt": str, "temperature": float, "generated": str}
    """
    results = []
    for prompt in prompts:
        for temp in temperatures:
            text = generate(
                model, tokenizer, prompt,
                max_tokens=max_tokens,
                temperature=temp,
                top_k=top_k,
                device=device,
            )
            results.append({
                "prompt": prompt,
                "temperature": temp,
                "generated": text,
            })
    return results


# ---------------------------------------------------------------------------
# Quick test (requires a trained model and tokenizer)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    sys.path.insert(0, ".")
    from config import ModelConfig
    from model import MiniGPT
    from tokenizer import load_tokenizer

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--tokenizer", type=str, default="tokenizer/bpe.json")
    parser.add_argument("--prompt", type=str, default="The ")
    parser.add_argument("--max_tokens", type=int, default=200)
    parser.add_argument("--temperature", type=float, default=0.8)
    parser.add_argument("--top_k", type=int, default=40)
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load tokenizer
    tok = load_tokenizer(args.tokenizer)

    # Load model
    ckpt = torch.load(args.checkpoint, map_location=device, weights_only=False)
    cfg_data = ckpt.get("config", {})
    if isinstance(cfg_data, dict):
        # Filter to only ModelConfig fields
        import dataclasses
        valid_fields = {f.name for f in dataclasses.fields(ModelConfig)}
        cfg = ModelConfig(**{k: v for k, v in cfg_data.items() if k in valid_fields})
    else:
        cfg = cfg_data
    model = MiniGPT(cfg).to(device)
    model.load_state_dict(ckpt["model"])
    model.eval()

    step = ckpt.get("step", "?")
    print(f"Loaded checkpoint (step {step})")
    print(f"Model: {sum(p.numel() for p in model.parameters()):,} params")
    print(f"Prompt: {args.prompt!r}")
    print(f"Temperature: {args.temperature}, Top-k: {args.top_k}")
    print("=" * 60)

    text = generate(
        model, tok, args.prompt,
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        top_k=args.top_k,
        device=device,
    )
    print(text)

    # Multi-temperature comparison
    print("\n" + "=" * 60)
    print("Temperature comparison:")
    print("=" * 60)
    for temp in [0.3, 0.8, 1.2]:
        text = generate(
            model, tok, args.prompt,
            max_tokens=100,
            temperature=temp,
            top_k=args.top_k,
            device=device,
        )
        print(f"\n--- T={temp} ---")
        print(text)
