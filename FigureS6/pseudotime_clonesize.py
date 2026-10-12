import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.stats import spearmanr

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42

tcr_cells = pd.read_csv("pseudotime_clonesize_plot_data.csv")

fig, ax = plt.subplots(figsize=(7.2, 6))
sc_ = ax.scatter(tcr_cells["UMAP1"], tcr_cells["UMAP2"],
                  c=tcr_cells["dpt_pseudotime"], s=tcr_cells["clone_size"].clip(upper=30) * 3 + 2,
                  cmap="Spectral_r", alpha=0.75, linewidths=0.2, edgecolors="white")
cbar = fig.colorbar(sc_, ax=ax, shrink=0.7, pad=0.02)
cbar.set_label("dpt_pseudotime", fontsize=9)
cbar.set_ticks([0, 1])
rho, pval = spearmanr(tcr_cells["dpt_pseudotime"], tcr_cells["clone_size"])
ax.text(0.02, 0.02, f"Spearman ρ = {rho:.2f} (n={len(tcr_cells)}, p<0.001)" if pval < 0.001
        else f"Spearman ρ = {rho:.2f} (n={len(tcr_cells)}, p={pval:.3f})",
        transform=ax.transAxes, fontsize=8.5, va="bottom",
        bbox=dict(boxstyle="round", facecolor="#f5f5f3", edgecolor="#d8d8d3"))
ax.set_xlabel("UMAP 1"); ax.set_ylabel("UMAP 2")
ax.set_xticks([]); ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)
fig.tight_layout()
fig.savefig("clone_size_on_pseudotime_UMAP.pdf", dpi=300, bbox_inches="tight")
