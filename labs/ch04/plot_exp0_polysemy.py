"""Generate polysemy visualization for Lab 4 Exp 0."""
import matplotlib.pyplot as plt
import numpy as np

# Data from experiment
words = ['bank\nfin. vs river', 'bank\nfin. vs avia.', 'bat\nsport vs animal',
         'light\nillum. vs weight', 'light\nillum. vs mood']
static_cos = [1.0, 1.0, 1.0, 1.0, 1.0]
context_cos = [0.6268, 0.4885, 0.6415, 0.6329, 0.5648]

x = np.arange(len(words))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 6))
bars1 = ax.bar(x - width/2, static_cos, width, label='Static (no context)', color='#9ca3af')
bars2 = ax.bar(x + width/2, context_cos, width, label='BERT contextual', color='#f97316')

ax.set_ylabel('Cosine Similarity', fontsize=13)
ax.set_title('Exp 0: Static vs Contextual Embedding — Polysemy Resolution', fontsize=15, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(words, fontsize=11)
ax.set_ylim(0, 1.15)
ax.legend(fontsize=12)
ax.axhline(y=1.0, color='gray', linestyle='--', alpha=0.3)

# Annotate
for bar in bars1:
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.02,
            '1.00', ha='center', va='bottom', fontsize=11, fontweight='bold', color='#6b7280')
for bar in bars2:
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.02,
            f'{bar.get_height():.2f}', ha='center', va='bottom', fontsize=11, fontweight='bold', color='#ea580c')

# Add annotation arrow
ax.annotate('Static: identical vectors\nregardless of meaning',
            xy=(0 - width/2, 1.0), xytext=(-0.8, 0.82),
            fontsize=10, color='#6b7280',
            arrowprops=dict(arrowstyle='->', color='#6b7280'))
ax.annotate('BERT: different vectors\nfor different senses',
            xy=(0 + width/2, 0.63), xytext=(1.5, 0.35),
            fontsize=10, color='#ea580c',
            arrowprops=dict(arrowstyle='->', color='#ea580c'))

plt.tight_layout()
plt.savefig('answers/figures/exp0_polysemy.png', dpi=150, bbox_inches='tight')
print("Saved exp0_polysemy.png")
