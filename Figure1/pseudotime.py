import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

df = pd.read_csv("Neu_pseudotime_plot_data.csv")

branch_cols = [c for c in df.columns if c.startswith('branch_prob_')]

fig, axes = plt.subplots(1, 1 + len(branch_cols), figsize=(5 * (1 + len(branch_cols)), 5))

sc0 = axes[0].scatter(df['UMAP_1'], df['UMAP_2'], c=df['pseudotime'], cmap='Spectral_r', s=5, rasterized=True)
plt.colorbar(sc0, ax=axes[0])

for ax, col in zip(axes[1:], branch_cols):
    sc1 = ax.scatter(df['UMAP_1'], df['UMAP_2'], c=df[col], cmap='Spectral_r', s=5, rasterized=True)
    plt.colorbar(sc1, ax=ax)

for ax in axes:
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ['top', 'right', 'left', 'bottom']:
        ax.spines[spine].set_visible(False)

plt.tight_layout()
plt.savefig('pseudotime_2.pdf')
