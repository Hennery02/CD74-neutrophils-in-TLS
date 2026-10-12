import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

df = pd.read_csv("UMAP_cluster1_plot_data.csv")

custom_palette = ['#845C75', '#D6B16C', '#AD6559', '#72704C', '#8B795D', '#546983',
                   '#8E3B17', '#9A9D5F', '#635277', '#68855C', '#635277']

categories = df['cluster_1'].astype('category').cat.categories.tolist()
colors = {cat: custom_palette[i % len(custom_palette)] for i, cat in enumerate(categories)}

fig, ax = plt.subplots(figsize=(6, 6))
for cat in categories:
    sub = df[df['cluster_1'] == cat]
    ax.scatter(sub['UMAP_1'], sub['UMAP_2'], s=8, c=[colors[cat]], label=cat,
               rasterized=True, linewidths=0)
    cx, cy = sub['UMAP_1'].median(), sub['UMAP_2'].median()
    ax.text(cx, cy, cat, fontsize=12, ha='center', va='center',
            path_effects=None, color='black', weight='bold')

ax.set_xlabel('UMAP_1')
ax.set_ylabel('UMAP_2')
ax.set_xticks([])
ax.set_yticks([])
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)

fig.savefig('umap_cluster1_labelondata.pdf', dpi=300, bbox_inches='tight')
