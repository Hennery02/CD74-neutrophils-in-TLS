import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

df = pd.read_csv("UMAP_log2_UMI_plot_data.csv", index_col=0)

fig, ax = plt.subplots(figsize=(4, 4))
sca = ax.scatter(df['UMAP1'], df['UMAP2'], c=df['total_counts_log2'], cmap='viridis', s=3, rasterized=True)
ax.set_xlabel('UMAP1')
ax.set_ylabel('UMAP2')
fig.colorbar(sca, ax=ax, label='total_counts_log2', shrink=0.6)
plt.tight_layout()
plt.savefig('UMAP_log2_UMI.pdf', format='pdf', dpi=300, bbox_inches='tight')
