import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

df = pd.read_csv("HLA_violin_plot_data.csv", index_col='cell_barcode')

gene_list_HLA = ['HLA-A', 'HLA-B', 'HLA-C', 'HLA-E', 'HLA-F', 'HLA-G',
                  'HLA-DPA1', 'HLA-DPB1', 'HLA-DQA1', 'HLA-DQB1', 'HLA-DRA', 'HLA-DRB1']
ordered_clusters = ['Subcluster_6', 'Subcluster_2', 'Subcluster_1',
                     'Subcluster_3', 'Subcluster_4', 'Subcluster_7',
                     'Subcluster_5']
row_palette = ["#86AA7D", "#CBB396", "#d2981a", "#457277", "#8f657d", "#a53e1f", "#42819F"]
row_colors = dict(zip(ordered_clusters, row_palette))

fig, axes = plt.subplots(len(ordered_clusters), 1, figsize=(len(gene_list_HLA) * 0.7, len(ordered_clusters) * 0.9),
                          sharex=True)

for ax, cluster in zip(axes, ordered_clusters):
    sub = df[df['cell_type'] == cluster]
    data_long = sub[gene_list_HLA].melt(var_name='gene', value_name='expression')
    data_long['gene'] = pd.Categorical(data_long['gene'], categories=gene_list_HLA, ordered=True)
    sns.violinplot(data=data_long, x='gene', y='expression', hue='gene', ax=ax,
                    palette=[row_colors[cluster]] * len(gene_list_HLA),
                    inner=None, linewidth=0.5, cut=0, legend=False)
    ax.set_ylabel(cluster, rotation=0, ha='right', va='center', fontsize=8)
    ax.set_xlabel('')
    ax.set_yticks([])
    for spine in ['top', 'right', 'left']:
        ax.spines[spine].set_visible(False)

axes[-1].set_xticks(range(len(gene_list_HLA)))
axes[-1].set_xticklabels(gene_list_HLA, rotation=90)

plt.tight_layout()
plt.savefig('gene_HLA_violin.pdf')
