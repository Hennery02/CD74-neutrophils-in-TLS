import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm, LinearSegmentedColormap
import seaborn as sns

plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

plot_data = pd.read_csv("Neu_cytokine_heatmap_plot_data.csv", index_col=0)
sig = plot_data['sig']
scaled_sorted = plot_data.drop(columns=['sig', 'padj'])

colors_custom = [
    (0.0, '#2166ac'), (0.40, '#92c5de'), (0.45, '#f0f0f0'),
    (0.58, '#f0f0f0'), (0.60, '#f4a582'), (1.0, '#b2182b'),
]
cmap_wide_white = LinearSegmentedColormap.from_list('RdBu_wide_white', colors_custom)

vmax = 5
g = sns.clustermap(
    scaled_sorted, method='average', metric='euclidean', cmap=cmap_wide_white,
    norm=TwoSlopeNorm(vmin=-vmax, vcenter=0, vmax=vmax),
    figsize=(4.5, max(10, len(scaled_sorted) * 0.22)),
    linewidths=0.3, linecolor='white',
    dendrogram_ratio=(0.12, 0.04), cbar_pos=(1.02, 0.45, 0.02, 0.15),
    cbar_kws={'label': 'Cell percentage\n(scaled by subtype)', 'ticks': [-vmax, 0, vmax], 'format': '%.1f'},
    yticklabels=True, xticklabels=True, col_cluster=True,
    tree_kws={'linewidths': 0.8, 'colors': 'black'},
)

ax = g.ax_heatmap
ytick_labels = [t.get_text() for t in ax.get_yticklabels()]
for i, label in enumerate(ytick_labels):
    s = sig.loc[label] if label in sig.index else ''
    if isinstance(s, str) and s:
        ax.text(len(scaled_sorted.columns) + 0.15, i + 0.5, s, va='center', ha='left',
                 fontsize=9, color='#d62728', fontweight='bold', transform=ax.transData)

g.ax_heatmap.tick_params(axis='x', labelsize=9, rotation=45)
g.ax_heatmap.tick_params(axis='y', labelsize=7.5, rotation=0)
g.ax_cbar.set_ylabel('Scaled proportion', fontsize=7)
g.ax_cbar.tick_params(labelsize=7)

plt.savefig('cytokine_heatmap.pdf', bbox_inches='tight', dpi=300)
