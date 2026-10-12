import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from adjustText import adjust_text

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

result = pd.read_csv('TLS_vs_nonTLS_DEG_plot_data.csv', index_col=0)

fc_thresh = 1.0
top_up = result[result['sig'] == 'up'].nlargest(10, 'scores').index.tolist()
top_down = result[result['sig'] == 'down'].nsmallest(10, 'scores').index.tolist()
top_genes = top_up + top_down

color_map = {'up': '#d62728', 'down': '#7388c1', 'normal': '#d7d7d7'}

plot_result = result.copy()
plot_result['log2FC'] = plot_result['log2FC'].clip(-10, 10)

fig, ax = plt.subplots(figsize=(5, 5))

for sig, grp in plot_result.groupby('sig'):
    ax.scatter(grp['log2FC'], grp['scores'],
               c=color_map[sig], s=8, alpha=0.7, linewidths=0,
               label=f"{sig}: {len(grp)}" if sig != 'normal' else None,
               zorder=2 if sig != 'normal' else 1)

ax.axvline(fc_thresh, color='grey', lw=0.8, ls='--')
ax.axvline(-fc_thresh, color='grey', lw=0.8, ls='--')
ax.axhline(0, color='grey', lw=0.8, ls='--')
ax.set_xlim(-10, 10)

texts = []
for gene in top_genes:
    if gene not in plot_result.index:
        continue
    x = plot_result.loc[gene, 'log2FC']
    y = plot_result.loc[gene, 'scores']
    c = color_map[plot_result.loc[gene, 'sig']]
    t = ax.text(x, y, gene, fontsize=16, color=c)
    texts.append(t)

adjust_text(texts, ax=ax, arrowprops=dict(arrowstyle='-', color='grey', lw=0.5))

ax.set_xlabel('log2FC', fontsize=12)
ax.set_ylabel('Wilcoxon score', fontsize=12)
ax.legend(fontsize=9, frameon=False)
plt.tight_layout()

fig.savefig('TLS_vs_nonTLS_volcano.pdf', bbox_inches='tight')
print('Done.')
