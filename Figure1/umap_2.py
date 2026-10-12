import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

df = pd.read_csv("Lineage_C_UMAP_plot_data.csv")

order = ['Subcluster_1', 'Subcluster_2', 'Subcluster_3', 'Subcluster_4',
         'Subcluster_5', 'Subcluster_6', 'Subcluster_7']
palette = ["#d2981a", "#CBB396", "#457277", "#8f657d", "#42819F", "#86AA7D", "#a53e1f"]
colors = dict(zip(order, palette))

fig, ax = plt.subplots(figsize=(6, 6))
for cat in order:
    sub = df[df['cell_type'] == cat]
    ax.scatter(sub['UMAP_1'], sub['UMAP_2'], s=10, c=colors[cat], label=cat,
               rasterized=True, linewidths=0.3, edgecolors='white')

ax.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10, frameon=False)
ax.set_xlabel('UMAP_1')
ax.set_ylabel('UMAP_2')
ax.set_xticks([])
ax.set_yticks([])
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)

fig.savefig('umap_legend.pdf', dpi=300, bbox_inches='tight')
