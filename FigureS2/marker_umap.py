import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

df = pd.read_csv("UMAP_marks_gene_plot_data_deidentified.csv", index_col=0)

marker_gene_list = [c for c in df.columns if c not in ('UMAP1', 'UMAP2')]

ncols = 4
nrows = int(np.ceil(len(marker_gene_list) / ncols))
fig, axes = plt.subplots(nrows, ncols, figsize=(ncols * 3, nrows * 3))
axes = axes.flatten()

for i, gene in enumerate(marker_gene_list):
    ax = axes[i]
    vmax = np.percentile(df[gene], 99.2)
    sca = ax.scatter(df['UMAP1'], df['UMAP2'], c=df[gene], cmap='RdBu_r', s=1, vmax=vmax, rasterized=True)
    ax.set_xticks([])
    ax.set_yticks([])
    fig.colorbar(sca, ax=ax, shrink=0.6)

for j in range(len(marker_gene_list), len(axes)):
    axes[j].axis('off')

plt.tight_layout()
plt.savefig('UMAP_marks_gene.pdf', format='pdf', dpi=300, bbox_inches='tight')
