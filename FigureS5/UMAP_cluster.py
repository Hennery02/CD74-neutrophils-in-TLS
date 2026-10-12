import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patheffects import withStroke

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

df = pd.read_csv("umap_cluster_1_plot_data.csv", index_col=0)
color_df = pd.read_csv("umap_cluster_1_color_map.csv")
color_map = dict(zip(color_df['cluster_1'], color_df['color']))
categories = list(color_df['cluster_1'])

fig, ax = plt.subplots(figsize=(5, 5))
for cat in categories:
    sub = df[df['cluster_1'] == cat]
    ax.scatter(sub['UMAP1'], sub['UMAP2'], c=color_map[cat], s=2, label=cat,
               edgecolors='none', rasterized=True)
ax.set_xlabel('X_umap1')
ax.set_ylabel('X_umap2')
ax.set_xticks([])
ax.set_yticks([])
legend = ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=10,
                    frameon=False, ncols=2, markerscale=2)
for text in legend.get_texts():
    text.set_path_effects([withStroke(linewidth=1, foreground='white')])
plt.tight_layout()
plt.savefig('umap_cluster_1.pdf', format='pdf', dpi=300, bbox_inches='tight')
