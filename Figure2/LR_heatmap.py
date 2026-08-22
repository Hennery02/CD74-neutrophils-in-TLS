import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42

OUT_DIR = "."
IN_CSV = "panelG_LR_bin_mean.csv"

MATURITY_ORDER = ["immature", "mature"]

HIGHLIGHT_COLORS = {
    "HLA-DPA1_Lineage_B": "#8172B3", "HLA-DPB1_Lineage_B": "#8172B3",
    "HLA-DQA1_Lineage_B": "#8172B3", "HLA-DMA_Lineage_B": "#8172B3",
    "HLA-DMB_Lineage_B": "#8172B3", "HLA-DQA2_Lineage_B": "#8172B3",
    "HLA-DOA_Lineage_B": "#8172B3", "HLA-DOB_Lineage_B": "#8172B3",
    "HLA-DQB1_Lineage_B": "#8172B3", "HLA-DRA_Lineage_B": "#8172B3",
    "HLA-DRB1_Lineage_B": "#8172B3", "HLA-DRB3_Lineage_B": "#8172B3",
    "HLA-DRB4_Lineage_B": "#8172B3", "HLA-DRB5_Lineage_B": "#8172B3",
    "LTB-LTBR": "#E4572E",
    "LTA_TNFRSF14": "#E4572E", "LTA_TNFRSF1A": "#E4572E",
    "LTA_TNFRSF1B": "#E4572E",
    "TNFSF14_LTBR": "#E4572E", "TNFSF14_TNFRSF14": "#E4572E",
    "CXCL13_CXCR5": "#C44E52",
    "CCL19_CCR7": "#C44E52", "CCL21_CCR7": "#C44E52",
}

bin_mean = pd.read_csv(IN_CSV)
highlight_found = [c for c in bin_mean.columns if c not in ("maturity", "norm_bin", "bin_mid")]

N_HEATMAP_COLS = 200


def smooth_xy(x, y, n_out=200, bandwidth=0.12):
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    order = np.argsort(x)
    x, y = x[order], y[order]
    x_smooth = np.linspace(x.min(), x.max(), n_out)
    weights = np.exp(-0.5 * ((x_smooth[:, None] - x[None, :]) / bandwidth) ** 2)
    weights /= weights.sum(axis=1, keepdims=True)
    return x_smooth, weights @ y


def build_smoothed_zscore_matrix(mat_label, names, bin_mean_df):
    sub = bin_mean_df[(bin_mean_df.maturity == mat_label) & (bin_mean_df.norm_bin != ">1.0")].sort_values("bin_mid")
    mat_smooth = np.zeros((len(names), N_HEATMAP_COLS))
    for r, name in enumerate(names):
        xs, ys = smooth_xy(sub.bin_mid.values, sub[name].values, n_out=N_HEATMAP_COLS)
        mat_smooth[r] = ys
    row_mean = mat_smooth.mean(axis=1, keepdims=True)
    row_std = mat_smooth.std(axis=1, keepdims=True)
    row_std[row_std == 0] = 1
    return (mat_smooth - row_mean) / row_std


def get_peak_positions(mat_z_full, names):
    x_smooth = np.linspace(0, 1, N_HEATMAP_COLS)
    peaks = {}
    for row, name in enumerate(names):
        row_vals = mat_z_full[row]
        if np.all(np.isnan(row_vals)) or np.nanstd(row_vals) == 0:
            peaks[name] = 0.5
            continue
        peaks[name] = x_smooth[np.nanargmax(row_vals)]
    return peaks


n_groups = len(MATURITY_ORDER)
width_ratios = [1.0, 1.0] * n_groups
fig = plt.figure(figsize=(6.5 * n_groups, 0.32 * len(highlight_found) + 2.5))
gs = fig.add_gridspec(1, n_groups * 2, width_ratios=width_ratios, wspace=0.05)

for i, mat in enumerate(MATURITY_ORDER):
    mat_z_full = build_smoothed_zscore_matrix(mat, highlight_found, bin_mean)
    peaks = get_peak_positions(mat_z_full, highlight_found)
    order = np.argsort([peaks[n] for n in highlight_found])
    mat_z_sub = mat_z_full[order]
    names_sub = [highlight_found[j] for j in order]
    colors_sub = [HIGHLIGHT_COLORS[n] for n in names_sub]

    ax = fig.add_subplot(gs[0, i * 2 + 1])
    ax.imshow(mat_z_sub, aspect="auto", cmap="RdYlBu_r", vmin=-2, vmax=2, interpolation="bilinear")
    ax.set_xticks([0, N_HEATMAP_COLS - 1])
    ax.set_xticklabels(["Proximal", "Distal"], fontsize=10)
    ax.set_yticks(range(len(names_sub)))
    ax.set_yticklabels(names_sub, fontsize=8)
    ax.yaxis.tick_right()
    ax.tick_params(axis="y", length=0)
    for tick, color in zip(ax.get_yticklabels(), colors_sub):
        tick.set_color(color)
    ax_blank = fig.add_subplot(gs[0, i * 2])
    ax_blank.axis("off")

plt.tight_layout()
out_path = "LR_heatmap"
fig.savefig(f"{OUT_DIR}/{out_path}.pdf", dpi=150, bbox_inches="tight")
fig.savefig(f"{OUT_DIR}/{out_path}.png", dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"Saved {out_path}.*")
