import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42

OUT_DIR = "."
IN_CSV = "panelF_pathway_bin_mean.csv"

MATURITY_ORDER = ["immature", "mature"]

HIGHLIGHT_LABELS = {
    "HALLMARK_INTERFERON_ALPHA_RESPONSE": ("IFN-alpha response", "#E4572E"),
    "HALLMARK_INTERFERON_GAMMA_RESPONSE": ("IFN-gamma response", "#E4572E"),
    "HALLMARK_INFLAMMATORY_RESPONSE": ("Inflammatory response", "#E4572E"),
    "HALLMARK_TNFA_SIGNALING_VIA_NFKB": ("TNF-alpha via NF-kB", "#E4572E"),
    "HALLMARK_IL6_JAK_STAT3_SIGNALING": ("IL-6/JAK/STAT3", "#E4572E"),
    "HALLMARK_IL2_STAT5_SIGNALING": ("IL-2/STAT5", "#E4572E"),
    "HALLMARK_COMPLEMENT": ("Complement", "#E4572E"),
    "HALLMARK_OXIDATIVE_PHOSPHORYLATION": ("Oxidative phosphorylation", "#3B7EA1"),
    "GOBP_RESPONSE_TO_METAL_ION": ("Metal-response (GO)", "#8172B3"),
    "GOBP_NON_CANONICAL_NF_KAPPAB_SIGNAL_TRANSDUCTION": ("Non-canonical NF-kB (GO)", "#8172B3"),
    "GOBP_B_CELL_PROLIFERATION": ("B Cell Proliferation (GO)", "#55A868"),
    "GOBP_IMMUNOLOGICAL_MEMORY_FORMATION_PROCESS": ("Immunological memory formation (GO)", "#55A868"),
    "GOBP_POSITIVE_REGULATION_OF_B_CELL_ACTIVATION": ("Pos. Reg. B Cell Activation (GO)", "#55A868"),
    "GOBP_POSITIVE_REGULATION_OF_CD4_POSITIVE_ALPHA_BETA_T_CELL_DIFFERENTIATION": ("Pos. Reg. CD4 T Differentiation (GO)", "#C44E52"),
    "GOBP_GERMINAL_CENTER_B_CELL_DIFFERENTIATION": ("GC B Cell Differentiation (GO)", "#55A868"),
    "GOBP_GERMINAL_CENTER_FORMATION": ("GC Formation (GO)", "#55A868"),
    "GOBP_REGULATION_OF_GERMINAL_CENTER_FORMATION": ("Reg. of GC Formation (GO)", "#55A868"),
    "GOBP_B_CELL_ACTIVATION": ("B Cell Activation (GO)", "#55A868"),
    "GOBP_POSITIVE_REGULATION_OF_T_CELL_PROLIFERATION": ("Pos. Reg. T Cell Proliferation (GO)", "#C44E52"),
}

bin_mean = pd.read_csv(IN_CSV)
sig_cols = [c for c in bin_mean.columns if c.startswith("sig__")]
highlight_keys = [c.replace("sig__", "") for c in sig_cols]

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


def build_smoothed_zscore_matrix(mat_label, names):
    sub = bin_mean[(bin_mean.maturity == mat_label) & (bin_mean.norm_bin != ">1.0")].sort_values("bin_mid")
    mat_smooth = np.zeros((len(names), N_HEATMAP_COLS))
    for r, name in enumerate(names):
        xs, ys = smooth_xy(sub.bin_mid.values, sub[f"sig__{name}"].values, n_out=N_HEATMAP_COLS)
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


n_highlight = len(highlight_keys)
n_groups = len(MATURITY_ORDER)
width_ratios2 = [1.0, 1.0] * n_groups
fig2 = plt.figure(figsize=(6.2 * n_groups, 0.32 * n_highlight + 2))
gs2 = fig2.add_gridspec(1, n_groups * 2, width_ratios=width_ratios2, wspace=0.05)

for i, mat in enumerate(MATURITY_ORDER):
    mat_z_full = build_smoothed_zscore_matrix(mat, highlight_keys)
    peaks = get_peak_positions(mat_z_full, highlight_keys)
    order = np.argsort([peaks[n] for n in highlight_keys])
    mat_z_sub = mat_z_full[order]
    names_sub = [highlight_keys[j] for j in order]
    labels_sub = [HIGHLIGHT_LABELS[n][0] for n in names_sub]
    colors_sub = [HIGHLIGHT_LABELS[n][1] for n in names_sub]

    ax = fig2.add_subplot(gs2[0, i * 2 + 1])
    ax.imshow(mat_z_sub, aspect="auto", cmap="RdYlBu_r", vmin=-2, vmax=2, interpolation="bilinear")
    ax.set_xticks([0, N_HEATMAP_COLS - 1])
    ax.set_xticklabels(["Proximal", "Distal"], fontsize=10)
    ax.set_yticks(range(n_highlight))
    ax.set_yticklabels(labels_sub, fontsize=8)
    ax.yaxis.tick_right()
    ax.tick_params(axis="y", length=0)
    for tick, color in zip(ax.get_yticklabels(), colors_sub):
        tick.set_color(color)
    ax_blank = fig2.add_subplot(gs2[0, i * 2])
    ax_blank.axis("off")

plt.tight_layout()
out2 = "pathway_heatmap"
fig2.savefig(f"{OUT_DIR}/{out2}.pdf", dpi=150, bbox_inches="tight")
fig2.savefig(f"{OUT_DIR}/{out2}.png", dpi=150, bbox_inches="tight")
plt.close(fig2)
print(f"Saved {out2}.*")
