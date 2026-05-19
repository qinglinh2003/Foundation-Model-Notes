"""
Lab 2 — Encoder-Decoder Transformer (vanilla, Vaswani 2017 style)
==================================================================
Reference implementation. Five components correspond directly to Ch2:

    1. ScaledDotProductAttention   (Ch2 §2.2)
    2. make_causal_mask            (Ch2 §2.3.1)
    3. MultiHeadAttention          (Ch2 §2.4)
    4. SinusoidalPositionalEncoding(Ch2 §2.5.2)
    5. TransformerBlock            (Ch2 §2.6, pre-norm)

The TransformerBlock exposes two ablation flags --- `use_residual` and
`use_ffn` --- that drive Experiment 2's rank-collapse study. Setting both
to False yields a "pure SAN" block, the exact configuration Dong et al.
(2021) showed collapses doubly-exponentially with depth.

The top-level Seq2SeqTransformer exposes additional flags for ablating
positional encoding (Exp 3) and causal masking (Exp 1). One model class,
all five experiments.
"""

from __future__ import annotations
import math

import torch
import torch.nn as nn
import torch.nn.functional as F


# ===========================================================================
# 1. Scaled Dot-Product Attention  (Ch2 §2.2)
# ===========================================================================

class ScaledDotProductAttention(nn.Module):
    """
    Attention(Q, K, V) = softmax(Q K^T / sqrt(d_k) + mask) V

    Shapes:
        Q : (B, h, T_q, d_k)
        K : (B, h, T_k, d_k)
        V : (B, h, T_k, d_v)
        mask : additive, broadcastable to (B, h, T_q, T_k); use -inf at
               forbidden positions.
    Returns:
        out  : (B, h, T_q, d_v)
        attn : (B, h, T_q, T_k)   softmax weights
    """

    def forward(self, Q, K, V, mask=None):
        d_k = Q.shape[-1]
        scores = (Q @ K.transpose(-2, -1)) / math.sqrt(d_k)
        if mask is not None:
            scores = scores + mask
        attn = F.softmax(scores, dim=-1)
        out = attn @ V
        return out, attn


# ===========================================================================
# 2. Causal mask  (Ch2 §2.3.1)
# ===========================================================================

def make_causal_mask(T: int, device=None) -> torch.Tensor:
    """
    Lower-triangular additive mask of shape (T, T):
        mask[i, j] = 0     if j <= i
                     -inf  if j  > i
    """
    mask = torch.zeros(T, T, device=device)
    forbidden = torch.triu(
        torch.ones(T, T, device=device, dtype=torch.bool), diagonal=1
    )
    return mask.masked_fill(forbidden, float("-inf"))


# ===========================================================================
# 3. Multi-Head Attention  (Ch2 §2.4)
# ===========================================================================

class MultiHeadAttention(nn.Module):
    """
    h independent attention heads share d_model parameters.
    Each head: d_k = d_v = d_model // h.
    """

    def __init__(self, d_model: int, num_heads: int):
        super().__init__()
        assert d_model % num_heads == 0, "d_model must be divisible by num_heads"
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads

        self.W_q = nn.Linear(d_model, d_model, bias=False)
        self.W_k = nn.Linear(d_model, d_model, bias=False)
        self.W_v = nn.Linear(d_model, d_model, bias=False)
        self.W_o = nn.Linear(d_model, d_model)
        self.attention = ScaledDotProductAttention()

    def forward(self, q_in, k_in, v_in, mask=None):
        """
        q_in : (B, T_q, d_model)
        k_in : (B, T_k, d_model)
        v_in : (B, T_k, d_model)
        mask : (broadcast to) (B, h, T_q, T_k)
        Returns out (B, T_q, d_model), attn (B, h, T_q, T_k).
        """
        B, T_q, _ = q_in.shape
        T_k = k_in.shape[1]

        # Project, then split into heads.
        Q = self.W_q(q_in).view(B, T_q, self.num_heads, self.d_k).transpose(1, 2)
        K = self.W_k(k_in).view(B, T_k, self.num_heads, self.d_k).transpose(1, 2)
        V = self.W_v(v_in).view(B, T_k, self.num_heads, self.d_k).transpose(1, 2)

        out, attn = self.attention(Q, K, V, mask)

        # Concat heads, project.
        out = out.transpose(1, 2).contiguous().view(B, T_q, self.d_model)
        out = self.W_o(out)
        return out, attn


# ===========================================================================
# 4. Sinusoidal Positional Encoding  (Ch2 §2.5.2)
# ===========================================================================

class SinusoidalPositionalEncoding(nn.Module):
    """
    PE(t, 2i)   = sin(t / 10000^(2i / d_model))
    PE(t, 2i+1) = cos(t / 10000^(2i / d_model))
    """

    def __init__(self, d_model: int, max_len: int = 64):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2, dtype=torch.float)
            * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        self.register_buffer("pe", pe.unsqueeze(0))  # (1, max_len, d_model)

    def forward(self, x):
        """x: (B, T, d_model) -> x + PE[:T]"""
        return x + self.pe[:, : x.size(1)]


# ===========================================================================
# 5. Transformer block (configurable, pre-norm)  (Ch2 §2.6)
# ===========================================================================

class FFN(nn.Module):
    """Position-wise FFN: Linear -> ReLU -> Linear."""

    def __init__(self, d_model: int, d_ffn: int, dropout: float = 0.1):
        super().__init__()
        self.fc1 = nn.Linear(d_model, d_ffn)
        self.fc2 = nn.Linear(d_ffn, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        return self.fc2(self.dropout(F.relu(self.fc1(x))))


class TransformerBlock(nn.Module):
    """
    Pre-norm block:
        z = x + sublayer(LayerNorm(x))

    Encoder mode (is_decoder=False):
        sublayers = [ self-attn, FFN ]

    Decoder mode (is_decoder=True):
        sublayers = [ masked self-attn, cross-attn, FFN ]

    Ablation flags:
        use_residual=False : drop the `x +` skip on every sublayer.
                             Triggers Dong-style rank collapse with depth.
        use_ffn=False      : bypass the FFN sublayer entirely.
                             Tests whether attention's weighted averaging
                             can replace per-token nonlinearity.
    """

    def __init__(
        self,
        d_model: int,
        num_heads: int,
        d_ffn: int,
        is_decoder: bool = False,
        use_residual: bool = True,
        use_ffn: bool = True,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.is_decoder = is_decoder
        self.use_residual = use_residual
        self.use_ffn = use_ffn

        self.norm1 = nn.LayerNorm(d_model)
        self.self_attn = MultiHeadAttention(d_model, num_heads)

        if is_decoder:
            self.norm2 = nn.LayerNorm(d_model)
            self.cross_attn = MultiHeadAttention(d_model, num_heads)

        if use_ffn:
            self.norm3 = nn.LayerNorm(d_model)
            self.ffn = FFN(d_model, d_ffn, dropout)

        self.dropout = nn.Dropout(dropout)

    def _maybe_add(self, x, sublayer_out):
        """x + dropout(sublayer) when use_residual; else dropout(sublayer)."""
        if self.use_residual:
            return x + self.dropout(sublayer_out)
        return self.dropout(sublayer_out)

    def forward(self, x, self_mask=None, cross_kv=None, cross_mask=None):
        # ---- self-attention sublayer ----
        z = self.norm1(x)
        sa_out, self_w = self.self_attn(z, z, z, mask=self_mask)
        x = self._maybe_add(x, sa_out)

        # ---- cross-attention sublayer (decoder only) ----
        cross_w = None
        if self.is_decoder:
            z = self.norm2(x)
            ca_out, cross_w = self.cross_attn(z, cross_kv, cross_kv, mask=cross_mask)
            x = self._maybe_add(x, ca_out)

        # ---- FFN sublayer ----
        if self.use_ffn:
            z = self.norm3(x)
            x = self._maybe_add(x, self.ffn(z))

        return x, self_w, cross_w


# ===========================================================================
# Encoder / Decoder / Seq2SeqTransformer  (assembly, all provided)
# ===========================================================================

class Encoder(nn.Module):
    def __init__(
        self, vocab_size, d_model, num_heads, d_ffn, num_layers, max_len,
        pad_idx, use_pe=True, use_residual=True, use_ffn=True, dropout=0.1,
    ):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, d_model, padding_idx=pad_idx)
        self.pe = SinusoidalPositionalEncoding(d_model, max_len) if use_pe else None
        self.dropout = nn.Dropout(dropout)
        self.blocks = nn.ModuleList([
            TransformerBlock(d_model, num_heads, d_ffn, is_decoder=False,
                             use_residual=use_residual, use_ffn=use_ffn,
                             dropout=dropout)
            for _ in range(num_layers)
        ])
        self.norm = nn.LayerNorm(d_model)

    def forward(self, src, src_pad_mask=None):
        x = self.embed(src)
        if self.pe is not None:
            x = self.pe(x)
        x = self.dropout(x)
        attn_weights = []
        for block in self.blocks:
            x, w, _ = block(x, self_mask=src_pad_mask)
            attn_weights.append(w)
        return self.norm(x), attn_weights


class Decoder(nn.Module):
    def __init__(
        self, vocab_size, d_model, num_heads, d_ffn, num_layers, max_len,
        pad_idx, use_pe=True, use_residual=True, use_ffn=True, dropout=0.1,
    ):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, d_model, padding_idx=pad_idx)
        self.pe = SinusoidalPositionalEncoding(d_model, max_len) if use_pe else None
        self.dropout = nn.Dropout(dropout)
        self.blocks = nn.ModuleList([
            TransformerBlock(d_model, num_heads, d_ffn, is_decoder=True,
                             use_residual=use_residual, use_ffn=use_ffn,
                             dropout=dropout)
            for _ in range(num_layers)
        ])
        self.norm = nn.LayerNorm(d_model)
        self.fc = nn.Linear(d_model, vocab_size)

    def forward(self, tgt, memory, tgt_self_mask=None, mem_pad_mask=None):
        x = self.embed(tgt)
        if self.pe is not None:
            x = self.pe(x)
        x = self.dropout(x)
        self_ws, cross_ws = [], []
        for block in self.blocks:
            x, sw, cw = block(x, self_mask=tgt_self_mask,
                              cross_kv=memory, cross_mask=mem_pad_mask)
            self_ws.append(sw)
            cross_ws.append(cw)
        return self.fc(self.norm(x)), self_ws, cross_ws


class Seq2SeqTransformer(nn.Module):
    """
    Single configurable model class drives all five experiments.

    Constructor flags:
        use_encoder_pe   : encoder positional encoding on/off  (Exp 3)
        use_decoder_pe   : decoder positional encoding on/off  (Exp 3)
        use_causal_mask  : decoder causal mask on/off          (Exp 1)
        use_residual     : skip connections on/off             (Exp 2)
        use_ffn          : FFN sublayer on/off                 (Exp 2)
        num_heads        : multi-head count                    (Exp 4)
    """

    def __init__(
        self,
        vocab_size: int,
        d_model: int = 128,
        num_heads: int = 4,
        d_ffn: int = 512,
        num_enc_layers: int = 2,
        num_dec_layers: int = 2,
        max_len: int = 32,
        pad_idx: int = 0,
        use_encoder_pe: bool = True,
        use_decoder_pe: bool = True,
        use_causal_mask: bool = True,
        use_residual: bool = True,
        use_ffn: bool = True,
        dropout: float = 0.1,
    ):
        super().__init__()
        self.pad_idx = pad_idx
        self.use_causal_mask = use_causal_mask

        self.encoder = Encoder(
            vocab_size, d_model, num_heads, d_ffn, num_enc_layers, max_len,
            pad_idx, use_pe=use_encoder_pe, use_residual=use_residual,
            use_ffn=use_ffn, dropout=dropout,
        )
        self.decoder = Decoder(
            vocab_size, d_model, num_heads, d_ffn, num_dec_layers, max_len,
            pad_idx, use_pe=use_decoder_pe, use_residual=use_residual,
            use_ffn=use_ffn, dropout=dropout,
        )

    def make_pad_mask(self, seq: torch.Tensor) -> torch.Tensor:
        """(B, T) -> (B, 1, 1, T) additive: 0 for real tokens, -inf for pad."""
        is_pad = (seq == self.pad_idx).unsqueeze(1).unsqueeze(2)  # (B, 1, 1, T)
        mask = torch.zeros_like(is_pad, dtype=torch.float)
        return mask.masked_fill(is_pad, float("-inf"))

    def forward(self, src, dec_in):
        """
        src    : (B, T_src)
        dec_in : (B, T_tgt)
        Returns:
            logits        : (B, T_tgt, vocab_size)
            cross_weights : list of (B, num_heads, T_tgt, T_src) per layer
        """
        src_pad = self.make_pad_mask(src)
        memory, _ = self.encoder(src, src_pad)

        tgt_pad = self.make_pad_mask(dec_in)
        if self.use_causal_mask:
            causal = make_causal_mask(dec_in.size(1), device=dec_in.device)
            tgt_self_mask = tgt_pad + causal.unsqueeze(0).unsqueeze(0)
        else:
            tgt_self_mask = tgt_pad

        logits, _, cross_ws = self.decoder(
            dec_in, memory, tgt_self_mask=tgt_self_mask, mem_pad_mask=src_pad,
        )
        return logits, cross_ws

    @torch.no_grad()
    def greedy_decode(self, src, sos_idx: int, eos_idx: int, max_len: int = 14):
        """Autoregressive greedy decoding for evaluation/generation."""
        self.eval()
        B = src.size(0)
        device = src.device

        src_pad = self.make_pad_mask(src)
        memory, _ = self.encoder(src, src_pad)

        dec = torch.full((B, 1), sos_idx, dtype=torch.long, device=device)
        finished = torch.zeros(B, dtype=torch.bool, device=device)
        for _ in range(max_len - 1):
            tgt_pad = self.make_pad_mask(dec)
            if self.use_causal_mask:
                causal = make_causal_mask(dec.size(1), device=device)
                tgt_self_mask = tgt_pad + causal.unsqueeze(0).unsqueeze(0)
            else:
                tgt_self_mask = tgt_pad
            logits, _, _ = self.decoder(
                dec, memory, tgt_self_mask=tgt_self_mask, mem_pad_mask=src_pad,
            )
            next_tok = logits[:, -1, :].argmax(dim=-1, keepdim=True)
            dec = torch.cat([dec, next_tok], dim=1)
            finished = finished | (next_tok.squeeze(1) == eos_idx)
            if finished.all():
                break
        return dec


# ===========================================================================
# Smoke test
# ===========================================================================

if __name__ == "__main__":
    from data import build_dataloaders

    train_loader, _, _, vocab, _ = build_dataloaders(batch_size=8)
    batch = next(iter(train_loader))

    print("=== Vanilla baseline ===")
    model = Seq2SeqTransformer(vocab_size=vocab.size, pad_idx=vocab.pad_idx)
    logits, cross = model(batch["src"], batch["dec_in"])
    loss = F.cross_entropy(
        logits.reshape(-1, vocab.size),
        batch["dec_out"].reshape(-1),
        ignore_index=vocab.pad_idx,
    )
    loss.backward()
    print(f"  param count       {sum(p.numel() for p in model.parameters()):,}")
    print(f"  logits shape      {tuple(logits.shape)}")
    print(f"  cross-attn shape  {tuple(cross[0].shape)}  (B, h, T_tgt, T_src)")
    print(f"  forward loss      {loss.item():.4f}")

    pred = model.greedy_decode(batch["src"], vocab.sos_idx, vocab.eos_idx)
    print(f"  greedy decode     {tuple(pred.shape)}")
    for i in range(min(5, pred.size(0))):
        print(f"    {batch['lemma'][i]:8s} ({batch['tag'][i]:7s}) -> "
              f"pred={vocab.decode(pred[i, 1:].tolist())!r:12s} gold={batch['inflected'][i]!r}")

    print("\n=== Pure SAN ablation (no residual, no FFN) ===")
    san = Seq2SeqTransformer(vocab_size=vocab.size, pad_idx=vocab.pad_idx,
                             use_residual=False, use_ffn=False)
    logits, _ = san(batch["src"], batch["dec_in"])
    print(f"  param count       {sum(p.numel() for p in san.parameters()):,}")
    print(f"  forward OK")
