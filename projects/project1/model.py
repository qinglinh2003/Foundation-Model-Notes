"""
Project 1: MiniGPT Model
--------------------------
Implement a decoder-only Transformer for language modeling.

Architecture requirements:
    - Causal (autoregressive) attention mask
    - Pre-layer normalization (LayerNorm before attention and FFN)
    - Positional encoding: learned absolute or RoPE (configurable)
    - Language modeling head: linear projection to vocab_size (weight-tied with embedding)

You may reference Lab 3 for intuition, but write this implementation independently.
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F

from config import ModelConfig


class CausalSelfAttention(nn.Module):
    """
    Multi-head causal self-attention.

    Inputs:
        x: (B, T, D)  — B=batch, T=sequence length, D=d_model

    Outputs:
        out: (B, T, D)

    Requirements:
        - Position i must NOT attend to position j > i.
        - If using RoPE, apply rotary embeddings to Q and K before the dot product.
    """

    def __init__(self, config: ModelConfig):
        super().__init__()
        assert config.d_model % config.n_heads == 0
        self.config = config
        self.n_heads = config.n_heads
        self.head_dim = config.d_model // config.n_heads
        self.use_rope = config.pos_encoding == "rope"

        self.qkv = nn.Linear(config.d_model, 3 * config.d_model, bias=False)
        self.proj = nn.Linear(config.d_model, config.d_model, bias=False)
        self.dropout = nn.Dropout(config.dropout)

        mask = torch.tril(torch.ones(config.context_length, config.context_length))
        self.register_buffer("causal_mask", mask.view(1, 1, config.context_length, config.context_length))

        if self.use_rope:
            inv_freq = 1.0 / (10000 ** (torch.arange(0, self.head_dim, 2).float() / self.head_dim))
            positions = torch.arange(config.context_length).float()
            freqs = torch.outer(positions, inv_freq)
            self.register_buffer("rope_cos", freqs.cos().view(1, 1, config.context_length, -1))
            self.register_buffer("rope_sin", freqs.sin().view(1, 1, config.context_length, -1))

    def _apply_rope(self, x: torch.Tensor) -> torch.Tensor:
        """Apply rotary position embeddings to a (B, H, T, D_head) tensor."""
        t = x.size(2)
        x_even = x[..., 0::2]
        x_odd = x[..., 1::2]
        cos = self.rope_cos[:, :, :t, :]
        sin = self.rope_sin[:, :, :t, :]

        rotated = torch.empty_like(x)
        rotated[..., 0::2] = x_even * cos - x_odd * sin
        rotated[..., 1::2] = x_even * sin + x_odd * cos
        return rotated

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        b, t, d = x.shape
        q, k, v = self.qkv(x).chunk(3, dim=-1)

        q = q.view(b, t, self.n_heads, self.head_dim).transpose(1, 2)
        k = k.view(b, t, self.n_heads, self.head_dim).transpose(1, 2)
        v = v.view(b, t, self.n_heads, self.head_dim).transpose(1, 2)

        if self.use_rope:
            q = self._apply_rope(q)
            k = self._apply_rope(k)

        scores = q @ k.transpose(-2, -1) / math.sqrt(self.head_dim)
        scores = scores.masked_fill(self.causal_mask[:, :, :t, :t] == 0, float("-inf"))
        attn = F.softmax(scores, dim=-1)
        attn = self.dropout(attn)

        out = attn @ v
        out = out.transpose(1, 2).contiguous().view(b, t, d)
        return self.dropout(self.proj(out))


class FeedForward(nn.Module):
    """
    Position-wise feed-forward network.

    Architecture: Linear(D, 4D) -> GELU -> Linear(4D, D) -> Dropout
    """

    def __init__(self, config: ModelConfig):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(config.d_model, config.d_ff),
            nn.GELU(),
            nn.Linear(config.d_ff, config.d_model),
            nn.Dropout(config.dropout),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


class TransformerBlock(nn.Module):
    """
    One Transformer block with pre-layer normalization.

    Structure:
        x = x + Attention(LayerNorm(x))
        x = x + FFN(LayerNorm(x))
    """

    def __init__(self, config: ModelConfig):
        super().__init__()
        self.ln_1 = nn.LayerNorm(config.d_model)
        self.attn = CausalSelfAttention(config)
        self.ln_2 = nn.LayerNorm(config.d_model)
        self.ffn = FeedForward(config)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.ln_1(x))
        x = x + self.ffn(self.ln_2(x))
        return x


class MiniGPT(nn.Module):
    """
    Full decoder-only language model.

    Components:
        1. Token embedding: (vocab_size, d_model)
        2. Position embedding: (context_length, d_model) if learned; else RoPE in attention
        3. Stack of TransformerBlocks
        4. Final LayerNorm
        5. Language modeling head (linear projection to vocab_size)
           - Weight-tie with token embedding for parameter efficiency

    Forward:
        Input:  token IDs of shape (B, T), dtype=long
        Output: logits of shape (B, T, vocab_size)
    """

    def __init__(self, config: ModelConfig):
        super().__init__()
        self.config = config
        self.token_embedding = nn.Embedding(config.vocab_size, config.d_model)
        self.position_embedding = (
            nn.Embedding(config.context_length, config.d_model)
            if config.pos_encoding == "learned"
            else None
        )
        self.dropout = nn.Dropout(config.dropout)
        self.blocks = nn.ModuleList([TransformerBlock(config) for _ in range(config.n_layers)])
        self.ln_f = nn.LayerNorm(config.d_model)
        self.lm_head = nn.Linear(config.d_model, config.vocab_size, bias=False)
        self.lm_head.weight = self.token_embedding.weight

        self.apply(self._init_weights)
        for name, param in self.named_parameters():
            if name.endswith("proj.weight") or name.endswith("ffn.net.2.weight"):
                nn.init.normal_(param, mean=0.0, std=0.02 / math.sqrt(2 * config.n_layers))

    def _init_weights(self, module: nn.Module) -> None:
        if isinstance(module, nn.Linear):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, idx: torch.Tensor) -> torch.Tensor:
        """
        Args:
            idx: (B, T) tensor of token IDs

        Returns:
            logits: (B, T, vocab_size) tensor of unnormalized log-probabilities
        """
        b, t = idx.shape
        if t > self.config.context_length:
            raise ValueError(f"Sequence length {t} exceeds context length {self.config.context_length}")

        x = self.token_embedding(idx)
        if self.position_embedding is not None:
            pos = torch.arange(t, device=idx.device)
            x = x + self.position_embedding(pos).unsqueeze(0)
        x = self.dropout(x)

        for block in self.blocks:
            x = block(x)
        x = self.ln_f(x)
        return self.lm_head(x)

    def count_parameters(self) -> int:
        """Return total number of trainable parameters."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)


# ---------------------------------------------------------------------------
# Quick test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    cfg = ModelConfig()
    model = MiniGPT(cfg)
    print(f"Parameters: {model.count_parameters():,}")

    # Smoke test: random input
    x = torch.randint(0, cfg.vocab_size, (2, cfg.context_length))
    logits = model(x)
    assert logits.shape == (2, cfg.context_length, cfg.vocab_size), \
        f"Expected (2, {cfg.context_length}, {cfg.vocab_size}), got {logits.shape}"
    print(f"Forward pass OK: {logits.shape}")
