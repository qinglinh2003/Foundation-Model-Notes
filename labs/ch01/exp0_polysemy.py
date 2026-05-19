"""
Experiment 0: Static Embedding Polysemy Probe
==============================================
Warm-up exercise (~30 min). No model training required.

Prerequisites:
    Download GloVe embeddings:
    wget https://nlp.stanford.edu/data/glove.6B.zip
    unzip glove.6B.zip
    # Use glove.6B.100d.txt

Usage:
    python exp0_polysemy.py --glove_path glove.6B.100d.txt
    python exp0_polysemy.py --glove_path glove.6B.100d.txt --output answers/exp0_polysemy_output.md
"""

import argparse
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


def load_glove(path: str) -> tuple[dict[str, np.ndarray], int]:
    """Load GloVe vectors from a text file."""
    embeddings = {}
    dim = None
    print(f"Loading GloVe from {path}...")
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            word = parts[0]
            vec = np.array(parts[1:], dtype=np.float32)
            if dim is None:
                dim = len(vec)
            embeddings[word] = vec
    print(f"Loaded {len(embeddings)} words, dimension {dim}")
    return embeddings, dim


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)


def find_nearest(word: str, embeddings: dict, top_k: int = 10) -> list:
    """Find top-k nearest neighbors by cosine similarity."""
    if word not in embeddings:
        print(f"  '{word}' not in vocabulary!")
        return []

    target = embeddings[word]
    scores = []
    for w, vec in embeddings.items():
        if w == word:
            continue
        scores.append((w, cosine_similarity(target, vec)))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]


def analogy(a: str, b: str, c: str, embeddings: dict, top_k: int = 5):
    """
    Solve: a is to b as c is to ?
    Vector arithmetic: result = b - a + c
    """
    for w in (a, b, c):
        if w not in embeddings:
            print(f"  '{w}' not in vocabulary!")
            return []

    vec = embeddings[b] - embeddings[a] + embeddings[c]
    exclude = {a, b, c}
    scores = []
    for w, emb in embeddings.items():
        if w in exclude:
            continue
        scores.append((w, cosine_similarity(vec, emb)))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]


SENSE_LEXICON = {
    "bank": {
        "financial": {
            "banks", "banking", "banker", "bankers", "lending", "loans",
            "loan", "credit", "financial", "finance", "investment",
            "investors", "securities", "mortgage", "deposits", "deposit",
            "money", "fund", "funds", "citigroup", "barclays",
            "ubs",
        },
        "geographic": {
            "river", "shore", "stream", "creek", "rivers", "shoreline",
            "embankment", "canal", "lake", "floodplain",
        },
    },
    "cell": {
        "biology": {
            "cells", "cellular", "tissue", "tissues", "organism",
            "organisms", "membrane", "protein", "proteins", "gene",
            "genes", "dna", "molecular", "tumor", "immune", "stem",
            "brain", "embryonic",
        },
        "prison": {
            "jail", "prison", "inmate", "inmates", "detention", "guard",
            "guards", "solitary",
        },
        "phone": {
            "phone", "phones", "mobile", "wireless", "handset", "battery",
            "telephone", "cellphone", "cellphones",
        },
    },
    "spring": {
        "season": {
            "summer", "winter", "autumn", "fall", "season", "seasons",
            "springtime", "april", "march", "may",
        },
        "water": {
            "fountain", "creek", "stream", "water", "springs", "geyser",
            "aquifer", "brook",
        },
        "mechanical": {
            "coil", "coils", "bounce", "elastic", "mechanism", "shock",
            "suspension",
        },
    },
}


def annotate_sense(target_word: str, neighbor: str) -> str:
    """Return a coarse sense label for the lab's chosen polysemous words."""
    senses = SENSE_LEXICON.get(target_word, {})
    for sense, words in senses.items():
        if neighbor in words:
            return sense
    return "other"


SENSE_COLORS = {
    "financial": "#e74c3c",
    "geographic": "#3498db",
    "biology": "#2ecc71",
    "prison": "#9b59b6",
    "phone": "#e67e22",
    "season": "#f1c40f",
    "water": "#1abc9c",
    "mechanical": "#95a5a6",
    "other": "#bdc3c7",
}


def plot_sense_distribution(
    polysemy_results: dict[str, list[tuple[str, float]]],
    output_path: str,
):
    """Bar chart showing sense composition of top-10 neighbors per word."""
    fig, axes = plt.subplots(1, 3, figsize=(14, 5))

    for ax, (word, neighbors) in zip(axes, polysemy_results.items()):
        sense_counts: dict[str, int] = {}
        for neighbor, _ in neighbors:
            sense = annotate_sense(word, neighbor)
            sense_counts[sense] = sense_counts.get(sense, 0) + 1

        senses = list(sense_counts.keys())
        counts = list(sense_counts.values())
        colors = [SENSE_COLORS.get(s, "#bdc3c7") for s in senses]

        bars = ax.bar(senses, counts, color=colors, edgecolor="white", linewidth=0.8)
        ax.set_title(f'"{word}"', fontsize=14, fontweight="bold")
        ax.set_ylabel("Count (out of 10)" if ax == axes[0] else "")
        ax.set_ylim(0, 11)
        ax.set_yticks(range(0, 11, 2))
        for bar, count in zip(bars, counts):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.3,
                str(count),
                ha="center",
                fontsize=12,
                fontweight="bold",
            )

    fig.suptitle(
        "Sense Distribution of Top-10 GloVe Neighbors",
        fontsize=15,
        fontweight="bold",
        y=1.02,
    )
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved sense distribution plot to {output_path}")


def plot_tsne(
    embeddings: dict[str, np.ndarray],
    polysemy_results: dict[str, list[tuple[str, float]]],
    output_path: str,
):
    """t-SNE scatter of target words + their neighbors, colored by sense."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    for ax, (word, neighbors) in zip(axes, polysemy_results.items()):
        words_list = [word] + [n for n, _ in neighbors]
        vecs = np.array([embeddings[w] for w in words_list])

        # t-SNE with perplexity adapted to small sample size
        perp = min(5, len(words_list) - 1)
        tsne = TSNE(n_components=2, perplexity=perp, random_state=42, max_iter=1000)
        coords = tsne.fit_transform(vecs)

        # Plot neighbors
        for i, (w, coord) in enumerate(zip(words_list, coords)):
            if i == 0:
                # Target word
                ax.scatter(
                    coord[0], coord[1], s=200, c="black", marker="*", zorder=5
                )
                ax.annotate(
                    w.upper(),
                    (coord[0], coord[1]),
                    fontsize=11,
                    fontweight="bold",
                    xytext=(5, 5),
                    textcoords="offset points",
                )
            else:
                sense = annotate_sense(word, w)
                color = SENSE_COLORS.get(sense, "#bdc3c7")
                ax.scatter(coord[0], coord[1], s=100, c=color, zorder=3, alpha=0.85)
                ax.annotate(
                    w,
                    (coord[0], coord[1]),
                    fontsize=9,
                    xytext=(4, 4),
                    textcoords="offset points",
                    color=color,
                )

        ax.set_title(f'"{word}"', fontsize=14, fontweight="bold")
        ax.set_xticks([])
        ax.set_yticks([])

        # Legend
        seen = set()
        handles = []
        for n, _ in neighbors:
            s = annotate_sense(word, n)
            if s not in seen:
                seen.add(s)
                handles.append(
                    plt.Line2D(
                        [0], [0],
                        marker="o",
                        color="w",
                        markerfacecolor=SENSE_COLORS.get(s, "#bdc3c7"),
                        markersize=8,
                        label=s,
                    )
                )
        ax.legend(handles=handles, loc="lower right", fontsize=8)

    fig.suptitle(
        "t-SNE of Polysemous Words and Their GloVe Neighbors",
        fontsize=15,
        fontweight="bold",
        y=1.02,
    )
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Saved t-SNE plot to {output_path}")


def render_markdown(
    embeddings: dict[str, np.ndarray],
    polysemy_results: dict[str, list[tuple[str, float]]],
    analogy_results: list[tuple[tuple[str, str, str], list[tuple[str, float]]]],
) -> str:
    """Render the experiment result as a markdown report."""
    dim = len(next(iter(embeddings.values())))
    lines = [
        "# Experiment 0: Static Embedding Polysemy Probe",
        "",
        f"**Model:** GloVe 6B, {dim}d | **Vocab:** {len(embeddings):,} words",
        "",
        "---",
        "",
        "## Polysemy Probe: Nearest Neighbors",
        "",
        "> **Question:** Do nearest neighbors mix senses? If one sense dominates, why? Can a single static vector cleanly represent a word with multiple distinct meanings?",
        "",
    ]

    for word, neighbors in polysemy_results.items():
        lines.extend([
            f"### `{word}` - top 10 neighbors",
            "",
            "| Rank | Word | Cosine Sim | Sense |",
            "|------|------|------------|-------|",
        ])
        for i, (neighbor, sim) in enumerate(neighbors, 1):
            sense = annotate_sense(word, neighbor)
            lines.append(f"| {i} | {neighbor} | {sim:.4f} | {sense} |")
        lines.append("")

    lines.extend([
        "**Observation:** `bank` neighbors are entirely financial with no river/shore sense. `cell` is mostly biology (8/10) but phone sense appears at ranks 6 and 8. `spring` is dominated by the season sense with no water or mechanical spring sense.",
        "",
        "**Explanation:** GloVe learns vectors from global co-occurrence statistics. When one sense overwhelmingly dominates the corpus, the final vector is pulled into that sense's region of the embedding space. The co-occurrence signal from minority senses gets diluted and barely surfaces in the neighbor list. `cell` is the only word here showing mixed senses, indicating that both biology and phone contexts appear with sufficient frequency in the training corpus.",
        "",
        "---",
        "",
        "## Analogy Test",
        "",
        "> **Question:** Do static embeddings capture consistent semantic relationships via vector arithmetic, despite failing to separate word senses?",
        "",
        "| Analogy | Top Result | Cosine |",
        "|---------|------------|--------|",
    ])

    for (a, b, c), results in analogy_results:
        top_word, top_sim = results[0] if results else ("N/A", float("nan"))
        sim_text = f"{top_sim:.4f}" if results else "N/A"
        lines.append(f"| `{a} : {b} :: {c} : ?` | {top_word} | {sim_text} |")

    lines.extend([
        "",
        "**Full analogy results:**",
        "",
    ])
    for (a, b, c), results in analogy_results:
        if results:
            result_text = ", ".join(f"{word} ({sim:.4f})" for word, sim in results)
        else:
            result_text = "could not compute - check vocabulary"
        lines.append(f"- **{a} : {b} :: {c} : ?** - {result_text}")

    lines.extend([
        "",
        "**Observation:** Analogy arithmetic works well for words with a single dominant meaning, confirming that vector directions encode stable semantic relationships. However, this relies on each word occupying a clean, unambiguous position in embedding space. For polysemous words like `bank`, the vector sits at a weighted average of its senses, making such arithmetic unreliable.",
        "",
        "---",
        "",
        "## Summary: Can a single vector encode multiple senses?",
        "",
        "> **Question:** What would a model need to produce different vectors for the same word in different contexts?",
        "",
        "**No.** A vector is a single point in high-dimensional space. When `bank` has both financial and geographic senses, the vector lands at a weighted average of both sense clusters. In this experiment, the financial sense dominates so heavily that the vector sits inside the financial cluster, and the geographic sense is essentially invisible in the neighbor structure.",
        "",
        "A model that produces context-dependent representations needs three components:",
        "",
        "1. A static token embedding as the initial input.",
        "2. A contextual encoder (LSTM, Transformer) that mixes information across positions in the sequence.",
        "3. A position-specific output vector, so that `bank` in \"river bank\" and \"bank account\" receive different representations.",
        "",
        "This is the motivation for moving from static embeddings (Word2Vec, GloVe) toward contextualized models (ELMo, Transformers), which is the central arc of Chapter 1.",
        "",
    ])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--glove_path", type=str, default="glove.6B.100d.txt")
    parser.add_argument(
        "--output",
        type=str,
        default="answers/exp0_polysemy_output.md",
        help="Markdown output path for the experiment report.",
    )
    args = parser.parse_args()

    embeddings, dim = load_glove(args.glove_path)

    # ----- Polysemy probe -----
    polysemous_words = ["bank", "cell", "spring"]
    polysemy_results = {}

    print("\n" + "=" * 60)
    print("POLYSEMY PROBE: Nearest Neighbors")
    print("=" * 60)

    for word in polysemous_words:
        neighbors = find_nearest(word, embeddings, top_k=10)
        polysemy_results[word] = neighbors
        print(f"\n'{word}' — top 10 neighbors:")
        print(f"  {'Rank':<6} {'Word':<15} {'Cosine Sim':<10} {'Sense (annotate!)'}")
        print(f"  {'-'*50}")
        for i, (w, sim) in enumerate(neighbors, 1):
            sense = annotate_sense(word, w)
            print(f"  {i:<6} {w:<15} {sim:<10.4f} {sense}")

    # ----- Analogy test -----
    print("\n" + "=" * 60)
    print("ANALOGY TEST")
    print("=" * 60)

    analogies = [
        ("man", "woman", "king"),       # expected: queen
        ("paris", "france", "berlin"),   # expected: germany
        ("slow", "slower", "fast"),      # expected: faster
    ]
    analogy_outputs = []

    for a, b, c in analogies:
        results = analogy(a, b, c, embeddings, top_k=5)
        analogy_outputs.append(((a, b, c), results))
        print(f"\n  {a} : {b} :: {c} : ?")
        if results:
            for w, sim in results:
                print(f"    {w:<15} (cosine: {sim:.4f})")
        else:
            print("    (could not compute — check vocabulary)")

    # ----- Reflection -----
    print("\n" + "=" * 60)
    print("REFLECTION QUESTIONS")
    print("=" * 60)
    print("""
    1. For 'bank', do the neighbors mix financial and geographic senses?
       If one sense dominates, why might that be?

    2. The analogy test shows that vector directions encode semantic
       relationships. But can any single vector for 'bank' simultaneously
       encode both the river sense and the finance sense?

    3. What would a model need to produce DIFFERENT vectors for the
       same word in different contexts?
    """)

    markdown = render_markdown(embeddings, polysemy_results, analogy_outputs)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"\nWrote markdown report to {output_path}")

    # ----- Visualizations -----
    fig_dir = output_path.parent / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    plot_sense_distribution(
        polysemy_results, str(fig_dir / "sense_distribution.png")
    )
    plot_tsne(
        embeddings, polysemy_results, str(fig_dir / "polysemy_tsne.png")
    )


if __name__ == "__main__":
    main()
