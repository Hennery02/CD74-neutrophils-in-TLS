import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42

SPATIAL_CMAP = LinearSegmentedColormap.from_list(
    "warm_sequential", ["#E8E8E8", "#FDE3B0", "#F5A94E", "#D46A1E", "#7A3B0E"]
)

PATIENT_ORDER = ["Patient01", "Patient02", "Patient03", "Patient04", "Patient05",
                  "Patient06", "Patient07", "Patient08", "Patient09", "Patient10"]
MARKER_GENES = ["CD3D", "MS4A1", "BCL6", "CD74", "HLA-DRA", "LTB"]
CELLTYPE_LABELS = ["CellType_A", "CellType_B", "CellType_C", "CellType_D"]

PCT_OVERRIDE = {
    "tls12_score": dict(vmin_pct=1, vmax_pct=99), "imprint_score": dict(vmin_pct=1, vmax_pct=99),
    "marker22_score": dict(vmin_pct=1, vmax_pct=99),
    "CD3D": dict(vmin_pct=1, vmax_pct=99), "MS4A1": dict(vmin_pct=1, vmax_pct=99),
    "BCL6": dict(vmin_pct=1, vmax_pct=99), "LTB": dict(vmin_pct=1, vmax_pct=99),
    "CD74": dict(vmin_pct=60, vmax_pct=99), "HLA-DRA": dict(vmin_pct=60, vmax_pct=99),
}

plot_df = pd.read_csv("A_spatial_panel_plot_data.csv")

score_cols = [("tls12_score", "TLS score\n(TLS12)"), ("imprint_score", "TLS score\n(imprint)"),
              ("marker22_score", "TLS score\n(marker22)")]
gene_cols = [(g, g) for g in MARKER_GENES]
celltype_cols = [(label, label) for label in CELLTYPE_LABELS]
all_cols = score_cols + gene_cols + celltype_cols
n_cols = len(all_cols)
n_patients = len(PATIENT_ORDER)

fig, axes = plt.subplots(n_patients, n_cols, figsize=(2.6 * n_cols, 2.5 * n_patients))
for row, patient in enumerate(PATIENT_ORDER):
    tls_maturity = plot_df.loc[plot_df.patient == patient, "tls_maturity"].iloc[0]
    for col, (col_name, col_title) in enumerate(all_cols):
        ax = axes[row, col]
        sub = plot_df[(plot_df.patient == patient) & (plot_df.panel_col == col_name)]
        vals = sub["value"].values
        if len(vals) == 0 or np.all(np.isnan(vals)):
            ax.axis("off")
            continue
        pct = PCT_OVERRIDE.get(col_name, dict(vmin_pct=1, vmax_pct=99))
        vmin = np.nanpercentile(vals, pct["vmin_pct"])
        vmax = np.nanpercentile(vals, pct["vmax_pct"])
        if vmax <= vmin:
            vmax = np.nanmax(vals)
        if vmax <= vmin:
            vmax = vmin + 1e-6
        sc_plot = ax.scatter(sub.x, -sub.y, c=vals, cmap=SPATIAL_CMAP,
                              vmin=vmin, vmax=vmax, s=9, linewidths=0, rasterized=True)
        ax.set_aspect("equal")
        ax.axis("off")
        if col == 0:
            ax.annotate(f"{patient}\n{tls_maturity}", xy=(-0.35, 0.5),
                        xycoords="axes fraction", ha="right", va="center", fontsize=8.5)
        cb = plt.colorbar(sc_plot, ax=ax, shrink=0.7, pad=0.02, fraction=0.06)
        cb.ax.tick_params(labelsize=6)

plt.tight_layout(rect=[0.04, 0, 1, 1])
plt.savefig("spatial_panel_all_patients.pdf", dpi=180)
plt.close()
