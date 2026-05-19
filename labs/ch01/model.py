"""
Lab 1 — Model definitions
==========================
All models for Lab 1 experiments.

Sections marked with  # TODO: YOUR CODE HERE  require student implementation.
The surrounding scaffolding (class structure, forward signatures, helper
methods) is provided so students can focus on the core logic.
"""

import torch
import torch.nn as nn
import torch.nn.functional as F


# ===================================================================
# Experiments 1–3: Character-level language model (RNN / LSTM / GRU)
# ===================================================================

class CharLM(nn.Module):
    """
    Character-level language model with switchable recurrent core.

    Args:
        vocab_size  : number of characters in vocabulary
        embed_dim   : character embedding dimension (default 64)
        hidden_size : recurrent hidden state size (default 256)
        rnn_type    : one of "rnn", "lstm", "gru"
        num_layers  : number of recurrent layers (default 1)
    """

    def __init__(self, vocab_size: int, embed_dim: int = 64,
                 hidden_size: int = 256, rnn_type: str = "lstm",
                 num_layers: int = 1):
        super().__init__()
        self.rnn_type = rnn_type.lower()
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        # ---------------------------------------------------------------
        # Embedding layer: maps character indices → dense vectors
        # ---------------------------------------------------------------
        self.embedding = nn.Embedding(vocab_size, embed_dim)

        # ---------------------------------------------------------------
        # Recurrent core
        # ---------------------------------------------------------------
        rnn_cls = {"rnn": nn.RNN, "lstm": nn.LSTM, "gru": nn.GRU}[self.rnn_type]
        self.rnn = rnn_cls(embed_dim, hidden_size, num_layers=num_layers,
                           batch_first=True)

        # ---------------------------------------------------------------
        # Output projection: hidden state → logits over vocabulary
        # ---------------------------------------------------------------
        self.fc = nn.Linear(hidden_size, vocab_size)

    def forward(self, x, hidden=None):
        """
        Args:
            x      : (batch, seq_len) integer token indices
            hidden : previous hidden state (None on first call)

        Returns:
            logits : (batch, seq_len, vocab_size)
            hidden : updated hidden state (detached from graph)
        """
        emb = self.embedding(x)                  # (batch, seq_len, embed_dim)
        output, hidden = self.rnn(emb, hidden)   # (batch, seq_len, hidden_size)
        logits = self.fc(output)                  # (batch, seq_len, vocab_size)

        # ---------------------------------------------------------------
        # Detach hidden state to truncate BPTT
        # ---------------------------------------------------------------
        if self.rnn_type == "lstm":
            hidden = (hidden[0].detach(), hidden[1].detach())
        else:
            hidden = hidden.detach()

        return logits, hidden

    def count_parameters(self):
        return sum(p.numel() for p in self.parameters())


# ===================================================================
# Experiment 2: Delayed-memory probe classifier
# ===================================================================

class DelayedMemoryClassifier(nn.Module):
    """
    Reads a sequence and predicts the signal token based on the
    hidden state at the [QUERY] position.

    Args:
        vocab_size  : total vocabulary size (content + special tokens)
        embed_dim   : embedding dimension (default 32)
        hidden_size : recurrent hidden size (default 128)
        num_classes : number of possible signal tokens
        rnn_type    : "rnn", "lstm", or "gru"
    """

    def __init__(self, vocab_size: int, embed_dim: int = 32,
                 hidden_size: int = 128, num_classes: int = 10,
                 rnn_type: str = "lstm", pad_idx: int = 2):
        super().__init__()
        self.rnn_type = rnn_type.lower()
        self.pad_idx = pad_idx

        self.embedding = nn.Embedding(vocab_size, embed_dim)

        # ---------------------------------------------------------------
        # Recurrent core
        # ---------------------------------------------------------------
        rnn_cls = {"rnn": nn.RNN, "lstm": nn.LSTM, "gru": nn.GRU}[self.rnn_type]
        self.rnn = rnn_cls(embed_dim, hidden_size, batch_first=True)

        # Classification head: final hidden state → class logits
        self.classifier = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        """
        Args:
            x : (batch, seq_len) integer token indices

        Returns:
            logits : (batch, num_classes)
        """
        emb = self.embedding(x)
        output, _ = self.rnn(emb)   # (batch, seq_len, hidden_size)

        # ---------------------------------------------------------------
        # Extract hidden state at last valid (non-PAD) position
        # ---------------------------------------------------------------
        lengths = (x != self.pad_idx).sum(dim=1)  # (batch,)
        batch_idx = torch.arange(x.size(0), device=x.device)
        last_hidden = output[batch_idx, lengths - 1]  # (batch, hidden_size)

        logits = self.classifier(last_hidden)
        return logits


# ===================================================================
# Experiment 4: Seq2Seq with optional attention
# ===================================================================

class Encoder(nn.Module):
    """LSTM encoder: maps source sequence → hidden states + final state."""

    def __init__(self, vocab_size: int, embed_dim: int = 64,
                 hidden_size: int = 128):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.rnn = nn.LSTM(embed_dim, hidden_size, batch_first=True)

    def forward(self, src):
        """
        Args:
            src : (batch, src_len)

        Returns:
            outputs : (batch, src_len, hidden_size)  — all hidden states
            hidden  : (h_n, c_n) — final hidden state
        """
        emb = self.embedding(src)
        outputs, hidden = self.rnn(emb)
        return outputs, hidden


class Decoder(nn.Module):
    """
    LSTM decoder with OPTIONAL Bahdanau (additive) attention.

    Args:
        vocab_size   : target vocabulary size
        embed_dim    : target embedding dimension
        hidden_size  : must match encoder hidden size
        use_attention: if True, apply Bahdanau attention
    """

    def __init__(self, vocab_size: int, embed_dim: int = 64,
                 hidden_size: int = 128, use_attention: bool = False):
        super().__init__()
        self.use_attention = use_attention
        self.hidden_size = hidden_size

        self.embedding = nn.Embedding(vocab_size, embed_dim)

        # If using attention, decoder input = embed_dim + hidden_size
        # (because we concatenate context vector with embedding)
        rnn_input_size = embed_dim + hidden_size if use_attention else embed_dim
        self.rnn = nn.LSTM(rnn_input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, vocab_size)

        if use_attention:
            # ---------------------------------------------------------------
            # Bahdanau (additive) attention projection layers
            # ---------------------------------------------------------------
            self.W1 = nn.Linear(hidden_size, hidden_size, bias=False)
            self.W2 = nn.Linear(hidden_size, hidden_size, bias=False)
            self.V = nn.Linear(hidden_size, 1, bias=False)

    def _compute_attention(self, decoder_hidden, encoder_outputs):
        """
        Bahdanau attention.

        Args:
            decoder_hidden  : (batch, hidden_size) — current decoder state
            encoder_outputs : (batch, src_len, hidden_size)

        Returns:
            context : (batch, 1, hidden_size) — weighted sum of encoder states
            weights : (batch, src_len) — attention weights (for visualization)
        """
        # ---------------------------------------------------------------
        # Bahdanau attention scoring
        # ---------------------------------------------------------------
        query = self.W1(decoder_hidden).unsqueeze(1)    # (batch, 1, hidden)
        keys = self.W2(encoder_outputs)                  # (batch, src_len, hidden)
        scores = self.V(torch.tanh(query + keys))        # (batch, src_len, 1)
        scores = scores.squeeze(-1)                      # (batch, src_len)
        weights = F.softmax(scores, dim=-1)              # (batch, src_len)
        context = torch.bmm(weights.unsqueeze(1), encoder_outputs)  # (batch, 1, hidden)
        return context, weights

    def forward(self, dec_input, hidden, encoder_outputs=None):
        """
        Args:
            dec_input       : (batch, tgt_len) target token indices
            hidden          : (h, c) from encoder or previous step
            encoder_outputs : (batch, src_len, hidden_size), needed if attention

        Returns:
            logits          : (batch, tgt_len, vocab_size)
            hidden          : updated hidden state
            attn_weights    : (batch, tgt_len, src_len) or None
        """
        emb = self.embedding(dec_input)   # (batch, tgt_len, embed_dim)

        if not self.use_attention:
            # ---------------------------------------------------------------
            # No attention: just run decoder LSTM on embeddings
            # ---------------------------------------------------------------
            output, hidden = self.rnn(emb, hidden)
            logits = self.fc(output)
            return logits, hidden, None

        # ---------------------------------------------------------------
        # With attention: step through one token at a time
        # ---------------------------------------------------------------
        outputs = []
        attn_weights_all = []

        for t in range(emb.size(1)):
            # Current decoder hidden for attention query
            h_t = hidden[0][-1]  # (batch, hidden_size) — last layer h

            # ---------------------------------------------------------------
            # Attention decoder forward step
            # ---------------------------------------------------------------
            context, attn_w = self._compute_attention(h_t, encoder_outputs)
            rnn_input = torch.cat([emb[:, t:t+1, :], context], dim=-1)
            output, hidden = self.rnn(rnn_input, hidden)
            outputs.append(output)
            attn_weights_all.append(attn_w)

        outputs = torch.cat(outputs, dim=1)         # (batch, tgt_len, hidden)
        logits = self.fc(outputs)                     # (batch, tgt_len, vocab)
        attn_weights = torch.stack(attn_weights_all, dim=1)  # (batch, tgt, src)
        return logits, hidden, attn_weights


class Seq2Seq(nn.Module):
    """Wraps Encoder + Decoder into a single module."""

    def __init__(self, src_vocab_size: int, tgt_vocab_size: int,
                 embed_dim: int = 64, hidden_size: int = 128,
                 use_attention: bool = False):
        super().__init__()
        self.encoder = Encoder(src_vocab_size, embed_dim, hidden_size)
        self.decoder = Decoder(tgt_vocab_size, embed_dim, hidden_size,
                               use_attention)

    def forward(self, src, dec_input):
        """
        Args:
            src       : (batch, src_len)
            dec_input : (batch, tgt_len)

        Returns:
            logits      : (batch, tgt_len, tgt_vocab_size)
            attn_weights: (batch, tgt_len, src_len) or None
        """
        encoder_outputs, hidden = self.encoder(src)
        logits, _, attn_weights = self.decoder(
            dec_input, hidden,
            encoder_outputs if self.decoder.use_attention else None
        )
        return logits, attn_weights

    @torch.no_grad()
    def greedy_decode(self, src, sos_idx: int, max_len: int):
        """
        Autoregressive greedy decoding for evaluation.

        Args:
            src     : (batch, src_len)
            sos_idx : decoder start token
            max_len : number of tokens to generate

        Returns:
            preds        : (batch, max_len)
            attn_weights : (batch, max_len, src_len) or None
        """
        encoder_outputs, hidden = self.encoder(src)
        batch_size = src.size(0)
        dec_input = torch.full(
            (batch_size, 1), sos_idx, dtype=torch.long, device=src.device
        )
        preds = []
        weights = []

        for _ in range(max_len):
            logits, hidden, attn = self.decoder(
                dec_input,
                hidden,
                encoder_outputs if self.decoder.use_attention else None,
            )
            next_token = logits[:, -1, :].argmax(dim=-1, keepdim=True)
            preds.append(next_token)
            if attn is not None:
                weights.append(attn[:, -1, :])
            dec_input = next_token

        preds = torch.cat(preds, dim=1)
        if weights:
            weights = torch.stack(weights, dim=1)
        else:
            weights = None
        return preds, weights
