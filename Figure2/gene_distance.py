import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42

OUT_DIR = "."
IN_CSV = "panelD_gene_distance_bin_mean.csv"

MATURITY_COLORS = {"immature": "#F5D08C", "mature": "#F3AFAE"}
MATURITY_ORDER = ["immature", "mature"]
GENE_TREND = ["CD74", "HLA-DRA", "CD4", "LTB", "MS4A1", "CD79A", "CXCL13", "CCL19", "CCL21"]

bin_mean = pd.read_csv(IN_CSV)

GENE_N_COLS = 3
n_genes = len(GENE_TREND)
gene_n_rows = int(np.ceil(n_genes / GENE_N_COLS))
fig, axes = plt.subplots(gene_n_rows, GENE_N_COLS, figsize=(3.6 * GENE_N_COLS, 3.2 * gene_n_rows))
axes = np.atleast_2d(axes)
for i, g in enumerate(GENE_TREND):
    ax = axes[i // GENE_N_COLS][i % GENE_N_COLS]
    col = f"gene__{g}"
    for mat in MATURITY_ORDER:
        sub = bin_mean[bin_mean.maturity == mat].sort_values("bin_mid")
        sub = sub[sub.norm_bin != ">1.0"]
        ax.plot(sub.bin_mid, sub[col], color=MATURITY_COLORS[mat], lw=2, marker="o", markersize=3, label=mat)
    ax.set_xlabel("Normalized distance to niche anchor", fontsize=7)
    if i % GENE_N_COLS == 0:
        ax.set_ylabel("Gene expression", fontsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
for j in range(n_genes, gene_n_rows * GENE_N_COLS):
    axes[j // GENE_N_COLS][j % GENE_N_COLS].axis("off")
handles, labels_lg = axes[0][0].get_legend_handles_labels()
fig.legend(handles, labels_lg, loc="lower center", ncol=2, fontsize=10, bbox_to_anchor=(0.5, -0.02))
plt.tight_layout(rect=[0, 0.03, 1, 1])
out = "gene_distance_curves"
fig.savefig(f"{OUT_DIR}/{out}.pdf", dpi=180)
fig.savefig(f"{OUT_DIR}/{out}.png", dpi=180)
plt.close(fig)
print(f"Saved {out}.*")
