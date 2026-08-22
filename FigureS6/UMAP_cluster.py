import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

df = pd.read_csv("umap_cluster_1_plot_data.csv", index_col=0)

color_map = {
    'Lineage_A_Subtype_3': '#66c2a5', 'Lineage_A_Subtype_2': '#8da0cb',
    'Lineage_A_Subtype_4': '#ffd92f', 'Lineage_A_Subtype_1': '#b3b3b3',
}

fig, ax = plt.subplots(figsize=(6, 5))
for cat, color in color_map.items():
    sub = df[df['cluster_1'] == cat]
    ax.scatter(sub['UMAP1'], sub['UMAP2'], c=color, s=8, label=cat, rasterized=True)
ax.set_xlabel('UMAP1')
ax.set_ylabel('UMAP2')
ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
plt.tight_layout()
plt.savefig('umap_cluster_1.pdf', format='pdf', dpi=300, bbox_inches='tight')
