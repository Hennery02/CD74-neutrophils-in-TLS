import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42

MATURITY_ORDER = ["Patient01", "Patient02", "Patient03", "Patient04", "Patient05",
                   "Patient06", "Patient07", "Patient08", "Patient09", "Patient10"]
MATURITY_LABEL = {"immature": "imTLS", "mature": "mTLS", "none": "nTLS"}

SPATIAL_CMAP = LinearSegmentedColormap.from_list(
    "warm_sequential", ["#E8E8E8", "#FDE3B0", "#F5A94E", "#D46A1E", "#7A3B0E"]
)

plot_df = pd.read_csv("F_pathway_spatial_plot_data_deidentified.csv")
F_METRICS = plot_df[["sig_key", "display_name", "vmin_mode"]].drop_duplicates().itertuples(index=False)


def plot_spatial_metric_grid(long_df, display_name, vmin_mode="zero", spot_size=9):
    fig, axes = plt.subplots(4, 3, figsize=(8.4, 10.4))
    axes = axes.flatten()
    for ax, patient in zip(axes, MATURITY_ORDER):
        sub = long_df[long_df.patient == patient]
        vals = sub["value"].values
        vmax = np.nanquantile(vals, 0.99)
        if vmax <= 0:
            vmax = np.nanmax(vals)
        vmax = max(vmax, 1e-6)
        if vmin_mode == "quantile":
            vmin = np.nanquantile(vals, 0.70)
            if vmin >= vmax:
                vmin = np.nanmin(vals)
        else:
            vmin = 0
        sc_plot = ax.scatter(sub.px_x, -sub.px_y, c=vals, cmap=SPATIAL_CMAP,
                              vmin=vmin, vmax=vmax, s=spot_size, linewidths=0, rasterized=True)
        ax.set_aspect("equal")
        ax.axis("off")
        plt.colorbar(sc_plot, ax=ax, shrink=0.75, pad=0.02, fraction=0.06)
    for ax in axes[len(MATURITY_ORDER):]:
        ax.axis("off")
    plt.tight_layout()
    safe_name = display_name.split(' (')[0].replace('/', '-').replace(' ', '_')
    plt.savefig(f"pathway_{safe_name}.pdf", bbox_inches="tight")
    plt.close(fig)


for sig_key, display_name, vmin_mode in F_METRICS:
    sub = plot_df[plot_df.sig_key == sig_key]
    plot_spatial_metric_grid(sub, display_name, vmin_mode=vmin_mode)
