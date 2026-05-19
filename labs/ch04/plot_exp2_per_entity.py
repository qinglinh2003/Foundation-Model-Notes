"""Generate per-entity F1 breakdown for Lab 4 Exp 2."""
import matplotlib.pyplot as plt
import numpy as np

entities = ['B-PER', 'B-ORG', 'B-LOC', 'B-MISC', 'I-PER', 'I-ORG', 'I-LOC', 'I-MISC']
bert_f1 = [99.0, 90.6, 95.6, 89.0, 98.5, 86.1, 84.9, 78.5]
gpt_f1 = [78.0, 46.0, 74.3, 50.0, 96.1, 71.1, 67.2, 65.0]
gaps = [b - g for b, g in zip(bert_f1, gpt_f1)]

x = np.arange(len(entities))
width = 0.35

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), gridspec_kw={'height_ratios': [3, 1]})

# Top: grouped bars
bars1 = ax1.bar(x - width/2, bert_f1, width, label='DistilBERT (bidirectional)', color='#f97316')
bars2 = ax1.bar(x + width/2, gpt_f1, width, label='DistilGPT2 (causal)', color='#3b82f6')

ax1.set_ylabel('F1 Score (%)', fontsize=13)
ax1.set_title('Exp 2: Per-Entity NER F1 — Bidirectional vs Causal', fontsize=15, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(entities, fontsize=12)
ax1.set_ylim(0, 110)
ax1.legend(fontsize=12, loc='upper right')

# Add value labels
for bar in bars1:
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
             f'{bar.get_height():.0f}', ha='center', va='bottom', fontsize=9, color='#ea580c')
for bar in bars2:
    ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
             f'{bar.get_height():.0f}', ha='center', va='bottom', fontsize=9, color='#2563eb')

# Separator line between B- and I-
ax1.axvline(x=3.5, color='gray', linestyle=':', alpha=0.5)
ax1.text(1.5, 105, 'B- (boundary) labels', ha='center', fontsize=11, fontstyle='italic', color='#6b7280')
ax1.text(5.5, 105, 'I- (continuation) labels', ha='center', fontsize=11, fontstyle='italic', color='#6b7280')

# Bottom: gap chart
colors = ['#dc2626' if g > 20 else '#f59e0b' if g > 10 else '#22c55e' for g in gaps]
bars3 = ax2.bar(x, gaps, 0.6, color=colors)
ax2.set_ylabel('BERT advantage (pp)', fontsize=12)
ax2.set_xticks(x)
ax2.set_xticklabels(entities, fontsize=12)
ax2.axhline(y=0, color='black', linewidth=0.5)
ax2.set_ylim(0, 50)

for bar, gap in zip(bars3, gaps):
    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
             f'+{gap:.0f}pp', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Highlight B-ORG
ax2.annotate('B-ORG: +44.6pp\nGPT cannot see\nright context at\nentity boundary',
             xy=(1, 44.6), xytext=(3, 42),
             fontsize=10, color='#dc2626', fontweight='bold',
             arrowprops=dict(arrowstyle='->', color='#dc2626', lw=2))

plt.tight_layout()
plt.savefig('answers/figures/exp2_per_entity_f1.png', dpi=150, bbox_inches='tight')
print("Saved exp2_per_entity_f1.png")
