"""
Lab 3 — Model definitions
==========================
A configurable mini decoder-only GPT for architecture diagnostics.

The implementation is complete so the lab can be run end to end. Experiment 0
still compares a deliberately buggy local no-shift loss against the correct
shifted loss below.
"""

import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from dataclasses import dataclass
from typing import Optional


# ===================================================================
# Configuration
# ===================================================================

@dataclass
class GPTConfig:
    """All architecture hyperparameters in one place."""
    vocab_size: int = 65          # Tiny Shakespeare has ~65 characters
    seq_len: int = 256
    d_model: int = 128
    n_heads: int = 4
    n_layers: int = 4
    ffn_mult: int = 4             # FFN inner dim = ffn_mult * d_model
    dropout: float = 0.1
    use_residual: bool = True     # Toggle for Exp 1
    norm_type: str = "pre"        # "pre" or "post", for Exp 1
    pe_type: str = "learned"      # "none", "learned", "rope", for Exp 2
    weight_tying: bool = True


# ===================================================================
# Positional Encoding variants
# ===================================================================

class LearnedPE(nn.Module):
    """Learned absolute positional embeddings (GPT-2 style)."""

    def __init__(self, seq_len: int, d_model: int):
        super().__init__()
        self.pe = nn.Embedding(seq_len, d_model)

    def forward(self, x: torch.Tensor, offset: int = 0) -> torch.Tensor:
        """Add positional embeddings. x: [B, T, D]

        offset is required for KV-cache decoding. If we decode one token at
        a time, that token must receive its true absolute position rather than
        position 0 on every step.
        """
        T = x.size(1)
        positions = torch.arange(offset, offset + T, device=x.device)
        return x + self.pe(positions)


class RoPE(nn.Module):
    """
    Rotary Position Embedding.
    Applied directly to Q and K inside attention, not to the residual stream.
    """

    def __init__(self, d_head: int, max_len: int = 4096):
        super().__init__()
        # Precompute frequency bands
        freqs = 1.0 / (10000.0 ** (torch.arange(0, d_head, 2).float() / d_head))
        self.register_buffer("freqs", freqs)
        # Precompute sin/cos for max_len positions
        t = torch.arange(max_len).float()
        angles = torch.outer(t, freqs)  # [max_len, d_head/2]
        self.register_buffer("cos_cached", angles.cos())  # [max_len, d_head/2]
        self.register_buffer("sin_cached", angles.sin())  # [max_len, d_head/2]

    def forward(self, x: torch.Tensor, offset: int = 0) -> torch.Tensor:
        """
        Apply rotary embedding to x.
        x: [B, n_heads, T, d_head]
        offset: starting position (for KV cache incremental decoding)
        """
        T = x.size(2)
        cos = self.cos_cached[offset : offset + T]  # [T, d_head/2]
        sin = self.sin_cached[offset : offset + T]  # [T, d_head/2]

        # Split into pairs and rotate
        x1, x2 = x[..., ::2], x[..., 1::2]  # even and odd dimensions
        # Apply rotation: [x1, x2] -> [x1*cos - x2*sin, x1*sin + x2*cos]
        out = torch.stack([x1 * cos - x2 * sin, x1 * sin + x2 * cos], dim=-1)
        return out.flatten(-2)  # merge last two dims back


# ===================================================================
# Multi-Head Self-Attention
# ===================================================================

class MultiHeadSelfAttention(nn.Module):
    """Standard multi-head causal self-attention."""

    def __init__(self, config: GPTConfig):
        super().__init__()
        self.n_heads = config.n_heads
        self.d_head = config.d_model // config.n_heads
        self.d_model = config.d_model

        self.qkv_proj = nn.Linear(config.d_model, 3 * config.d_model, bias=False)
        self.out_proj = nn.Linear(config.d_model, config.d_model, bias=False)
        self.dropout = nn.Dropout(config.dropout)
        self.scale = math.sqrt(self.d_head)

        # RoPE (only used if config.pe_type == "rope")
        self.rope = RoPE(self.d_head, max_len=config.seq_len * 2) if config.pe_type == "rope" else None

    def forward(self, x: torch.Tensor, kv_cache: Optional[tuple] = None,
                offset: int = 0) -> tuple:
        """
        Args:
            x: [B, T, D]
            kv_cache: optional (cached_K, cached_V) each [B, n_heads, T_past, d_head]
            offset: position offset for RoPE when using KV cache

        Returns:
            output: [B, T, D]
            new_kv_cache: (K, V) for caching
        """
        B, T, D = x.shape

        # Project to Q, K, V
        qkv = self.qkv_proj(x)  # [B, T, 3*D]
        q, k, v = qkv.chunk(3, dim=-1)

        # Reshape to [B, n_heads, T, d_head]
        q = q.view(B, T, self.n_heads, self.d_head).transpose(1, 2)
        k = k.view(B, T, self.n_heads, self.d_head).transpose(1, 2)
        v = v.view(B, T, self.n_heads, self.d_head).transpose(1, 2)

        # Apply RoPE if configured
        if self.rope is not None:
            q = self.rope(q, offset=offset)
            k = self.rope(k, offset=offset)

        # Append to KV cache if provided
        if kv_cache is not None:
            past_k, past_v = kv_cache
            k = torch.cat([past_k, k], dim=2)  # [B, n_heads, T_past+T, d_head]
            v = torch.cat([past_v, v], dim=2)

        new_kv_cache = (k, v)

        # Compute attention scores
        scores = torch.matmul(q, k.transpose(-2, -1)) / self.scale  # [B, H, T, T_kv]

        # Causal mask: each query position can only attend to current and past
        T_kv = k.size(2)
        causal_mask = torch.triu(
            torch.ones(T, T_kv, device=x.device, dtype=torch.bool),
            diagonal=T_kv - T + 1
        )
        scores = scores.masked_fill(causal_mask.unsqueeze(0).unsqueeze(0), float("-inf"))

        # Softmax + dropout + weighted sum
        attn_weights = F.softmax(scores, dim=-1)
        attn_weights = self.dropout(attn_weights)
        out = torch.matmul(attn_weights, v)  # [B, H, T, d_head]

        # Reshape back to [B, T, D]
        out = out.transpose(1, 2).contiguous().view(B, T, D)
        out = self.out_proj(out)
        return out, new_kv_cache


# ===================================================================
# Feed-Forward Network
# ===================================================================

class FFN(nn.Module):
    """Standard two-layer MLP with GELU activation."""

    def __init__(self, config: GPTConfig):
        super().__init__()
        inner_dim = config.d_model * config.ffn_mult
        self.fc1 = nn.Linear(config.d_model, inner_dim, bias=False)
        self.fc2 = nn.Linear(inner_dim, config.d_model, bias=False)
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.dropout(self.fc2(F.gelu(self.fc1(x))))


# ===================================================================
# Decoder Block
# ===================================================================

class DecoderBlock(nn.Module):
    """
    A single Transformer decoder block.

    Supports pre-norm and post-norm configurations, and optional residual.
    """

    def __init__(self, config: GPTConfig):
        super().__init__()
        self.attn = MultiHeadSelfAttention(config)
        self.ffn = FFN(config)
        self.ln1 = nn.LayerNorm(config.d_model)
        self.ln2 = nn.LayerNorm(config.d_model)
        self.use_residual = config.use_residual
        self.norm_type = config.norm_type
        self.dropout = nn.Dropout(config.dropout)

    def forward(self, x: torch.Tensor, kv_cache: Optional[tuple] = None,
                offset: int = 0) -> tuple:
        """
        Args:
            x: [B, T, D]
            kv_cache: optional KV cache for this layer
            offset: position offset for RoPE

        Returns:
            output: [B, T, D]
            new_kv_cache: updated cache for this layer
        """
        if self.norm_type == "pre":
            # Pre-norm: normalize before sublayer, residual around sublayer
            attn_out, new_cache = self.attn(self.ln1(x), kv_cache, offset)
            if self.use_residual:
                x = x + self.dropout(attn_out)
            else:
                x = self.dropout(attn_out)
            ffn_out = self.ffn(self.ln2(x))
            if self.use_residual:
                x = x + self.dropout(ffn_out)
            else:
                x = self.dropout(ffn_out)
        else:
            # Post-norm: normalize after residual addition
            attn_out, new_cache = self.attn(x, kv_cache, offset)
            if self.use_residual:
                x = self.ln1(x + self.dropout(attn_out))
            else:
                x = self.ln1(self.dropout(attn_out))
            ffn_out = self.ffn(x)
            if self.use_residual:
                x = self.ln2(x + self.dropout(ffn_out))
            else:
                x = self.ln2(self.dropout(ffn_out))

        return x, new_cache


# ===================================================================
# Full GPT Model
# ===================================================================

class GPT(nn.Module):
    """
    Minimal decoder-only GPT.

    Architecture:
        token_emb -> [+ pos_emb] -> N x DecoderBlock -> final_norm -> lm_head
    """

    def __init__(self, config: GPTConfig):
        super().__init__()
        self.config = config

        # Token embedding
        self.token_emb = nn.Embedding(config.vocab_size, config.d_model)

        # Positional encoding (depends on config.pe_type)
        if config.pe_type == "learned":
            self.pos_enc = LearnedPE(config.seq_len, config.d_model)
        else:
            # "none" or "rope" — RoPE is applied inside attention, not here
            self.pos_enc = None

        # Decoder blocks
        self.blocks = nn.ModuleList([
            DecoderBlock(config) for _ in range(config.n_layers)
        ])

        # Final layer norm and LM head
        self.final_norm = nn.LayerNorm(config.d_model)
        self.lm_head = nn.Linear(config.d_model, config.vocab_size, bias=False)

        # Weight tying
        if config.weight_tying:
            self.lm_head.weight = self.token_emb.weight

        # Initialize weights
        self.apply(self._init_weights)

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, input_ids: torch.Tensor,
                kv_caches: Optional[list] = None) -> tuple:
        """
        Args:
            input_ids: [B, T] token indices
            kv_caches: optional list of (K, V) tuples, one per layer.
                       If provided, input_ids should be the NEW tokens only.

        Returns:
            logits: [B, T, vocab_size]
            new_kv_caches: list of (K, V) tuples for all layers
        """
        # Determine offset from KV cache
        if kv_caches is not None and kv_caches[0] is not None:
            offset = kv_caches[0][0].size(2)  # T_past
        else:
            offset = 0

        # Token embeddings
        x = self.token_emb(input_ids)

        # Positional encoding (learned PE needs offset for cache decoding)
        if self.pos_enc is not None:
            x = self.pos_enc(x, offset=offset)

        # Pass through decoder blocks
        new_kv_caches = []
        for i, block in enumerate(self.blocks):
            cache_i = kv_caches[i] if kv_caches else None
            x, new_cache = block(x, kv_cache=cache_i, offset=offset)
            new_kv_caches.append(new_cache)

        # Final norm and LM head
        x = self.final_norm(x)
        logits = self.lm_head(x)

        return logits, new_kv_caches

    @torch.no_grad()
    def generate(self, prompt_ids: torch.Tensor, max_new_tokens: int = 200,
                 temperature: float = 1.0, use_cache: bool = True) -> torch.Tensor:
        """
        Autoregressive generation.

        Args:
            prompt_ids: [1, T_prompt] initial token indices
            max_new_tokens: number of tokens to generate
            temperature: sampling temperature (1.0 = unchanged)
            use_cache: if True, use KV cache for efficiency

        Returns:
            generated: [1, T_prompt + max_new_tokens] full sequence
        """
        self.eval()
        generated = prompt_ids.clone()
        kv_caches = None

        if use_cache:
            # Prefill: process full prompt at once
            logits, kv_caches = self(generated)
            next_logits = logits[:, -1, :] / temperature
            probs = F.softmax(next_logits, dim=-1)
            next_token = torch.multinomial(probs, num_samples=1)
            generated = torch.cat([generated, next_token], dim=1)

            # Decode: one token at a time with cache
            for _ in range(max_new_tokens - 1):
                logits, kv_caches = self(next_token, kv_caches=kv_caches)
                next_logits = logits[:, -1, :] / temperature
                probs = F.softmax(next_logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)
                generated = torch.cat([generated, next_token], dim=1)
        else:
            # No cache: feed entire sequence each step
            for _ in range(max_new_tokens):
                logits, _ = self(generated)
                next_logits = logits[:, -1, :] / temperature
                probs = F.softmax(next_logits, dim=-1)
                next_token = torch.multinomial(probs, num_samples=1)
                generated = torch.cat([generated, next_token], dim=1)

        return generated


# ===================================================================
# Loss function
# ===================================================================

def shifted_ce_loss(logits: torch.Tensor, input_ids: torch.Tensor) -> torch.Tensor:
    """
    Compute cross-entropy loss for next-token prediction.

    Args:
        logits: [B, T, V] raw model outputs
        input_ids: [B, T] input token indices (same as fed to model)

    Returns:
        scalar loss
    """
    B, T, V = logits.shape
    # Correct shifted loss: logits[:, t] predicts input_ids[:, t+1]
    logits_shifted = logits[:, :-1, :].contiguous()
    targets_shifted = input_ids[:, 1:].contiguous()
    loss = F.cross_entropy(
        logits_shifted.view(-1, V),
        targets_shifted.view(-1)
    )
    return loss
