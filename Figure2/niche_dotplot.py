import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

TARGET_CELLTYPES = ["Subcluster_7", "CellType_E", "CellType_A", "CellType_B", "CellType_C"]
TARGET_LABELS = {"Subcluster_7": "CellType_D", "CellType_E": "CellType_E",
                  "CellType_A": "CellType_A", "CellType_B": "CellType_B",
                  "CellType_C": "CellType_C"}

df = pd.read_csv("C_niche_dotplot_plot_data.csv")
df = df.set_index("celltype")
niche_cols = [c for c in df.columns if c.startswith("niche_")]
n_fact = len(niche_cols)
patient = df["patient"].iloc[0]
maturity = df["tls_maturity"].iloc[0]

sub = df.loc[TARGET_CELLTYPES, niche_cols]
sub_norm = sub.div(sub.max(axis=1), axis=0)
mat = (sub_norm * 100).T.values

CMAP = "RdPu"
fig, ax = plt.subplots(figsize=(3.6, 0.35 * n_fact + 1.2))
x_grid, y_grid = np.meshgrid(range(len(TARGET_CELLTYPES)), range(n_fact))
vals = mat.flatten()
sc_plot = ax.scatter(x_grid.flatten(), y_grid.flatten(), c=vals, s=120,
                      cmap=CMAP, vmin=0, vmax=100, edgecolors="none")

ax.set_yticks(range(n_fact))
ax.set_yticklabels(niche_cols, fontsize=8)
ax.set_xticks(range(len(TARGET_CELLTYPES)))
ax.set_xticklabels([TARGET_LABELS[ct] for ct in TARGET_CELLTYPES], fontsize=8, rotation=45, ha="right")
ax.set_xlim(-0.6, len(TARGET_CELLTYPES) - 0.4)
ax.set_ylim(-0.6, n_fact - 0.4)
ax.invert_yaxis()
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
plt.colorbar(sc_plot, ax=ax, label="%", shrink=0.8, pad=0.03)
plt.tight_layout()
plt.savefig("targeted_celltype_niche_dotplot.pdf", bbox_inches="tight")
plt.close()
