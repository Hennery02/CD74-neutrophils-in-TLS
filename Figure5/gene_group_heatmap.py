import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

mean_expr = pd.read_csv("gene_group_heatmap_plot_data.csv", index_col=0)

gene_groups = {
    'GeneGroup_1': ['CD74', 'HLA-DRA', 'HLA-DRB1', 'CD80', 'CD86'],
    'GeneGroup_2': ['LTBR', 'NFKB2', 'RELB'],
    'GeneGroup_3': ['CXCL13', 'CCL19', 'CCL21', 'CCL3', 'CCL5', 'TNFSF13B', 'CCR7'],
}
gene_list = [g for genes in gene_groups.values() for g in genes]

row_order = [c for c in mean_expr.index if c != 'Subcluster_7'] + ['Subcluster_7'] \
    if 'Subcluster_7' in mean_expr.index else list(mean_expr.index)
row_order = list(mean_expr.index)

scaled = (mean_expr[gene_list] - mean_expr[gene_list].min()) / (mean_expr[gene_list].max() - mean_expr[gene_list].min())
mat = scaled.loc[row_order].values

fig, ax = plt.subplots(figsize=(8, 4))
im = ax.imshow(mat, cmap='Blues', vmin=0, vmax=1, aspect='auto')

ax.set_xticks(range(len(gene_list)))
ax.set_xticklabels(gene_list, rotation=90, fontsize=9)
ax.set_yticks(range(len(row_order)))
ax.set_yticklabels(row_order, fontsize=9)

for spine in ax.spines.values():
    spine.set_visible(True)
ax.set_xticks(np.arange(-0.5, len(gene_list), 1), minor=True)
ax.set_yticks(np.arange(-0.5, len(row_order), 1), minor=True)
ax.grid(which='minor', color='#dddddd', linewidth=0.5)
ax.tick_params(which='minor', length=0)

pos = 0
for group_name, genes in gene_groups.items():
    n = len(genes)
    ax.text(pos + n / 2 - 0.5, -1.2, group_name, ha='center', va='bottom', fontsize=10)
    pos += n

cbar = plt.colorbar(im, ax=ax, shrink=0.8)
cbar.set_label('mean expression', fontsize=9)

plt.tight_layout()
plt.savefig('matrixplot_hotmap_new.pdf', bbox_inches='tight')
