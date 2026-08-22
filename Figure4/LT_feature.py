import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

df = pd.read_csv("LT_feature_plot_data.csv")
marker_genes = ['LTB', 'LTA', 'TNFSF14', 'TNF']

fig, axes = plt.subplots(1, 4, figsize=(20, 4.2))
for ax, gene in zip(axes, marker_genes):
    sc_plot = ax.scatter(df['UMAP_1'], df['UMAP_2'], c=df[gene], cmap='RdBu_r',
                          s=2, linewidths=0, rasterized=True,
                          vmax=df[gene].quantile(0.992))
    ax.set_xlabel('X_umap1')
    ax.set_ylabel('X_umap2')
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    plt.colorbar(sc_plot, ax=ax, shrink=0.8)

plt.tight_layout()
fig.savefig('UMAP_LTB.pdf', dpi=300, bbox_inches='tight')
