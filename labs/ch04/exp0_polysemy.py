"""
Lab 4 — Experiment 0: Polysemy Sanity Check
============================================
Corresponds to: Ch.4 Sec.4.2 (bidirectional attention)

Closes the loop from Lab 1 Exp 0: static embeddings cannot distinguish
polysemous words. BERT's contextual embeddings can.

Measures cosine distance between the same word in different contexts.

Usage:
    python exp0_polysemy.py
"""

import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
from data import POLYSEMY_EXAMPLES


def get_word_embedding(model, tokenizer, sentence, target_word, device):
    """
    Extract the contextual embedding for `target_word` in `sentence`.
    If the word is split into subwords, average the subword embeddings.
    """
    inputs = tokenizer(sentence, return_tensors="pt", padding=True,
                       truncation=True, max_length=128).to(device)

    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
    hidden = outputs.hidden_states[-1][0]  # [seq_len, hidden]

    # Find token positions for the target word
    tokens = tokenizer.tokenize(sentence)
    token_ids = tokenizer.encode(sentence, add_special_tokens=True)

    # Find the target word in the original tokens
    target_tokens = tokenizer.tokenize(target_word)
    target_len = len(target_tokens)

    # Search for the target subword sequence
    for i in range(len(tokens)):
        if tokens[i:i + target_len] == target_tokens:
            # +1 for [CLS] token offset
            start = i + 1
            end = start + target_len
            word_emb = hidden[start:end].mean(dim=0)
            return word_emb

    # Fallback: try case-insensitive match on first subword
    target_lower = target_tokens[0].lower().replace("##", "")
    for i, tok in enumerate(tokens):
        if target_lower in tok.lower():
            return hidden[i + 1]

    raise ValueError(f"Could not find '{target_word}' in tokens: {tokens}")


def cosine_sim(a, b):
    """Cosine similarity between two vectors."""
    return F.cosine_similarity(a.unsqueeze(0), b.unsqueeze(0)).item()


def main():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # Load BERT
    print("\nLoading DistilBERT...")
    bert_name = "distilbert-base-uncased"
    bert_tokenizer = AutoTokenizer.from_pretrained(bert_name)
    bert_model = AutoModel.from_pretrained(bert_name).to(device).eval()

    print("\n" + "=" * 70)
    print("Experiment 0: Polysemy — Static vs Contextual Embeddings")
    print("=" * 70)

    for word, examples in POLYSEMY_EXAMPLES.items():
        print(f"\n── Word: '{word}' ({'/' .join(e[1] for e in examples)}) ──")

        # --- Static embeddings (token embedding layer, no context) ---
        static_embs = []
        for sent, sense in examples:
            inputs = bert_tokenizer(sent, return_tensors="pt").to(device)
            with torch.no_grad():
                # Raw token embedding, no transformer layers
                raw_emb = bert_model.embeddings.word_embeddings(inputs["input_ids"])[0]
            # Find the target word tokens
            target_toks = bert_tokenizer.tokenize(word)
            all_toks = bert_tokenizer.tokenize(sent)
            for i in range(len(all_toks)):
                if all_toks[i:i + len(target_toks)] == target_toks:
                    emb = raw_emb[i + 1:i + 1 + len(target_toks)].mean(dim=0)
                    static_embs.append((emb, sense))
                    break

        # --- Contextual embeddings ---
        contextual_embs = []
        for sent, sense in examples:
            emb = get_word_embedding(bert_model, bert_tokenizer, sent, word, device)
            contextual_embs.append((emb, sense))

        # --- Compare ---
        print(f"\n  Static embeddings (type-level, no context):")
        for i in range(len(static_embs)):
            for j in range(i + 1, len(static_embs)):
                sim = cosine_sim(static_embs[i][0], static_embs[j][0])
                print(f"    '{static_embs[i][1]}' vs '{static_embs[j][1]}': "
                      f"cosine = {sim:.4f}")

        print(f"\n  Contextual embeddings (BERT, full context):")
        for i in range(len(contextual_embs)):
            for j in range(i + 1, len(contextual_embs)):
                sim = cosine_sim(contextual_embs[i][0], contextual_embs[j][0])
                print(f"    '{contextual_embs[i][1]}' vs '{contextual_embs[j][1]}': "
                      f"cosine = {sim:.4f}")

    # --- Summary ---
    print("\n" + "=" * 70)
    print("DIAGNOSIS")
    print("=" * 70)
    print("  Static embeddings: same word → same (or nearly identical) vector,")
    print("  regardless of meaning. Cosine similarity ≈ 1.0 across senses.")
    print()
    print("  Contextual embeddings: same word → different vectors depending")
    print("  on context. Cosine similarity drops significantly between senses.")
    print()
    print("  This closes the loop from Lab 1 Exp 0: static embeddings CANNOT")
    print("  distinguish polysemy. BERT's bidirectional attention CAN.")


if __name__ == "__main__":
    main()
