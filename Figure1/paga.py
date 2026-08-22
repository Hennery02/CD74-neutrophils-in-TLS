import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plot_df = pd.read_csv('../../data/Lineage_C_PAGA_plot_data.csv', index_col=0)
conn = pd.read_csv('../../data/Lineage_C_PAGA_connectivities_tree.csv', index_col=0)

categories = conn.index.tolist()
colors = plt.get_cmap('tab10').colors[:len(categories)]
color_map = dict(zip(categories, colors))

fig, ax = plt.subplots(figsize=(6, 6))
for cat in categories:
    sub = plot_df[plot_df['cell_type'] == cat]
    ax.scatter(sub['UMAP1'], sub['UMAP2'], s=10, alpha=.2, color=color_map[cat], linewidths=0)

node_pos = plot_df.groupby('cell_type')[['UMAP1', 'UMAP2']].mean().loc[categories]
for cat in categories:
    x, y = node_pos.loc[cat]
    ax.scatter([x], [y], s=400, color=color_map[cat], edgecolors='black', zorder=3)
    ax.annotate(cat, (x, y), textcoords="offset points", xytext=(0, 12),
                ha='center', fontsize=9, fontweight='bold', zorder=4)

for i, src in enumerate(categories):
    for j, tgt in enumerate(categories):
        w = conn.iloc[i, j]
        if w > 0:
            x0, y0 = node_pos.loc[src]
            x1, y1 = node_pos.loc[tgt]
            ax.annotate('', xy=(x1, y1), xytext=(x0, y0), zorder=5,
                        arrowprops=dict(arrowstyle='->', color='black', lw=1.5, zorder=5))

ax.axis('off')
fig.savefig('../../data/paga_graph.pdf', format='pdf', bbox_inches='tight')
