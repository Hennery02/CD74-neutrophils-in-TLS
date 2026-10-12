import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

df = pd.read_csv("UMAP_tissue_type_plot_data.csv", index_col=0)

color_map = {'Fraction_A': '#005387', 'tumor': '#9EC5DA'}

rng = np.random.default_rng(0)
order = rng.permutation(df.index)
df = df.loc[order]
colors = df['tissue_type'].map(color_map)

fig, ax = plt.subplots(figsize=(4, 4))
ax.scatter(df['UMAP1'], df['UMAP2'], c=colors, s=3, rasterized=True)
ax.set_xlabel('UMAP1')
ax.set_ylabel('UMAP2')
handles = [Line2D([0], [0], marker='o', color='w', markerfacecolor=c, markersize=6, label=cat)
           for cat, c in color_map.items()]
ax.legend(handles=handles, bbox_to_anchor=(1.02, 1), loc='upper left', fontsize=8)
plt.tight_layout()
plt.savefig('UMAP_tissue_type.pdf', format='pdf', dpi=300, bbox_inches='tight')
