import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plot_df = pd.read_csv("B_niche_spatial_plot_data.csv")
n_niche = plot_df["niche"].nunique()

ncols = min(n_niche, 4)
nrows = int(np.ceil(n_niche / ncols))
fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 3 * nrows), squeeze=False)
axes = axes.flatten()
for i in range(n_niche):
    ax = axes[i]
    sub = plot_df[plot_df.niche == i]
    w = sub["weight"].values
    vmin, vmax = np.percentile(w, [1, 99])
    if vmax <= vmin:
        vmax = vmin + 1e-9
    sc_plot = ax.scatter(sub.px_x, -sub.px_y, c=w, cmap="viridis",
                          vmin=vmin, vmax=vmax, s=4, linewidths=0, rasterized=True)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    plt.colorbar(sc_plot, ax=ax, fraction=0.046, pad=0.02)

for j in range(n_niche, len(axes)):
    axes[j].axis("off")

plt.tight_layout()
plt.savefig("niche_spatial_bestnfact_Patient06.pdf", bbox_inches="tight")
plt.close()
