import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

df = pd.read_csv("B_Plasma_UMAP_plot_data.csv")
with open("B_Plasma_UMAP_cluster1_order.txt") as f:
    categories = [line.strip() for line in f if line.strip()]
df['cluster_1'] = pd.Categorical(df['cluster_1'], categories=categories)

cmap = plt.get_cmap('Set2')
colors = {cat: cmap(i) for i, cat in enumerate(categories)}

fig, ax = plt.subplots(figsize=(7, 7))
for cat in categories:
    sub = df[df['cluster_1'] == cat]
    ax.scatter(sub['UMAP_1'], sub['UMAP_2'], s=8, c=[colors[cat]], label=cat,
               rasterized=True, linewidths=0)
    cx, cy = sub['UMAP_1'].median(), sub['UMAP_2'].median()
    ax.text(cx, cy, cat, fontsize=11, ha='center', va='center', color='black', weight='bold')

ax.set_xticks([])
ax.set_yticks([])
for spine in ['top', 'right', 'left', 'bottom']:
    ax.spines[spine].set_visible(False)
fig.savefig('umap_cluster1_labelondata.pdf', dpi=300, bbox_inches='tight')
plt.close(fig)
